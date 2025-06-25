# YT-video summariser

A project to automatically summarize YouTube videos using transcript extraction, chunked summarization with Groq LLM, and a FastAPI backend. Includes a React frontend for user interaction.

## Features
- Extracts transcripts from YouTube videos
- Chunks transcripts and summarizes each part using Groq LLM
- Aggregates summaries for a final concise output
- REST API built with FastAPI
- React frontend for submitting video URLs and viewing summaries

## Project Structure
```
YT-video summariser/
├── summarizer.py           # Main Python summarization logic
├── transcript.ipynb        # Jupyter notebook for development and testing
├── api.py                  # FastAPI backend
├── groq_api_key.txt        # (gitignored) Groq API key
├── frontend/
│   └── video-summary-app/  # React frontend app
│       ├── src/
│       ├── public/
│       └── ...
└── .gitignore
```

## Setup

### 1. Backend (Python)
- Python 3.8+
- Install dependencies:
  ```sh
  pip install -r requirements.txt
  # or manually:
  pip install fastapi uvicorn youtube-transcript-api groq
  ```
- Add your Groq API key to `groq_api_key.txt` (do not commit this file)
- Run the API:
  ```sh
  uvicorn api:app --reload
  ```

### 2. Frontend (React)
- Go to `frontend/video-summary-app`
- Install dependencies:
  ```sh
  npm install
  ```
- Start the development server:
  ```sh
  npm start
  ```

## Usage
- Open the React frontend in your browser (usually at http://localhost:3000)
- Enter a YouTube video URL and submit
- The backend will process the video and return a summary

## Notes
- The API key is stored in `groq_api_key.txt` and is gitignored for security.
- Summarization uses chunked processing for long transcripts.
- You can use the notebook for experimentation and development.

## License
MIT
