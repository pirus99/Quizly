from rest_framework.serializers import ModelSerializer

from quiz_app.models import Quiz, Question


class QuestionSerializer(ModelSerializer):
    class Meta:
        model = Question
        fields = ['question_title', 'question_options', 'answer']

class QuizCreationSerializer(ModelSerializer):
    """
    Serializer for creating and updating quizzes with nested questions.
    
    Handles the creation of Quiz objects along with their associated Question
    objects in a single transaction.
    """
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'created_at', 'updated_at', 'video_url', 'questions']

    def create(self, validated_data):
        """
        Create a quiz with nested questions.
        
        Extracts question data, creates the quiz, then creates all associated
        questions linked to the quiz.
        """
        questions_data = validated_data.pop('questions', [])
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        quiz = Quiz.objects.create(user=user, **validated_data)

        for q in questions_data:
            Question.objects.create(quiz=quiz, **q)

        return quiz
    
class QuizListSerializer(ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'created_at', 'updated_at', 'video_url', 'questions']