from django.urls import path
from . import views


app_name = 'communities'

urlpatterns = [
    path('', views.review_list),  # 리뷰 전체
    path('<int:movie_pk>/create/', views.review_create),  # 리뷰 작성
    path('<int:review_pk>/', views.review_detail_RUD),  # 리뷰 1개 조회, 수정, 삭제
    path('<int:review_pk>/like/', views.like_article), # 게시글 좋아요
    path('<int:review_pk>/comments/', views.comment_create),  # 댓글 생성
    path('<int:review_pk>/comments/<int:comment_pk>/', views.comment_UD),  # 댓글 수정, 삭제


    # path('<int:review_pk>/like', views.like_review),
]