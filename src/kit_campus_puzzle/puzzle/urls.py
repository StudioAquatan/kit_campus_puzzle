from django.urls.conf import path
from .views import (
    PuzzleView,
    PuzzleListView,
    PuzzleEditView
)

app_name = 'puzzle'
urlpatterns = [
    path('<int:puzzle_id>/', PuzzleView.as_view(), name='detail'),
    path('list/', PuzzleListView.as_view(), name='list'),
    path('edit/<int:puzzle_id>/', PuzzleEditView.as_view(), name='edit'),
]
