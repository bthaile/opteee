#!/usr/bin/env python3
"""
Semantic PDF Processor for Academic Papers

Intelligently chunks PDFs while preserving context and meaning:
- Detects section headers and keeps sections together
- Splits at paragraph boundaries (not mid-sentence)
- Injects section context into each chunk
- Handles tables and figures gracefully

Usage:
    python3 process_pdfs.py                              # Process default directory
    python3 process_pdfs.py --source /path/to/pdfs       # Custom source directory
    python3 process_pdfs.py --force                      # Force reprocess all
    python3 process_pdfs.py --analyze                    # Analyze without processing
"""

import os
import json
import hashlib
import argparse
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple, Optional

# PDF extraction
try:
    import pdfplumber
    from pypdf import PdfReader
except ImportError:
    print("❌ Missing dependencies. Install with:")
    print("   pip3 install pdfplumber pypdf")
    exit(1)

# Import config if available, otherwise use defaults
try:
    from pipeline_config import CHUNK_SIZE, OVERLAP, MIN_CHUNK_WORDS
except ImportError:
    CHUNK_SIZE = 250  # Target words per chunk
    OVERLAP = 50      # Words of overlap
    MIN_CHUNK_WORDS = 30  # Minimum words for valid chunk

# Directories
DEFAULT_PDF_SOURCE = '/Users/bradfordhaile/Downloads/outlier-pro-market-study'
PROCESSED_PDF_DIR = 'processed_pdfs'

# Section header patterns (academic papers)
SECTION_PATTERNS = [
    # Numbered sections: "1.", "1.1", "2.3.1", etc.
    r'^(\d+\.[\d.]*)\s+([A-Z][^.!?\n]{5,80})$',
    # Roman numerals: "I.", "II.", "III.", etc.
    r'^([IVX]+\.)\s+([A-Z][^.!?\n]{5,80})$',
    # Capitalized headers: "INTRODUCTION", "METHODOLOGY", etc.
    r'^([A-Z]{4,}(?:\s+[A-Z]{2,})*)$',
    # Title case headers with colon
    r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*):?\s*$',
]

# Common section names in academic papers
KNOWN_SECTIONS = [
    'abstract', 'introduction', 'background', 'literature review',
    'methodology', 'methods', 'data', 'data and methodology',
    'results', 'findings', 'analysis', 'discussion',
    'conclusion', 'conclusions', 'summary', 'implications',
    'references', 'bibliography', 'appendix', 'acknowledgments'
]


def normalize_pdf_date(value: Optional[str]) -> str:
    """
    Normalize PDF CreationDate and other date formats to YYYYMMDD.
    Handles PDF spec format (D:YYYYMMDDHHmmss+tz) and standard formats.
    Returns empty string if unparseable.
    """
    if not value or not isinstance(value, str):
        return ""
    value = value.strip()
    if not value or value.lower() in {"unknown", "n/a", "none", "null"}:
        return ""
    # PDF CreationDate: D:20030901031723+02'00' or D:20030901031723
    if value.startswith("D:") and len(value) >= 10:
        try:
            yyyymmdd = value[2:10]
            if yyyymmdd.isdigit():
                return yyyymmdd
        except (IndexError, TypeError):
            pass
    # Already YYYYMMDD
    if re.fullmatch(r"\d{8}", value):
        return value
    # ISO or YYYY-MM-DD
    try:
        if "T" in value:
            dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
            return dt.strftime("%Y%m%d")
        dt = datetime.strptime(value.split("T")[0], "%Y-%m-%d")
        return dt.strftime("%Y%m%d")
    except ValueError:
        return ""


def extract_pdf_metadata(pdf_path: str) -> Dict:
    """Extract metadata from PDF"""
    metadata = {
        'title': '',
        'author': '',
        'subject': '',
        'creation_date': '',
        'total_pages': 0
    }
    
    try:
        with open(pdf_path, 'rb') as f:
            reader = PdfReader(f)
            if reader.metadata:
                metadata['title'] = str(reader.metadata.get('/Title', '') or '')
                metadata['author'] = str(reader.metadata.get('/Author', '') or '')
                metadata['subject'] = str(reader.metadata.get('/Subject', '') or '')
                metadata['creation_date'] = str(reader.metadata.get('/CreationDate', '') or '')
            metadata['total_pages'] = len(reader.pages)
    except Exception as e:
        print(f"  ⚠️ Metadata extraction error: {e}")
    
    return metadata


