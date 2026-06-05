"""
Image Compression Script for Retford.info
Compresses images in the /public directory while maintaining good quality.
"""

import os
import json
import hashlib
from PIL import Image
from pathlib import Path

# Configuration
PUBLIC_DIR = Path("./src/assets/img")
CACHE_FILE = Path(".image_compression_cache.json")
QUALITY = 85  # 85 is a good balance between quality and file size
MAX_WIDTH = 1920  # Maximum width for images
MAX_HEIGHT = 1920  # Maximum height for images
SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.webp', '.JPG'}
IGNORED_FILENAME_PREFIXES = ('themeparkmaps',)

def get_file_size_kb(filepath):
    """Get file size in KB."""
    return os.path.getsize(filepath) / 1024

def get_file_hash(filepath):
    """Get MD5 hash of file to detect changes."""
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def load_cache():
    """Load the compression cache."""
    if CACHE_FILE.exists():
        try:
            with open(CACHE_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_cache(cache):
    """Save the compression cache."""
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache, f, indent=2)

def is_already_compressed(image_path, cache):
    """Check if image has already been compressed."""
    path_str = str(image_path)
    if path_str not in cache:
        return False
    
    # Check if file has been modified since compression
    try:
        current_hash = get_file_hash(image_path)
        return cache[path_str].get('hash') == current_hash
    except:
        return False

def compress_image(image_path):
    """Compress a single image."""
    original_size = get_file_size_kb(image_path)
    
    try:
        with Image.open(image_path) as img:
            # Store original format
            original_format = img.format
            
            # Convert RGBA to RGB for JPEG
            if image_path.suffix.lower() in ['.jpg', '.jpeg'] and img.mode in ('RGBA', 'LA', 'P'):
                # Create a white background
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            elif img.mode not in ('RGB', 'L'):
                img = img.convert('RGB')
            
            # Resize if image is too large
            if img.width > MAX_WIDTH or img.height > MAX_HEIGHT:
                img.thumbnail((MAX_WIDTH, MAX_HEIGHT), Image.Resampling.LANCZOS)
            
            # Save with compression
            if image_path.suffix.lower() in ['.jpg', '.jpeg']:
                img.save(image_path, 'JPEG', quality=QUALITY, optimize=True)
            elif image_path.suffix.lower() == '.png':
                img.save(image_path, 'PNG', optimize=True)
            elif image_path.suffix.lower() == '.webp':
                img.save(image_path, 'WEBP', quality=QUALITY)
        
        new_size = get_file_size_kb(image_path)
        reduction = original_size - new_size
        reduction_percent = (reduction / original_size * 100) if original_size > 0 else 0
        
        return {
            'success': True,
            'original_size': original_size,
            'new_size': new_size,
            'reduction': reduction,
            'reduction_percent': reduction_percent
        }
    
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def main():
    """Main function to process all images."""
    if not PUBLIC_DIR.exists():
        print(f"Error: {PUBLIC_DIR} directory not found!")
        return
    
    print("🖼️  Image Compression Tool for Retford.info")
    print("=" * 60)
    print(f"Quality setting: {QUALITY}%")
    print(f"Max dimensions: {MAX_WIDTH}x{MAX_HEIGHT}px")
    print("=" * 60)
    print()
    
    # Load cache
    cache = load_cache()
    
    # Find all images
    image_files = []
    for ext in SUPPORTED_FORMATS:
        image_files.extend(PUBLIC_DIR.rglob(f"*{ext}"))
    
    image_files = [
        img for img in image_files
        if not img.name.lower().startswith(IGNORED_FILENAME_PREFIXES)
    ]
    
    if not image_files:
        print("No images found in the public directory.")
        return
    
    print(f"Found {len(image_files)} image(s) to process\n")
    
    total_original = 0
    total_new = 0
    processed_count = 0
    skipped_count = 0
    cached_count = 0
    error_count = 0
    
    for image_path in image_files:
        relative_path = image_path.relative_to(PUBLIC_DIR)
        print(f"Processing: {relative_path}")
        
        # Check if already compressed
        if is_already_compressed(image_path, cache):
            print(f"  ✓ Already compressed (cached)\n")
            cached_count += 1
            continue
        
        original_size = get_file_size_kb(image_path)
        
        # Skip very small images (likely already optimized or icons)
        if original_size < 10:
            print(f"  ⏩ Skipped (too small: {original_size:.1f} KB)\n")
            skipped_count += 1
            continue
        
        result = compress_image(image_path)
        
        if result['success']:
            # Add to cache
            cache[str(image_path)] = {
                'hash': get_file_hash(image_path),
                'size': result['new_size']
            }
            
            if result['reduction'] > 1:  # Only count if saved more than 1KB
                print(f"  ✅ {result['original_size']:.1f} KB → {result['new_size']:.1f} KB")
                print(f"  💾 Saved {result['reduction']:.1f} KB ({result['reduction_percent']:.1f}%)\n")
                total_original += result['original_size']
                total_new += result['new_size']
                processed_count += 1
            else:
                print(f"  ✓ Already optimized ({result['new_size']:.1f} KB)\n")
                skipped_count += 1
        else:
            print(f"  ❌ Error: {result['error']}\n")
            error_count += 1
    
    # Save cache
    save_cache(cache)
    
    # Summary
    print("=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    print(f"Total images found: {len(image_files)}")
    print(f"Compressed: {processed_count}")
    print(f"Already compressed (cached): {cached_count}")
    print(f"Skipped: {skipped_count}")
    print(f"Errors: {error_count}")
    
    if processed_count > 0:
        total_reduction = total_original - total_new
        total_percent = (total_reduction / total_original * 100) if total_original > 0 else 0
        print(f"\nTotal size before: {total_original:.1f} KB")
        print(f"Total size after: {total_new:.1f} KB")
        print(f"Total saved: {total_reduction:.1f} KB ({total_percent:.1f}%)")
    
    print("\n✨ Done!")

if __name__ == "__main__":
    main()
