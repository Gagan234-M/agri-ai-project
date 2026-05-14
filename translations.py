# Translations for multilanguage support
# Kannada, English, Hindi

TRANSLATIONS = {
    'en': {
        # UI Strings
        'title': 'Agri AI Disease Detection',
        'select_image': 'Select Crop Image',
        'predict_button': 'Predict Disease',
        'disease_label': 'Disease',
        'confidence_label': 'Confidence',
        'why_disease': 'Why this disease?',
        'suggested_remedies': 'Suggested Remedies',
        'language': 'Language',
        
        # Class Names (Disease/Plant Names)
        'healthy_cardamon': 'Healthy Cardamom',
        'diseased_cardamon': 'Cardamom Leaf Spot',
        'healthy_rice': 'Healthy Rice Plant',
        'rice_smut': 'Rice False Smut',
        
        # Explanations
        'explanation_rice_smut': 'AI detected fungal smut patterns and grain discoloration in rice crop.',
        'explanation_cardamom_disease': 'AI detected infected leaf spot regions in cardamom crop.',
        'explanation_healthy_rice': 'AI detected healthy rice crop characteristics.',
        'explanation_healthy_cardamom': 'AI detected healthy cardamom leaf patterns.',
        
        # Grad-CAM Explanations
        'ai_explanation': 'AI Model Explanation (Grad-CAM)',
        'gradcam_info': 'How the AI sees it:',
        'gradcam_description': 'The highlighted areas show regions the AI model focused on to make this prediction. Bright colors indicate higher importance.',
        
        # Integrated Gradients
        'integrated_gradients_title': 'Feature Attribution Analysis',
        'integrated_gradients_description': 'Shows which pixels contribute most to the prediction. Warmer colors indicate higher attribution.',
        
        # LIME Explanations
        'lime_title': 'Local Interpretable Model-Agnostic Explanations',
        'lime_description': 'Highlights image segments that most influence the prediction. Useful for understanding local decision boundaries.',
        
        # Remedies
        'remedies': {
            'Rice False Smut': [
                'Use certified seeds',
                'Avoid excess nitrogen fertilizer',
                'Apply recommended fungicide'
            ],
            'Cardamom Leaf Spot': [
                'Remove infected leaves',
                'Use copper fungicide',
                'Maintain proper drainage'
            ],
            'Healthy Rice Plant': [
                'No disease detected',
                'Maintain proper irrigation',
                'Continue good farming practices'
            ],
            'Healthy Cardamom': [
                'No disease detected',
                'Maintain proper shade',
                'Use organic manure regularly'
            ]
        }
    },
    
    'kn': {
        # UI Strings - Kannada
        'title': 'ಕೃಷಿ AI ರೋಗ ಪತ್ತೆ ವ್ಯವಸ್ಥೆ',
        'select_image': 'ಬೆಳೆಯ ಚಿತ್ರ ಆಯ್ಕೆ ಮಾಡಿ',
        'predict_button': 'ರೋಗ ಮುನ್ನಾಮೂದ',
        'disease_label': 'ರೋಗ',
        'confidence_label': 'ವಿಶ್ವಾಸಾರ್ಹತೆ',
        'why_disease': 'ಈ ರೋಗ ಏಕೆ?',
        'suggested_remedies': 'ಸೂಚಿತ ಪರಿಹಾರಗಳು',
        'language': 'ಭಾಷೆ',
        
        # Class Names - Kannada
        'healthy_cardamon': 'ಆರೋಗ್ಯಕರ ಏಲಕ್ಕಿ',
        'diseased_cardamon': 'ಏಲಕ್ಕಿ ಪತ್ರ ಕಲೆ',
        'healthy_rice': 'ಆರೋಗ್ಯಕರ ಅಕ್ಕಿ ಬೆಳೆ',
        'rice_smut': 'ಅಕ್ಕಿ ಸುಸ್ತ ರೋಗ',
        
        # Explanations - Kannada
        'explanation_rice_smut': 'AI ಅಕ್ಕಿ ಬೆಳೆಯಲ್ಲಿ ಶಿಲೀಂಧ್ರ ಸುಸ್ತ ಮಾದರಿ ಮತ್ತು ಧಾನ್ಯ ಬಣ್ಣ ಬದಲಾವಣೆ ಪತ್ತೆ ಹಿಡಿದಿದೆ.',
        'explanation_cardamom_disease': 'AI ಏಲಕ್ಕಿ ಬೆಳೆಯಲ್ಲಿ ಸೋಂಕಿತ ಪತ್ರ ಕಲೆ ಪ್ರದೇಶಗಳು ಪತ್ತೆ ಹಿಡಿದಿದೆ.',
        'explanation_healthy_rice': 'AI ಆರೋಗ್ಯಕರ ಅಕ್ಕಿ ಬೆಳೆಯ ಗುಣಲಕ್ಷಣಗಳು ಪತ್ತೆ ಹಿಡಿದಿದೆ.',
        'explanation_healthy_cardamom': 'AI ಆರೋಗ್ಯಕರ ಏಲಕ್ಕಿ ಪತ್ರ ಮಾದರಿಗಳು ಪತ್ತೆ ಹಿಡಿದಿದೆ.',
        
        # Grad-CAM Explanations - Kannada
        'ai_explanation': 'AI ಮಾದರಿ ವಿವರಣೆ (Grad-CAM)',
        'gradcam_info': 'AI ಹೇಗೆ ನೋಡಿತ್ತೆ:',
        'gradcam_description': 'ಹೈಲೈಟ್ ಮಾಡಿದ ಪ್ರದೇಶಗಳು AI ಮಾದರಿ ಈ ಮುನ್ನಾಮೂದಿಗಾಗಿ ಕೇಂದ್ರೀಕೃತ ಪ್ರದೇಶಗಳನ್ನು ತೋರಿಸುತ್ತವೆ.',
        
        # Integrated Gradients - Kannada
        'integrated_gradients_title': 'ವೈಶಿಷ್ಟ್ಯ ಆಪರ್ಚನ ವಿಶ್ಲೇಷಣೆ',
        'integrated_gradients_description': 'ಯಾವ ಪಿಕ್ಸೆಲ್‍ಗಳು ಮುನ್ನಾಮೂದಿಗೆ ಹೆಚ್ಚಾಗಿ ಕೊಡುಗೆ ನೀಡುತ್ತವೆ ಎಂಬುದನ್ನು ತೋರಿಸುತ್ತದೆ.',
        
        # LIME - Kannada
        'lime_title': 'ಸ್ಥಳೀಯ ವ್ಯಾಖ್ಯಾನಕ್ಕೆ ಸುಲಭವಾದ ಮಾದರಿ-ಅಜ್ಞೇಯ ವಿವರಣೆಗಳು',
        'lime_description': 'ಮುನ್ನಾಮೂದಿ ಮೇಲೆ ಹೆಚ್ಚು ಪ್ರಭಾವ ಬೀರುವ ಚಿತ್ರ ವಿಭಾಗಗಳನ್ನು ಹೈಲೈಟ್ ಮಾಡುತ್ತದೆ.',
        
        # Remedies - Kannada
        'remedies': {
            'ಅಕ್ಕಿ ಸುಸ್ತ ರೋಗ': [
                'ಪ್ರಮಾಣಿತ ಬೀಜಗಳನ್ನು ಬಳಸಿ',
                'ಹೆಚ್ಚಿನ ನೈಟ್ರೋಜನ್ ಸಾರವನ್ನು ತಪ್ಪಿಸಿ',
                'ಶಿಲೀಂಧ್ರನಾಶಕ ಅನ್ವಯ ಮಾಡಿ'
            ],
            'ಏಲಕ್ಕಿ ಪತ್ರ ಕಲೆ': [
                'ಸೋಂಕಿತ ಪತ್ರಗಳನ್ನು ತೆಗೆದುಹಾಕಿ',
                'ತಾಮ್ರ ಶಿಲೀಂಧ್ರನಾಶಕ ಬಳಸಿ',
                'ಸರಿಯಾದ ನೀರಾವರಣ ಕಾಪಾಡಿ'
            ],
            'ಆರೋಗ್ಯಕರ ಅಕ್ಕಿ ಬೆಳೆ': [
                'ಕೋಸ್ಟ ರೋಗ ಇಲ್ಲ',
                'ಸರಿಯಾದ ನೀರಾವರಣ ನಿರ್ವಹಣೆ ಮಾಡಿ',
                'ಚೆನ್ನಾಗಿ ಕೃಷಿ ಅಭ್ಯಾಸ ಮುಂದುವರಿಸಿ'
            ],
            'ಆರೋಗ್ಯಕರ ಏಲಕ್ಕಿ': [
                'ಕೋಸ್ಟ ರೋಗ ಇಲ್ಲ',
                'ಸರಿಯಾದ ನೆರಳು ನಿರ್ವಹಣೆ ಮಾಡಿ',
                'ನಿಯಮಿತವಾಗಿ ಸಾವಯವ ಸಾರವನ್ನು ಬಳಸಿ'
            ]
        }
    },
    
    'hi': {
        # UI Strings - Hindi
        'title': 'कृषि AI रोग पहचान',
        'select_image': 'फसल की तस्वीर चुनें',
        'predict_button': 'रोग की भविष्यवाणी करें',
        'disease_label': 'रोग',
        'confidence_label': 'आत्मविश्वास',
        'why_disease': 'यह रोग क्यों?',
        'suggested_remedies': 'सुझाए गए उपचार',
        'language': 'भाषा',
        
        # Class Names - Hindi
        'healthy_cardamon': 'स्वस्थ इलायची',
        'diseased_cardamon': 'इलायची पत्ती धब्बा',
        'healthy_rice': 'स्वस्थ चावल का पौधा',
        'rice_smut': 'चावल गलन रोग',
        
        # Explanations - Hindi
        'explanation_rice_smut': 'AI ने चावल की फसल में कवक स्मट पैटर्न और अनाज का रंग परिवर्तन पहचाना।',
        'explanation_cardamom_disease': 'AI ने इलायची की फसल में संक्रमित पत्ती धब्बे क्षेत्रों को पहचाना।',
        'explanation_healthy_rice': 'AI ने स्वस्थ चावल की फसल की विशेषताओं को पहचाना।',
        'explanation_healthy_cardamom': 'AI ने स्वस्थ इलायची के पत्ते के पैटर्न को पहचाना।',
        
        # Grad-CAM Explanations - Hindi
        'ai_explanation': 'AI मॉडल व्याख्या (Grad-CAM)',
        'gradcam_info': 'AI इसे कैसे देखता है:',
        'gradcam_description': 'हाइलाइट किए गए क्षेत्र उन क्षेत्रों को दिखाते हैं जिन पर AI मॉडल इस भविष्यवाणी के लिए केंद्रित था।',
        
        # Integrated Gradients - Hindi
        'integrated_gradients_title': 'विशेषता एट्रिब्यूशन विश्लेषण',
        'integrated_gradients_description': 'दिखाता है कि कौन से पिक्सेल भविष्यवाणी के लिए सबसे अधिक महत्वपूर्ण हैं।',
        
        # LIME - Hindi
        'lime_title': 'स्थानीय व्याख्या योग्य मॉडल-अज्ञेयवादी व्याख्या',
        'lime_description': 'छवि खंडों को हाइलाइट करता है जो भविष्यवाणी को सबसे अधिक प्रभावित करते हैं।',
        
        # Remedies - Hindi
        'remedies': {
            'चावल गलन रोग': [
                'प्रमाणित बीज का उपयोग करें',
                'अधिक नाइट्रोजन खाद से बचें',
                'अनुशंसित कवकनाशी लागू करें'
            ],
            'इलायची पत्ती धब्बा': [
                'संक्रमित पत्तियों को हटाएं',
                'तांबे का कवकनाशी उपयोग करें',
                'उचित जल निकासी बनाए रखें'
            ],
            'स्वस्थ चावल का पौधा': [
                'कोई रोग नहीं पाया गया',
                'उचित सिंचाई बनाए रखें',
                'अच्छी खेती के तरीकों को जारी रखें'
            ],
            'स्वस्थ इलायची': [
                'कोई रोग नहीं पाया गया',
                'उचित छाया बनाए रखें',
                'नियमित रूप से जैविक खाद का उपयोग करें'
            ]
        }
    }
}

def get_translation(language, key):
    """Get translation for a given key in specified language"""
    if language not in TRANSLATIONS:
        language = 'en'  # Default to English
    
    translations = TRANSLATIONS[language]
    return translations.get(key, key)

def get_remedies(language, disease_name):
    """Get remedies for a disease in specified language"""
    if language not in TRANSLATIONS:
        language = 'en'
    
    remedies_dict = TRANSLATIONS[language]['remedies']
    return remedies_dict.get(disease_name, [])

def get_all_translations(language):
    """Get all translations for a language"""
    if language not in TRANSLATIONS:
        language = 'en'
    return TRANSLATIONS[language]