def is_section_header(text: str) -> Tuple[bool, str]:
    """
    Detect if a line is a section header.
    Returns (is_header, normalized_header_text)
    """
    text = text.strip()
    
    if not text or len(text) < 3 or len(text) > 100:
        return False, ""
    
    # Check known section names
    text_lower = text.lower().strip('.:')
    if text_lower in KNOWN_SECTIONS:
        return True, text
    
    # Check patterns
    for pattern in SECTION_PATTERNS:
        match = re.match(pattern, text, re.MULTILINE)
        if match:
            return True, text
    
    # Check if all caps (likely header)
    if text.isupper() and len(text.split()) <= 6:
        return True, text
    
    return False, ""


def extract_text_with_structure(pdf_path: str) -> List[Dict]:
    """
    Extract text from PDF preserving paragraph and section structure.
    Returns list of {'type': 'section'|'paragraph'|'table', 'text': str, 'page': int}
    """
    elements = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            # Extract text
            text = page.extract_text() or ""
            
            if not text.strip():
                continue
            
            # Split into lines and group into paragraphs
            lines = text.split('\n')
            current_paragraph = []
            
            for line in lines:
                line = line.strip()
                
                if not line:
                    # Empty line = paragraph break
                    if current_paragraph:
                        para_text = ' '.join(current_paragraph)
                        is_header, header_text = is_section_header(para_text)
                        
                        if is_header:
                            elements.append({
                                'type': 'section',
                                'text': header_text,
                                'page': page_num
                            })
                        elif len(para_text.split()) >= 5:  # Min 5 words for paragraph
                            elements.append({
                                'type': 'paragraph',
                                'text': para_text,
                                'page': page_num
                            })
                        current_paragraph = []
                else:
                    # Check if this line alone is a header
                    is_header, header_text = is_section_header(line)
                    if is_header and not current_paragraph:
                        elements.append({
                            'type': 'section',
                            'text': header_text,
                            'page': page_num
                        })
                    else:
                        current_paragraph.append(line)
            
            # Don't forget last paragraph on page
            if current_paragraph:
                para_text = ' '.join(current_paragraph)
                if len(para_text.split()) >= 5:
                    elements.append({
                        'type': 'paragraph',
                        'text': para_text,
                        'page': page_num
                    })
    
    return elements


def create_semantic_chunks(
    elements: List[Dict],
    target_size: int = CHUNK_SIZE,
    overlap: int = OVERLAP,
    min_words: int = MIN_CHUNK_WORDS
) -> List[Dict]:
    """
    Create semantic chunks that respect section and paragraph boundaries.
    Each chunk includes its section context for better retrieval.
    """
    chunks = []
    current_section = "Document"  # Default section name
    current_chunk_text = []
    current_chunk_pages = set()
    chunk_index = 0
    
    def flush_chunk():
        nonlocal current_chunk_text, current_chunk_pages, chunk_index
        if current_chunk_text:
            text = ' '.join(current_chunk_text)
            word_count = len(text.split())
            
            if word_count >= min_words:
                chunks.append({
                    'text': text,
                    'section': current_section,
                    'pages': sorted(current_chunk_pages),
                    'word_count': word_count,
                    'chunk_index': chunk_index
                })
                chunk_index += 1
            
            # Keep overlap for next chunk (last N words)
            if overlap > 0:
                words = text.split()
                overlap_words = words[-overlap:] if len(words) > overlap else []
                current_chunk_text = overlap_words
                # Keep page reference for overlap
            else:
                current_chunk_text = []
            current_chunk_pages = set()
    
    for element in elements:
        if element['type'] == 'section':
            # New section - flush current chunk and update section
            flush_chunk()
            current_section = element['text']
            current_chunk_pages.add(element['page'])
            
        elif element['type'] == 'paragraph':
            para_words = element['text'].split()
            current_chunk_pages.add(element['page'])
            
            # If adding this paragraph would exceed target, flush first
            current_word_count = len(' '.join(current_chunk_text).split())
            if current_word_count + len(para_words) > target_size * 1.2:  # 20% buffer
                flush_chunk()
                current_chunk_pages.add(element['page'])
            
            current_chunk_text.extend(para_words)
            
            # If we've reached target size at a paragraph boundary, flush
            current_word_count = len(' '.join(current_chunk_text).split())
            if current_word_count >= target_size:
                flush_chunk()
    
    # Flush any remaining content
    flush_chunk()
    
    return chunks


