from django import template
from blog.models import Category,Post
from django.db.models import Count
from account.models import Profile
from django.shortcuts import get_object_or_404

register= template.Library()

@register.inclusion_tag('blog/post-category.html')
def post_category():
    category_counts=Category.objects.annotate(post_count=Count('post'))
    cat_dict={}
    for category in category_counts:
        category_title=category.slug
        category_count=category.post_count
        cat_dict[category_title]=category_count
        #annotate return a queryset which has the instances of the table and 
        # the added fields which were cpmputed form the existing fields
    return {
        'categories':cat_dict,
         }






@register.inclusion_tag('blog/popular-posts.html')
def popular_posts():
  posts = Post.objects.order_by('-counted_views')[:6]
  return {
    'posts':posts
  }


@register.inclusion_tag('blog/categories.html')
def categories_list():
   categories=Category.objects.all()
   return {
      'categories':categories
   }