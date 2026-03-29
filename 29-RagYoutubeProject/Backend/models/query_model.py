from pydantic import BaseModel

class Query(BaseModel):
    question: str
    video_id: str     # ← user sends the YouTube video ID with each request