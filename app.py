import streamlit as st
import whisper
import os
import tempfile
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from docx import Document
from streamlit_mic_recorder import mic_recorder

# Set Page Config
st.set_page_config(page_title="AI Summarizer", layout="wide")

# Theme Settings
light_theme = {"bg": "#ffffff", "text": "#333333", "accent": "#FDCB58", "button": "#FFD700"}
dark_theme = {"bg": "#121212", "text": "#f1f1f1", "accent": "#FDCB58", "button": "#FFA500"}

# Theme Toggle
if "theme" not in st.session_state:
    st.session_state.theme = "light"

def toggle_theme():
    st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"

theme = light_theme if st.session_state.theme == "light" else dark_theme

# Apply Theme Styles
st.markdown(f"""
    <style>
        body {{
            background-color: {theme['bg']};
            color: {theme['text']};
            transition: 0.5s ease-in-out;
        }}
        .stButton>button {{
            background-color: {theme['button']} !important;
            color: black !important;
            border-radius: 10px;
            font-weight: bold;
            transition: 0.3s;
        }}
        .stButton>button:hover {{
            background-color: #ffcc00 !important;
        }}
        .summary-box {{
            padding: 10px;
            border-radius: 10px;
            background: {theme['accent']};
            color: black;
            font-weight: bold;
        }}
        .footer {{
            position: fixed;
            bottom: 10px;
            right: 20px;
            font-size: 12px;
            color: {theme['text']};
        }}
    </style>
""", unsafe_allow_html=True)

# Sidebar Theme Toggle
st.sidebar.toggle("🌙 Dark Mode", key="dark_mode", on_change=toggle_theme)

# Page Header
st.title("AI Summarizer")
st.write("This AI-powered summarization tool allows you to quickly generate concise summaries from text, documents, and speech. Upload a document, paste text, or record your voice, and get an accurate summary in seconds.")

# Load Whisper Model
whisper_model = whisper.load_model("base")

# Summarization Function
def summarize_text(text, length):
    if not text.strip():
        return "No valid text to summarize."
    
    try:
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = LsaSummarizer()
        num_sentences = {"Short": 2, "Medium": 4, "Long": 6}[length]
        summary = summarizer(parser.document, num_sentences)
        return " ".join([str(sentence) for sentence in summary])
    except Exception as e:
        return f"Error in summarization: {str(e)}"

# Tabs
tab1, tab2, tab3 = st.tabs(["📂 File Summarizer", "📝 Text Summarizer", "🎤 Speech-to-Text"])

# === FILE SUMMARIZER ===
with tab1:
    st.subheader("📂 Upload Word Document for Summarization")
    uploaded_file = st.file_uploader("Upload a .docx file", type=["docx"])
    summary_length = st.select_slider("Summary Length", options=["Short", "Medium", "Long"], key="file_summary")

    def extract_text_from_docx(docx_file):
        try:
            doc = Document(docx_file)
            return "\n".join([para.text for para in doc.paragraphs if para.text])
        except:
            return None

    if uploaded_file:
        st.write(f"📄 File Name: `{uploaded_file.name}` | 📏 Size: `{uploaded_file.size // 1024} KB`")
        extracted_text = extract_text_from_docx(uploaded_file)
        if extracted_text:
            st.text_area("Extracted Text", extracted_text, height=150)
            if st.button("⚡ Summarize"):
                summarized_text = summarize_text(extracted_text, summary_length)
                st.success("Summary:")
                st.markdown(f"<div class='summary-box'>{summarized_text}</div>", unsafe_allow_html=True)
                st.download_button("📥 Download Summary", summarized_text, file_name="summary.txt")
        else:
            st.error("Error reading document.")

# === TEXT SUMMARIZER ===
with tab2:
    st.subheader("📝 Enter Text for Summarization")
    input_text = st.text_area("Paste your text here", key="text_input", height=150)
    summary_length_text = st.select_slider("Summary Length", options=["Short", "Medium", "Long"], key="text_summary")

    # Word Count Display
    word_count = len(input_text.split())
    st.write(f"📝 Word Count: `{word_count}`")

    if st.button("⚡ Summarize Text"):
        if input_text:
            summarized_text = summarize_text(input_text, summary_length_text)
            st.success("Summary:")
            st.markdown(f"<div class='summary-box'>{summarized_text}</div>", unsafe_allow_html=True)
            st.download_button("📥 Download Summary", summarized_text, file_name="summary.txt")
        else:
            st.error("Please enter text to summarize.")

# === SPEECH-TO-TEXT SUMMARIZATION ===
with tab3:
    st.subheader("🎤 Record or Upload Audio for Transcription & Summarization")

    # Record Audio from Browser
    recorded_audio = mic_recorder(start_prompt="🎙 Start Recording", stop_prompt="🛑 Stop Recording")

    # Upload MP3/WAV File
    uploaded_audio = st.file_uploader("Upload audio file (MP3, WAV)", type=["mp3", "wav"])
    summary_length_audio = st.select_slider("Summary Length", options=["Short", "Medium", "Long"], key="audio_summary")

    audio_file_path = None

    if recorded_audio:
        audio_bytes = recorded_audio["bytes"]
        temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        temp_audio.write(audio_bytes)
        temp_audio.close()
        audio_file_path = temp_audio.name

    elif uploaded_audio:
        st.write(f"🎵 File Name: `{uploaded_audio.name}` | 📏 Size: `{uploaded_audio.size // 1024} KB`")
        temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        temp_audio.write(uploaded_audio.getbuffer())
        temp_audio.close()
        audio_file_path = temp_audio.name

    if audio_file_path:
        st.audio(audio_file_path)

        # Transcription
        try:
            with st.spinner("🔄 Transcribing audio..."):
                result = whisper_model.transcribe(audio_file_path)
                transcribed_text = result["text"]
            
            if transcribed_text:
                st.success("🎤 Transcribed Text:")
                st.text_area("Transcription", transcribed_text, height=120)

                # Summarization
                summarized_text = summarize_text(transcribed_text, summary_length_audio)
                st.success("📝 Summarized Text:")
                st.markdown(f"<div class='summary-box'>{summarized_text}</div>", unsafe_allow_html=True)
                st.download_button("📥 Download Summary", summarized_text, file_name="speech_summary.txt")
        except Exception as e:
            st.error(f"Error in transcription: {str(e)}")

    # Cleanup Temporary Files
    if audio_file_path and os.path.exists(audio_file_path):
        os.remove(audio_file_path)

# Footer
st.markdown("<div class='footer'>Created by Haaris</div>", unsafe_allow_html=True)
