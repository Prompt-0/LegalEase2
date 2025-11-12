from rest_framework import serializers
from .models import LegalAct, Chapter, Section

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ('section_number', 'title', 'content')

class ChapterSerializer(serializers.ModelSerializer):
    # This will nest all sections inside each chapter
    sections = SectionSerializer(many=True, read_only=True)

    class Meta:
        model = Chapter
        fields = ('chapter_number', 'title', 'sections')

class LegalActSerializer(serializers.ModelSerializer):
    # This will nest all chapters inside each act
    chapters = ChapterSerializer(many=True, read_only=True)

    class Meta:
        model = LegalAct
        fields = ('id', 'name', 'description', 'category', 'chapters')
