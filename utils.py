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