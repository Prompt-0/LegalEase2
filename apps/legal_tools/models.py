from django.db import models

class LegalAct(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    category = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

class Chapter(models.Model):
    act = models.ForeignKey(LegalAct, related_name='chapters', on_delete=models.CASCADE)
    chapter_number = models.CharField(max_length=50)
    title = models.CharField(max_length=500)

    class Meta:
        ordering = ['id'] # Ensure chapters are ordered by creation

    def __str__(self):
        return f"{self.act.name} - Ch. {self.chapter_number}: {self.title}"

class Section(models.Model):
    chapter = models.ForeignKey(Chapter, related_name='sections', on_delete=models.CASCADE)
    section_number = models.CharField(max_length=50)
    title = models.CharField(max_length=500)
    content = models.TextField()

    class Meta:
        ordering = ['id'] # Ensure sections are ordered by creation

    def __str__(self):
        return f"Sec. {self.section_number}: {self.title}"
