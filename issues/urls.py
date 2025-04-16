from django.urls import path
from .views import IssueListView
from . import views 

urlpatterns = [
    path('', IssueListView.as_view(), name='issue-list'),
    path('issues/<int:issue_id>/', views.issue_view, name='issue_detail')
]