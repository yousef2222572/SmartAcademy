from django.contrib.auth.forms import AuthenticationForm ,UserCreationForm,UserChangeForm
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _



attrs={'class':'form-control'}


class UserLoginForm(AuthenticationForm):
    
    def clean_username(self):
        username = self.cleaned_data['username']

        user = User.objects.filter(username=username).first()

        if not user:
            user = User.objects.filter(email=username).first()

        if user:
            return user.username

        return username

    def __init__(self,*args, **kwargs):
        super(UserLoginForm,self).__init__( *args, **kwargs)
        
        
    username=forms.CharField(
        label=_('User name or Email'),
        widget=forms.TextInput(attrs=attrs)
    )
    password=forms.CharField(
        label=_('Password'),
        widget=forms.TextInput(attrs=attrs)
    )

class UserFormCreation(UserCreationForm):
    
    
    def __init__(self,*args,**kwargs):
        super(UserFormCreation,self).__init__(*args,**kwargs)
        
    first_name=forms.CharField(
        label=_('First name'),
        widget=forms.TextInput(attrs=attrs)
    )
    last_name=forms.CharField(
        label=_('Last name'),
        widget=forms.TextInput(attrs=attrs)
    )

    username=forms.CharField(
        label=_('User name'),
        widget=forms.TextInput(attrs=attrs)
    )
    email=forms.EmailField(
        label=_('Email'),
        widget=forms.TextInput(attrs=attrs)
    )
    password1=forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(attrs=attrs)
    )
    password2=forms.CharField(
        label=_('Password confirmation'),
        strip=False,
        widget=forms.PasswordInput(attrs=attrs)
    )
    
    class Meta (UserCreationForm.Meta):
        fields=('first_name','last_name','username','email')
        
        
class UserProfileView(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('password', None)
        self.fields['email'].disabled = True
        self.fields['username'].disabled = True
    class Meta:
        model=User
        fields=['username','email','first_name','last_name'] 
        exclude=['password']
        widgets={
            'first_name':forms.TextInput(attrs=attrs),
            'last_name':forms.TextInput(attrs=attrs),
            'email':forms.TextInput(attrs=attrs),
            'username':forms.TextInput(attrs=attrs),
        }
        
        
class UserForgotPasswordView(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('password', None)
        self.fields['email'].disabled = True
        self.fields['username'].disabled = True
    class Meta:
        model=User
        fields=['username','email'] 
        exclude=['password']
        widgets={
            'email':forms.TextInput(attrs=attrs),
            'username':forms.TextInput(attrs=attrs)
        }






class ForgotPasswordEmailForm(forms.Form):
    email = forms.EmailField(label=_('Email'))