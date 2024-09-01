from django import forms
from social.models import User as OurUser


class ChangeAliasForm(forms.ModelForm):
    class Meta:
        model = OurUser
        fields = ['alias']
        widgets = {
            'alias': forms.TextInput(attrs={'placeholder': 'Enter your new alias'}),
        }

    def clean_alias(self):
        alias = self.cleaned_data.get('alias')
        if len(alias) < 3:
            raise forms.ValidationError("Alias must be at least 3 characters long.")
        return alias

class ChangeAvatarForm(forms.ModelForm):
    class Meta:
        model = OurUser
        fields = ['avatar']
