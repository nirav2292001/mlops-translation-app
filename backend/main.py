from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from translator import translate, get_supported_languages
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import time
from database import log_translation, get_recent_translations
from typing import List, Dict, Any, Optional

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use specific domain in production
    allow_methods=["*"],
    allow_headers=["*"],
)

class TranslationRequest(BaseModel):
    text: str
    target_lang: str = 'de'  # Default to German

@app.get("/languages")
async def list_supported_languages():
    """Return the list of supported translation languages."""
    return get_supported_languages()

@app.post("/translate")
async def translate_text(request: TranslationRequest):
    start_time = time.time()
    
    try:
        # Perform translation with the specified target language
        translated_text = translate(request.text, request.target_lang)
        
        # Log to MongoDB
        metadata = {
            "model": f"Helsinki-NLP/opus-mt-en-{request.target_lang}",
            "target_language": request.target_lang,
            "input_length": len(request.text),
            "processing_time_ms": (time.time() - start_time) * 1000
        }
        log_translation(request.text, translated_text, metadata)
        
        return {
            "translated_text": translated_text,
            "target_language": request.target_lang
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation error: {str(e)}")

@app.get("/translations", response_model=List[Dict[str, Any]])
async def get_translations(limit: int = 10):
    """
    Retrieve recent translations from the database.
    
    Args:
        limit: Maximum number of translations to return (default: 10)
    """
    try:
        translations = get_recent_translations(limit)
        # Convert ObjectId to string for JSON serialization
        for trans in translations:
            trans['_id'] = str(trans['_id'])
            trans['timestamp'] = trans['timestamp'].isoformat()
        return translations
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run directly if this is the main file
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
