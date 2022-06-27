from django.urls import path
from . import views




app_name = 'movies'

urlpatterns = [
    path('', views.MovieListView.as_view()),
    path('all/', views.index),  # 메인 페이지
    #path('movielist/', views.movielist),
    path('<int:movie_pk>/', views.detail),  # 영화 상세 페이지
    #path('<int:movie_pk>/up/', views.detail_up),
    # 검색 페이지(djagno에서 페이지 자체를 만들어야하는지 모르겠어서 일단 주석처리)
    path('genres/', views.genres),
    path('genres/<int:genre_pk>/', views.genre_detail),
    path('<int:movie_pk>/linecomments/', views.linecomments),
    path('<int:movie_pk>/<int:linecomment_pk>/delete/', views.comment_delete),
    path('<int:movie_pk>/like/', views.like_movie),
    path('<int:movie_pk>/save/', views.save_movie),
    path('search-result/', views.MovieSearchView.as_view()),
    path('recommendation/', views.recommendation),
    # path('now_play/', views.now_play),
    path('reservation/<str:movie_title>/', views.reservation),

]

