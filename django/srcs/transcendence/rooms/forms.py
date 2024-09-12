from django import forms
from .models import Room

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['game_mode', 'is_public']

       
        game_mode = forms.ChoiceField(
            choices=Room.GAME_MODES,
            widget=forms.Select(attrs={'class': 'form-select'}),
            label='Game Mode'
        )
        
        is_public = forms.ChoiceField(
            choices=[('public', 'Public'), ('private', 'Private')],
            widget=forms.Select(attrs={'class': 'form-select'}),
            label='Privacy'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class JoinPrivateForm(forms.Form):
    room_id = forms.CharField(
        max_length=6,
        label='Room id',
    )

    class Meta:
        model = Room
        fields = ['room_id']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
