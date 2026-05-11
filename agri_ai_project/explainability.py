import tensorflow as tf
import numpy as np
import cv2
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

try:
    import lime
    import lime.lime_image
    LIME_AVAILABLE = True
except ImportError:
    LIME_AVAILABLE = False


class ComprehensiveExplainability:
    """
    Multi-method explainability for agricultural disease detection.
    Combines Grad-CAM, LIME, Integrated Gradients, and Feature Analysis.
    """
    
    def __init__(self, model):
        """Initialize with trained model"""
        self.model = model
        self.layer_name = 'global_average_pooling2d'
        self.grad_model = tf.keras.models.Model(
            [model.inputs],
            [model.get_layer(self.layer_name).output, model.output]
        )
    
    # ========================
    # 1. GRAD-CAM EXPLANATION
    # ========================
    
    def generate_gradcam(self, img_array):
        """Generate Grad-CAM heatmap"""
        try:
            img_tensor = tf.convert_to_tensor(img_array, dtype=tf.float32)
            
            with tf.GradientTape() as tape:
                tape.watch(img_tensor)
                conv_outputs, predictions = self.grad_model(img_tensor)
                pred_index = tf.argmax(predictions[0])
                class_channel = predictions[:, pred_index]
            
            grads = tape.gradient(class_channel, conv_outputs)
            pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
            conv_outputs = conv_outputs[0]
            heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]
            heatmap = tf.squeeze(heatmap)
            heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
            
            return heatmap.numpy()
        except Exception as e:
            print(f"Grad-CAM error: {str(e)}")
            return None
    
    def visualize_gradcam(self, img_array, original_img_path, output_path):
        """Create Grad-CAM visualization"""
        try:
            heatmap = self.generate_gradcam(img_array)
            if heatmap is None:
                return None
            
            heatmap = cv2.resize(heatmap, (224, 224))
            original_img = cv2.imread(str(original_img_path))
            
            if original_img is None:
                return None
            
            original_img = cv2.resize(original_img, (224, 224))
            original_img_float = original_img.astype(np.float32) / 255.0
            heatmap_colored = cv2.applyColorMap((heatmap * 255).astype(np.uint8), cv2.COLORMAP_JET)
            heatmap_colored_float = heatmap_colored.astype(np.float32) / 255.0
            superimposed = cv2.addWeighted(original_img_float, 0.6, heatmap_colored_float, 0.4, 0)
            superimposed = (superimposed * 255).astype(np.uint8)
            
            cv2.imwrite(str(output_path), superimposed)
            return str(output_path)
        except Exception as e:
            print(f"Grad-CAM visualization error: {str(e)}")
            return None
    
    # ========================
    # 2. INTEGRATED GRADIENTS
    # ========================
    
    def integrated_gradients(self, img_array, baseline=None, steps=20):
        """
        Compute Integrated Gradients - measures importance of each pixel.
        Shows how changes in pixel values affect predictions.
        """
        try:
            if baseline is None:
                baseline = np.zeros_like(img_array)
            
            img_array = tf.convert_to_tensor(img_array, dtype=tf.float32)
            baseline = tf.convert_to_tensor(baseline, dtype=tf.float32)
            
            integrated_grads = np.zeros_like(img_array.numpy())
            
            for step in range(steps):
                alpha = step / steps
                interpolated = baseline + alpha * (img_array - baseline)
                
                with tf.GradientTape() as tape:
                    tape.watch(interpolated)
                    predictions = self.model(interpolated)
                    pred_class = tf.argmax(predictions[0])
                    class_score = predictions[0, pred_class]
                
                grads = tape.gradient(class_score, interpolated)
                integrated_grads += grads.numpy()
            
            integrated_grads /= steps
            integrated_grads = (img_array.numpy() - baseline.numpy()) * integrated_grads
            
            # Aggregate across color channels
            attribution = np.mean(np.abs(integrated_grads[0]), axis=2)
            attribution = (attribution - attribution.min()) / (attribution.max() - attribution.min() + 1e-8)
            
            return attribution
        except Exception as e:
            print(f"Integrated Gradients error: {str(e)}")
            return None
    
    def visualize_integrated_gradients(self, img_array, original_img_path, output_path):
        """Create Integrated Gradients visualization"""
        try:
            attribution = self.integrated_gradients(img_array)
            if attribution is None:
                return None
            
            attribution = cv2.resize(attribution, (224, 224))
            original_img = cv2.imread(str(original_img_path))
            
            if original_img is None:
                return None
            
            original_img = cv2.resize(original_img, (224, 224))
            original_img_float = original_img.astype(np.float32) / 255.0
            
            # Use INFERNO colormap for different visualization
            attribution_colored = cv2.applyColorMap((attribution * 255).astype(np.uint8), cv2.COLORMAP_INFERNO)
            attribution_colored_float = attribution_colored.astype(np.float32) / 255.0
            
            superimposed = cv2.addWeighted(original_img_float, 0.5, attribution_colored_float, 0.5, 0)
            superimposed = (superimposed * 255).astype(np.uint8)
            
            cv2.imwrite(str(output_path), superimposed)
            return str(output_path)
        except Exception as e:
            print(f"Integrated Gradients visualization error: {str(e)}")
            return None
    
    # ========================
    # 3. LIME EXPLANATION
    # ========================
    
    def lime_explanation(self, img_array, original_img_path, output_path, num_samples=1000):
        """
        LIME (Local Interpretable Model-agnostic Explanations)
        Shows which image segments contribute to the prediction.
        """
        if not LIME_AVAILABLE:
            return None
        
        try:
            original_img = cv2.imread(str(original_img_path))
            if original_img is None:
                return None
            
            original_img = cv2.resize(original_img, (224, 224))
            original_img_rgb = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)
            original_img_normalized = original_img_rgb.astype(np.float32) / 255.0
            
            # Create LIME explainer
            explainer = lime.lime_image.LimeImageExplainer()
            
            # Define prediction function
            def predict_fn(images):
                return self.model.predict(images, verbose=0)
            
            # Generate explanation
            explanation = explainer.explain_instance(
                original_img_normalized,
                predict_fn,
                top_labels=1,
                num_samples=num_samples,
                distance_metric='cosine'
            )
            
            # Get image and mask
            image, mask = explanation.get_image_and_mask(
                explanation.top_labels[0],
                positive_only=True,
                num_features=10,
                hide_rest=False
            )
            
            # Convert back to BGR for saving
            image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            cv2.imwrite(str(output_path), (image_bgr * 255).astype(np.uint8))
            
            return str(output_path)
        except Exception as e:
            print(f"LIME explanation error: {str(e)}")
            return None
    
    # ========================
    # 4. FEATURE IMPORTANCE
    # ========================
    
    def channel_importance(self, img_array):
        """
        Analyze importance of color channels (R, G, B)
        Shows which color information the model relies on.
        """
        try:
            predictions_original = self.model.predict(img_array, verbose=0)
            original_confidence = np.max(predictions_original)
            
            channel_importance = {}
            
            # Test each channel
            for i, channel_name in enumerate(['Red', 'Green', 'Blue']):
                img_copy = img_array.copy()
                img_copy[:, :, :, i] = 0  # Zero out channel
                
                predictions_zeroed = self.model.predict(img_copy, verbose=0)
                zeroed_confidence = np.max(predictions_zeroed)
                
                # Importance = drop in confidence
                importance = original_confidence - zeroed_confidence
                channel_importance[channel_name] = float(importance)
            
            return channel_importance
        except Exception as e:
            print(f"Channel importance error: {str(e)}")
            return {}
    
    def spatial_importance(self, img_array, grid_size=4):
        """
        Analyze importance of different image regions.
        Shows which parts of the image are most important.
        """
        try:
            predictions_original = self.model.predict(img_array, verbose=0)
            original_confidence = np.max(predictions_original)
            
            spatial_importance = {}
            patch_height = 224 // grid_size
            patch_width = 224 // grid_size
            
            for i in range(grid_size):
                for j in range(grid_size):
                    img_copy = img_array.copy()
                    
                    # Blur specific region
                    y_start = i * patch_height
                    y_end = (i + 1) * patch_height
                    x_start = j * patch_width
                    x_end = (j + 1) * patch_width
                    
                    region = img_copy[0, y_start:y_end, x_start:x_end, :].copy()
                    blurred = cv2.GaussianBlur(region, (11, 11), 2)
                    img_copy[0, y_start:y_end, x_start:x_end, :] = blurred
                    
                    predictions_blurred = self.model.predict(img_copy, verbose=0)
                    blurred_confidence = np.max(predictions_blurred)
                    
                    # Importance = drop in confidence
                    importance = original_confidence - blurred_confidence
                    spatial_importance[f"Region_{i}_{j}"] = float(importance)
            
            return spatial_importance
        except Exception as e:
            print(f"Spatial importance error: {str(e)}")
            return {}
    
    # ========================
    # 5. PREDICTION CONFIDENCE ANALYSIS
    # ========================
    
    def confidence_analysis(self, img_array, class_names):
        """Analyze prediction confidence across all classes"""
        try:
            predictions = self.model.predict(img_array, verbose=0)[0]
            
            analysis = {}
            for i, class_name in enumerate(class_names):
                confidence = float(predictions[i]) * 100
                analysis[class_name] = {
                    'confidence': confidence,
                    'rank': 0
                }
            
            # Add ranking
            sorted_classes = sorted(analysis.items(), key=lambda x: x[1]['confidence'], reverse=True)
            for rank, (class_name, data) in enumerate(sorted_classes):
                analysis[class_name]['rank'] = rank + 1
            
            return analysis
        except Exception as e:
            print(f"Confidence analysis error: {str(e)}")
            return {}


