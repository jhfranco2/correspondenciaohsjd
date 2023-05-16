from django import forms

from correspondencia.models import Libro


class LibroForm(forms.ModelForm):
    SIGLA_CHOICES = (
        ('C','CI'),
        ('Z','Z.AND'),
        ('G','G.AND')
    )

    IMPORTANCIA_CHOICES = (
        ('A', 'Alta'),
        ('B', 'Baja'),
        ('M', 'Media'),
        ('S', 'Sin importancia'),
    )

    TDOCUMENTO_CHOICES = (
        ('F','FACTURA'),
        ('N','NOTA CREDITO'),
        ('O','OTRO')
    )

    REMITENTE_DESTINATARIO_CHOICES = (
        ('R','REMITENTE'),
        ('D','DESTINATARIO')
    )

    sigla = forms.ChoiceField(choices=SIGLA_CHOICES,widget=forms.Select(attrs={'class': 'form-control'}))
    importancia = forms.ChoiceField(choices=IMPORTANCIA_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    tipo_documento = forms.ChoiceField(choices=TDOCUMENTO_CHOICES,widget=forms.Select(attrs={'class': 'form-control'}))
    remitente_destinatario = forms.ChoiceField(choices=REMITENTE_DESTINATARIO_CHOICES,widget=forms.Select(attrs={'class': 'form-control'}))
    

    class Meta:
        model = Libro
        fields = '__all__'
        widgets = {
            'numero_documento' : forms.TextInput(attrs={'class': 'form-control'}),
            'proveedor': forms.TextInput(attrs={'class':'form-control'}),
            'fecha_solicitud': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'fecha_entrada':  forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'remitente_destinario': forms.Select(attrs={'class':'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_destinatario_remitente': forms.TextInput(attrs={'class': 'form-control'}),
            'asunto': forms.TextInput(attrs={'class': 'form-control'}),
            'proceso': forms.Select(attrs={'class': 'form-control'}),
            'quien_firma': forms.TextInput(attrs={'class': 'form-control'}),
            'quien_solicita_recibe': forms.TextInput(attrs={'class': 'form-control'}),
            'salida': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'registro_de_entrega': forms.TextInput(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control'}),
        }
