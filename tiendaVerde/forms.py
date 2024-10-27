from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate

# Define los roles disponibles
ROLES = [
    ('Cliente', 'Cliente'),
]

class FormularioRegistro(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Requerido. Ingresa un correo válido.")
    rol = forms.ChoiceField(choices=ROLES, required=True, help_text="Selecciona tu rol.")

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2', 'rol']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este correo electrónico ya está registrado.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email']  # Asignar el correo como username (aunque no se usará en el formulario)
        if commit:
            user.save()
            # Asignar el grupo basado en la elección del usuario
            rol_seleccionado = self.cleaned_data['rol']
            grupo, created = Group.objects.get_or_create(name=rol_seleccionado)
            user.groups.add(grupo)
        return user
class FormularioInicioSesion(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(username=email, password=password)
        if not user:
            raise forms.ValidationError("Correo o contraseña incorrectos")
        return self.cleaned_data