def get_comprehensive_explanation(model, img_array, original_img_path, output_dir, class_names):
    """
    Generate all explainability visualizations.
    
    Returns dictionary with all explanation methods and file paths.
    """
    explainer = ComprehensiveExplainability(model)
    
    explanations = {
        'gradcam': None,
        'integrated_gradients': None,
        'lime': None,
        'channel_importance': {},
        'spatial_importance': {},
        'confidence_analysis': {}
    }
    
    # Generate Grad-CAM
    gradcam_path = explainer.visualize_gradcam(
        img_array,
        original_img_path,
        Path(output_dir) / 'gradcam.png'
    )
    if gradcam_path:
        explanations['gradcam'] = gradcam_path.replace('\\', '/')
    
    # Generate Integrated Gradients
    ig_path = explainer.visualize_integrated_gradients(
        img_array,
        original_img_path,
        Path(output_dir) / 'integrated_gradients.png'
    )
    if ig_path:
        explanations['integrated_gradients'] = ig_path.replace('\\', '/')
    
    # Generate LIME (reduced samples for speed)
    lime_path = explainer.lime_explanation(
        img_array,
        original_img_path,
        Path(output_dir) / 'lime_explanation.png',
        num_samples=200
    )
    if lime_path:
        explanations['lime'] = lime_path.replace('\\', '/')
    
    # Channel importance
    explanations['channel_importance'] = explainer.channel_importance(img_array)
    
    # Spatial importance
    explanations['spatial_importance'] = explainer.spatial_importance(img_array, grid_size=2)
    
    # Confidence analysis
    explanations['confidence_analysis'] = explainer.confidence_analysis(img_array, class_names)
    
    return explanations
