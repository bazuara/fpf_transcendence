from django import forms
from social.models import User as OurUser


class ChangeAliasForm(forms.ModelForm):
    class Meta:
        model = OurUser
        fields = ['alias']
        widgets = {
            'alias': forms.TextInput(attrs={
                'style': 'color: #28df28; background-color: #181A1B; border-color: #181A1B;  font-family: "Bebas Neue", sans-serif',
                'class': 'form-control',
            }),
        }

class ChangeAvatarForm(forms.ModelForm):
    class Meta:
        model = OurUser
        fields = ['avatar']
        widgets = {
            'avatar': forms.FileInput(attrs={
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


class ManageFriendsForm(forms.ModelForm):
    user_id = forms.IntegerField(widget=forms.HiddenInput())
    action = forms.ChoiceField(choices=[('add', 'Add'), ('delete', 'Delete')], widget=forms.HiddenInput())

    class Meta:
        model = OurUser
        fields = ['name', 'friends']
