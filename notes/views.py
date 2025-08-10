from django.shortcuts import render
from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from authentication.permissions import IsUploaderOrAdmin
from .models import Domain, Branch, Year, Subject,Note
from .serializers import DomainSerializer, BranchSerializer, YearSerializer, SubjectSerializer, NoteSerializer

# Create your views here.

# --Upload Note --
class UploadNoteView(generics.CreateAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsUploaderOrAdmin]
    
# --Browse Note --
class ListNotesView(generics.ListCreateAPIView):
    queryset = Note.objects.all().order_by('-upload_date')
    serializer_class = NoteSerializer
    
# --- Domain Views ---
class DomainListView(generics.ListCreateAPIView):
    queryset = Domain.objects.all()
    serializer_class = DomainSerializer
    
# --- Branch Views ---
class BranchListView(generics.ListCreateAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    
# --- Year Views ---
class YearListView(generics.ListCreateAPIView):
    queryset = Year.objects.all()
    serializer_class = YearSerializer
    
# --- Subject Views ---  
class SubjectListView(generics.ListCreateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    