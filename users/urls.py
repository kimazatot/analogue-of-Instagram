from django.urls import path
from .views import FollowerList, UserActivity, UserProfileDetail

urlpatterns = [
    path('followers/', FollowerList.as_view()),
    path('user-activity/', UserActivity.as_view()),
    path('user-profile/<str:username>/', UserProfileDetail.as_view())
]
