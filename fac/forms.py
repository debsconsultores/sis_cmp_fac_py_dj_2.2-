from django import forms

from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model=Cliente
        fields=['nombres','apellidos','tipo',
            'celular','estado']
        exclude = ['um','fm','uc','fc']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })