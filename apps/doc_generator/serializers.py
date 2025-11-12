from rest_framework import serializers
from .models import DocumentTemplate

class DocumentTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentTemplate
        fields = ('id', 'name', 'description', 'js_file_path', 'icon_class')
