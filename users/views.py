from .models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import UserProfile
from rest_framework import status
from django.http import Http404
from django.utils import timezone


class UserProfileDetail(APIView):
    def get(self, request, username):
        username = request.user.username
        try:
            user_profile = UserProfile.objects.get(user__username=username)
        except UserProfile.DoesNotExist:
            raise Http404

        return Response({'username': user_profile.user.username, 'bio': user_profile.bio,
                         'profile_pic': user_profile.profile_pic.url})


class FollowerList(APIView):
    def get(self, request, username):
        try:
            user_profile = UserProfile.objects.get(user__username=username)
        except Http404:
            raise Http404
        followers = user_profile.followers.all()
        follower_list = [follower.follower_profile.user.username for follower in followers]
        return Response(follower_list)


class UserActivity(APIView):
    def get(self, request):
        users = User.objects.all()

        for user in users:
            if user.last_activity is not None and (timezone.now() - user.last_activity).seconds < 300:
                user.is_online = True
            else:
                user.is_online = False
            user.save()
