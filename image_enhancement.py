"""
Image Enhancement Module for Robust Disease Detection
Handles: Blurry images, Rotations, Low-quality images, Poor lighting
"""

import cv2
import numpy as np
from PIL import Image, ImageEnhance
import warnings
warnings.filterwarnings('ignore')


class ImageQualityAnalyzer:
    """Analyzes and enhances image quality for better predictions"""
    
    @staticmethod
    def detect_blur(image_path, threshold=100):
        """
        Detect if image is blurry using Laplacian variance.
        Returns: (is_blurry: bool, blur_score: float)
        """
        try:
            img = cv2.imread(str(image_path))
            if img is None:
                return False, 0
            
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
            
            is_blurry = laplacian_var < threshold
            return is_blurry, laplacian_var
        except Exception as e:
            print(f"Blur detection error: {str(e)}")
            return False, 0
    
    @staticmethod
    def detect_rotation(image_path):
        """
        Detect if image needs rotation (simple heuristic).
        Returns: (rotation_angle: int, needs_rotation: bool)
        """
        try:
            img = cv2.imread(str(image_path))
            if img is None:
                return 0, False
            
            height, width = img.shape[:2]
            
            # If width > height*1.5, might be rotated 90 degrees
            if width > height * 1.5:
                return 90, True
            
            return 0, False
        except Exception as e:
            print(f"Rotation detection error: {str(e)}")
            return 0, False
    
    @staticmethod
    def enhance_low_quality_image(image_path, output_path=None):
        """
        Enhance low-quality images:
        - Denoise
        - Improve contrast
        - Adjust brightness
        - Sharpen details
        """
        try:
            # Read image
            img = cv2.imread(str(image_path))
            if img is None:
                return image_path, False
            
            # Convert BGR to RGB for PIL
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img_pil = Image.fromarray(img_rgb)
            
            # 1. Denoise (reduce noise)
            img_cv = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
            denoised = cv2.fastNlMeansDenoisingColored(
                img_cv,
                h=10,
                hForColorComponents=10,
                templateWindowSize=7,
                searchWindowSize=21
            )
            
            # 2. Improve contrast using PIL
            denoised_rgb = cv2.cvtColor(denoised, cv2.COLOR_BGR2RGB)
            img_pil = Image.fromarray(denoised_rgb)
            
            # Enhance contrast
            enhancer = ImageEnhance.Contrast(img_pil)
            img_pil = enhancer.enhance(1.3)  # Increase contrast by 30%
            
            # Enhance brightness
            enhancer = ImageEnhance.Brightness(img_pil)
            img_pil = enhancer.enhance(1.1)  # Increase brightness by 10%
            
            # 3. Sharpen details
            enhancer = ImageEnhance.Sharpness(img_pil)
            img_pil = enhancer.enhance(1.5)  # Increase sharpness by 50%
            
            # Save enhanced image if path provided
            if output_path:
                img_pil.save(output_path)
                return output_path, True
            
            # Convert back to array and return original path (in-memory)
            return image_path, True
            
        except Exception as e:
            print(f"Image enhancement error: {str(e)}")
            return image_path, False
    
    @staticmethod
    def correct_rotation(image_path, rotation_angle=90):
        """Rotate image by specified angle"""
        try:
            img = cv2.imread(str(image_path))
            if img is None:
                return image_path, False
            
            height, width = img.shape[:2]
            center = (width // 2, height // 2)
            
            # Get rotation matrix
            rotation_matrix = cv2.getRotationMatrix2D(center, rotation_angle, 1.0)
            rotated = cv2.warpAffine(img, rotation_matrix, (width, height))
            
            # Save rotated image
            cv2.imwrite(str(image_path), rotated)
            return image_path, True
            
        except Exception as e:
            print(f"Rotation correction error: {str(e)}")
            return image_path, False
    
    @staticmethod
    def auto_enhance_image(image_path):
        """
        Automatically detect and fix common image quality issues
        Returns: (processed_image_path, quality_report: dict)
        """
        quality_report = {
            'blur_detected': False,
            'blur_score': 0,
            'rotation_detected': False,
            'rotation_angle': 0,
            'enhanced': False,
            'warnings': []
        }
        
        try:
            # 1. Detect blur
            is_blurry, blur_score = ImageQualityAnalyzer.detect_blur(image_path)
            quality_report['blur_detected'] = is_blurry
            quality_report['blur_score'] = float(blur_score)
            
            if is_blurry:
                quality_report['warnings'].append(
                    "⚠️ Image appears blurry. Enhancing sharpness..."
                )
            
            # 2. Detect rotation
            rotation_angle, needs_rotation = ImageQualityAnalyzer.detect_rotation(image_path)
            if needs_rotation:
                quality_report['rotation_detected'] = True
                quality_report['rotation_angle'] = rotation_angle
                quality_report['warnings'].append(
                    f"🔄 Image appears rotated. Auto-correcting by {rotation_angle}°..."
                )
                ImageQualityAnalyzer.correct_rotation(image_path, rotation_angle)
            
            # 3. Enhance if blurry or low quality
            if is_blurry or blur_score < 150:
                enhanced_path, success = ImageQualityAnalyzer.enhance_low_quality_image(
                    image_path,
                    output_path=image_path  # Overwrite
                )
                if success:
                    quality_report['enhanced'] = True
                    quality_report['warnings'].append(
                        "✨ Applied denoising, contrast & sharpness enhancements"
                    )
            
            return image_path, quality_report
            
        except Exception as e:
            quality_report['warnings'].append(f"Enhancement skipped: {str(e)}")
            return image_path, quality_report


# For backward compatibility with existing code
def process_image_with_quality_check(image_path):
    """
    Main function to process image and return quality info
    """
    analyzer = ImageQualityAnalyzer()
    processed_path, quality_report = analyzer.auto_enhance_image(image_path)
    return processed_path, quality_report
