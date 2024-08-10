from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Enter your name',
                                                                       'class': 'common-input mb-20 form-control',
                                                                       'onfocus': "this.placeholder = ''",
                                                                       'onblur': "this.placeholder = 'Enter your name'"
                                                                       }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Enter email address',
                                                          'pattern': "[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+.[A-Za-z]{1,63}$",
                                                          'class': 'common-input mb-20 form-control',
                                                          'onfocus': "this.placeholder = ''",
                                                          'onblur': "this.placeholder = 'Enter email address'"
                                                          }))
    subject = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Enter subject',
                                                                         'class': 'common-input mb-20 form-control'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter your message',
                                                                       'class': 'common-input mb-20 form-control',
                                                                       'onfocus': "this.placeholder = ''",
                                                                       'onblur': "this.placeholder = 'Enter your message'"}))
    