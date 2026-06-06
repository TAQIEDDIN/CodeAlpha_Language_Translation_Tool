from langdetect import detect, DetectorFactory, LangDetectException

from utils.translator import LANGUAGES

DetectorFactory.seed = 0


def detect_language(text):
    try:
        if not text or not text.strip():
            return {"success": False, "error": "No text provided for detection."}
        if len(text.strip()) < 3:
            return {"success": False, "error": "Text too short for reliable detection (min 3 characters)."}
        code = detect(text)
        name = _get_language_name_from_code(code)
        if name:
            return {"success": True, "language_code": code, "language_name": name}
        return {"success": True, "language_code": code, "language_name": code}
    except LangDetectException:
        return {"success": False, "error": "Could not detect language. Try selecting manually."}
    except Exception as e:
        return {"success": False, "error": f"Detection error: {str(e)}"}


def _get_language_name_from_code(code):
    for name, lang_code in LANGUAGES.items():
        if lang_code == code:
            return name
    return None
