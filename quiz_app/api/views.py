from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import time

from quiz_app.api.serializers import QuizCreationSerializer

from quiz_app.api.services import (
    validate_youtube_url,
    download_audio_from_youtube,
    transcribe_audio,
    create_quiz_from_transcript,
    cleanup_temp_files
    )

class CreateQuizView(APIView):
    def post(self, request):
        audio_path = "temp_audio/" + str(int(time.time()))
        
        youtube_url = validate_youtube_url(request.data.get('url'))
        download_audio_from_youtube(youtube_url, audio_path)
        transcript = transcribe_audio(audio_path)
        quiz_data = create_quiz_from_transcript(transcript)
        cleanup_temp_files(audio_path + ".mp3")
        

        data = {
            "title": quiz_data['title'],
            "description": quiz_data['description'],
            "video_url": youtube_url,
            "questions": quiz_data['questions']
        }

        serializer = QuizCreationSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)