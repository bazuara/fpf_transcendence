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
                'accept'        : 'image/*',            # Restrict file types
                'title'         : 'Error:',             # Tooltip text
                'class'         : 'form-control',       # Custom CSS class
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