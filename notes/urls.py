from django.urls import path
from .views import (
    UploadNoteView, ListNotesView, DomainListView,
    BranchListView, YearListView, SubjectListView
)

urlpatterns = [
    path('upload/', UploadNoteView.as_view(), name='upload_note'),
    path('notes/', ListNotesView.as_view(), name='list_notes'),
    path('domains/', DomainListView.as_view(), name='list_domains'),
    path('branches/', BranchListView.as_view(), name='list_branches'),
    path('years/', YearListView.as_view(), name='list_years'),
    path('subjects/', SubjectListView.as_view(), name='list_subjects'),
]
