from django import forms
from .models import Room

class RoomForm(forms.ModelForm):
    game_mode = forms.ChoiceField(
        choices=Room.GAME_MODES,
        widget=forms.Select(attrs={
            'style': 'color: #28df28; background-color: #181A1B; border: 1px solid #181A1B; padding: 10px; border-radius: 4px; font-family: "Bebas Neue", sans-serif; border-color: #181A1B;',
        }),
        label='Game Mode'
    )
    
    is_public = forms.ChoiceField(
        choices=[('public', 'Public'), ('private', 'Private')],
        widget=forms.Select(attrs={
            'style': 'color: #28df28; background-color: #181A1B; border: 1px solid #181A1B; padding: 10px; border-radius: 4px; font-family: "Bebas Neue", sans-serif; border-color: #181A1B;',
        }),
        label='Privacy'
    )
    
    class Meta:
        model = Room
        fields = ['game_mode', 'is_public']

class JoinPrivateForm(forms.Form):
    room_id = forms.CharField(
        max_length=6,
        label='Room id',
        widget=forms.TextInput(attrs={
            'style': 'color: #28df28; background-color: #181A1B; border-color: #181A1B;  font-family: "Bebas Neue", sans-serif',
            'class': 'form-control custom-input',
        })
    )

    class Meta:
        model = Room
        fields = ['room_id']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
