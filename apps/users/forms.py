from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile

class UserRegisterForm(UserCreationForm):
    """
    Custom registration form to add email and user_type.
    """
    email = forms.EmailField(required=True, help_text="Required. A valid email address.")
    user_type = forms.ChoiceField(choices=Profile.USER_TYPE_CHOICES)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            user.profile.user_type = self.cleaned_data['user_type']
            user.profile.save()
        return user


class UserLoginForm(AuthenticationForm):
    """
    A simple custom login form to ensure consistent styling.
    """
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


class UserProfileForm(forms.ModelForm):
    """
    A form for users to update their profile information.
    """
    class Meta:
        model = Profile
        # --- NEW: Added lawyer fields ---
        fields = (
            'user_type',
            'specialization',
            'location',
            'experience_years',
            'phone_number'
        )
        widgets = {
            'specialization': forms.TextInput(attrs={'placeholder': 'e.g., Criminal Law'}),
            'location': forms.TextInput(attrs={'placeholder': 'e.g., Delhi High Court'}),
            'experience_years': forms.NumberInput(attrs={'placeholder': 'e.g., 5'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'e.g., +91...'}),
        }
