from youtube_transcript_api import YouTubeTranscriptApi
import time

def get_transcript(video_id):
    for attempt in range(3):
        try:
            ytt_api = YouTubeTranscriptApi()  # ✅ must instantiate in v1.x

            try:
                # Try English first directly
                fetched = ytt_api.fetch(video_id, languages=['en'])
            except Exception:
                # Fall back: list available, pick first, translate to English
                transcript_list = ytt_api.list(video_id)  # ✅ .list() not .list_transcripts()
                available = list(transcript_list)
                fetched = available[0].translate('en').fetch()

            # ✅ v1.x returns FetchedTranscript object with .text attribute per snippet
            text = " ".join([snippet.text for snippet in fetched])
            return text

        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < 2:
                time.sleep(3)
                continue
            raise RuntimeError(f"Could not fetch transcript: {str(e)}")