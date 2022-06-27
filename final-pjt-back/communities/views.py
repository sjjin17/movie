from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Review, Comment
from movies.models import Movie
from .serializers import ReviewListSerializer, ReviewCreateSerializer, ReviewSerializer, CommentCreateSerializer, CommentListSerializer, ReviewLikeSerializer



# 리뷰 전체 보기
@api_view(['GET'])
def review_list(request):
    if request.method == 'GET':
        reviews = get_list_or_404(Review)
        serializer = ReviewListSerializer(reviews, many=True)
        return Response(serializer.data)


# 로그인 상태가 아니라서 확인은 못함
# 리뷰 생성
# 리뷰 생성 후 리뷰 전체보기 갱신(새로고침했을 때 다시 갱신할건지,, 아니면 그냥 생성된 것만 하는지)
@api_view(['POST'])
def review_create(request, movie_pk):
    serializer = ReviewCreateSerializer(data=request.data)
    movie = get_object_or_404(Movie, pk=movie_pk)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user, movie=movie)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_RUD(request, review_pk):
    # 리뷰 보기get, 수정put, delete
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == 'GET':
        serializer = ReviewSerializer(review)
        return Response(serializer.data)

    elif request.method == 'PUT':
        if request.user == review.user:  # 이 부분 주석처리 하면 postman 돌아감
            serializer = ReviewSerializer(instance=review, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)

    elif request.method == 'DELETE':
        if request.user == review.user:  # 이 부분 주석처리 하면 postman 돌아감
            review.delete()
            data = {
                'delete' : f'{review.user}가 쓰신 {review_pk}번 글이 삭제되었습니다.',
            }
            return Response(data, status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def like_article(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    user = request.user
    if review.like_users.filter(pk=user.pk).exists():
        review.like_users.remove(user)
        serializer = ReviewLikeSerializer(review)
        return Response(serializer.data)
    else:
        review.like_users.add(user)
        serializer = ReviewLikeSerializer(review)
        return Response(serializer.data)



# 댓글 생성
@api_view(['POST'])
def comment_create(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    serializer = CommentCreateSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user, review=review)
        # 리뷰 작성 후 리뷰 전체 보기
        comments = review.comment_set.all()  # 이 리뷰의 모든 댓글들
        serializer = CommentListSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    


@api_view(['PUT', 'DELETE'])
def comment_UD(request, review_pk, comment_pk):
    review = get_object_or_404(Review, pk=review_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.method == 'PUT':
        if request.user == comment.user: # 이거 주석처리하면 잘 돌아감
            serializer = CommentListSerializer(instance=comment, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                # 댓글 수정 후 review_pk 리뷰의 댓글 전체 보기
                comments = review.comment_set.all()  # 이 리뷰의 모든 댓글들
                serializer = CommentListSerializer(comments, many=True)
                return Response(serializer.data)

    elif request.method == 'DELETE':
        if request.user == comment.user:  # 이거 주석처리하면 잘 돌아감
            comment.delete()
            # 댓글 수정 후 review_pk 리뷰의 댓글 전체 보기
            comments = review.comment_set.all()  # 이 리뷰의 모든 댓글들
            serializer = CommentListSerializer(comments, many=True)
            return Response(serializer.data)



