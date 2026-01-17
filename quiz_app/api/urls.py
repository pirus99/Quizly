from django.urls import path
from quiz_app.api.views import CreateQuizView, ListQuizzesView, SingleQuizView

urlpatterns = [
    path("createQuiz/", CreateQuizView.as_view(), name="create-quiz"),
    path("quizzes/", ListQuizzesView.as_view(), name="list-quizzes"),
    path("quizzes/<int:quiz_id>/", SingleQuizView.as_view(), name="single-quiz"),
]