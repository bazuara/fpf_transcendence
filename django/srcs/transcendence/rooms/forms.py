from django import forms
from .models import Room

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['game_mode', 'is_public']  # Incluye los campos que deseas en el formulario

        # Opcionalmente, puedes personalizar los widgets y etiquetas aquí
        game_mode = forms.ChoiceField(
            choices=Room.GAME_MODES,  # Usa las opciones definidas en tu modelo
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

class RoomIDForm(forms.Form):
    number = forms.IntegerField(label='ENTER A ROOM ID')