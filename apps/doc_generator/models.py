from django.db import models

class DocumentTemplate(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    # This stores the path to the specific JS file that powers this template
    js_file_path = models.CharField(max_length=255, help_text="e.g., js/doc_templates/legal_notice.js")
    icon_class = models.CharField(max_length=100, blank=True, default="fas fa-file-alt")

    def __str__(self):
        return self.name
