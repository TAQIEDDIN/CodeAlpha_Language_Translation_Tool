from deep_translator import GoogleTranslator

LANGUAGES = {
    "Afrikaans": "af", "Albanian": "sq", "Amharic": "am", "Arabic": "ar",
    "Armenian": "hy", "Azerbaijani": "az", "Basque": "eu", "Belarusian": "be",
    "Bengali": "bn", "Bosnian": "bs", "Bulgarian": "bg", "Catalan": "ca",
    "Cebuano": "ceb", "Chinese (Simplified)": "zh-CN", "Chinese (Traditional)": "zh-TW",
    "Corsican": "co", "Croatian": "hr", "Czech": "cs", "Danish": "da",
    "Dutch": "nl", "English": "en", "Esperanto": "eo", "Estonian": "et",
    "Finnish": "fi", "French": "fr", "Frisian": "fy", "Galician": "gl",
    "Georgian": "ka", "German": "de", "Greek": "el", "Gujarati": "gu",
    "Haitian Creole": "ht", "Hausa": "ha", "Hawaiian": "haw", "Hebrew": "iw",
    "Hindi": "hi", "Hmong": "hmn", "Hungarian": "hu", "Icelandic": "is",
    "Igbo": "ig", "Indonesian": "id", "Irish": "ga", "Italian": "it",
    "Japanese": "ja", "Javanese": "jw", "Kannada": "kn", "Kazakh": "kk",
    "Khmer": "km", "Kinyarwanda": "rw", "Korean": "ko", "Kurdish": "ku",
    "Kyrgyz": "ky", "Lao": "lo", "Latin": "la", "Latvian": "lv",
    "Lithuanian": "lt", "Luxembourgish": "lb", "Macedonian": "mk",
    "Malagasy": "mg", "Malay": "ms", "Malayalam": "ml", "Maltese": "mt",
    "Maori": "mi", "Marathi": "mr", "Mongolian": "mn", "Myanmar (Burmese)": "my",
    "Nepali": "ne", "Norwegian": "no", "Nyanja (Chichewa)": "ny",
    "Odia (Oriya)": "or", "Pashto": "ps", "Persian": "fa", "Polish": "pl",
    "Portuguese": "pt", "Punjabi": "pa", "Romanian": "ro", "Russian": "ru",
    "Samoan": "sm", "Scots Gaelic": "gd", "Serbian": "sr", "Sesotho": "st",
    "Shona": "sn", "Sindhi": "sd", "Sinhala (Sinhalese)": "si", "Slovak": "sk",
    "Slovenian": "sl", "Somali": "so", "Spanish": "es", "Sundanese": "su",
    "Swahili": "sw", "Swedish": "sv", "Tagalog (Filipino)": "tl", "Tajik": "tg",
    "Tamil": "ta", "Tatar": "tt", "Telugu": "te", "Thai": "th",
    "Turkish": "tr", "Turkmen": "tk", "Ukrainian": "uk", "Urdu": "ur",
    "Uyghur": "ug", "Uzbek": "uz", "Vietnamese": "vi", "Welsh": "cy",
    "Xhosa": "xh", "Yiddish": "yi", "Yoruba": "yo", "Zulu": "zu"
}


def translate_text(text, source_lang="auto", target_lang="en"):
    try:
        if not text or not text.strip():
            return {"success": False, "error": "Please enter text to translate."}
        if source_lang == "auto":
            translator = GoogleTranslator(source="auto", target=target_lang)
        else:
            translator = GoogleTranslator(source=source_lang, target=target_lang)
        result = translator.translate(text)
        if not result or result.strip() == "":
            return {"success": False, "error": "Translation returned empty result. Try a different language pair."}
        return {"success": True, "translated_text": result}
    except Exception as e:
        error_msg = str(e)
        if "too many" in error_msg.lower():
            return {"success": False, "error": "Too many requests. Please wait a moment and try again."}
        if "not supported" in error_msg.lower():
            return {"success": False, "error": "Unsupported language combination. Please try different languages."}
        if "connection" in error_msg.lower():
            return {"success": False, "error": "Network error. Please check your internet connection."}
        return {"success": False, "error": f"Translation failed: {error_msg}"}


def get_language_name(code):
    for name, lang_code in LANGUAGES.items():
        if lang_code == code:
            return name
    return code


def get_language_code(name):
    return LANGUAGES.get(name, name)
