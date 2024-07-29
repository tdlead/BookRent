from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter

def main(video_id):
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    transcript = transcript_list.find_manually_created_transcript(['de'])
    transcript= transcript.fetch()
    formatter = JSONFormatter()

# .format_transcript(transcript) turns the transcript into a JSON string.
    json_formatted = formatter.format_transcript(transcript)


# Now we can write it out to a file.
    with open('1.json', 'w', encoding='utf-8') as json_file:
        json_file.write(json_formatted)
    
                                                
# Example usage
if __name__ == "__main__":
        video_id = 'JDjZTYQX2xY'
        main(video_id)
