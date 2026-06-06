import io
import tempfile
from gtts import gTTS, gTTSError


def text_to_speech(text, lang="en"):
    try:
        if not text or not text.strip():
            return {"success": False, "error": "No text provided for speech synthesis."}
        tts = gTTS(text=text, lang=lang, slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return {"success": True, "audio_bytes": fp.read()}
    except gTTSError as e:
        return {"success": False, "error": f"Speech synthesis error: {str(e)}"}
    except Exception as e:
        return {"success": False, "error": f"Speech error: {str(e)}"}
