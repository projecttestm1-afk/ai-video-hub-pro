# 🎬 AI Video Hub Pro

End-to-end AI pipeline for YouTube video translation, dubbing, and analytics.
This project automates the full workflow of video localization — from download to voice-over — and includes an optional data tracking pipeline (ETL) for monitoring usage and performance.

## 🚀 Why this project matters
Most tools only handle one part of video localization. This solution provides a complete system:
- Content ingestion
- AI processing
- Voice synthesis
- Analytics tracking

👉 **Suitable for:** Content creators, Automation workflows, Data-driven video production.

---

## ⚙️ Core Features

**🎥 Video Processing**
- Download videos via `yt-dlp`
- Extract and prepare audio automatically

**🧠 Speech Recognition (ASR)**
- High-accuracy transcription using `OpenAI Whisper`

**🌍 Translation**
- Multi-language support via `deep-translator`

**🔊 Voice Synthesis**
- Natural voice-over using `edge-tts`
- Timing preserved for realistic dubbing

**💻 Web Interface**
- Simple UI built with `Streamlit`

**📊 Built-in Analytics (Key Feature)**
- Tracks usage data: Video URL, Selected voice, Processing status, Timestamp.
- Sends data to Google Sheets via API (ETL pipeline).
- *👉 This demonstrates real-world data engineering + automation skills.*

---

## 🏗 System Architecture
```text
User Input (Streamlit UI)
        ↓
yt-dlp → Audio Extraction
        ↓
Whisper (ASR)
        ↓
Translation
        ↓
Edge-TTS (Voice)
        ↓
Output Video
        ↓
📊 Analytics → Google Sheets (ETL)
🧩 Tech Stack
Python

Streamlit

OpenAI Whisper

Edge-TTS

yt-dlp

deep-translator

Pandas

Requests

Google Apps Script (ETL API)

⚡ Quick Start
1) Requirements
Install FFmpeg:

Linux: sudo apt install ffmpeg

macOS: brew install ffmpeg

Windows: Download from the official site and add to PATH.

2) Setup
Bash
git clone [https://github.com/projecttestm1-afk/ai-video-hub-pro.git](https://github.com/projecttestm1-afk/ai-video-hub-pro.git)
cd ai-video-hub-pro

python -m venv venv

# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate

pip install -r requirements.txt
3) Run
Bash
streamlit run app.py
📊 Analytics Setup (Google Sheets ETL)
This is the strongest part of your portfolio — do not skip it.

1) Create Google Sheet
Columns example:
Date | Video URL | Voice | Status

2) Add Apps Script
Go to: Extensions → Apps Script. Paste the following code:

JavaScript
function doPost(e) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  
  const data = JSON.parse(e.postData.contents);
  
  sheet.appendRow([
    new Date(), 
    data.video_url, 
    data.voice, 
    data.status
  ]);
  
  return ContentService
    .createTextOutput("Success")
    .setMimeType(ContentService.MimeType.TEXT);
}
3) Deploy
Deploy → New deployment

Type: Web app

Access: Anyone

Copy the Web App URL.

4) Connect in project
Create a .env file in the root directory:

Code snippet
GOOGLE_SHEET_URL=your_web_app_url
📈 What this project demonstrates
End-to-end automation pipeline

API integration

ETL pipeline design

Data collection & tracking

Real-world analytics workflow

👉 This is not just a script — it's a data product.

🔮 Possible Improvements
[ ] Dashboard in Looker Studio / Power BI

[ ] Cost tracking per video

[ ] Multi-language batch processing

[ ] Queue system (Celery / Redis)

[ ] Cloud deployment

👤 Author
Developed as a portfolio project focused on: Automation, Data analytics, and Practical ETL systems.

⭐ If you find this useful — consider starring the repo!


## 🎬 Demo

https://github.com/user-attachments/assets/771774e9-a540-45aa-be23-012c3afae5f7








