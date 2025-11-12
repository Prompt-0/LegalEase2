from rest_framework import serializers
from .models import PoliceStation, LegalCase, Helpline
from apps.users.models import Profile
from django.contrib.auth.models import User

class LawyerUserSerializer(serializers.ModelSerializer):
    """ A serializer for basic user info (name) """
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class LawyerProfileSerializer(serializers.ModelSerializer):
    """
    A serializer for the public-facing Lawyer Profile.
    It includes nested user info.
    """
    # This nests the UserSerializer inside this one
    user = LawyerUserSerializer(read_only=True)

    class Meta:
        model = Profile
        # These are the fields that will be public in the API
        fields = (
            'id',
            'user',
            'specialization',
            'location',
            'experience_years',
            'phone_number'
        )

class PoliceStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PoliceStation
        fields = '__all__'

class LegalCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegalCase
        fields = '__all__'

# ... (at the end of the file, after LegalCaseSerializer) ...

class HelplineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Helpline
        fields = '__all__'
