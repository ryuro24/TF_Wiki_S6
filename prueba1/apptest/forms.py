from django import forms
from .models import Usuario
from django.core.exceptions import ValidationError

class RegistroUsuarioForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control bg-dark-x border-0 mb-2',
            'placeholder': 'Ingrese su contraseña',
            'style': 'background-color: #ffffff;',
            'id': 'id_contrasena'
        })
    )
    password2 = forms.CharField(
        label='Confirmar Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control bg-dark-x border-0 mb-2',
            'placeholder': 'Confirme su contraseña',
            'style': 'background-color: #ffffff;',
            'id': 'id_confirmar_contrasena'
        })
    )

    class Meta:
        model = Usuario
        fields = ('email',)
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control bg-dark-x border-0',
                'placeholder': 'nombre@ejemplo.com',
                'style': 'background-color: #ffffff;',
                'id': 'id_email'
            })
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return password2

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo ya está registrado.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])  # Encripta la contraseña
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control bg-dark-x border-0',
            'placeholder': 'nombre@ejemplo.com',
            'style': 'background-color: #ffffff;',
            'id': 'id_email'
        }),
        label='Correo electrónico'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control bg-dark-x border-0 mb-2',
            'placeholder': 'Ingrese su contraseña',
            'style': 'background-color: #ffffff;',
            'id': 'id_contrasena'
        }),
        label='Contraseña'
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            try:
                usuario = Usuario.objects.get(email__iexact=email)
                if not usuario.check_password(password):
                    raise forms.ValidationError("Correo electrónico o contraseña incorrectos.")
            except Usuario.DoesNotExist:
                raise forms.ValidationError("Correo electrónico o contraseña incorrectos.")

        return cleaned_data




class EditarUsernameForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['username']
        labels = {
            'username': 'Nuevo nombre de usuario',
        }

class CambiarContrasenaForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput,
        required=True,
        label='Nueva contraseña'
    )


