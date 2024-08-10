from django.urls import path
from django.views.generic import TemplateView
from .views import IndexView,DetailedAboutView,ContactView,PrimaryAboutView

app_name='website'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('about/<str:cat_name>', DetailedAboutView.as_view(),name='detailed_about'),
    path('about', PrimaryAboutView.as_view(),name='about'),
    path('contact', ContactView.as_view(),name='contact'),
    

]