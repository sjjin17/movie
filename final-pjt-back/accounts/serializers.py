from dataclasses import field
from rest_framework import serializers
from django.contrib.auth import get_user_model
from communities.models import Review, Comment
from movies.models import Movie, OneLineComment, Genre

user = get_user_model()

class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ('pk', 'title', 'content',)


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('pk', 'content',)


class OneLineCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = OneLineComment
        fields = ('pk', 'content',)


# 프로필에 영화 분석 -> 장르
class MovieMyListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ('id', 'title', 'genres', 'poster_path',)


# # following 목록
# class FollowListSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = user
#         fields = ('pk', 'followings',)


# 내 프로필 페이지(찜한 영화(포스터, 장르포함), 좋아요한 영화(포스터, 장르포함), 팔로잉 수, 팔로워 수, 리뷰, 한줄평, 댓글)
class MyProfileSerializer(serializers.ModelSerializer):
    # class MovieGenreserializer(serializers.ModelSerializer):

    #     class Meta:
    #         model = Genre
    #         fields = '__all__'

    # hate_genre = MovieGenreserializer(many=True, read_only=True)
    review_set = ReviewSerializer(many=True, read_only=True)
    review_count = serializers.IntegerField(source='review_set.count', read_only=True)
    comment_set = CommentSerializer(many=True, read_only=True)
    comment_count = serializers.IntegerField(source='comment_set.count', read_only=True)
    onelinecomment_set = OneLineCommentSerializer(many=True, read_only=True)
    onelinecomment_count = serializers.IntegerField(source='onelinecomment_set.count', read_only=True)
    save_movies = MovieMyListSerializer(many=True, read_only=True)
    like_movies = MovieMyListSerializer(many=True, read_only=True)
    followers_count = serializers.IntegerField(source='followers.count', read_only=True)
    followings_count = serializers.IntegerField(source='followings.count', read_only=True)
    save_movies_count = serializers.IntegerField(source='save_movies.count', read_only=True)
    like_movies_count = serializers.IntegerField(source='like_movies.count', read_only=True)

    class Meta:
        model = user
        fields = ('__all__')

# 남의 프로필 페이지(좋아요한 영화(포스터, 장르포함), 팔로잉 수, 팔로워 수, 리뷰, 한줄평)
class YourProfileSerializer(serializers.ModelSerializer):
    like_movies = MovieMyListSerializer(many=True, read_only=True)
    like_movies_count = serializers.IntegerField(source='like_movies.count', read_only=True)
    
    review_set = ReviewSerializer(many=True, read_only=True)
    review_count = serializers.IntegerField(source='review_set.count', read_only=True)
    onelinecomment_set = OneLineCommentSerializer(many=True, read_only=True)
    onelinecomment_count = serializers.IntegerField(source='onelinecomment_set.count', read_only=True)
    # followers = FollowListSerializer(many=True, read_only=True)
    # followers = ProfileListSerializer(many=True, read_only=True)
    
    followers_count = serializers.IntegerField(source='followers.count', read_only=True)
    followings_count = serializers.IntegerField(source='followings.count', read_only=True)

    class Meta:
        model = user
        fields  = ('__all__')


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class MovieGenreserializer(serializers.ModelSerializer):

        class Meta:
            model = Genre
            fields = '__all__'

    hate_genre = MovieGenreserializer(many=True, read_only=True)

    class Meta:
        model = user
        fields = ('pk', 'username', 'password', 'nickname','profile_img', 'hate_genre',)


class EditProfileSerializer(serializers.ModelSerializer):
    hate_genre = serializers.SlugRelatedField(many=True, read_only=True, slug_field='id')
    # hate_genre = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = user
        fields = ('pk', 'username', 'nickname', 'profile_img', 'hate_genre',)
        # depth = 2
        