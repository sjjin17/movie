from rest_framework import serializers
from .models import Genre, Movie, MoviePeople, OneLineComment, Provider
from django.contrib.auth import get_user_model


class MovieSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('pk', 'title',)




# 메인페이지 
class MovieListSerializer(serializers.ModelSerializer):

    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = get_user_model()
            fields = ('pk', 'hate_user',)

    hate_user = UserSerializer(read_only=True)
    #genres = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = ('id', 'poster_path','genres','hate_user',)



# 검색 후 or 메인페이지
class MovieTitleListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ('id', 'title', 'poster_path',)





# 검색 전 movie를 장르, 날짜, 평점 순으로 분류  (장르를 다시 개봉일순, 평점순으로 분류해야 함)
# 검색전
class MovieGenreListSerializer(serializers.ModelSerializer):

    
    class Meta:
        model = Movie
        fields = ('id', 'title', 'poster_path','vote_average', 'release_date',) # 평점, 최신순

# 장르별 영화
class GenreMovieSerializer(serializers.ModelSerializer):
    movies_genres = MovieGenreListSerializer(many=True, read_only=True)
    genres_count = serializers.IntegerField(source='movies_genres.count', read_only = True)
    class Meta:
        model = Genre
        fields = '__all__'



class WatchProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = '__all__'


# movie detail 조회

# 한줄평(상세페이지 아랫부분)
class LineCommentSerializer(serializers.ModelSerializer):
    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = get_user_model()
            fields = ('pk', 'nickname',)
    user = UserSerializer(read_only=True)
    class Meta:
        model = OneLineComment
        fields = '__all__'
        read_only_fields = ('movie','like_users')


# 인물정보 => 디테일
class MoviePeopleListSerializer(serializers.ModelSerializer):

    class Meta:
        model = MoviePeople
        fields = '__all__'


# 장르의 아이디와 장르의 이름을 디테일에서 보여주기 위해 => MovieSerializer(디테일)에서 사용
class GenreSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Genre
        fields = '__all__'

# 상세페이지
class MovieSerializer(serializers.ModelSerializer):
    # class LineCommentSerializer(serializers.ModelSerializer):
    #     class Meta:
    #         model = OneLineComment
    #         fields = '__all__'
    #         read_only_fields = ('movie',)

    
    onelinecomment_set = LineCommentSerializer(many=True, read_only=True)
    comment_count = serializers.IntegerField(source='onelinecomment_set.count', read_only = True)
    genres = GenreSerializer(many=True, read_only=True)
    actors = MoviePeopleListSerializer(many=True, read_only=True)
    directors = MoviePeopleListSerializer(many=True, read_only=True)
    like_users_count = serializers.IntegerField(source='like_users.count', read_only=True)
    save_users_count = serializers.IntegerField(source='save_users.count', read_only=True)
    watch_providers = WatchProviderSerializer(many=True, read_only=True)
    class Meta:
        model = Movie
        exclude = ('popularity',)
        


# # movie 정보만(상세페이지 윗부분)
# class MovieDetailSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Movie
#         exclude = ('popularity',)
        






# 위의 LineCommentSerializer와 동일..
# class LineCommentListSerializer(serializers.ModelSerializer):
#     class UserSerializer(serializers.ModelSerializer):
#         class Meta:
#             model = get_user_model()
#             fields = ('pk', 'nickname')
#     user = UserSerializer(read_only=True)
#     class Meta:
#         model = OneLineComment
#         fields = '__all__'
#         read_only_fields = ('movie',)
