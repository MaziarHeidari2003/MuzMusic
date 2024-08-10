from django import  forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class SignUpForm(UserCreationForm):
    

    email = forms.EmailField(label='',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'chickcorea@gmail.com'}))  
    first_name = forms.CharField(label='',max_length=100,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Chick'}))    
    last_name = forms.CharField(label='',max_length=100,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Corea'}))

    class Meta:
        model=User
        fields=['username','last_name','first_name','email','password1','password2']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''



# class EditProfileForm(forms.ModelForm):
#         email=forms.EmailField(widget=forms.EmailInput({'class':'form-control'}))
#         first_name=forms.CharField(max_length=100,widget=forms.TextInput({'class':'form-control'}))
#         last_name=forms.CharField(max_length=100,widget=forms.TextInput({'class':'form-control'}))
#         username=forms.CharField(max_length=100, widget=forms.TextInput({'class':'form-control'}))
#         class Meta:
#             model= Profile
#             fields= ['profile_image','bio']
#             exclude=['user']
#             widgets = {
#             'bio': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Field 1'}),
#             'field2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Field 2'}),
#             ...
#         }



class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']  # Add other user fields as necessary
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'max_length': 150}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'max_length': 150}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'max_length': 150}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'max_length': 150}),
        }
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_image']  # Add other profile fields as necessary
        widgets={
            'bio':forms.Textarea(attrs={'class':'form-control','placeholder':'Let us know you even more!'})
        }

class EditUserProfileForm(forms.Form):
    user_form = UserForm()
    profile_form = ProfileForm()        


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': '***'
    }))