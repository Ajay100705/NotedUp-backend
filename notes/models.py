from django.db import models
from authentication.models import User

class Domain(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Branch(models.Model):
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, related_name='branches')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.domain.name} - {self.name}"


class Year(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='years')
    year_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.branch.name} - {self.year_name}"


class Subject(models.Model):
    year = models.ForeignKey(Year, on_delete=models.CASCADE, related_name='subjects')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.year.year_name} - {self.name}"


class Note(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='notes/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
