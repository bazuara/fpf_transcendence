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


class AddFriendForm(forms.ModelForm):
    user_id = forms.IntegerField(widget=forms.HiddenInput())
    action = forms.ChoiceField(choices=[('add', 'Add'), ('delete', 'Delete')], widget=forms.HiddenInput())

    class Meta:
        model = OurUser
        fields = ['name', 'friends']
