from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import UserText, UserFile


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if not username or not password:
        return Response({'error': 'Username and password are required'}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username is already taken'}, status=400)

    user = User.objects.create(username=username, password=make_password(password))
    return Response({'message': 'User created successfully'})


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)

    if user is None:
        return Response({'error': 'Invalid credentials'}, status=400)

    refresh = RefreshToken.for_user(user)
    return Response({'refresh': str(refresh), 'access': str(refresh.access_token)})


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def user_text(request):
    if request.method == 'GET':
        user_text, _ = UserText.objects.get_or_create(user=request.user)
        return Response({'text': user_text.text})
    else:  # POST
        text = request.data.get('text')
        user_text, _ = UserText.objects.get_or_create(user=request.user)
        user_text.text = text
        user_text.save()
        return Response({'message': 'Text saved successfully'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_file(request):
    file = request.FILES.get('file')
    if not file:
        return Response({'message': 'No file provided'}, status=400)

    user_file = UserFile(user=request.user, file=file)
    user_file.save()
    return Response({'message': 'File uploaded successfully'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_files(request):
    files = UserFile.objects.filter(user=request.user)
    return Response({'files': [file.file.name for file in files]})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def download_file(request):
    file_name = request.data.get('file_name')
    user_file = UserFile.objects.filter(user=request.user, file=file_name).first()
    if not user_file:
        return Response({'message': 'File not found'}, status=404)

    response = HttpResponse(user_file.file, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{user_file.file.name}"'
    return response


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_file(request):
    file_name = request.data.get('file_name')
    user_file = UserFile.objects.filter(user=request.user, file=file_name).first()

    if not user_file:
        return Response({'message': 'File not found'}, status=404)

    # 删除文件系统中的文件
    if user_file.file:
        user_file.file.delete()

    # 删除数据库中的记录
    user_file.delete()
    return Response({'message': 'File deleted successfully'})


def view_404(request):
    # 直接返回404json
    return Response({'message': '404 Not Found'}, status=404)


def register_page(request):
    return render(request, 'register.html')


def login_page(request):
    return render(request, 'login.html')


def text_page(request):
    return render(request, 'index.html')
