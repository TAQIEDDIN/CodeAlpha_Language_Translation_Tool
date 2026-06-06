# 🌍 AI Language Translation Tool

An AI-powered language translation tool built with Python and Streamlit. Translate text between 100+ languages with features like auto-detection, text-to-speech, and translation history.

## ✨ Features

- **Text Translation** – Translate text between 100+ languages using Google Translate API
- **Auto Language Detection** – Automatically detect the source language
- **Text-to-Speech** – Listen to translated text with gTTS
- **Copy to Clipboard** – One-click copy of translated text
- **Download as TXT** – Save translations as text files
- **Translation History** – View recent translations in the sidebar
- **Character Counter** – Track input length in real-time
- **Dark Mode UI** – Modern, eye-friendly interface
- **Responsive Design** – Works on desktop and mobile

## 🛠️ Technologies Used

| Technology | Purpose |
|-----------|---------|
| Python 3.11+ | Core programming language |
| Streamlit | Web application framework |
| Deep Translator | Google Translate API wrapper |
| gTTS | Text-to-speech synthesis |
| Pyperclip | Clipboard operations |
| Langdetect | Language detection |

## 📥 Installation

### Prerequisites

- Python 3.11 or higher
- pip package manager

### Steps

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/CodeAlpha_Language_Translation_Tool.git
cd CodeAlpha_Language_Translation_Tool
```

2. **Create a virtual environment (recommended)**

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Run the application**

```bash
streamlit run app.py
```

5. Open your browser at `http://localhost:8501`

## 🚀 Usage

1. Enter or paste text in the input area
2. Select source language (or choose "Auto Detect")
3. Select target language
4. Click **Translate**
5. View the translated result
6. Use **Copy**, **Speak**, or **Download** buttons as needed

## 📸 Screenshots

> Add screenshots to the `screenshots/` folder and link them here.

| Main Interface | Translation Result |
|---------------|-------------------|
| *(screenshot here)* | *(screenshot here)* |

## 🗂️ Project Structure

```
CodeAlpha_Language_Translation_Tool/
├── app.py                 # Main application
├── requirements.txt       # Dependencies
├── README.md              # Documentation
├── assets/
│   └── logo.png           # Brand assets
├── utils/
│   ├── translator.py      # Translation logic
│   ├── language_detector.py  # Language detection
│   └── speech.py           # Text-to-speech
└── screenshots/           # Screenshots
```

## 🧪 Future Improvements

- Add support for document translation (PDF, DOCX)
- Implement offline translation models
- Add user authentication
- Support batch translation
- Add more TTS voice options
- Export translations as PDF

## 👤 Author

**Taqi Eddine El Mamouni**


## 📄 License

This project is licensed under the MIT License.
