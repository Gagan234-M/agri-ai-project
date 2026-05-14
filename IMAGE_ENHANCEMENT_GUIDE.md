# Image Enhancement & Robustness Improvements

## Overview
Enhanced your agricultural disease detection system to handle real-world edge cases:
- **Blurry images** - Automatic sharpness detection and enhancement
- **Rotated images** - Automatic rotation detection and correction
- **Low-quality images** - Denoising, contrast, and brightness enhancement
- **Poor lighting** - Automatic brightness adjustment
- **Low contrast** - Automatic contrast enhancement

---

## What Was Added

### 1. **New Module: `image_enhancement.py`**

Contains the `ImageQualityAnalyzer` class with the following capabilities:

#### A. **Blur Detection**
```python
detect_blur(image_path, threshold=100)
```
- Uses Laplacian variance to detect blurry images
- Returns blur score and whether image is blurry
- Threshold can be adjusted (lower = more sensitive)

#### B. **Rotation Detection**
```python
detect_rotation(image_path)
```
- Detects if images are rotated 90 degrees
- Useful for sideways phone photos
- Returns rotation angle

#### C. **Image Enhancement**
```python
enhance_low_quality_image(image_path)
```
Applies multiple filters:
1. **Denoising** - Reduces noise while preserving edges
2. **Contrast Enhancement** - +30% contrast boost
3. **Brightness Adjustment** - +10% brightness for dark images
4. **Sharpness Enhancement** - +50% sharpness for blurry images

#### D. **Automatic Quality Assessment**
```python
auto_enhance_image(image_path)
```
Single function that:
- Detects blur, rotation, and quality issues
- Automatically fixes problems
- Returns detailed quality report with warnings

### 2. **Modified `app.py`**

**Changes made:**
- Imported the new `image_enhancement` module
- Added `quality_warnings` list to track enhancement actions
- Calls `process_image_with_quality_check()` before image preprocessing
- Displays user-friendly warnings about detected/corrected issues
- Added CSS styling for warning messages

---

## How It Works

### Process Flow
```
User uploads image
        ↓
Quality Analyzer checks image
        ↓
Detects issues:
├─ Blur detected?
├─ Rotation detected?
└─ Low contrast/brightness?
        ↓
Auto-enhancement applied
├─ Denoise if blurry
├─ Rotate if needed
├─ Enhance contrast/brightness
└─ Sharpen details
        ↓
Model makes prediction with improved image
        ↓
Warnings displayed to user
```

### Quality Report Example
```python
{
    'blur_detected': True,
    'blur_score': 85.5,              # Laplacian variance
    'rotation_detected': False,
    'rotation_angle': 0,
    'enhanced': True,
    'warnings': [
        "⚠️ Image appears blurry. Enhancing sharpness...",
        "✨ Applied denoising, contrast & sharpness enhancements"
    ]
}
```

---

## User Interface Changes

### Quality Warning Display
When image quality issues are detected, users see:
```
ℹ️ Image appears blurry. Enhancing sharpness...
ℹ️ Applied denoising, contrast & sharpness enhancements
```

Styled with:
- Yellow/orange warning box
- Clear emoji indicators
- Before and after explanation

---

## Test Cases

### Test 1: Blurry Image
1. Upload a blurry photo of a rice plant
2. System detects blur and enhances sharpness
3. Prediction still works with improved accuracy
4. Warning message appears

### Test 2: Rotated Image
1. Upload an image rotated 90° (sideways)
2. System detects rotation and auto-corrects
3. Model receives properly oriented image
4. Prediction accuracy improves

### Test 3: Low-Quality Image
1. Upload a low-quality, dark image
2. System applies multiple enhancements:
   - Denoising reduces artifacts
   - Contrast boost improves feature visibility
   - Brightness adjustment helps dark areas
   - Sharpness enhancement clarifies details
3. Warnings explain what was done
4. Better prediction confidence

### Test 4: Normal Quality Image
1. Upload a clear, well-lit image
2. No enhancements needed
3. Prediction proceeds normally
4. No warnings shown

---

## Technical Details

### Blur Detection Algorithm
Uses Laplacian operator variance:
- **High variance** (>100): Sharp image
- **Low variance** (<100): Blurry image
- Detected images get sharpening filter

### Denoising Algorithm
Non-Local Means Denoising (fastNlMeansDenoisingColored):
- Preserves edges while removing noise
- Parameters tuned for plant leaves
- Effective on compressed/noisy images

### Enhancement Parameters
```python
Contrast:  1.3x (30% boost)
Brightness: 1.1x (10% boost)
Sharpness: 1.5x (50% boost)
Denoise h-value: 10
```

Can be adjusted in `image_enhancement.py` if needed.

---

## Benefits

### ✅ **Robustness**
- Works with real-world imperfect images
- Farmer photos often blurry/low-quality
- Phone photos may be rotated

### ✅ **User Experience**
- Transparent about what's happening
- Explains detected issues
- Shows enhancement process

### ✅ **Better Predictions**
- Enhanced images have better features
- Model sees clearer patterns
- Fewer misclassifications

### ✅ **No Extra Dependencies**
- Uses libraries already in requirements.txt
- No additional installation needed
- Minimal performance overhead

---

## How to Test

### Run the application:
```bash
cd agri_ai_project
python app.py
```

### Test with different image types:

1. **Dataset images**: Should work perfectly (no enhancements needed)
2. **Blurry images**: Download from Google Images, apply blur filter
3. **Rotated images**: Rotate images 90° and upload
4. **Low-quality**: Find compressed/dark plant photos
5. **Normal photos**: Your own plant photos

### Monitor warnings:
- Check if quality warnings appear
- Verify they match detected issues
- Confirm enhanced images look correct

---

## Files Modified

| File | Changes |
|------|---------|
| `app.py` | Added import, quality check call, warning display |
| `requirements.txt` | No changes (all deps already present) |

## Files Added

| File | Purpose |
|------|---------|
| `image_enhancement.py` | New image quality analysis and enhancement module |

---

## Future Enhancements

1. **Adaptive Enhancement**
   - Adjust enhancement parameters based on detected issues
   - Learn optimal parameters per crop type

2. **Advanced Rotation**
   - Detect rotation at any angle (not just 90°)
   - Use edge detection for more accurate correction

3. **Lighting Correction**
   - Histogram equalization
   - Gamma correction
   - White balance adjustment

4. **Compression Artifact Removal**
   - Detect JPEG compression artifacts
   - Apply post-processing filters

5. **Performance Metrics**
   - Log blur scores and enhancement metrics
   - Track improvement in prediction confidence
   - Analytics dashboard

---

## Troubleshooting

### Enhancement too aggressive?
Adjust parameters in `image_enhancement.py`:
```python
contrast: 1.3  → 1.2 (reduce boost)
sharpness: 1.5 → 1.3 (reduce boost)
```

### Missing warnings?
Ensure quality report is passed to template:
```python
quality_warnings=quality_warnings
```

### Enhancement not working?
Check if image can be read:
```python
img = cv2.imread(image_path)
if img is None:
    print("Image reading failed")
```

---

## Summary

Your agricultural disease detection system is now **robust to real-world conditions**:
- ✅ Handles blurry phone photos
- ✅ Corrects rotated images
- ✅ Improves low-quality inputs
- ✅ Provides transparency to users
- ✅ Maintains accuracy with enhanced images

Perfect for farmers in the field! 🌾
