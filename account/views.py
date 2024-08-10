from django.shortcuts import render,redirect
from django.urls import reverse
from .forms import SignUpForm,LoginForm,ProfileForm,UserForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from django.views.generic import ListView
from .models import Profile
from django.core.mail import send_mail,EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from decouple import config

def register_user(request):
    if not request.user.is_authenticated:
        form=SignUpForm()
        if request.method == 'POST':
            form=SignUpForm(request.POST)
            if form.is_valid():
                user=form.save(commit=False)
                # user.first_name=form['first_name'].value().capitalize()
                # user.last_name=form['last_name'].value().capitalize()
                user.first_name = form.cleaned_data['first_name'].capitalize()
                user.last_name = form.cleaned_data['last_name'].capitalize()
                user.save()
                first_name=user.first_name
                last_name=user.last_name
                welcome_message=f'Welcome to MuzMusic Dear {first_name} {last_name}'
                blog_link=config('BLOG_LINK')
                index_link=config('INDEX_LINK')
                username=form.cleaned_data['username']
                password=form.cleaned_data['password1']
                email=form.cleaned_data['email']
                context= {
                    'welcome_message':welcome_message,
                    'first_name':first_name,
                    'last_name':last_name,
                    'blog_link':blog_link,
                    'index_link':index_link
                }
                user=authenticate(username=username,password=password)
                login(request,user)
            
                messages.success(request,(f'Welcome to MuzMusic dear {first_name}'))
                html_message=render_to_string('account/email.html',context=context)
                plain_message= strip_tags(html_message)
                message=EmailMultiAlternatives(subject='Welcome Mail',body=plain_message,from_email=config('EMAIL'),
                        to=[email] 
                        )
                message.attach_alternative(html_message,'text/html')
                message.send()
                
                return redirect(reverse('bio', kwargs={'username': username}))

            else:
                for field, errors in form.errors.items():
                    messages.add_message(request, messages.ERROR,mark_safe( f"Field {field} has the following errors: {errors}"))
        return render(request,'account/register.html',{
            'form':form
        })
    else:
        return redirect('website:index')
    
@login_required
def bio(request,username):
    form=ProfileForm(request.POST,request.FILES or None)
    profile=Profile.objects.get(user__username=username)
    if request.method == 'POST':
        if form.is_valid():
            bio = form.cleaned_data['bio']
            image = form.cleaned_data['profile_image']
            profile.bio=bio
            profile.profile_image=image
            profile.save()

            return redirect('website:index')

    return render(request,'account/bio.html',{
        'form':form
    })


@login_required
def logout_user(request):
  logout(request)
  return redirect('/')




def login_user(request):
    form=LoginForm()
    if request.method == 'POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            # password=request.POST['password']
            # username=request.POST['username']
            password=form.cleaned_data['password']
            username=form.cleaned_data['username']
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                #messages.success(request,(f'You just logged in dear {request.user.first_name}'))
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                return redirect('website:index')
            else:
               messages.success(request,('Username or Password incorrect'))

    return render(request,'account/login.html',{
        'form':form,
    })



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

@login_required
def members_profile(request):
    profiles=Profile.objects.all()
    return render(request, 'account/members.html', {'profiles': profiles})



