import tensorflow as tf
import numpy as np
import cv2
from pathlib import Path


class GradCAM:
    """
    Grad-CAM implementation for generating visual explanations of model predictions.
    Helps understand which parts of the image the model focuses on for classification.
    """
    
    def __init__(self, model, layer_name):
        """
        Initialize Grad-CAM.
        
        Args:
            model: Trained Keras model
            layer_name: Name of the convolutional layer to visualize
        """
        self.model = model
        self.layer_name = layer_name
        self.grad_model = tf.keras.models.Model(
            [model.inputs],
            [model.get_layer(layer_name).output, model.output]
        )
    
    def generate_heatmap(self, img_array, pred_index=None):
        """
        Generate Grad-CAM heatmap for an image.
        
        Args:
            img_array: Preprocessed image array (normalized, shape: (1, 224, 224, 3))
            pred_index: Class index for which to generate CAM. If None, uses predicted class.
        
        Returns:
            heatmap: Grad-CAM heatmap (shape: (224, 224))
        """
        # Convert to tensor
        img_tensor = tf.convert_to_tensor(img_array)
        
        with tf.GradientTape() as tape:
            tape.watch(img_tensor)
            conv_outputs, predictions = self.grad_model(img_tensor)
            
            # If pred_index is None, use the class with highest prediction
            if pred_index is None:
                pred_index = tf.argmax(predictions[0])
            
            class_channel = predictions[:, pred_index]
        
        # Compute gradients with respect to convolutional layer output
        grads = tape.gradient(class_channel, conv_outputs)
        
        # Global average pooling
        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
        
        # Generate heatmap
        conv_outputs = conv_outputs[0]
        heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]
        heatmap = tf.squeeze(heatmap)
        
        # Normalize heatmap
        heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
        
        return heatmap.numpy()
    
    def visualize_with_gradcam(self, img_array, original_img_path, output_path):
        """
        Create visualization combining original image with Grad-CAM heatmap.
        
        Args:
            img_array: Preprocessed image array
            original_img_path: Path to original image
            output_path: Path where to save visualization
        
        Returns:
            output_path: Path to saved visualization
        """
        # Generate heatmap
        heatmap = self.generate_heatmap(img_array)
        
        # Resize heatmap to original image size
        heatmap = cv2.resize(heatmap, (224, 224))
        
        # Read original image
        original_img = cv2.imread(str(original_img_path))
        if original_img is None:
            raise ValueError(f"Could not read image from {original_img_path}")
        
        original_img = cv2.resize(original_img, (224, 224))
        
        # Convert to float and normalize
        original_img_float = original_img.astype(np.float32) / 255.0
        
        # Create colormap heatmap
        heatmap_colored = cv2.applyColorMap((heatmap * 255).astype(np.uint8), cv2.COLORMAP_JET)
        heatmap_colored_float = heatmap_colored.astype(np.float32) / 255.0
        
        # Blend original image with heatmap
        superimposed = cv2.addWeighted(original_img_float, 0.6, heatmap_colored_float, 0.4, 0)
        superimposed = (superimposed * 255).astype(np.uint8)
        
        # Save result
        cv2.imwrite(str(output_path), superimposed)
        
        return str(output_path)


def get_gradcam_explanation(model, img_array, original_img_path, output_path, layer_name='global_average_pooling2d'):
    """
    Wrapper function to generate Grad-CAM visualization and get explanation.
    
    Args:
        model: Trained model
        img_array: Preprocessed image array
        original_img_path: Path to original image
        output_path: Path to save visualization
        layer_name: Convolutional layer name
    
    Returns:
        gradcam_path: Path to saved Grad-CAM visualization
    """
    try:
        grad_cam = GradCAM(model, layer_name)
        gradcam_path = grad_cam.visualize_with_gradcam(img_array, original_img_path, output_path)
        return gradcam_path
    except Exception as e:
        print(f"Error generating Grad-CAM: {str(e)}")
        return None
