from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .serializers import MyProfileSerializer, YourProfileSerializer, UserSerializer, EditProfileSerializer


# postman으로 확인 못 함
@api_view(['GET'])
def profile(request, user_pk):
    user = get_object_or_404(get_user_model(), pk=user_pk)
    if request.user == user:  # 내 프로필
        serializer = MyProfileSerializer(user)
        return Response(serializer.data)
        
    else:  # 남의 프로필
        serializer = YourProfileSerializer(user)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    password = request.data.get('password')
    passwordConfirmation = request.data.get('passwordConfirmation')    
    if password != passwordConfirmation:
        return Response({ 'password': '비밀번호가 일치하지 않습니다.'})

    if len(password) < 8:
        return Response({ 'password': '비밀번호는 8자이상 입력하세요'})

    else:
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            user.set_password(request.data.get('password'))
            user.save()
            return Response(serializer.data)


@api_view(['PUT'])
def editprofile(request, user_pk):
    user = get_object_or_404(get_user_model(), pk=user_pk)
    if request.data['pk'] == user.pk:
    # if request.user == user:
        # serializer = EditProfileSerializer(instance=user, data=request.data, partial=True)
        # if serializer.is_valid(raise_exception=True):
        #     serializer.save()
        #     # 장르 id 입력 후 장르 이름도 나오도록 serializer 재설정
        #     serializer = UserSerializer(user)
            
        #     return Response(data=serializer.data, status=status.HTTP_200_OK)
        data = request.data
        hate_genres = data['hate_genre']
        user.hate_genre.clear()
        for genre in hate_genres:
            user.hate_genre.add(genre)
        # print(data.get('nickname'))
        if data.get('nickname'):
            user.nickname = data['nickname']
        user.save()
        serializer = UserSerializer(user)
            
        return Response(data=serializer.data, status=status.HTTP_200_OK)
        
    # 남의 회원정보 수정 권한 x / 유효하지 않은 값이면 400에러
    return Response(staus=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# def editprofiletwo(request):
#     print('?')
#     print(request.user)
#     print('?')
#     pass