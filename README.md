# 🎬 AI Video Dubber Pro

Інструмент для автоматичного дубляжу відео з вбудованою аналітикою.

## 🚀 Як запустити (на будь-якій системі)
1. **Клонувати проєкт:**
   `git clone https://github.com/projecttestm1-afk/ai-video-hub-pro.git`

2. **Створити віртуальне середовище:**
   `python -m venv venv`

3. **Активувати:**
   - Linux/macOS: `source venv/bin/activate`
   - Windows: `venv\Scripts\activate`

4. **Встановити залежності:**
   `pip install -r requirements.txt`

5. **Налаштувати секрети:**
   Створіть файл `.env` і додайте свій `GOOGLE_SHEET_URL`.

6. **Запуск:**
   `streamlit run app.py`

## 📊 Аналітика
Дані про кожен запит автоматично відправляються в Google Sheets через Apps Script API.
