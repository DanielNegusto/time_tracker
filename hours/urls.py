from django.urls import path
from .views import (
    ProjectListCreateView,
    ProjectDetailView,
    ReportView,
    AddSpentTimeView,
)

urlpatterns = [
    path("projects/", ProjectListCreateView.as_view(), name="project-list-create"),
    path("projects/<int:pk>/", ProjectDetailView.as_view(), name="project-detail"),
    path("add_time/", AddSpentTimeView.as_view(), name="add_spent_time"),
    path("report/<int:project_id>/", ReportView.as_view(), name="report"),
]
