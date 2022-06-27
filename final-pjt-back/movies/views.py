from django.shortcuts import render, get_list_or_404, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import generics
from rest_framework import status
from .models import Genre, Movie, OneLineComment
from communities.models import Review
from .serializers import LineCommentSerializer, GenreMovieSerializer, GenreSerializer, MovieListSerializer, MovieSerializer, MovieTitleListSerializer, MovieSearchSerializer
from django.contrib.auth import get_user_model
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
#from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException

import time

# class ProductList(generics.ListAPIView):
#     queryset = Movie.objects.all()
#     serializer_class = ProductSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['category', 'in_stock']


class MovieListView(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSearchSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']


class MovieSearchView(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'actors__also_known_as']


@api_view(['GET'])
def index(request):
    movies = get_list_or_404(Movie)
    serializer = MovieListSerializer(movies, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def movielist(request):
    movies = get_list_or_404(Movie)
    serializer = MovieTitleListSerializer(movies, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = MovieSerializer(movie)
    return Response(serializer.data)



# @api_view(['GET'])
# def detail_up(request, movie_pk):
#     movie = get_object_or_404(Movie, pk=movie_pk)
#     serializer = MovieDetailSerializer(movie)
#     return Response(serializer.data)



@api_view(['GET'])
def genres(request):
    genres = get_list_or_404(Genre)
    serializer = GenreSerializer(genres, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def genre_detail(request, genre_pk):
    genre = get_object_or_404(Genre, pk=genre_pk)
    serializer = GenreMovieSerializer(genre)
    
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def linecomments(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    linecomments = movie.onelinecomment_set.all()
    print(linecomments)
    #linecomment = get_list_or_404(OneLineComment).filter(pk=movie_pk).filter(pk=request.user.pk)
    if request.method == 'GET':
        serializer = LineCommentSerializer(linecomments, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = LineCommentSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid(raise_exception=True):
            print(2)
            serializer.save(movie=movie, user=request.user)  # user=request.user
            print(3)
            return Response(serializer.data, status=status.HTTP_201_CREATED)



@api_view(['DELETE'])
def comment_delete(request, movie_pk, linecomment_pk):
    linecomment = get_object_or_404(OneLineComment, pk=linecomment_pk)
    # if request.user == linecomment.user:
    linecomment.delete()
    data = {
        'delete': f'{linecomment.user}가 쓰신 {linecomment_pk}번 글이 삭제되었습니다.'
    }
    return Response(data, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def like_movie(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    user = request.user
    if movie.like_users.filter(pk=user.pk).exists():
        movie.like_users.remove(user)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)
    else:
        movie.like_users.add(user)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)

@api_view(['POST'])
def save_movie(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    user = request.user
    if movie.save_users.filter(pk=user.pk).exists():
        movie.save_users.remove(user)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)
    else:
        movie.save_users.add(user)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)


# 추천 알고리즘 짜기
import math
import numpy


def user_based_filtering(reviews_dict, me):  # my=user_pk, you=다른 사람 pk
    movies = Movie.objects.all()
    movies_pk = []  # db에 있는 모든 영화 데이터
    for movie in movies:
        movies_pk.append(movie.pk)

    my_movies = set(reviews_dict[me].keys()) # 내가 리뷰한 영화 pk들
  
    similar_score={} # 사용자간 유사도 결과 {다른 사람 pk : 그 사람과의 유사도}
    no_watch_movie = set()  # 남이 봤는데 내가 안 본 영화 목록
    for you in reviews_dict.keys():
        if you != me:
            you_movies = set(reviews_dict[you].keys())
            intersect = my_movies.intersection(you_movies)  # 영화 교집합
            if len(intersect) >= 3:  # 평가내린 영화가 3개 이상 겹치면
                no_watch_movie.update(you_movies - my_movies)
                my_star_rate = [reviews_dict[me][i] for i in intersect]
                you_star_rate = [reviews_dict[you][i] for i in intersect]
                dot = numpy.dot(my_star_rate, you_star_rate)
                distance = math.sqrt(sum([i ** 2 for i in my_star_rate])) * math.sqrt(sum([i ** 2 for i in you_star_rate]))
                similar = dot / distance
                similar_score[you] = similar
    # print(similar_score) = {6: 1.0, 7: 0.9660917830792958, 8: 0.4386692417126296, 9: 0.9014913017684524}

    # neighbor에 나와 유사도가 비슷한 사람 순으로 pk값을 저장
    tmp = sorted(similar_score.items(), key=lambda x: x[1], reverse=True)  # 내림차순 정렬
    
    # knn 알고리즘에서 k = 5로 지정함, 즉 유사도 높은 5명만 확인함
    neighbor = []
    for (person, similar) in tmp[:5]:
        if similar >= 0.6:
            neighbor.append(person)

    recommend_movies = {} # {영화 id : 추천도}
    for movie in no_watch_movie:  # 내가 안 본 영화를 for문 돌기
        up = 0  # 분자
        cnt = 0  # 분모
        # 영화 1개 (이웃이 몇명 봤는가)
        for you in neighbor: # 모든 이웃을 돌면서
            if movie in reviews_dict[you].keys():  # you가 이 영화를 봤다면 r, s 저장해둠
                up += reviews_dict[you][movie] * similar_score[you]  # you평점 * you와 my의 유사도
                cnt += 1
        if cnt and up / cnt >= 2.5:  # 추천도가 2.5 이상이면
            recommend_movies[movie] = up / cnt
    return sorted(recommend_movies.items(), key=lambda x: x[1], reverse=True)[:15]  # 영화 추천도 높은 순으로 정렬 후 15개 자름


@api_view(['GET'])
def recommendation(request):
    user = request.user.pk
    reviews = Review.objects.all()
    reviews_dict = {}
    for review in reviews:
        if reviews_dict.get(review.user.pk):
            reviews_dict[review.user.pk].update({review.movie.pk: int(review.star_rate)})
        else:
            reviews_dict[review.user.pk] = {review.movie.pk: int(review.star_rate)}
    # print(reviews_dict) {1: {12: 5}, 4: {13: 5, 58: 3}, ... 9: {11: 3, 24: 1, 12: 3, 18: 1, 252: 5, 176: 5, 162: 1, 497: 5}}

    data = []  # {id : id, title, poster_path} 이 형태로 들어가야 함
    if reviews_dict.get(user):  # 내가 리뷰를 하나라면 남겼으면
        recommend_movies = user_based_filtering(reviews_dict, user)  # 추천 영화 15개 나옴
        for (moviepk, tmp) in recommend_movies:  # pk, 추천도가 담긴 리스트
            movie = Movie.objects.get(pk=moviepk)
            data.append({"id": moviepk, "title": movie.title, "poster_path": movie.poster_path})
 
    return Response(data)



# @api_view(['GET'])
# def now_play(request):
#     print(request.response)
#     # movie = get_object_or_404(Movie, pk=movie_pk)
#     # movie_title = movie.title
#     # path = 'C:/Program Files (x86)/chromedriver_win32/chromedriver.exe'
#     # options = webdriver.ChromeOptions()
#     # options.add_experimental_option('excludeSwitches', ['enable-logging'])
#     # driver = webdriver.Chrome(path, chrome_options=options)
#     # driver.get('https://www.cgv.co.kr/')
#     # time.sleep(1)  
#     # element = driver.find_element(By.CSS_SELECTOR, '[id="header_keyword"]').send_keys("movie_title" + Keys.RETURN)
#     # return 

    
#     url = 'http://www.cgv.co.kr/movies/?lt=1&ft=1'
#     response = requests.get(url).text
#     #print(response)

#     now_play_movies = []
#     data = BeautifulSoup(response, 'html.parser')
#     for movie in data.findAll('strong',  attrs={'class': 'title'}):
#         # print(movie.text)
#         now_play_movies += [movie.text]

#     data = {
#     "now_play_movies": now_play_movies,
#     }

#     return Response(data, status=status.HTTP_200_OK)


def check_exists_by_xpath(xpath): # 함수 선언
    try: # 아래 코드 실행해보기
        webdriver.find_element(By.XPATH, xpath) # xpath를 통해 요소 검색
    except NoSuchElementException: # 만일 요소가 없다는 오류가 발생했다면
        return False # False를 반환 → 요소 없음
    return True # True를 반환 → 요소 있음

@api_view(['GET'])
@permission_classes([AllowAny])
def reservation(request, movie_title):

    path = 'C:/Program Files (x86)/chromedriver_win32/chromedriver.exe'
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("headless")
    # 페이지가 완전히 로드되는 것을 기다리지 않음 => 빨리 다음 화면으로 넘어갈 때 유용하다.
    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "none"

    driver = webdriver.Chrome(path, chrome_options=options)
    driver.get('https://www.cgv.co.kr/')
   
    element = driver.find_element(By.CSS_SELECTOR, '[id="header_keyword"]').send_keys(movie_title + Keys.RETURN)
    # 예매하기 버튼이 있으면 예매하기 버튼을 누른 후 그 주소를 반환하고 없으면 False를 반환
    try:
        now_movie = driver.find_element(By.XPATH, '//*[@id="preOrderMovie_list"]/li/div/div[3]/a[2]')
        now_movie.click()
        movie_url = driver.current_url
    except NoSuchElementException:
        movie_url = driver.current_url

    # 예매하기 버튼이 있으면 True를 반환하고 없으면 False를 반환한다.
    # try:
    #     driver.find_element(By.XPATH, '//*[@id="preOrderMovie_list"]/li/div/div[3]/a[2]')
    #     now_movie = True
    # except NoSuchElementException:
    #     now_movie = False
    # if now_movie == True:
    #     driver.find_element(By.XPATH, '//*[@id="preOrderMovie_list"]/li/div/div[3]/a[2]').click()  # 예매하기 버튼 눌러주기
    #     movie_url = driver.current_url
    # else:
    #     movie_url = False
    
    data = {
        "movie_url": movie_url
    }
    return Response(data, status=status.HTTP_200_OK)
    