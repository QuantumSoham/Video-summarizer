# summarizer.py
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi
from groq import Groq

def extract_video_id(url):
    parsed_url = urlparse(url)
    if 'youtu.be' in parsed_url.netloc:
        return parsed_url.path[1:]
    if 'youtube.com' in parsed_url.netloc:
        if parsed_url.path == '/watch':
            return parse_qs(parsed_url.query).get('v', [None])[0]
        elif parsed_url.path.startswith('/embed/'):
            return parsed_url.path.split('/embed/')[1]
    return None

def get_transcript(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
    return " ".join([entry['text'] for entry in transcript])

def chunk_text(text, max_tokens=2000, overlap=200):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + max_tokens, len(words))
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += max_tokens - overlap
    return chunks

def summarize_chunk_groq(chunk, client, past_chunk_summary):
    prompt = f'''You are a Transcript summarizer bot. 
Here is what was summarized from previous segment: {past_chunk_summary}
Summarize the following YouTube transcript segment:\n\n{chunk}
Only use the given chunk. Don't add extra information.
'''
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=512,
        top_p=1,
        stream=True,
    )
    summary = ""
    for part in completion:
        summary += getattr(part.choices[0].delta, "content", "") or ""
    return summary

def summarize_youtube_video(url):
    video_id = extract_video_id(url)
    if not video_id:
        raise ValueError("Invalid YouTube URL")
    
    transcript = get_transcript(video_id)
    chunks = chunk_text(transcript)

    client = Groq(api_key="YOUR_GROQ_API_KEY")
    all_summaries = []
    past_chunk_summary = "No previous chunk yet."

    for chunk in chunks:
        summary = summarize_chunk_groq(chunk, client, past_chunk_summary)
        all_summaries.append(summary)
        past_chunk_summary = summary

    final_input = "\n".join(all_summaries)
    final_summary = summarize_chunk_groq(
        final_input,
        client,
        "This is the final summary. No more chunks. No need to say 'summary' explicitly."
    )
    return final_summary
