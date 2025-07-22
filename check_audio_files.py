#!/usr/bin/env python3
"""
Audio File Diagnostic Tool

Check audio files for common issues that might cause transcription problems.

Usage:
    python3 check_audio_files.py [--fix] [--dir audio_files]
"""

import os
import subprocess
import argparse
from pathlib import Path
import json

def check_audio_file(file_path):
    """Check if an audio file is valid and get its properties"""
    try:
        # Get detailed file information
        cmd = [
            'ffprobe', '-v', 'quiet', '-print_format', 'json',
            '-show_format', '-show_streams', str(file_path)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        
        if result.returncode != 0:
            return {"valid": False, "error": "ffprobe failed", "details": result.stderr}
        
        info = json.loads(result.stdout)
        
        # Check for audio streams
        audio_streams = [s for s in info.get('streams', []) if s.get('codec_type') == 'audio']
        video_streams = [s for s in info.get('streams', []) if s.get('codec_type') == 'video']
        
        format_info = info.get('format', {})
        duration = float(format_info.get('duration', 0))
        size_mb = float(format_info.get('size', 0)) / (1024 * 1024)
        
        # Determine file status
        if not audio_streams:
            status = "NO_AUDIO"
            issue = "File has no audio streams"
        elif len(video_streams) > 0:
            status = "VIDEO_FILE"
            issue = "File contains video (may be misnamed)"
        elif duration < 1.0:
            status = "TOO_SHORT"
            issue = f"Duration too short: {duration:.2f}s"
        elif size_mb < 0.01:  # Less than 10KB
            status = "TOO_SMALL"
            issue = f"File too small: {size_mb:.3f}MB"
        else:
            status = "VALID"
            issue = None
        
        return {
            "valid": status == "VALID",
            "status": status,
            "issue": issue,
            "audio_streams": len(audio_streams),
            "video_streams": len(video_streams),
            "duration": duration,
            "size_mb": size_mb,
            "codec": audio_streams[0].get('codec_name') if audio_streams else None
        }
        
    except subprocess.TimeoutExpired:
        return {"valid": False, "error": "Timeout", "details": "ffprobe timed out"}
    except json.JSONDecodeError:
        return {"valid": False, "error": "Invalid JSON", "details": "ffprobe output not valid JSON"}
    except Exception as e:
        return {"valid": False, "error": "Exception", "details": str(e)}

def fix_audio_file(input_file, output_file):
    """Try to fix an audio file by re-encoding it"""
    try:
        cmd = [
            'ffmpeg', '-i', str(input_file),
            '-vn',  # No video
            '-acodec', 'libmp3lame',  # MP3 codec
            '-ar', '16000',  # Sample rate
            '-ac', '1',  # Mono
            '-y',  # Overwrite
            str(output_file)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        return result.returncode == 0, result.stderr
        
    except Exception as e:
        return False, str(e)

def main():
    parser = argparse.ArgumentParser(description='Check audio files for transcription issues')
    parser.add_argument('--dir', default='audio_files', help='Directory to check')
    parser.add_argument('--fix', action='store_true', help='Try to fix problematic files')
    parser.add_argument('--extensions', default='mp3,wav,m4a,flac,ogg', help='File extensions to check')
    
    args = parser.parse_args()
    
    # Find audio files
    input_dir = Path(args.dir)
    extensions = args.extensions.split(',')
    
    audio_files = []
    for ext in extensions:
        audio_files.extend(input_dir.glob(f"*.{ext}"))
    
    if not audio_files:
        print(f"❌ No audio files found in {input_dir}")
        return
    
    print(f" Checking {len(audio_files)} audio files...")
    
    # Check each file
    valid_files = []
    problematic_files = []
    
    for audio_file in audio_files:
        print(f"📁 Checking {audio_file.name}...", end=" ")
        
        result = check_audio_file(audio_file)
        
        if result["valid"]:
            print("✅")
            valid_files.append((audio_file, result))
        else:
            print(f"❌ {result.get('issue', result.get('error', 'Unknown error'))}")
            problematic_files.append((audio_file, result))
    
    # Summary
    print(f"\n📊 Summary:")
    print(f"  ✅ Valid files: {len(valid_files)}")
    print(f"  ❌ Problematic files: {len(problematic_files)}")
    
    if problematic_files:
        print(f"\n❌ Problematic Files:")
        for file_path, result in problematic_files:
            print(f"  • {file_path.name}: {result.get('status', 'ERROR')} - {result.get('issue', result.get('error'))}")
            
            # Show details for some issues
            if result.get('video_streams', 0) > 0:
                print(f"    Has {result['video_streams']} video stream(s) and {result.get('audio_streams', 0)} audio stream(s)")
            
        if args.fix:
            print(f"\n🔧 Attempting to fix problematic files...")
            fixed_dir = input_dir / "fixed"
            fixed_dir.mkdir(exist_ok=True)
            
            for file_path, result in problematic_files:
                if result.get('status') in ['VIDEO_FILE', 'NO_AUDIO']:
                    print(f"  🔄 Fixing {file_path.name}...")
                    output_file = fixed_dir / f"{file_path.stem}_fixed.mp3"
                    
                    success, error_msg = fix_audio_file(file_path, output_file)
                    
                    if success:
                        print(f"    ✅ Fixed: {output_file}")
                    else:
                        print(f"    ❌ Failed: {error_msg[:100]}")
    
    if valid_files:
        total_duration = sum(f[1]['duration'] for f in valid_files)
        total_size = sum(f[1]['size_mb'] for f in valid_files)
        print(f"\n📈 Valid Files Stats:")
        print(f"  Total duration: {total_duration/60:.1f} minutes")
        print(f"  Total size: {total_size:.1f} MB")
        print(f"  Average duration: {total_duration/len(valid_files):.1f} seconds")

if __name__ == "__main__":
    main() 