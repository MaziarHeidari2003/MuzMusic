from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import ListView,DetailView,CreateView,UpdateView,FormView
from .models import Post,Comment
from django.db.models import Q,F
from account.models import Profile
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import PostCreateForm,CommentForm
from django.utils.safestring import mark_safe
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail,EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from decouple import config



class BasePostListView(ListView):
    model = Post
    paginate_by = 5  # Default pagination
    context_object_name='posts'
    ordering=['-id']

    def get_queryset(self):
        queryset = super().get_queryset()  # Retrieve all posts by default
        
        # Get the search query from GET parameters
        search_query = self.request.GET.get('search', '')
        if search_query:
            # Filter posts based on title, content, or author's username
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(post_author__username__icontains=search_query)
            )
        

           # Filter by category if provided
        cat_name = self.kwargs.get('cat_name')
        if cat_name:
            queryset = queryset.filter(category__slug=cat_name)
        # Filter by author if provided
        author_name = self.kwargs.get('author_name')
        if author_name:
            queryset = queryset.filter(post_author__username=author_name)
        return queryset
  


class BlogCategoryView(LoginRequiredMixin,BasePostListView):
    template_name = 'blog/blog-home.html'
    
    def get_queryset(self):
        return super().get_queryset()  # Calls the base logic to filter by category

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        return context

class BlogAuthorView(LoginRequiredMixin,BasePostListView):
    template_name = 'blog/blog-author.html'
    
    def get_queryset(self):
        return super().get_queryset()  # Calls the base logic to filter by author
    
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
    
        username=self.kwargs['author_name']
        profile=get_object_or_404(Profile,user__username=username)
        following=profile.follows.all().exclude(user__username=username)
        followed=profile.followed_by.all().exclude(user__username=username)
        context['username']=username
        context['following']=following
        context['followed']=followed
        context['profile']=profile
        return context



class BlogHomeView(BasePostListView):
    template_name = 'blog/blog-home.html'  # Specify the template for the main blog view




class BlogSingleView(LoginRequiredMixin,DetailView):
    model=Post 
    template_name='blog/blog-single.html'
    context_object_name='post'   

    def get_context_data(self,**kwargs):
        context= super().get_context_data(**kwargs)
        Post.objects.filter(id=self.kwargs.get('pk')).update(counted_views=F('counted_views') + 1)
        post_tobe_liked=get_object_or_404(Post,id=self.kwargs['pk'])
        total_likes=post_tobe_liked.total_likes()
        post = self.get_object()
        post_author=Profile.objects.get(user=post.post_author)
        comments = Comment.objects.filter(post=post).order_by('-created')
        
        form=CommentForm()
        liked=False
        if post_tobe_liked.likes.filter(id=self.request.user.id).exists():
            liked=True
        context['liked']=liked
        context['total_likes']=total_likes    
        context['comments'] = comments  # Add the comments to the context
        context['form']=form
        context['profile']=post_author
        print(post_author)
        return context  
    

        # if you use get instead of filter you are encountring an error! = > AttributeError at /blog/single-view/1
        # 'Post' object has no attribute 'update'

        # this was a solution!
        # post=Post.objects.get(id=self.kwargs.get('pk'))
        # post.counted_views +=1
        # post.save()
    def post(self, request, *args, **kwargs):
            form = CommentForm(request.POST)
            if form.is_valid():
                form.save()
                # sometimes i dont understand difference between the obj and its id
                return HttpResponseRedirect(reverse('blog:single_view',kwargs={'pk':self.get_object().id}))

            return self.get(request, *args, **kwargs)
       

# i dont like this func, i am feeling some code smell
# follwing and unfollowing
# i was a method in the account app, i didint even change the name so that i know there is code smell
# @login_required(login_url='account/login')
# def members_profile(request):
#         if request.method == 'POST':
#             current_user_profile=request.user.profile
#             action=request.POST['follow']
#             target_profile=request.POST['target_profile']
#             print(action)
#             if action == 'unfollow':
#                 current_user_profile.follows.remove(target_profile)
#             else:
#                 current_user_profile.follows.add(target_profile
#             current_user_profile.save()    
#             return HttpResponseRedirect(reverse('blog:blog_author',kwargs={'author_name':s}))        


class PostCreateView(LoginRequiredMixin,CreateView):
    template_name='blog/create-post.html'
    model=Post
    # fields=['title','post_author','category','content','image_file','audio_file']
    form_class = PostCreateForm

    
    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs['data'] = {'post_author': self.request.user}  # Set the default value for post_author field
    #     return kwargs

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST,request.FILES)
        if form.is_valid():
            post_author=form.cleaned_data['post_author']
            followed_by=post_author.profile.followed_by.all().exclude(pk=post_author.pk)
            email_list = [follower.user.email for follower in followed_by]
            # email_list = []
            # for e in followed_by:
            #     email_list.append(e.user.email)



                # The ','.join() function takes a list of strings as an argument and concatenates
                # them into a single string. It places a specified string separator (in this case, a comma ,) 
                # between each pair of adjacent strings.
            form.save()
            post_id = post_author.username

            post_url = f'https://muzmusic.ir/blog/author/{post_id}'
            link = f'{post_author.username} has a new post! <a href="{post_url}">Let\'s check it out!</a>'
            html_message = f'{link}'

            # Strip HTML tags to create a plain text version
            plain_message = strip_tags(html_message)

            # Create the email message
            email = EmailMultiAlternatives(
                subject='New Notification from MuzMusic',
                body=plain_message,  # Plain text version
                from_email=config('EMAIL'),
                to=email_list,
            )

# Attach the HTML version
            email.attach_alternative(html_message, "text/html")

# Send the email
            email.send()


        else:
             for field, errors in form.errors.items():
                messages.add_message(request, messages.ERROR,mark_safe( f"Field {field} has the following errors: {errors}"))
        return redirect('blog:blog_home')
        # actually i want to return the user the sigle page of the post but i cant!



def likeView(request,pk):
    post=get_object_or_404(Post,id=pk)

    liked =False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked=False
    else:
        post.likes.add(request.user)
        liked=True
    return HttpResponseRedirect(reverse('blog:single_view',kwargs={'pk':pk}))        




# def follow_view(request,pk):
#     current_user_id=request.user.id
#     current_profile_id=pk
#     follow_unfollow(current_user_id,current_profile_id)
#     return HttpResponseRedirect(reverse('blog:author_view', ))
def follow_unfollow(request):
    if request.method == 'POST':
        target_profile=Profile.objects.get(user__username=request.POST.get('target_profile'))
        current_user_profile=Profile.objects.get(user__username=request.POST.get('user_id'))
        print(current_user_profile,target_profile)
        action = current_user_profile.follows.filter(id=target_profile.id).exists()

        if action:
            print('remove')
            current_user_profile.follows.remove(target_profile.id)
        else:
            print('add')
            current_user_profile.follows.add(target_profile.id)

        return redirect(request.META.get('HTTP_REFERER', '/default_redirect_url/'))
