import os
import argparse
from pathlib import Path

def count_files(directory, recursive=False, file_type=None):
    """
    Count files in a directory.
    
    Args:
        directory (str): Path to the directory
        recursive (bool): Whether to count files in subdirectories
        file_type (str): File extension to filter by (e.g., '.txt')
    
    Returns:
        tuple: (total_files, total_size_bytes)
    """
    total_files = 0
    total_size = 0
    
    if recursive:
        # Walk through directory and subdirectories
        for root, _, files in os.walk(directory):
            for file in files:
                if file_type is None or file.endswith(file_type):
                    file_path = os.path.join(root, file)
                    total_files += 1
                    total_size += os.path.getsize(file_path)
    else:
        # Count only files in the specified directory
        for file in os.listdir(directory):
            file_path = os.path.join(directory, file)
            if os.path.isfile(file_path):
                if file_type is None or file.endswith(file_type):
                    total_files += 1
                    total_size += os.path.getsize(file_path)
    
    return total_files, total_size

def format_size(size_bytes):
    """Convert size in bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} TB"

def main():
    parser = argparse.ArgumentParser(description='Count files in a directory')
    parser.add_argument('directory', help='Directory to count files in')
    parser.add_argument('-r', '--recursive', action='store_true', help='Count files in subdirectories')
    parser.add_argument('-t', '--type', help='File type to count (e.g., .txt)')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.directory):
        print(f"Error: Directory '{args.directory}' does not exist")
        return
    
    if not os.path.isdir(args.directory):
        print(f"Error: '{args.directory}' is not a directory")
        return
    
    total_files, total_size = count_files(args.directory, args.recursive, args.type)
    
    print(f"\nDirectory: {args.directory}")
    print(f"Total files: {total_files}")
    print(f"Total size: {format_size(total_size)}")
    
    if args.type:
        print(f"File type: {args.type}")
    if args.recursive:
        print("Including subdirectories")

if __name__ == "__main__":
    main() 