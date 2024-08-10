from django.shortcuts import render,redirect
from account.models import Profile
from .models import Maziar
from .forms import ContactForm
from django.urls import reverse_lazy,reverse
from django.core.mail import send_mail,EmailMultiAlternatives
from django.views.generic import TemplateView,ListView,FormView
from blog.forms import FollowForm
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from utils import follow_unfollow
from decouple import config



class IndexView(TemplateView):
    template_name = 'website/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch random profiles to display
        if self.request.user.is_authenticated:
            context['random_profiles'] = Profile.objects.exclude(user=self.request.user).order_by('?')
        else:
            context['random_profiles'] = Profile.objects.all().order_by('?')
   
        context['follow_form'] = FollowForm()
        return context
    
    def post(self, request, *args, **kwargs):
        form = FollowForm(request.POST)
        if form.is_valid():
            target_profile_id = form.cleaned_data['target_profile_id']
            current_user_profile = request.user.profile  # Assuming there's a one-to-one relation
            target_profile = Profile.objects.get(id=target_profile_id)
            follow_unfollow(current_user_profile, target_profile)
            # sometimes i dont understand difference between the obj and its id
            return redirect('website:index')  # Redirect back to the index page

        return self.get(request, *args, **kwargs)
# im kinda feeling code smell for habdling the unuthorized user in the index page
# i am adding condidtions for the random_profiles and i am creating a fake follow buttom
# for the unauthorized user to be taken to the login page




class PrimaryAboutView(TemplateView):
    template_name='website/about.html'



class DetailedAboutView(ListView):
    model=Maziar
    template_name='website/about.html'
    context_object_name= 'maziars'
    def get_queryset(self):

        queryset=super().get_queryset()
        for a in queryset:
            print(a.category)
        cat_name = self.kwargs.get('cat_name')
        print(cat_name)
        if cat_name:
            queryset = queryset.filter(category=cat_name)
            print(queryset)
        return queryset    




class ContactView(FormView):
    template_name = 'website/contact.html'
    form_class = ContactForm
    success_url= reverse_lazy('website:index')

    def form_valid(self, form):
        # This method is called when the form is valid
        name = form.cleaned_data.get('name')
        email = form.cleaned_data.get('email')
        subject = form.cleaned_data.get('subject')
        user_message = form.cleaned_data.get('message')

        # Send the email
        send_mail(subject,
                  user_message,
                  email,
                  [config('EMAIL')],
                  fail_silently=False)
        

       
        context= {
                'name':name,
            }
          
        html_message=render_to_string('website/new-email_2024-08-04T081801.251673.html',context=context)
        plain_message= strip_tags(html_message)
        message=EmailMultiAlternatives(subject='Message Received',body=plain_message,from_email='maziarheidari1124@gmail.com',
                    to=[email] 
                    )
        message.attach_alternative(html_message,'text/html')
        message.send()
            

        # Return the success URL
        return super().form_valid(form)