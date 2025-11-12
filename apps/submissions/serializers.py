from rest_framework import serializers
from .models import OnlineFIR, AnonymousReport, ContactMessage

class OnlineFIRSerializer(serializers.ModelSerializer):
    # User is set automatically from the view, so it's read-only here
    user = serializers.StringRelatedField(read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = OnlineFIR
        # We exclude 'user' and 'status' from the writable fields
        # They will be set by the server.
        exclude = ('user', 'status')

class AnonymousReportSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = AnonymousReport
        exclude = ('user', 'status')

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = '__all__'
        read_only_fields = ('created_at',)
