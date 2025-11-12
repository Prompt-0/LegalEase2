from django.db import models

class PoliceStation(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    pincode = models.CharField(max_length=10, blank=True)
    district = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=100, blank=True)
    # We can add latitude/longitude fields here later for maps

    def __str__(self):
        return self.name

class LegalCase(models.Model):
    title = models.CharField(max_length=500)
    summary = models.TextField()
    category = models.CharField(max_length=100, blank=True)
    # We can add full_text, related_acts, etc. later

    def __str__(self):
        return self.title

# ... (at the end of the file, after the LegalCase class) ...

class Helpline(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    phone_number = models.CharField(max_length=100)
    category = models.CharField(max_length=100, blank=True) # e.g., "Emergency", "Women", "Child"

    def __str__(self):
        return f"{self.name} ({self.phone_number})"
