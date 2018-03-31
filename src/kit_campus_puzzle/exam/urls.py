from django.urls.conf import path
from .views import (
    RankingView,
    ExamView,
    ExamListView,
    ResultView,
    HistoryView
)

app_name = 'exam'
urlpatterns = [
    path('ranking/', RankingView.as_view(), name='ranking'),
    path('list/', ExamListView.as_view(), name='list'),
    path('take/<int:puzzle_id>/', ExamView.as_view(), name='take'),
    path('result/<int:pk>/', ResultView.as_view(), name='result'),
    path('history/', HistoryView.as_view(), name='history')
]
