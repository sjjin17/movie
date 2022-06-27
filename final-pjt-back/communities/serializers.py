from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Review, Comment
from movies.models import Movie


User = get_user_model()

class MovieSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Movie
        fields = ('pk', 'title',)

# 리뷰 전체 보기(별점, 제목, 작성자, 작성시간, 좋아요 수)
class ReviewListSerializer(serializers.ModelSerializer):


    class UserSerializer(serializers.ModelSerializer):
        
        class Meta:
            model = User
            fields = ('pk', 'username', 'nickname',)
    

    # 작성자 id, username, nickname 출력
    user = UserSerializer(read_only=True)
    
    # like_users = UserSerializer(read_only=True, many=True) (누구인지 까지 뽑아내는 값)

    # 좋아요 수
    like_users_count = serializers.IntegerField(source='like_users.count', read_only=True)
    
    movie = MovieSerializer(read_only=True)

    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    
    class Meta:
        model = Review
        fields = ('pk', 'star_rate', 'title', 'user', 'created_at', 'updated_at', 'like_users_count', 'movie',)



# 리뷰 생성
class ReviewCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ('title', 'content', 'star_rate',)





# 리뷰 상세 페이지(별점, 리뷰제목, 작성자, 작성시간, 수정시간, 좋아요 수, 좋아요 기능, 댓글들(댓글내용, 댓글 작성자), 댓글수, )
class ReviewSerializer(serializers.ModelSerializer):

    # 작성자 닉네임까지 보이도록
    class UserSerializer(serializers.ModelSerializer):
        
        class Meta:
            model = User
            fields = ('pk', 'username', 'nickname')
    
    class MovieDetailSerializer(serializers.ModelSerializer):
    
        class Meta:
            model = Movie
            fields = ('pk', 'title', 'poster_path',)

    # 모든 댓글 추가를 위해(작성자, 내용, 수정시간 등등)
    class CommentSerializer(serializers.ModelSerializer):
        
        # 댓글 작성자 닉네임 보이기 위해
        class UserSerializer(serializers.ModelSerializer):
            
            class Meta:
                model = User
                fields = ('pk', 'username', 'nickname')
        
        user = UserSerializer(read_only=True)
        created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
        updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

        class Meta:
            model = Comment
            fields = ('pk', 'content', 'user', 'created_at', 'updated_at', 'review',)

    user = UserSerializer(read_only=True)
    # 좋아요 누른 사람들 -> 좋아요 기능을 위해
    like_users = UserSerializer(read_only=True, many=True)
    # 좋아요 수
    like_users_count = serializers.IntegerField(source='like_users.count', read_only=True)
    # 모든 댓글(comment_set 이름 바꾸면 조회 안 됨)
    comment_set = CommentSerializer(read_only=True, many=True)
    # 댓글 수
    comments_count = serializers.IntegerField(source='comment_set.count', read_only=True)
    
    # created_at = serializers.DateTimeField()
    # updated_at = serializers.DateTimeField()

    movie = MovieDetailSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ('pk', 'star_rate', 'title', 'content', 'user', 'created_at', 'updated_at', 'like_users', 'like_users_count', 'comment_set', 'comments_count', 'movie',)


# 댓글 작성
class CommentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('pk', 'content')


# 댓글 작성, 편집, 삭제 후 전체댓글 조회 + 댓글 수정
class CommentListSerializer(serializers.ModelSerializer):
    
    # 댓글 작성자 닉네임 보이기 위해
    class UserSerializer(serializers.ModelSerializer):
        
        class Meta:
            model = User
            fields = ('pk', 'username', 'nickname')
    
    user = UserSerializer(read_only=True)
    
    
    # 댓글 내용, 작성자, 작성시간, 수정시간
    class Meta:
        model = Comment
        fields = ('pk', 'content', 'user', 'created_at', 'updated_at', 'review',)
        read_only_fields = ('review',)


class ReviewLikeSerializer(serializers.ModelSerializer):
    
    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('pk', 'username')

    user = UserSerializer(read_only=True)
    like_users = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Review
        fields = ('pk', 'user', 'title', 'content', 'like_users')