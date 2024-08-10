**wierd error**

Page not found (404)
“D:\Programming\NewMuzMusic\media\account\register” does not exist

problem solver in the settings
MEDIA_URL = '/media/'


# Mordad 9th 1:30 am

follow and unfollow
```html

<div class="button-group-area mt-10">
        <form method="POST">
            {% csrf_token %}
            {% if profile in user.profile.follows.all %}
                <button href="#" name="follow" type="submit" value="unfollow" class="genric-btn success-border medium">Following</button>
            {% else %}	
                <button href="#" value="follow" name="follow" type="submit" class="genric-btn success-border medium">Follow</button>

            {% endif %}
        </form>
    </div>
```






# follwing and unfollowing
```python 

def members_profile(request):
    profiles=Profile.objects.all()
    if request.user.is_authenticated:
        if request.method == 'POST':
            current_user_profile=request.user.profile
            action=request.POST['follow']
            target_profile=request.POST['target_profile']
            if action == 'unfollow':
                current_user_profile.follows.remove(target_profile)
            else:
                current_user_profile.follows.add(target_profile)
            current_user_profile.save()    
    return render(request,'account/members.html',{
        'profiles':profiles
    })






```


# Mordad 9th 10 am
**just added the like button**





# Big Question
**when to use a form and when to use an a tag??**



# Mordad 9th 1:00 pm
now im going to work on the personal pages of the users
so i need a new template lets say blog-author.html



# Mordad 9th 6:00 pm
the problem is the  page of each user, in this page you can see the psots of a particular user and all the related info to the user, 
Actually i have difficulties accessing both posts and the specific profile.
i have to access the profile from the user
 blog/author/<str:author_name> 

**2 hours later , ihad a typo! its done**


# lets make the follow button a custom tag 
i think its a good approach to make it reusable
**Mordad 9th 8:00 pm**
the above approach is not gonna work , well two ways available 
1- make the following button an a tag so that using herf you can send the data to the same place
2- use the exising form and diefine two views for following
im lazy lets do the second approach


# Question
for the functions which do not really provide a template , for example a likeView , how should we set a url ? 
```python

    path('single-view/<int:pk>',BlogSingleView.as_view(), name='single_view'),

    path('single-view/<int:pk>',likeView, name='like_post'),

# i did this and the server stops when clicking on the like button!!!!!!!!!!!!!!!!!!!!!!!
```



# i wasnt able to make the custom login_url for login_reuired decorator
So i changed the url of the login view to accounts/login from account/login and 
the problem was solved!


# now i want to make the following func work!






# registration form
**Mordad 11th 1:00 am**

first the user inputs some data to register then before going to the index he goes to another page for the profile form, i used the bio method for it and i couldnt use the existing functions ,
i used the ProfileForm .




# Mordad 11th 
i started the day fresh . Lets go!

**making the follow button avalable in the index page**







# BIG VOW
form now , whenever i want to use only a tags whenever i want to post something only with a button! becouse its a hard to style a button and i want ot use a tag to head to a func

i added the follow button to the index page and its working fine with help pf ai actually to provide me a nice CBV 
the thing is that i cant style its buttom



# Mordad 11th 11 am
**Heading to post create form**

```python
class PostCreateForm(forms.ModelForm):
    category= forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}))
    class Meta:
        model = Post
        fields = ['title', 'post_author', 'category', 'content', 'image_file', 'audio_file']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }
```
this code is so instructive, i learnde how to have a manytomany fiekd in a form


**i should add another condiotion to popular posts rather than the coundted views**
i should add the date for at most 3 days
================================================================================================================================================================================i wasnt able to solve this problem



# Mordada 11th 
working on the comments

**when working with cbv if you have detailview and you want to have form lets say for comment ... what to do?**

should i have two classes  or do the whole thing in one class











================================================================================================================================================================================
i dont understand how to use the widgets ? in the Meta class our outside of it?
how is it gonna dieffer

```python 


# while widget was outside of the Meta it wasnt working
class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=['content']
        widgets = {
            'content':forms.Textarea(attrs={'class':'form-control mb-10'})
        }



```



# 13 Mordad 1:30 am
 i restericted some pages by CBV and this line 
 from django.contrib.auth.mixins import LoginRequiredMixin


now the only part i should worry is the follow buttons in the index and members page



# 13 Mordad 2:30 pa 
**configuring the email system**
```python
#settings.py
EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST= 'smtp.gmail.com'
EMAIL_USE_TLS=True
EMAIL_PORT=587
EMAIL_HOST_USER='maziarheidari1124@gmail.com'
EMAIL_HOST_PASSWORD=EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD') # not gonna work!
```
set EMAIL_HOST_PASSWORD="your_email_password"
this command will set the vaiable for password

the thing is that for the password you should create an app pssword instead of your gmail password

follow below instructions:
    Enable 2-Step Verification for your Google account:
Go to <https://myaccount.google.com/signinoptions/two-step-verification>
Follow the instructions to set up 2-Step Verification using your phone number.
Create an app password:
Go to <https://myaccount.google.com/apppasswords>
Under "Select app," choose "Custom" and provide a name for the password.
Click "Generate." Google will generate a 16-character app password.
Update your Django settings to use the app password:
Replace your actual Gmail password with the generated app password in your Django settings. This ensures your Django application can connect to the Gmail SMTP server securely.
Update your settings.py file with the app password:
Restart your Django application server.






# 13 Mordad 4:30 pm
now im trying to send the email via a nice looking html page 
first i had to go to beefreee website to find a good email template
then i created html file in the account directory and copied the code

```python 
#in the views

from django.core.mail import send_mail,EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

 html_message=render_to_string('account/email.html')
    plain_message= strip_tags(html_message)
    message=EmailMultiAlternatives(subject='Welcome Mail',body=plain_message,from_email='maziarheidari1124@gmail.com',
                     to=['sixifit732@eixdeal.com'] 
                      )
    message.attach_alternative(html_message,'text/html')
    message.send()



```

and last stap lets pass vars to email template





# Mordad 14th 
i added the reset password functionality , it was hard and i couldnt customize it that much,
I had to get rid of the app_name in the account.urls





```python 


from django.contrib.auth.models import User
from account.models import Profile


def follow_unfollow(current_user_profile, target_profile):
    action = current_user_profile.follows.filter(id=target_profile.id).exists()

    if action:
        print('remove')
        current_user_profile.follows.remove(target_profile.id)
    else:
        print('add')
        current_user_profile.follows.add(target_profile.id)


```




# 15 Mordad

some handlers for errors 
