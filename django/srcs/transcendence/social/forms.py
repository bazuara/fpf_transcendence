from django import forms
from social.models import User as OurUser


class ChangeAliasForm(forms.ModelForm):
    class Meta:
        model = OurUser
        fields = ['alias']

class ChangeAvatarForm(forms.ModelForm):
    class Meta:
        model = OurUser
        fields = ['avatar']
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={
                'class': 'custom-file-input',   # Custom CSS class
                'accept': 'image/*',           # Restrict file types
                'title': 'Error:',  # Tooltip text
            }),
        }
        labels = {
            'avatar': 'Profile Picture',  # Field label
        }
        help_texts = {
            'avatar': 'Upload a new profile picture (optional).',  # Help text under the field
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Additional customization after initialization
        self.fields['avatar'].widget.attrs.update({
            'accept': 'image/*',  # Restrict file types to images
            'class': 'form-control',  # Add additional CSS classes if needed
        })
        # Example: Set a custom placeholder for a text field if there were any
        self.fields['avatar'].widget.attrs.update({
            'placeholder': 'Enter asdasdasdtext here',
        })
