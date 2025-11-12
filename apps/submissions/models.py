from django.db import models
from django.contrib.auth.models import User

class SubmissionBase(models.Model):
    """
    An abstract base class for common fields.
    """
    STATUS_CHOICES = (
        ('SUBMITTED', 'Submitted'),
        ('IN_REVIEW', 'In Review'),
        ('CLOSED', 'Closed'),
    )

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='SUBMITTED')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']

class OnlineFIR(SubmissionBase):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    complainant_name = models.CharField(max_length=255)
    father_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50)
    address = models.TextField()
    district = models.CharField(max_length=100)
    subject = models.CharField(max_length=500)
    details = models.TextField()

    def __str__(self):
        return f"FIR by {self.complainant_name} ({self.subject})"

class AnonymousReport(SubmissionBase):
    # This can be null if the user is not logged in
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    incident_type = models.CharField(max_length=255)
    location = models.CharField(max_length=500)
    description = models.TextField()
    evidence_link = models.URLField(blank=True)

    def __str__(self):
        return f"Report ({self.incident_type}) at {self.location}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=500)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.name} ({self.subject})"
