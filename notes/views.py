from rest_framework import generics, filters
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from authentication.permissions import IsUploaderOrAdmin
from .models import Domain, Branch, Year, Subject, Note
from .serializers import DomainSerializer, BranchSerializer, YearSerializer, SubjectSerializer, NoteSerializer

# Upload Note
class UploadNoteView(generics.CreateAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)


# List Notes (read-only) with filtering & search
class ListNotesView(generics.ListAPIView):
    queryset = Note.objects.all().order_by('-upload_date')
    serializer_class = NoteSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['subject', 'subject__year', 'subject__year__branch', 'subject__year__branch__domain']
    search_fields = ['title', 'description']


# Domain Views
class DomainListView(generics.ListCreateAPIView):
    queryset = Domain.objects.all()
    serializer_class = DomainSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [AllowAny()]


# Branch Views
class BranchListView(generics.ListCreateAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [AllowAny()]


# Year Views
class YearListView(generics.ListCreateAPIView):
    queryset = Year.objects.all()
    serializer_class = YearSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [AllowAny()]


# Subject Views
class SubjectListView(generics.ListCreateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [AllowAny()]
