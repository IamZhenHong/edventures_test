from django.db import models


class Document(models.Model):
    file_name = models.CharField(max_length=255)  # Original name of the file
    file_type = models.CharField(max_length=10)  # e.g., 'pdf' or 'csv'
    file = models.FileField(upload_to='documents/')  # Store the uploaded file
    title = models.CharField(max_length=255)  # Title or summary of the document
    embeddings = models.JSONField(blank=True, null=True) 

    def __str__(self):
        return f"{self.title} ({self.file_type})"

    class Meta:
        verbose_name = "Document"
        verbose_name_plural = "Documents"