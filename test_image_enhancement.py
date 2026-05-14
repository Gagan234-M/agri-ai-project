"""
Quick Test Script for Image Enhancement
Tests blur detection, rotation detection, and enhancement
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from image_enhancement import ImageQualityAnalyzer

def test_quality_analyzer():
    """Test the image quality analyzer with sample images"""
    
    print("=" * 60)
    print("IMAGE ENHANCEMENT MODULE TEST")
    print("=" * 60)
    
    # Get sample images from dataset
    dataset_path = Path(__file__).parent / "dataset"
    
    if not dataset_path.exists():
        print("❌ Dataset folder not found!")
        return False
    
    # Find first image from each category
    test_images = {}
    for folder in dataset_path.glob("*/"):
        images = list(folder.glob("*.jpg")) + list(folder.glob("*.png"))
        if images:
            test_images[folder.name] = str(images[0])
    
    if not test_images:
        print("❌ No images found in dataset!")
        return False
    
    print(f"\n✅ Found {len(test_images)} categories to test\n")
    
    # Test each image
    analyzer = ImageQualityAnalyzer()
    
    for category, image_path in test_images.items():
        print(f"Testing: {category}")
        print(f"  Path: {image_path}")
        
        try:
            # Test blur detection
            is_blurry, blur_score = analyzer.detect_blur(image_path)
            print(f"  Blur Score: {blur_score:.2f} {'(Blurry ⚠️)' if is_blurry else '(Sharp ✅)'}")
            
            # Test rotation detection
            rotation_angle, needs_rotation = analyzer.detect_rotation(image_path)
            print(f"  Rotation: {rotation_angle}° {'(Detected)' if needs_rotation else '(Normal)'}")
            
            # Test quality report
            _, quality_report = analyzer.auto_enhance_image(image_path)
            print(f"  Enhanced: {'Yes ✨' if quality_report['enhanced'] else 'No'}")
            print(f"  Warnings: {len(quality_report['warnings'])}")
            for warning in quality_report['warnings']:
                print(f"    - {warning}")
            
            print()
            
        except Exception as e:
            print(f"  ❌ Error: {str(e)}\n")
            return False
    
    print("=" * 60)
    print("✅ ALL TESTS PASSED!")
    print("=" * 60)
    return True

if __name__ == "__main__":
    success = test_quality_analyzer()
    sys.exit(0 if success else 1)
