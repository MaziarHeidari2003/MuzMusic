from django.contrib import admin
from .models import Profile
from django.contrib.auth.models import User



# #mix profile info with user info
class ProfileInline(admin.StackedInline):
    model=Profile



class UserAdmin(admin.ModelAdmin):
    model=User
#     #just display username field on  admin page
    fields=['username','email','first_name','last_name']
    inlines=[ProfileInline]


admin.site.unregister(User)
admin.site.register(User,UserAdmin)



