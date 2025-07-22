#!/usr/bin/env python3
"""
Convert PNG to favicon.ico with multiple sizes
"""

from PIL import Image
import os

def convert_png_to_ico(png_path, ico_path):
    """Convert PNG to ICO with multiple sizes"""
    try:
        # Open the PNG image
        img = Image.open(png_path)
        
        # Convert to RGBA if not already
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Create different sizes for the favicon
        sizes = [16, 32, 48, 64]
        
        # Create a list to store all size variants
        icon_images = []
        
        for size in sizes:
            # Resize image maintaining aspect ratio
            resized = img.resize((size, size), Image.Resampling.LANCZOS)
            icon_images.append(resized)
        
        # Save as ICO with multiple sizes
        icon_images[0].save(
            ico_path,
            format='ICO',
            sizes=[(img.width, img.height) for img in icon_images],
            append_images=icon_images[1:]
        )
        
        print(f"✅ Successfully converted {png_path} to {ico_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error converting image: {e}")
        return False

if __name__ == "__main__":
    # Look for PNG file in current directory
    png_files = [f for f in os.listdir('.') if f.lower().endswith('.png')]
    
    if not png_files:
        print("❌ No PNG files found in current directory")
        print("💡 Please save your PNG image in this directory and run again")
        exit(1)
    
    # Use the first PNG file found
    png_file = png_files[0]
    print(f"🖼️  Found PNG file: {png_file}")
    
    # Convert to favicon.ico
    success = convert_png_to_ico(png_file, 'favicon.ico')
    
    if success:
        print("🎉 Favicon created successfully!")
        print("🔄 Refresh your browser to see the new favicon")
    else:
        print("❌ Failed to create favicon") 