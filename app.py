from flask import Flask, render_template_string, request
import os
import hashlib
import numpy as np
from werkzeug.utils import secure_filename

# TensorFlow models will be imported lazily
# Preprocessing will be imported lazily
from translations import get_translation, get_remedies, get_all_translations
from explainability import get_comprehensive_explanation
from image_enhancement import process_image_with_quality_check

app = Flask(__name__)

# Model will be loaded lazily to prevent 502 timeouts
model = None

def get_model():
    global model
    if model is None:
        print("--- Lazy Loading AI Model... ---")
        from tensorflow.keras.models import load_model
        model = load_model("plant_disease_model.h5", compile=False)
        print("--- AI Model Loaded Successfully! ---")
    return model

class_names = [
    "Healthy_cardamon",
    "diseased_cardamon",
    "healthy_rice_plant",
    "rice_false_smut"
]

# =========================
# UPLOAD FOLDER
# =========================

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# =========================
# EXPLANATION CACHE
# (avoids re-running slow AI analysis for the same image)
# =========================
_explanation_cache = {}  # { md5_hash: explanations_dict }

# =========================
# HTML UI
# =========================

HTML = """

<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Agri AI</title>

<style>

*{
    margin:0;
    padding:0;
    box-sizing:border-box;
    font-family:Arial,sans-serif;
}

body{
    background:linear-gradient(135deg,#11998e,#38ef7d,#1e3c72);
    min-height:100vh;
    display:flex;
    justify-content:center;
    align-items:center;
    padding:20px;
}

.container{
    background:white;
    width:600px;
    padding:30px;
    border-radius:20px;
    box-shadow:0 10px 30px rgba(0,0,0,0.2);
    text-align:center;
}

.language-selector{
    text-align:right;
    margin-bottom:20px;
}

.language-selector select{
    padding:8px 12px;
    border-radius:8px;
    border:2px solid #38ef7d;
    background-color:white;
    cursor:pointer;
    font-size:14px;
}

h1{
    color:#11998e;
    margin-bottom:15px;
}

.upload-box{
    border:2px dashed #38ef7d;
    padding:20px;
    border-radius:15px;
    background:#f8fffb;
    margin-top:20px;
}

.preview-image{
    width:100%;
    margin-top:20px;
    border-radius:15px;
    border:4px solid #38ef7d;
}

button{
    width:100%;
    margin-top:20px;
    padding:14px;
    border:none;
    border-radius:12px;
    background:linear-gradient(to right,#11998e,#1e3c72);
    color:white;
    font-size:18px;
    cursor:pointer;
    position:relative;
    transition:opacity 0.3s;
}

button:disabled{
    opacity:0.7;
    cursor:not-allowed;
}

.loading-overlay{
    display:none;
    position:fixed;
    inset:0;
    background:rgba(0,0,0,0.55);
    z-index:9999;
    justify-content:center;
    align-items:center;
    flex-direction:column;
    gap:20px;
}

.loading-overlay.active{
    display:flex;
}

.spinner{
    width:64px;
    height:64px;
    border:6px solid rgba(255,255,255,0.3);
    border-top-color:#38ef7d;
    border-radius:50%;
    animation:spin 0.9s linear infinite;
}

@keyframes spin{
    to{transform:rotate(360deg);}
}

.loading-text{
    color:white;
    font-size:18px;
    font-weight:bold;
    letter-spacing:0.5px;
    text-align:center;
}

.loading-sub{
    color:rgba(255,255,255,0.75);
    font-size:13px;
    text-align:center;
    margin-top:-10px;
}

.result{
    margin-top:25px;
    background:#f4fff8;
    padding:20px;
    border-radius:15px;
    text-align:left;
}

.gradcam-container{
    margin-top:20px;
    background:#ffffff;
    padding:15px;
    border-radius:10px;
    border:2px solid #38ef7d;
}

.gradcam-container h3{
    color:#11998e;
    margin-bottom:10px;
    text-align:center;
}

.gradcam-image{
    width:100%;
    max-width:400px;
    border-radius:10px;
    margin:10px auto;
    display:block;
}

.gradcam-info{
    background:#f0fffe;
    padding:10px;
    border-radius:8px;
    margin-top:10px;
    font-size:14px;
    color:#1e3c72;
}

.explanation-tabs{
    display:flex;
    gap:10px;
    margin-top:15px;
    flex-wrap:wrap;
}

.tab-button{
    padding:10px 15px;
    border:2px solid #38ef7d;
    background:white;
    color:#11998e;
    border-radius:8px;
    cursor:pointer;
    font-weight:bold;
    transition:0.3s;
}

.tab-button.active{
    background:#38ef7d;
    color:white;
}

.tab-button:hover{
    background:#38ef7d;
    color:white;
}

.tab-content{
    display:none;
    margin-top:15px;
    background:#f9fffe;
    padding:15px;
    border-radius:10px;
    border:2px solid #38ef7d;
}

.tab-content.active{
    display:block;
}

.explanation-image{
    width:100%;
    max-width:400px;
    border-radius:10px;
    margin:10px auto;
    display:block;
    border:2px solid #38ef7d;
}

.analysis-table{
    width:100%;
    border-collapse:collapse;
    margin-top:10px;
}

.analysis-table th,
.analysis-table td{
    padding:10px;
    text-align:left;
    border-bottom:1px solid #38ef7d;
}

.analysis-table th{
    background:#11998e;
    color:white;
    font-weight:bold;
}

.analysis-table tr:hover{
    background:#f0fffe;
}

.bar-chart{
    display:flex;
    align-items:center;
    gap:10px;
    margin:10px 0;
}

.bar-label{
    min-width:100px;
    font-weight:bold;
    color:#1e3c72;
}

.bar-container{
    flex:1;
    height:25px;
    background:#e0f7f4;
    border-radius:5px;
    overflow:hidden;
}

.bar-fill{
    height:100%;
    background:linear-gradient(to right,#11998e,#38ef7d);
    transition:width 0.3s;
}

.confidence-badge{
    display:inline-block;
    padding:5px 10px;
    border-radius:20px;
    font-size:12px;
    font-weight:bold;
    margin:5px 5px 5px 0;
}

.confidence-high{
    background:#4CAF50;
    color:white;
}

.confidence-medium{
    background:#FF9800;
    color:white;
}

.confidence-low{
    background:#f44336;
    color:white;
}

ul{
    padding-left:20px;
    margin-top:10px;
}

li{
    margin-bottom:8px;
}

.confidence{
    color:#1e3c72;
    font-weight:bold;
    margin-top:10px;
}

.quality-warnings{
    background:#fff3cd;
    border:2px solid #ffc107;
    border-radius:10px;
    padding:15px;
    margin-bottom:20px;
    border-left:4px solid #ff9800;
}

.warning-message{
    color:#856404;
    font-weight:500;
    margin:8px 0;
    padding:8px;
    background:#fffbea;
    border-radius:5px;
    border-left:3px solid #ff9800;
    padding-left:12px;
}

.warning-message:before{
    content:"ℹ️ ";
    margin-right:8px;
}

</style>

</head>

<body>

<div class="container">

    <div class="language-selector">
        <select id="languageSelect" onchange="changeLanguage(this.value)">
            <option value="en">🇬🇧 English</option>
            <option value="kn">🇮🇳 ಕನ್ನಡ (Kannada)</option>
            <option value="hi">🇮🇳 हिंदी (Hindi)</option>
        </select>
    </div>

    <h1>🌿 {{ title }}</h1>

    <form method="POST" enctype="multipart/form-data">

        <div class="upload-box">

            <h3>{{ select_image }}</h3>

            <input type="file"
                   name="image"
                   id="imageInput"
                   accept="image/*"
                   required>

        </div>

        <img id="preview"
             class="preview-image"
             style="display:none;">

        {% if uploaded_image %}
            <img src="{{ uploaded_image }}"
                 class="preview-image">
        {% endif %}

        <button type="submit" id="analyzeBtn">{{ predict_button }}</button>

    </form>

    <!-- Loading Overlay -->
    <div class="loading-overlay" id="loadingOverlay">
        <div class="spinner"></div>
        <div class="loading-text">🌿 Analysing your plant...</div>
        <div class="loading-sub">Running AI model &amp; generating explanations. Please wait.</div>
    </div>

    {% if prediction %}

    <div class="result">

        {% if quality_warnings %}
        <div class="quality-warnings">
            {% for warning in quality_warnings %}
            <div class="warning-message">{{ warning }}</div>
            {% endfor %}
        </div>
        {% endif %}

        <h2>{{ disease_label }}: {{ prediction }}</h2>

        <h3 class="confidence">
            {{ confidence_label }}: {{ confidence }}%
        </h3>

        <br>

        <h3>{{ why_disease }}</h3>

        <p>{{ explanation }}</p>

        <br>

        <h3>{{ suggested_remedies }}</h3>

        <ul>

            {% for remedy in remedies %}

            <li>{{ remedy }}</li>

            {% endfor %}

        </ul>

        {% if gradcam_image %}
        <div class="gradcam-container">
            <h3>🔍 {{ ai_explanation }}</h3>
            
            <!-- Explanation Tabs -->
            <div class="explanation-tabs">
                <button class="tab-button active" onclick="showTab('gradcam')">Grad-CAM</button>
                <button class="tab-button" onclick="showTab('integrated-gradients')">Integrated Gradients</button>
                {% if lime_image %}
                <button class="tab-button" onclick="showTab('lime')">LIME</button>
                {% endif %}
                <button class="tab-button" onclick="showTab('channel')">Channel Analysis</button>
                <button class="tab-button" onclick="showTab('spatial')">Spatial Analysis</button>
                <button class="tab-button" onclick="showTab('confidence')">Confidence</button>
            </div>
            
            <!-- Grad-CAM Tab -->
            <div id="gradcam" class="tab-content active">
                <h4>Gradient-weighted Class Activation Map</h4>
                <img src="{{ gradcam_image }}" class="explanation-image" alt="Grad-CAM">
                <div class="gradcam-info">
                    <strong>{{ gradcam_info }}</strong><br>
                    {{ gradcam_description }}
                </div>
            </div>
            
            <!-- Integrated Gradients Tab -->
            <div id="integrated-gradients" class="tab-content">
                <h4>Integrated Gradients Attribution</h4>
                {% if integrated_gradients_image %}
                <img src="{{ integrated_gradients_image }}" class="explanation-image" alt="Integrated Gradients">
                <div class="gradcam-info">
                    <strong>{{ integrated_gradients_title }}</strong><br>
                    {{ integrated_gradients_description }}
                </div>
                {% else %}
                <p>Integrated Gradients analysis in progress...</p>
                {% endif %}
            </div>
            
            <!-- LIME Tab -->
            {% if lime_image %}
            <div id="lime" class="tab-content">
                <h4>LIME - Local Interpretable Explanations</h4>
                <img src="{{ lime_image }}" class="explanation-image" alt="LIME">
                <div class="gradcam-info">
                    <strong>{{ lime_title }}</strong><br>
                    {{ lime_description }}
                </div>
            </div>
            {% endif %}
            
            <!-- Channel Importance Tab -->
            <div id="channel" class="tab-content">
                <h4>Color Channel Importance Analysis</h4>
                <p>Shows which color channels (R, G, B) are most important for the prediction:</p>
                {% for channel, importance in channel_importance.items() %}
                <div class="bar-chart">
                    <div class="bar-label">{{ channel }}</div>
                    <div class="bar-container">
                        <div class="bar-fill" style="width:{{ importance * 500 }}%"></div>
                    </div>
                    <span>{{ "%.2f"|format(importance) }}</span>
                </div>
                {% endfor %}
                <div class="gradcam-info">
                    <strong>Interpretation:</strong> Higher values indicate that color channel variations significantly affect the prediction confidence.
                </div>
            </div>
            
            <!-- Spatial Importance Tab -->
            <div id="spatial" class="tab-content">
                <h4>Spatial Region Importance Analysis</h4>
                <p>Importance of different image regions (4x4 grid):</p>
                <table class="analysis-table">
                    <thead>
                        <tr>
                            <th>Region</th>
                            <th>Importance Score</th>
                            <th>Visual</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for region, importance in spatial_importance.items() %}
                        <tr>
                            <td>{{ region }}</td>
                            <td>{{ "%.4f"|format(importance) }}</td>
                            <td>
                                <div class="bar-container" style="width:200px;">
                                    <div class="bar-fill" style="width:{{ importance * 500 }}%"></div>
                                </div>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
                <div class="gradcam-info">
                    <strong>Interpretation:</strong> Higher values indicate regions that significantly impact the disease prediction.
                </div>
            </div>
            
            <!-- Confidence Analysis Tab -->
            <div id="confidence" class="tab-content">
                <h4>Prediction Confidence Across All Classes</h4>
                <p>Model's confidence level for each crop/disease class:</p>
                {% for class_name, data in confidence_analysis.items() %}
                <div class="bar-chart">
                    <div class="bar-label">{{ class_name }}</div>
                    <div class="bar-container">
                        <div class="bar-fill" style="width:{{ data.confidence }}%"></div>
                    </div>
                    <span class="confidence-badge {% if data.confidence > 70 %}confidence-high{% elif data.confidence > 40 %}confidence-medium{% else %}confidence-low{% endif %}">
                        {{ "%.1f"|format(data.confidence) }}%
                    </span>
                </div>
                {% endfor %}
                <div class="gradcam-info">
                    <strong>Interpretation:</strong> Shows model's confidence distribution. The highest bar is the predicted class.
                </div>
            </div>
            
            <div class="gradcam-info" style="margin-top:20px; background:#fff3cd; border-left:4px solid #ffc107;">
                <strong>💡 Tip:</strong> Use different analysis methods to understand different aspects of the model's reasoning. 
                Combine insights for comprehensive model validation.
            </div>
        </div>
        {% endif %}

    </div>

    {% endif %}

</div>

<script>

const imageInput = document.getElementById('imageInput');
const preview = document.getElementById('preview');
const languageSelect = document.getElementById('languageSelect');

// Restore language preference from localStorage
const savedLanguage = localStorage.getItem('selectedLanguage') || 'en';
languageSelect.value = savedLanguage;

imageInput.addEventListener('change', function(){

    const file = this.files[0];

    if(file){

        const reader = new FileReader();

        preview.style.display = "block";

        reader.onload = function(e){
            preview.src = e.target.result;
        }

        reader.readAsDataURL(file);

    }

});

function changeLanguage(lang) {
    localStorage.setItem('selectedLanguage', lang);
    const url = new URL(window.location);
    url.searchParams.set('lang', lang);
    window.location.href = url.toString();
}

function showTab(tabName) {
    // Hide all tab contents
    const tabContents = document.querySelectorAll('.tab-content');
    tabContents.forEach(tab => tab.classList.remove('active'));
    
    // Remove active class from all buttons
    const buttons = document.querySelectorAll('.tab-button');
    buttons.forEach(btn => btn.classList.remove('active'));
    
    // Show selected tab
    const selectedTab = document.getElementById(tabName);
    if (selectedTab) {
        selectedTab.classList.add('active');
    }
    
    // Highlight active button
    event.target.classList.add('active');
}

// Show loading overlay on form submit
document.querySelector('form').addEventListener('submit', function() {
    const overlay = document.getElementById('loadingOverlay');
    const btn = document.getElementById('analyzeBtn');
    if (overlay) overlay.classList.add('active');
    if (btn) btn.disabled = true;
});

</script>

</body>
</html>

"""

