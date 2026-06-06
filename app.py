import streamlit as st
import pyperclip
from datetime import datetime

from utils.translator import translate_text, LANGUAGES, get_language_code
from utils.language_detector import detect_language
from utils.speech import text_to_speech

st.set_page_config(
    page_title="AI Language Translation Tool",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

LANGUAGE_NAMES = sorted(LANGUAGES.keys())


def apply_custom_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');

        * { font-family: 'Inter', sans-serif; }

        .stApp {
            background: #0f0f1a;
        }

        .main-header {
            background: linear-gradient(135deg, #1a1a3e 0%, #16213e 50%, #0f3460 100%);
            padding: 2.5rem 2rem;
            border-radius: 20px;
            text-align: center;
            margin-bottom: 2rem;
            border: 1px solid rgba(255,255,255,0.06);
            position: relative;
            overflow: hidden;
        }
        .main-header::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle at 30% 50%, rgba(102,126,234,0.08) 0%, transparent 60%),
                        radial-gradient(circle at 70% 50%, rgba(118,75,162,0.08) 0%, transparent 60%);
            animation: pulse 8s ease-in-out infinite;
        }
        @keyframes pulse {
            0%, 100% { transform: scale(1); opacity: 0.5; }
            50% { transform: scale(1.05); opacity: 1; }
        }
        .main-header h1 {
            font-size: 2.6rem;
            font-weight: 800;
            margin: 0;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            position: relative;
            letter-spacing: -1px;
        }
        .main-header .subtitle {
            font-size: 1.05rem;
            color: rgba(255,255,255,0.6);
            margin-top: 0.6rem;
            position: relative;
            font-weight: 300;
        }
        .main-header .glow {
            position: absolute;
            width: 300px;
            height: 300px;
            background: radial-gradient(circle, rgba(102,126,234,0.15) 0%, transparent 70%);
            border-radius: 50%;
            top: -100px;
            right: -100px;
            animation: float 6s ease-in-out infinite;
        }
        @keyframes float {
            0%, 100% { transform: translateY(0) rotate(0deg); }
            50% { transform: translateY(-20px) rotate(5deg); }
        }

        .card {
            background: linear-gradient(145deg, #1a1a2e, #16213e);
            border-radius: 16px;
            padding: 1.5rem;
            border: 1px solid rgba(255,255,255,0.06);
            margin-bottom: 1.2rem;
            box-shadow: 0 8px 32px rgba(0,0,0,0.2);
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .card:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 40px rgba(0,0,0,0.3);
        }
        .card-title {
            font-size: 0.85rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            color: rgba(255,255,255,0.4);
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .card-title i {
            font-size: 1rem;
        }

        .result-box {
            background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 100%);
            border-radius: 12px;
            padding: 1.3rem;
            border: 1px solid rgba(255,255,255,0.08);
            min-height: 120px;
            color: #e0e0e0;
            font-size: 1.05rem;
            line-height: 1.7;
            position: relative;
        }
        .result-box::before {
            content: '"';
            position: absolute;
            top: -5px;
            left: 10px;
            font-size: 3rem;
            color: rgba(102,126,234,0.15);
            font-family: serif;
        }

        .detected-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            background: rgba(102,126,234,0.15);
            color: #8892f0;
            padding: 0.3rem 0.9rem;
            border-radius: 20px;
            font-size: 0.78rem;
            font-weight: 500;
            border: 1px solid rgba(102,126,234,0.2);
            margin-bottom: 0.8rem;
        }

        .stTextArea textarea {
            background: #0f0f1a !important;
            border: 1px solid rgba(255,255,255,0.08) !important;
            border-radius: 12px !important;
            color: #e0e0e0 !important;
            font-size: 0.95rem !important;
            line-height: 1.6 !important;
            transition: border-color 0.2s !important;
        }
        .stTextArea textarea:focus {
            border-color: rgba(102,126,234,0.5) !important;
            box-shadow: 0 0 0 2px rgba(102,126,234,0.1) !important;
        }
        div[data-testid="stTextArea"] label { display: none; }

        .char-counter {
            text-align: right;
            font-size: 0.75rem;
            color: rgba(255,255,255,0.3);
            margin-top: 0.3rem;
            font-weight: 400;
        }

        .stSelectbox label { display: none; }
        div[data-testid="stSelectbox"] > div {
            background: #0f0f1a !important;
            border: 1px solid rgba(255,255,255,0.08) !important;
            border-radius: 10px !important;
            color: #e0e0e0 !important;
        }

        .stButton > button {
            border-radius: 10px !important;
            font-weight: 600 !important;
            transition: all 0.3s !important;
            height: 48px !important;
            letter-spacing: 0.3px !important;
        }
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #667eea, #764ba2) !important;
            border: none !important;
            color: white !important;
            font-size: 1rem !important;
            box-shadow: 0 4px 20px rgba(102,126,234,0.3) !important;
        }
        .stButton > button[kind="primary"]:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 30px rgba(102,126,234,0.4) !important;
        }
        .stButton > button:not([kind="primary"]) {
            background: rgba(255,255,255,0.05) !important;
            border: 1px solid rgba(255,255,255,0.08) !important;
            color: #c0c0c0 !important;
            font-size: 0.85rem !important;
        }
        .stButton > button:not([kind="primary"]):hover {
            background: rgba(255,255,255,0.1) !important;
            border-color: rgba(102,126,234,0.3) !important;
            color: white !important;
        }

        div[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0f0f1a 0%, #1a1a2e 100%) !important;
            border-right: 1px solid rgba(255,255,255,0.05) !important;
        }
        div[data-testid="stSidebar"] .sidebar-content { padding: 1.5rem 1.2rem; }
        .sidebar-section {
            margin-bottom: 2rem;
        }
        .sidebar-section h3 {
            font-size: 0.8rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            color: rgba(255,255,255,0.3);
            margin-bottom: 1rem;
        }
        .sidebar-text {
            color: rgba(255,255,255,0.55);
            font-size: 0.88rem;
            line-height: 1.7;
        }
        .sidebar-text strong { color: rgba(255,255,255,0.8); }
        .sidebar-divider {
            border: none;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.06), transparent);
            margin: 1.5rem 0;
        }

        .history-item {
            background: rgba(255,255,255,0.03);
            border-radius: 10px;
            padding: 0.8rem;
            margin-bottom: 0.6rem;
            border: 1px solid rgba(255,255,255,0.05);
            font-size: 0.82rem;
            color: rgba(255,255,255,0.7);
            transition: background 0.2s;
        }
        .history-item:hover { background: rgba(255,255,255,0.06); }
        .history-item .time {
            color: rgba(255,255,255,0.3);
            font-size: 0.7rem;
        }
        .history-item .lang-pair {
            color: rgba(255,255,255,0.5);
            font-size: 0.75rem;
            margin: 0.2rem 0;
        }
        .history-item .lang-pair strong { color: #8892f0; }

        .action-buttons {
            display: flex;
            gap: 0.5rem;
            margin-top: 1rem;
        }

        .footer {
            text-align: center;
            color: rgba(255,255,255,0.2);
            font-size: 0.8rem;
            padding: 2rem 0 1rem;
            border-top: 1px solid rgba(255,255,255,0.04);
            margin-top: 3rem;
        }
        .footer strong { color: rgba(255,255,255,0.35); }

        .placeholder-text {
            color: rgba(255,255,255,0.2);
            font-style: italic;
        }

        @media (max-width: 768px) {
            .main-header h1 { font-size: 1.8rem; }
            .main-header .subtitle { font-size: 0.9rem; }
        }

        div[data-testid="stMetricValue"] { font-size: 1.2rem !important; }
        .stAlert { border-radius: 10px !important; }
        div[data-testid="stAudio"] { margin-top: 0.5rem; }
        </style>
    """, unsafe_allow_html=True)


def render_header():
    st.markdown("""
        <div class="main-header">
            <div class="glow"></div>
            <h1><i class="fas fa-language" style="font-size: 2rem; margin-right: 0.5rem;"></i> AI Language Translation Tool</h1>
            <p class="subtitle">Translate Text Between Multiple Languages Using Artificial Intelligence</p>
        </div>
    """, unsafe_allow_html=True)


def render_sidebar():
    with st.sidebar:
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown("<h3><i class='fas fa-info-circle'></i> About Project</h3>", unsafe_allow_html=True)
        st.markdown("""
            <div class="sidebar-text">
                This <strong>AI-powered</strong> translation tool leverages the 
                Google Translate API to deliver fast, accurate translations 
                across <strong>100+ languages</strong> worldwide.
                <br><br>
                <i class="fas fa-check-circle" style="color: #667eea; margin-right: 6px;"></i> Real-time translation<br>
                <i class="fas fa-check-circle" style="color: #667eea; margin-right: 6px;"></i> Auto language detection<br>
                <i class="fas fa-check-circle" style="color: #667eea; margin-right: 6px;"></i> Text-to-speech output<br>
                <i class="fas fa-check-circle" style="color: #667eea; margin-right: 6px;"></i> Download & copy support<br>
                <i class="fas fa-check-circle" style="color: #667eea; margin-right: 6px;"></i> Translation history
            </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)

        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown("<h3><i class='fas fa-globe'></i> Supported Languages</h3>", unsafe_allow_html=True)
        st.markdown(f"""
            <div class="sidebar-text">
                <i class="fas fa-check" style="color: #667eea; font-size: 0.7rem;"></i> <strong>{len(LANGUAGES)}+ languages</strong><br>
                Including English, Spanish, French, German, Arabic, Turkish, Chinese, Japanese, Hindi, Russian, Portuguese, Italian, Dutch, Korean, and many more.
            </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)

        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown("<h3><i class='fas fa-history'></i> Translation History</h3>", unsafe_allow_html=True)

        if "history" not in st.session_state:
            st.session_state.history = []

        if not st.session_state.history:
            st.markdown('<div class="sidebar-text" style="color: rgba(255,255,255,0.25);">No translations yet.</div>', unsafe_allow_html=True)
        else:
            for item in reversed(st.session_state.history[-10:]):
                src = item.get("source_lang", "Auto")
                tgt = item.get("target_lang", "Unknown")
                text_short = item["original_text"][:55] + "..." if len(item["original_text"]) > 55 else item["original_text"]
                st.markdown(f"""
                    <div class="history-item">
                        <div class="time">{item['timestamp']}</div>
                        <div class="lang-pair"><strong>{src}</strong> <i class="fas fa-arrow-right" style="font-size: 0.6rem;"></i> <strong>{tgt}</strong></div>
                        <div>{text_short}</div>
                    </div>
                """, unsafe_allow_html=True)

        if st.session_state.history:
            if st.button("\U0001F5D1 Clear History", use_container_width=True):
                st.session_state.history = []
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


def render_main_content():
    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title"><i class="fas fa-pen-alt"></i> Enter Text</div>', unsafe_allow_html=True)
        text_input = st.text_area(
            "Enter text",
            value=st.session_state.get("input_text", ""),
            height=160,
            placeholder="Type or paste your text here...",
            label_visibility="collapsed",
            key="input_text",
        )
        char_count = len(text_input)
        st.markdown(f'<div class="char-counter"><i class="far fa-keyboard"></i> {char_count} / 5000 characters</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title"><i class="fas fa-sliders-h"></i> Language Settings</div>', unsafe_allow_html=True)
        src_col, mid_col, tgt_col = st.columns([5, 1, 5])
        with src_col:
            st.markdown('<div style="font-size:0.75rem;color:rgba(255,255,255,0.3);margin-bottom:0.3rem;font-weight:500;">SOURCE</div>', unsafe_allow_html=True)
            source_options = ["Auto Detect"] + LANGUAGE_NAMES
            source_lang = st.selectbox(
                "Source",
                options=source_options,
                index=0,
                label_visibility="collapsed",
                key="source_lang",
            )
        with mid_col:
            st.markdown('<div style="text-align:center;padding-top:1.8rem;color:rgba(255,255,255,0.2);">', unsafe_allow_html=True)
            st.markdown('<i class="fas fa-arrow-right fa-lg"></i>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with tgt_col:
            st.markdown('<div style="font-size:0.75rem;color:rgba(255,255,255,0.3);margin-bottom:0.3rem;font-weight:500;">TARGET</div>', unsafe_allow_html=True)
            target_lang = st.selectbox(
                "Target",
                options=LANGUAGE_NAMES,
                index=LANGUAGE_NAMES.index("English") if "English" in LANGUAGE_NAMES else 0,
                label_visibility="collapsed",
                key="target_lang",
            )
        st.markdown('</div>', unsafe_allow_html=True)

        translate_btn = st.button("\U0001F9D9 Translate Now", type="primary", use_container_width=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title"><i class="fas fa-exchange-alt"></i> Translation Result</div>', unsafe_allow_html=True)

        if "translated_text" not in st.session_state:
            st.session_state.translated_text = ""
        if "detected_lang" not in st.session_state:
            st.session_state.detected_lang = None

        if translate_btn:
            if not text_input.strip():
                st.error("Please enter some text to translate.")
            else:
                with st.spinner("Translating..."):
                    source_code = "auto" if source_lang == "Auto Detect" else get_language_code(source_lang)
                    target_code = get_language_code(target_lang)

                    if source_code != "auto":
                        result = translate_text(text_input, source_lang=source_code, target_lang=target_code)
                    else:
                        detection = detect_language(text_input)
                        if detection["success"]:
                            st.session_state.detected_lang = detection["language_name"]
                        result = translate_text(text_input, source_lang="auto", target_lang=target_code)

                    if result["success"]:
                        st.session_state.translated_text = result["translated_text"]
                        st.session_state.last_translation = {
                            "original_text": text_input,
                            "translated_text": result["translated_text"],
                            "source_lang": source_lang,
                            "target_lang": target_lang,
                            "timestamp": datetime.now().strftime("%H:%M"),
                        }
                    else:
                        st.error(result["error"])
                        st.session_state.translated_text = ""

        if st.session_state.detected_lang:
            st.markdown(f'<span class="detected-badge"><i class="fas fa-search"></i> Detected: {st.session_state.detected_lang}</span>', unsafe_allow_html=True)

        if st.session_state.translated_text:
            st.markdown(f'<div class="result-box">{st.session_state.translated_text}</div>', unsafe_allow_html=True)

            btn1, btn2, btn3 = st.columns(3)
            with btn1:
                if st.button("\U0001F4CB Copy", use_container_width=True):
                    try:
                        pyperclip.copy(st.session_state.translated_text)
                        st.toast("Copied to clipboard!", icon="✅")
                    except Exception:
                        st.warning("Clipboard unavailable", icon="⚠️")
            with btn2:
                if st.button("\U0001F50A Speak", use_container_width=True):
                    target_code = get_language_code(st.session_state.get("target_lang", "English"))
                    speech_result = text_to_speech(st.session_state.translated_text, lang=target_code)
                    if speech_result["success"]:
                        st.audio(speech_result["audio_bytes"], format="audio/mp3", autoplay=True)
                    else:
                        st.error(speech_result["error"])
            with btn3:
                target_lang_name = st.session_state.get("target_lang", "translated")
                file_name = f"translation_{target_lang_name.lower().replace(' ', '_')}.txt"
                st.download_button(
                    label="\U0001F4BE Save",
                    data=st.session_state.translated_text,
                    file_name=file_name,
                    mime="text/plain",
                    use_container_width=True,
                )
        else:
            st.markdown('<div class="result-box"><span class="placeholder-text"><i class="fas fa-arrow-left"></i> Enter text and click Translate to see results here</span></div>', unsafe_allow_html=True)

        if st.session_state.get("last_translation") and translate_btn:
            st.session_state.history.append(st.session_state.last_translation)

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
        <div class="footer">
            <i class="fas fa-code"></i> Built with <strong>Streamlit</strong> &bull; <strong>Google Translate API</strong> &bull; <strong>gTTS</strong><br>
            &copy; 2026 CodeAlpha Language Translation Tool &mdash; All Rights Reserved
        </div>
    """, unsafe_allow_html=True)


def main():
    apply_custom_css()
    render_header()
    render_sidebar()
    render_main_content()


if __name__ == "__main__":
    main()
