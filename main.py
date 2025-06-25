# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from summarizer import summarize_youtube_video
# main.py
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:3000"] for stricter
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class VideoRequest(BaseModel):
    url: str

@app.post("/summarize")
def summarize_endpoint(request: VideoRequest):
    try:
        print("Request received for:",request.url)
        summary = summarize_youtube_video(request.url)
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
