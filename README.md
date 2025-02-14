# **AI Summarizer**  

AI Summarizer is a web application that generates concise summaries from text, `.docx` files, and speech. It utilizes **Whisper AI** for speech-to-text transcription and **Sumy** for text summarization, providing an intuitive UI with **Streamlit**. Users can upload documents, paste text, or record audio and download summaries easily.  

## **Features**  
✅ Summarize text and `.docx` files  
✅ Convert speech to text using Whisper AI  
✅ Choose summary length: Short, Medium, or Long  
✅ Light/Dark mode toggle  
✅ Download summarized text  

## **Technology Stack**  
- **Frontend:** Streamlit  
- **Backend:** Whisper AI, Sumy  
- **File Handling:** Python-docx  
- **Audio Processing:** Streamlit-mic-recorder  

## **Installation**  
### **1. Clone the Repository**  
```sh
git clone https://github.com/your-username/ai-summarizer.git
cd ai-summarizer
```
### **2. Create a Virtual Environment (Optional but Recommended)**  
```sh
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```
### **3. Install Dependencies**  
```sh
pip install -r requirements.txt
```
### **4. Run the Application**  
```sh
streamlit run app.py
```

## **Requirements** (`requirements.txt`)  
```
streamlit
streamlit-mic-recorder
openai-whisper
torch
numpy
tqdm
ffmpeg-python
pydub  
sumy
scipy
python-docx
transformers
```

## **Usage**  
1. Open the app using the command above.  
2. Upload a `.docx` file, paste text, or record/upload audio.  
3. Choose summary length and generate the summary.  
4. Download the summary if needed.  
