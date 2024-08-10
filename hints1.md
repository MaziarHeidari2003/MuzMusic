# 6 Mordad 2:30 pm
**The first steps of the project:**

- Initializing the project,making a venv and installing the needed packages
- Just started the three app => website,blig,account 
- lets go config the apps and implement their urls
- lets go do the templates and static files


**what is the difference between STATIC_ROOT AND STATICFIELS_DIR?**

In Django, STATICFILES_DIRS and STATIC_ROOT serve different purposes within the context of static file management:
STATICFILES_DIRS: This setting is a list of directories where Django's staticfiles app will look for static files (such as CSS, JavaScript, and image files) when collecting them for deployment. These directories should contain the static files used by your project's various apps. The default value for this setting is an empty list, but you can define multiple directories as needed.
In the example you provided:
```python
STATICFILES_DIRS = [
    BASE_DIR / "static",
    "/var/www/static/",
]
```

Django will look for static files in both BASE_DIR / "static" (a path relative to your project's base directory) and /var/www/static/ (an absolute path) when collecting static files.
STATIC_ROOT: This setting defines the absolute filesystem path where Django's collectstatic command will collect all the static files from the locations defined in STATICFILES_DIRS. The collected files are placed in the directory specified by STATIC_ROOT, and this directory should be served by your web server during deployment.
Example:

```python
STATIC_ROOT = "/var/www/myproject/static/"
```

 **warning**
  (staticfiles.E002) The STATICFILES_DIRS setting should not contain the STATIC_ROOT setting.

This warning appears because the STATICFILES_DIRS setting should not include the directory specified in the STATIC_ROOT setting. The STATICFILES_DIRS setting is meant to specify the locations where Django should look for static files during development, while STATIC_ROOT is the destination directory where Django collects static files for deployment.
Including STATIC_ROOT in STATICFILES_DIRS can lead to issues during the static file collection process. When you run collectstatic, Django will try to copy the contents of STATIC_ROOT into itself, which might result in duplicated files, confusion during development, or errors during deployment.
To resolve this issue, make sure that STATICFILES_DIRS only contains the directories where your project's static files are located, excluding STATIC_ROOT. In your case, remove /var/www/static/ from STATICFILES_DIRS since it is already set as STATIC_ROOT.

**worth noting**
Its important to load the static in the base.html even if there are no directly static tags in it.


# Models
**Mordad 6th 4:00 pm**

**post validation**
i didin't want to force the user to have image and audio and content for his/her posts at the same time , so i needed a way to make sure that when saving a post , at ;east pne of these fields has value
- my solution
well maybe i can do the validation at the form created for posts but you know what i learning ! So lets just experiment ! Lets fo it in the post model:

```python 
    
    def clean(self):
        if (not self.image_file and not self.audio_file and not self.content):
            raise ValidationError("Either field1 or field2 must have a value.")

        super().clean()

```


**conmments for dead users**
so what should i do if a user deletes his/her account ? i will delete his posts, what about his comments? i want to let the comments stay

```python 
# in the comment model
comment_author = models.ForeignKey(User,on_delete=models.DO_NOTHING,null=True)
def __str__(self):
    try:
      return f'{self.commnet_author.username} : {self.content[:30]}'
    except:
      return f'no author : {self.content[:30]}'
    

```


**post relationship with authors and comments**
a simple foreingkey to the user table
- ManyToOne relationship is the same as foreignKey
So what to do for the comments?

DONT WE HAVE A OneToMany RELATIONSHIP?
Yes, Django and other relational databases also support "one-to-many" relationships. In a "one-to-many" relationship, a single object of one model can be related to multiple objects of another model. This is essentially the reverse of a "many-to-one" or "foreign key" relationship.
In Django, you can define a one-to-many relationship using a ForeignKey field on the "many" side, just like a many-to-one relationship. Django automatically creates a reverse relationship manager called <lowercase_model_name>_set on the "one" side, which allows accessing all related objects from the "many" side.




**user model**
i want a have a profile class which has a foreignkey to the django user table 
so I have to use signals

```python
#account.signals.py

from .models import Profile
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save,sender=User)
def post_save_create_profile(sender,instance,created,**kwargs): 
    if created:
        #Profile.objects.create(user=instance)
        user_profile=Profile(user=instance)
        user_profile.save()
        #Each user should follow him/herself
        user_profile.follow.set([instance.profile.id])
        user_profile.save()

#post_save.connect(post_save_create_profile,sender=User) => without the decorator        



#account.apps.py
   def ready(self):
        import account.signals
#account.init.py
default_app_config='account.apps.AccountConfig'
```

**lets do some magic in the admin panel of the account**
i learend how to unregsiter a model which is in the admin panel and how to mix to models into one , so that i can see them together in the admin panel
```python 

from django.contrib import admin
from .models import Profile
from django.contrib.auth.models import User


admin.site.register(User,UserAdmin)
#mix profile info with user info
class ProfileInline(admin.StackedInline):
    model=Profile

class UserAdmin(admin.ModelAdmin):
    model=User
    #just display username field on  admin page
    fields=['username']
    inlines=[ProfileInline]

#unregister the initial user
admin.site.unregister(User)

#register the new user panel
#admin.site.register(Profile)
#When wecreat the ProfileInline class  there is no need for the above line


```
**how to make the following option for users?**
```python

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    follow = models.ManyToManyField('self',related_name='follwed_by',
                                    symmetrical=False,blank=True)
 ```



# Mordad 6th 6:00 pm
now i dont really know what should the author field in the Post model , refer to!
User or Profile? Imma refer it the Profile




# Mordad 7th 1:00 am
so im dealing with forms, I  started the SignUpForm and it has challenges for me both in the views and forms , 
in the forms i had to deciede which fields to show to the user , i wanted to get rid of the username and use email and password for authentication but because of inherting from userCreateionForm i didnt dear! 
The other challenge was capitalizing the first_name and last_name before being saved to the data base 

```python
    if form.is_valid():
            user=form.save(commit=False)
            user.first_name=form['first_name'].value().capitalize()
            user.last_name=form['last_name'].value().capitalize()
            user.save()
```
In Django, a "BoundField" is a field object associated with a form that has been bound to some data, usually coming from user input or initial form data. It is a subclass of Django's Field class, which represents a single input field on a form.
When you create a form instance with some data, each field in the form gets populated with the corresponding data value and becomes a "BoundField". This allows you to interact with the field knowing that it has a specific value.
For example, when you write form = MyForm(request.POST), each field in MyForm is bound to the corresponding value from the request.POST dictionary, creating a set of BoundField instances.
Some common attributes and methods you can use with BoundField instances include:
.value: Returns the current value of the field as a string.
.data: Returns the data used to populate the field.
.errors: Returns an ErrorList object that contains any validation errors associated with the field.
.as_widget(): Renders the field as an HTML widget.
Working with BoundField instances is an essential part of handling form data in Django views and templates.



# Mordad 7th 10:00 am
i had problem fetching the categories related to a post, i didnt  know how to do it in a ManyToMany relateionship. I didnt know how to do it in a OneToMany realationship too!
```html

<ul class="tags">
    {% for cat in post.category.all %}
    <li><a href="#">
        {{cat.title}}
        {% if not forloop.last %}
        ,
        {% endif %}	
    </a></li>
    {% endfor %}
</ul>
```





# Mordad 7th 11:00 am
**media and static files config**
```python

#settings
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

#urls
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#this line solved the problem
# This line serves media files from the MEDIA_ROOT directory using the static function from django.conf.urls.static module. This approach is suitable for local development but is not recommended for production, as it is not designed to handle the performance demands and security requirements of a live site.
```
I had trouble showing the image i had uploaded adn the above line solved the problem
the folders post_image_files and post_audio_files were automatcally created . These folders were defined when creating the fields in the models



**The problem is that we dont have a media folder**
MEDIA_ROOT = BASE_DIR / 'media'
this line is in charge of creating the media folder
and the upload_to attrs in the models creates subfolders in the media!

Done!


# Dealing with redirecting the user to the single page
i learned something new 
i am now using th get_absolute_url method in models to this and its a lot cleaner than the other ways 
```html
		<a class="posts-title" href="{{post.get_absolute_url}}"><h3>{{post.title}}</h3></a>
```


============================================================================================
# Mordad 7th 1:00 pm
Dealing with single pages . I have an issue with having the audio_file form the post model in the template. Couldn't solve it!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
============================================================================================


============================================================================================
# Mordad 7th 2:00 pm
i seperatd the sidebar widgets into some other files and included them in the blog-single.html , Now i dont know to use teplate tags or views to send data to them

Imma use custom template tags 
============================================================================================

so i used custom template tags !!!!!!!
i use custom template tags for popular_posts, category counts, the author widget.






# Mordad 7th 4:00 pm
**Custom Template Tags**
one thing to note! Watch out not to choose the same name if you have custom tags in more than one app


**Now is the time to implement the ability to search posts**
its done , but i had trouble doing in CBV
```python 

class BlogView(ListView):
    model=Post
    template_name='blog/blog-home.html'
    context_object_name='posts'


    query=self.request.GET.get('search')
    def get_queryset(self):
        #query=self.request.GET.get('search')
        if query:
            return Post.objects.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(post_author__username__icontains=query)
            )
        else:
            return Post.objects.all()
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #query = self.request.GET.get('search')
        if query and not context['posts']:
            context['no_results_message'] = f"No results found for '{query}'."
        return context   

#overall i feel like i should use get_context_data when manipulating data and adding something else rather than the model to be passed to the template
```


# Mordad 7th 5:40 pm
**writer_widget custom tag**
- the thing about the writer-info is that it takes an arg which defienes which user's info is going to be shown based on the page we are.
So this arg should be differnt based on the page



# Mordad 7th 10:20 pm
I want to make the counted_views of every post to increment whenever someone the sigle page of the post, so we should modify the BlogSingle class
```python 

   def get_context_data(self,**kwargs):
        context= super().get_context_data(**kwargs)
        Post.objects.filter(id=self.kwargs.get('pk')).update(counted_views=F('counted_views') + 1)
        # if you use get instead of filter you are encountring an error! = > AttributeError at /blog/single-view/1
        # 'Post' object has no attribute 'update'

        # this was a solution!
        # post=Post.objects.get(id=self.kwargs.get('pk'))
        # post.counted_views +=1
        # post.save()
        return context  

```

**what is F**
In Django's ORM, F is an object that represents a model field reference. It is used to perform database operations using the values of fields directly in the database without having to load them into memory first
```python
books_with_review_count = Book.objects.annotate(review_count=Sum(('bookreview__count'))) 
books_with_review_count = Book.objects.annotate(review_count=Sum(F('bookreview__count'))) 

```
how are these querier different? 
The first query you provided is slightly incorrect, as you're missing the F object. The correct query should be:
python
Copy
books_with_review_count = Book.objects.annotate(review_count=Sum(F('bookreview__count')))
In this corrected query, the F('bookreview__count') part is essential for it to work properly. The F object allows Django to reference the count field of the BookReview model related to each Book instance. The Sum() function then aggregates those values for each Book.
If you omit the F object and just pass 'bookreview__count' as a string:
python
Copy
books_with_review_count = Book.objects.annotate(review_count=Sum('bookreview__count'))
Django would try to sum up the string 'bookreview__count' rather than the actual values from the related BookReview instances. As a result, the query would produce incorrect results, with each Book instance having the same review_count.
In summary, using the F object ensures that Django correctly interprets the expression and computes the aggregated values based on the actual field values from the related model instances.





# Mordad 8th 11:00 pm
**Dealing with messages**
```html

<h6 class="text-white">	
    {% if messages %}
    <div class="alert alert-dark" role="alert">
        {% for s in messages %}
            {{s}}
        {% endfor %}
        </div>
        {% endif %}	
</h6>

```
```python 
# dont forget to import mark_safe to escape the html tags
    user=authenticate(username=username,password=password)
    login(request,user)
    messages.success(request,(f'Welcome to MuzMusic dear {first_name}'))
    return redirect('website:index')
else:
        for field, errors in form.errors.items():
        messages.add_message(request, messages.ERROR,mark_safe( f"Field {field} has the following errors: {errors}"))


```


# Mordad 8th 11:30 pm

**Login form**
Im not  going to define a form , im going to use input tags


```python 


def login_user(request):
    if request.method == 'POST':
        username=request.POST.cleaned_data['username']
        password=request.POST.cleaned_data['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,(f'You just logged in dear {user.first_name}'))
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            return redirect('website:index')


    return render(request,'account/login.html',{
    })

#this code has a lesson, how to use the next param!!!!
```




# Mordad 8th 11:30 pm
============================================================================================
**its an important lesson**
```python 


class LoginForm(forms.Form):
     class Meta:
          moddel=User
          fields=['username','password']
          
     def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = '*******'

# first! you should sue the Meta class with forms.Modleform!!!!!!!


### Explanation

1. Use of forms.Form: Since you're creating a login form that doesn't directly map to a model, you should use forms.Form instead of forms.ModelForm.

2. Field Definitions: The username and password fields are defined as class attributes of the LoginForm. Each field can have its own widget and attributes.

3. Initialization Method: You don't need to override the init method unless you want to add additional customization beyond setting widget attributes. In this case, we set the attributes directly when defining the fields.

```


**next parameter**

```html

{% if request.GET.next %}
<input type="hidden" name="next" value="{{request.GET.next}}">
{% endif %}

```
```python 
#in login view
    if 'next' in request.POST:
        return redirect(request.POST.get('next'))
    return redirect('website:index')


```


# quick question 
- when you define a default for an image, how does djnago find the image?



**EDIT PROFILE OF THE USER**
```python 


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name', 'email']  # Add other user fields as necessary
        widgets={
            'username':forms.CharField(max_length=150,attrs={'class':'form-control'}),
            'last_name':forms.CharField(max_length=150,attrs={'class':'form-control'}),
            'first_name':forms.CharField(max_length=150,attrs={'class':'form-control'}),
            'email':forms.EmailField(max_length=150,attrs={'class':'form-control'})
        }

        # this code is going to get an erro cause of the attrs!





#         The issue you're encountering is due to the fact that the widgets attribute in a Django ModelForm should map field names to widget instances, not to field definitions. In your UserForm, you're trying to define the fields again inside the widgets dictionary, which is incorrect.

# Here's how you can correctly specify custom widgets for your form fields:

### Corrected UserForm

from django import forms
from django.contrib.auth.models import User

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


```



# Mordad 8th 4:50 pm
**I am happy to say that i was able to handle two forms at the same time**
I mean the edit form is a combination of the userForm and the ProfileForm

```python 
#views
@login_required
def edit_profile(request):
    profile = request.user.profile 
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST,request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('website:index')  # Redirect to a success page or profile page

    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)

    return render(request, 'account/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })


#forms

```