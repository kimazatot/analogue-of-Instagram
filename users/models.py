from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfile(models.Model):
    DoesNotExist = None
    objects = None
    username = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True)


class Followers(models.Model):
    user = models.ForeignKey(UserProfile, related_name='followers', on_delete=models.CASCADE)
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)


class UserActivity(models.Model):
    def update_last_activity(self, user_id):
        user = User.objects.get(pk=user_id)
        user.last_activity = timezone.now()
        user.save()