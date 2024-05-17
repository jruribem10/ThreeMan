from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm,SetPasswordForm
from django import forms
from .models import Profile



class SignUpForm(UserCreationForm):
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'Nombre de usuario'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Requerido. 150 caracteres o menos. Solo letras, dígitos y @/./+/-/_ permitidos.</small></span>'

		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['placeholder'] = 'Contraseña'
		self.fields['password1'].label = ''
		self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>No puede tener semejanza a los otros campos.</li><li>debe contener por lo menos 8 caracteres.</li><li>No puede ser muy comun.</li><li>No pueden ser solo numeros.</li></ul>'

		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['placeholder'] = 'Confirma tu contraseña'
		self.fields['password2'].label = ''
		self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Ingresa la misma contraseña que antes para verificar.</small></span>'
		
		self.fields['first_name'].widget.attrs['placeholder'] = 'Nombre'
		self.fields['last_name'].widget.attrs['placeholder'] = 'Apellido'
		self.fields['email'].widget.attrs['placeholder'] = 'Email'

class ChangePasswordForm(SetPasswordForm):
	class Meta:
		model = User
		fields = ['new_password1', 'new_password2']

	def __init__(self, *args, **kwargs):
		super(ChangePasswordForm, self).__init__(*args, **kwargs)

		self.fields['new_password1'].widget.attrs['class'] = 'form-control'
		self.fields['new_password1'].widget.attrs['placeholder'] = 'Contraseña'
		self.fields['new_password1'].label = ''
		self.fields['new_password1'].help_text = '<ul class="form-text text-muted small"><li>No puede tener semejanza a los otros campos.</li><li>debe contener por lo menos 8 caracteres.</li><li>No puede ser muy comun</li><li>No pueden ser solo numeros</li></ul>'
		self.fields['new_password2'].widget.attrs['class'] = 'form-control'
		self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirma tu contraseña'
		self.fields['new_password2'].label = ''
		self.fields['new_password2'].help_text = '<span class="form-text text-muted"><small>Ingresa la misma contraseña que antes para verificar.</small></span>'




class UpdateUserForm(UserChangeForm):
	# Hide Password stuff
	password = None
	# Get other fields
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}), required=False)
	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}), required=False)
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}), required=False)

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email')

	def __init__(self, *args, **kwargs):
		super(UpdateUserForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'Nombre'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Maximo 150 caracteres. letras, digitos y @/./+/-/_ son los unicos que estan permitidos</small></span>'

class UserInfoForm(forms.ModelForm):
	phone = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone'}), required=False)
	address1 = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address 1'}), required=False)
	address2 = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address 2'}), required=False)
	city = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'City'}), required=False)
	state = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'State'}), required=False)
	zipcode = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Zipcode'}), required=False)
	country = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Country'}), required=False)

	class Meta:
		model = Profile
		fields = ('phone', 'address1', 'address2', 'city', 'state', 'zipcode', 'country', )