# =========================
# MAIN ROUTE
# =========================

@app.route('/', methods=['GET', 'POST'])

def home():

    # Get language from query parameter or default to 'en'
    language = request.args.get('lang', 'en')
    if language not in ['en', 'kn', 'hi']:
        language = 'en'
    
    # Get all translations for the selected language
    trans = get_all_translations(language)

    prediction = None
    explanation = None
    remedy_list = None
    uploaded_image = None
    confidence = None
    gradcam_image = None
    integrated_gradients_image = None
    lime_image = None
    channel_importance = {}
    spatial_importance = {}
    confidence_analysis = {}
    quality_warnings = []

    if request.method == 'POST':

        file = request.files['image']

        filename = secure_filename(file.filename)

        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        file.save(filepath)

        uploaded_image = filepath

        # =========================
        # IMAGE QUALITY ENHANCEMENT
        # =========================
        
        filepath, quality_report = process_image_with_quality_check(filepath)
        quality_warnings = quality_report.get('warnings', [])

        # =========================
        # IMAGE PREPROCESSING
        # =========================
        from tensorflow.keras.preprocessing import image
        img = image.load_img(filepath, target_size=(224, 224))

        img_array = image.img_to_array(img)

        img_array = np.expand_dims(img_array, axis=0)

        img_array = img_array / 255.0

        # =========================
        # PREDICTION (Lazy Loading)
        # =========================

        model = get_model()
        prediction_result = model.predict(img_array)

        predicted_class = np.argmax(prediction_result)

        prediction = class_names[predicted_class]

        confidence = np.max(prediction_result) * 100

        confidence = round(confidence, 2)

        # =========================
        # COMPREHENSIVE EXPLAINABILITY (with cache)
        # =========================

        # Compute MD5 of the uploaded file for cache lookup
        with open(filepath, 'rb') as f:
            img_hash = hashlib.md5(f.read()).hexdigest()

        if img_hash in _explanation_cache:
            # Serve from cache – no GPU computation needed
            explanations = _explanation_cache[img_hash]
        else:
            try:
                explanations_dir = app.config['UPLOAD_FOLDER']
                os.makedirs(explanations_dir, exist_ok=True)

                explanations = get_comprehensive_explanation(
                    model=model,
                    img_array=img_array,
                    original_img_path=filepath,
                    output_dir=explanations_dir,
                    class_names=class_names
                )
                _explanation_cache[img_hash] = explanations

            except Exception as e:
                print(f"Warning: Could not generate comprehensive explanations: {str(e)}")
                explanations = {}

        # Extract explanation results
        if explanations.get('gradcam'):
            gradcam_image = explanations['gradcam']

        if explanations.get('integrated_gradients'):
            integrated_gradients_image = explanations['integrated_gradients']

        if explanations.get('lime'):
            lime_image = explanations['lime']

        channel_importance = explanations.get('channel_importance', {})
        spatial_importance = explanations.get('spatial_importance', {})
        confidence_analysis = explanations.get('confidence_analysis', {})

        # =========================
        # LABEL CONVERSION WITH TRANSLATIONS
        # =========================

        if prediction == "rice_false_smut":

            prediction = get_translation(language, 'rice_smut')

            explanation = get_translation(language, 'explanation_rice_smut')

        elif prediction == "diseased_cardamon":

            prediction = get_translation(language, 'diseased_cardamon')

            explanation = get_translation(language, 'explanation_cardamom_disease')

        elif prediction == "healthy_rice_plant":

            prediction = get_translation(language, 'healthy_rice')

            explanation = get_translation(language, 'explanation_healthy_rice')

        else:

            prediction = get_translation(language, 'healthy_cardamon')

            explanation = get_translation(language, 'explanation_healthy_cardamom')

        remedy_list = get_remedies(language, prediction)

    return render_template_string(

        HTML,

        title=trans['title'],
        select_image=trans['select_image'],
        predict_button=trans['predict_button'],
        disease_label=trans['disease_label'],
        confidence_label=trans['confidence_label'],
        why_disease=trans['why_disease'],
        suggested_remedies=trans['suggested_remedies'],
        ai_explanation=trans.get('ai_explanation', 'AI Model Explanation'),
        gradcam_info=trans.get('gradcam_info', 'How the AI sees it:'),
        gradcam_description=trans.get('gradcam_description', 'The highlighted areas show regions the AI model focused on to make this prediction. Bright colors indicate higher importance.'),
        integrated_gradients_title=trans.get('integrated_gradients_title', 'Feature Attribution Analysis'),
        integrated_gradients_description=trans.get('integrated_gradients_description', 'Shows which pixels are most important for the prediction.'),
        lime_title=trans.get('lime_title', 'Local Interpretable Model-Agnostic Explanations'),
        lime_description=trans.get('lime_description', 'Highlights image segments that contribute to the prediction.'),

        prediction=prediction,

        explanation=explanation,

        remedies=remedy_list,

        uploaded_image=uploaded_image,

        confidence=confidence,
        
        gradcam_image=gradcam_image,
        integrated_gradients_image=integrated_gradients_image,
        lime_image=lime_image,
        channel_importance=channel_importance,
        spatial_importance=spatial_importance,
        confidence_analysis=confidence_analysis,
        quality_warnings=quality_warnings
    )

# =========================
# RUN APP
# =========================

if __name__ == '__main__':

    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)