def process_pdf(
    pdf_path: str,
    output_dir: str = PROCESSED_PDF_DIR,
    force: bool = False,
    title_override: str = None,
    chunk_size: int = CHUNK_SIZE,
    overlap: int = OVERLAP
) -> Tuple[int, List[Dict]]:
    """
    Process a single PDF into semantic chunks.
    Returns (chunk_count, chunks_list)
    """
    filename = os.path.basename(pdf_path)
    output_filename = f"{Path(filename).stem}_processed.json"
    output_path = os.path.join(output_dir, output_filename)
    
    # Skip if already processed
    if os.path.exists(output_path) and not force:
        return -1, []  # -1 indicates skipped
    
    # Extract metadata
    metadata = extract_pdf_metadata(pdf_path)
    
    # Use filename as title if not in metadata (metadata often has junk like "Microsoft Word - ...")
    raw_title = title_override or metadata.get('title') or ''
    
    # Clean up title - remove common junk patterns
    title = re.sub(r'[\r\n]+', ' ', raw_title).strip()
    title = re.sub(r'^Microsoft Word\s*[-–—]\s*', '', title, flags=re.IGNORECASE)
    title = re.sub(r'\.docx?$', '', title, flags=re.IGNORECASE)
    title = re.sub(r'\.pdf$', '', title, flags=re.IGNORECASE)
    
    # If title is empty or too short, use filename
    if not title or len(title) < 5:
        title = Path(filename).stem
    
    # Clean filename-based title too
    title = title.replace('_', ' ').replace('-', ' - ')
    title = re.sub(r'\s+', ' ', title).strip()
    
    # Extract text with structure
    elements = extract_text_with_structure(pdf_path)
    
    if not elements:
        print(f"  ⚠️ No text extracted from {filename}")
        return 0, []
    
    # Create semantic chunks
    raw_chunks = create_semantic_chunks(elements, target_size=chunk_size, overlap=overlap)
    
    if not raw_chunks:
        print(f"  ⚠️ No valid chunks from {filename}")
        return 0, []
    
    # Build document ID from filename
    doc_id = hashlib.md5(filename.encode()).hexdigest()[:12]
    
    # Add full metadata to each chunk
    processed_chunks = []
    for chunk in raw_chunks:
        pages = chunk['pages']
        primary_page = pages[0] if pages else 1
        page_range = f"p.{min(pages)}-{max(pages)}" if len(pages) > 1 else f"p.{primary_page}"
        
        processed_chunk = {
            # Core text and title
            'text': chunk['text'],
            'title': title,
            
            # PDF-specific metadata
            'source_type': 'pdf',
            'document_id': doc_id,
            'source_file': filename,
            'section': chunk['section'],
            'page_number': primary_page,
            'page_range': page_range,
            'total_pages': metadata.get('total_pages', 0),
            'chunk_index': chunk['chunk_index'],
            'word_count': chunk['word_count'],
            'author': metadata.get('author', ''),
            
            # Compatibility with transcript format (for unified search)
            'video_id': '',
            'video_url': '',
            'video_url_with_timestamp': '',
            'start_timestamp': f"{chunk['section']} ({page_range})",
            'start_timestamp_seconds': 0,
            'upload_date': normalize_pdf_date(metadata.get('creation_date', '')),
            'duration': None,
        }
        processed_chunks.append(processed_chunk)
    
    # Save to output directory
    os.makedirs(output_dir, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(processed_chunks, f, indent=2, ensure_ascii=False)
    
    return len(processed_chunks), processed_chunks


def analyze_pdfs(source_dir: str) -> None:
    """Analyze PDFs without processing - show statistics"""
    pdf_files = [f for f in os.listdir(source_dir) if f.lower().endswith('.pdf')]
    
    print(f"\n📊 Analyzing {len(pdf_files)} PDFs in {source_dir}\n")
    
    total_pages = 0
    total_size = 0
    
    for filename in sorted(pdf_files)[:10]:  # Sample first 10
        pdf_path = os.path.join(source_dir, filename)
        size = os.path.getsize(pdf_path) / 1024 / 1024  # MB
        total_size += size
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                pages = len(pdf.pages)
                total_pages += pages
                print(f"  📄 {filename[:50]:<50} {pages:>3} pages  {size:>5.1f} MB")
        except Exception as e:
            print(f"  ❌ {filename}: {e}")
    
    if len(pdf_files) > 10:
        print(f"  ... and {len(pdf_files) - 10} more files")
    
    # Estimate total
    avg_pages = total_pages / min(10, len(pdf_files))
    est_total_pages = avg_pages * len(pdf_files)
    est_chunks = est_total_pages * 3  # ~3 chunks per page average
    
    print(f"\n📈 Estimates:")
    print(f"   Total PDFs: {len(pdf_files)}")
    print(f"   Est. total pages: ~{int(est_total_pages)}")
    print(f"   Est. total chunks: ~{int(est_chunks)}")
    print(f"   Est. JSON output: ~{est_chunks * 0.5 / 1024:.1f} MB")


def main():
    parser = argparse.ArgumentParser(
        description='Semantic PDF processor for academic papers',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 process_pdfs.py                                    # Process from default location
  python3 process_pdfs.py --source ~/my-pdfs --force         # Force reprocess custom dir
  python3 process_pdfs.py --analyze                          # Just show stats
        """
    )
    parser.add_argument('--source', '-s', type=str, default=DEFAULT_PDF_SOURCE,
                        help=f'Source directory for PDFs (default: {DEFAULT_PDF_SOURCE})')
    parser.add_argument('--output', '-o', type=str, default=PROCESSED_PDF_DIR,
                        help=f'Output directory (default: {PROCESSED_PDF_DIR})')
    parser.add_argument('--force', '-f', action='store_true',
                        help='Force reprocess all PDFs')
    parser.add_argument('--analyze', '-a', action='store_true',
                        help='Analyze PDFs without processing')
    parser.add_argument('--pdf', type=str,
                        help='Process only a specific PDF file')
    parser.add_argument('--chunk-size', type=int, default=CHUNK_SIZE,
                        help=f'Target words per chunk (default: {CHUNK_SIZE})')
    parser.add_argument('--overlap', type=int, default=OVERLAP,
                        help=f'Overlap words between chunks (default: {OVERLAP})')
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("📄 SEMANTIC PDF PROCESSOR")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    source_dir = args.source
    
    # Check source directory
    if not os.path.exists(source_dir):
        print(f"\n❌ Source directory not found: {source_dir}")
        return
    
    # Analyze mode
    if args.analyze:
        analyze_pdfs(source_dir)
        return
    
    # Get PDFs to process
    if args.pdf:
        # Specific PDF
        if os.path.exists(args.pdf):
            pdf_files = [args.pdf]
        elif os.path.exists(os.path.join(source_dir, args.pdf)):
            pdf_files = [os.path.join(source_dir, args.pdf)]
        else:
            print(f"❌ PDF not found: {args.pdf}")
            return
    else:
        # All PDFs in directory
        pdf_files = [
            os.path.join(source_dir, f)
            for f in os.listdir(source_dir)
            if f.lower().endswith('.pdf')
        ]
    
    if not pdf_files:
        print(f"\n⚠️ No PDF files found in {source_dir}")
        return
    
    print(f"\n📁 Source: {source_dir}")
    print(f"📁 Output: {args.output}")
    print(f"📄 PDFs found: {len(pdf_files)}")
    print(f"⚙️  Chunk size: {args.chunk_size} words, Overlap: {args.overlap} words")
    print()
    
    # Process each PDF (use args values directly)
    total_chunks = 0
    processed_count = 0
    skipped_count = 0
    failed_count = 0
    
    for i, pdf_path in enumerate(sorted(pdf_files), 1):
        filename = os.path.basename(pdf_path)
        print(f"[{i}/{len(pdf_files)}] {filename[:60]}")
        
        try:
            chunk_count, _ = process_pdf(
                pdf_path,
                output_dir=args.output,
                force=args.force,
                chunk_size=args.chunk_size,
                overlap=args.overlap
            )
            
            if chunk_count == -1:
                print(f"       ⏭️  Skipped (already processed)")
                skipped_count += 1
            elif chunk_count > 0:
                print(f"       ✅ Created {chunk_count} chunks")
                total_chunks += chunk_count
                processed_count += 1
            else:
                print(f"       ⚠️  No valid content")
                failed_count += 1
                
        except Exception as e:
            print(f"       ❌ Error: {e}")
            failed_count += 1
    
    # Calculate output size
    output_size = 0
    if os.path.exists(args.output):
        output_size = sum(
            os.path.getsize(os.path.join(args.output, f))
            for f in os.listdir(args.output)
            if f.endswith('.json')
        )
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 PROCESSING SUMMARY")
    print("=" * 70)
    print(f"  ✅ Processed: {processed_count} PDFs")
    print(f"  ⏭️  Skipped: {skipped_count} (already done)")
    print(f"  ❌ Failed: {failed_count}")
    print(f"  📦 Total chunks: {total_chunks}")
    print(f"  💾 Output size: {output_size / 1024 / 1024:.2f} MB")
    print(f"  📁 Output dir: {args.output}/")
    
    if processed_count > 0:
        print(f"\n✅ Done! Commit the processed chunks:")
        print(f"   git add {args.output}/")
        print(f"   git commit -m 'Add {processed_count} processed PDF documents'")
        print(f"   git push")


if __name__ == "__main__":
    main()
