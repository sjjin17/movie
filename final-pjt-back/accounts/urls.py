from django.urls import path
from . import views


app_name = 'accounts'

urlpatterns = [
    path('profile/<int:user_pk>/', views.profile),  # 프로필 페이지
    path('signup/', views.signup),
    path('profile/<int:user_pk>/edit/', views.editprofile),  # 회원정보 수정
    # path('profile/edit/2/', views.editprofiletwo),  # 회원정보 수정
]