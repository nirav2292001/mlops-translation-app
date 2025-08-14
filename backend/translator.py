from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import mlflow
import time
from typing import Dict, Optional
import os

# Supported languages and their corresponding models
SUPPORTED_LANGUAGES = {
    'de': 'Helsinki-NLP/opus-mt-en-de',  # German
    'fr': 'Helsinki-NLP/opus-mt-en-fr',  # French
    'es': 'Helsinki-NLP/opus-mt-en-es',  # Spanish
    'it': 'Helsinki-NLP/opus-mt-en-it',  # Italian
    'pt': 'Helsinki-NLP/opus-mt-en-pt',  # Portuguese
    'ru': 'Helsinki-NLP/opus-mt-en-ru',  # Russian
    'zh': 'Helsinki-NLP/opus-mt-en-zh'   # Chinese
}

# MLflow tracking settings
MLFLOW_DIR = os.getenv("MLFLOW_DIR", "/mlflow_logs")
os.makedirs(MLFLOW_DIR, exist_ok=True)
mlflow.set_tracking_uri(f"file:{MLFLOW_DIR}")
mlflow.set_experiment("translation_service")

# Cache for loaded models
_models: Dict[str, Dict] = {}

def get_model(lang_code: str):
    """Get or load the model for the specified language code."""
    if lang_code not in SUPPORTED_LANGUAGES:
        raise ValueError(f"Unsupported language code: {lang_code}")
    
    if lang_code not in _models:
        model_name = SUPPORTED_LANGUAGES[lang_code]
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        _models[lang_code] = {
            'tokenizer': tokenizer,
            'model': model,
            'pipeline': pipeline('translation_en_to_xx', model=model, tokenizer=tokenizer, src_lang='en', tgt_lang=lang_code)
        }
    
    return _models[lang_code]

def translate(text: str, target_lang: str = 'de') -> str:
    """
    Translate text from English to the target language.
    
    Args:
        text: The input text to translate (English)
        target_lang: Target language code (e.g., 'de' for German, 'fr' for French)
        
    Returns:
        Translated text in the target language
    """
    if not text.strip():
        return ""
        
    with mlflow.start_run():
        try:
            # Get or load the model for the target language
            model_info = get_model(target_lang)
            
            # Log basic params
            mlflow.log_param("model", SUPPORTED_LANGUAGES[target_lang])
            mlflow.log_param("target_language", target_lang)
            mlflow.log_param("input_length", len(text))

            # Inference timing
            start_time = time.time()
            
            # Use the pipeline for translation
            translation = model_info['pipeline'](text, max_length=512, num_beams=4, early_stopping=True)
            translated_text = translation[0]['translation_text']
            
            end_time = time.time()

            # Log metrics and outputs
            mlflow.log_metric("inference_time_ms", (end_time - start_time) * 1000)
            mlflow.log_text(text, "input.txt")
            mlflow.log_text(translated_text, "output.txt")

            return translated_text
            
        except Exception as e:
            mlflow.log_param("error", str(e))
            raise ValueError(f"Translation failed: {str(e)}")

def get_supported_languages() -> Dict[str, str]:
    """Return a dictionary of supported language codes and their display names."""
    return {
        'de': 'German',
        'fr': 'French',
        'es': 'Spanish',
        'it': 'Italian',
        'pt': 'Portuguese',
        'ru': 'Russian',
        'zh': 'Chinese'
    }
