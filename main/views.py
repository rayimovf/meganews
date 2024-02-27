from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination

from .models import Category, Banner, Profile, About, Information, Team, Contact, Tags, Post, PostVideos, SavedPost
from .serializer import CategorySerializer, BannerSerializer, AboutSerializer, InformationSerializer, \
    TeamSerializer, ContactSerializer, TagsSerializer, PostSerializer, PostVideosSerializer, SavedPostSerializer


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 100


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


@api_view(['GET'])
def get_category(request):
    category = Category.objects.all()
    ser_data = CategorySerializer(category, many=True).data
    return Response(ser_data)


@api_view(['GET'])
def get_banner(request):
    banner = Banner.objects.all().order_by('-id')[:3]
    ser_data = BannerSerializer(banner, many=True).data
    return Response(ser_data)


@api_view(['GET'])
def lasts_post(request):
    post = Post.objects.all().order_by('-id')[:6]
    ser_data = PostSerializer(post, many=True).data
    return Response(ser_data)


@api_view(['GET'])
def lasts_videos(request):
    video = PostVideos.objects.all().order_by('-id')[:2]
    ser_data = PostVideosSerializer(video, many=True).data
    return Response(ser_data)


@api_view(['GET'])
def single_post(request, pk):
    post = Post.objects.get(id=pk)
    post.viewed += 1
    post.save()
    category_id = post.category.id
    category = Post.objects.filter(category_id=category_id)
    context = {
        'post': PostSerializer(post).data,
        'category': PostSerializer(category, many=True).data
    }
    print(post.viewed)
    return Response(context)


@api_view(['GET'])
def get_tag(request):
    tags = Tags.objects.all()
    ser_data = TagsSerializer(tags, many=True).data
    return Response(ser_data)
    

@api_view(['GET'])
def single_category(request, pk):
    post = Post.objects.filter(category_id=pk)
    pagination_class = LargeResultsSetPagination
    paginator = pagination_class()
    result_page = paginator.paginate_queryset(post, request)
    ser_data = PostSerializer(result_page, many=True).data
    return paginator.get_paginated_response(ser_data)


@api_view(['GET'])
def get_about(request):
    about = About.objects.last()
    ser_data = AboutSerializer(about).data
    return Response(ser_data)


@api_view(['GET'])
def get_information(request):
    information = Information.objects.last()
    ser_data = InformationSerializer(information).data
    return Response(ser_data)


@api_view(['GET'])
def get_team(request):
    team = Team.objects.all().order_by('-id')[:6]
    ser_data = TeamSerializer(team, many=True).data
    return Response(ser_data)


@api_view(['POST'])
def create_contact(request):
    try:
        subject = request.POST.get('subject')
        name = request.POST.get('name')
        email = request.POST.get('email')
        explanation = request.POST.get('explanation')
        if request.FILES.get('file'):
            file = request.FILES.get('file')
        contact = Contact.objects.create(subject=subject, name=name, email=email, explanation=explanation, file=file)
        contact.save()
        sta = status.HTTP_201_CREATED
        data = {
            'success': True,
            'contact': ContactSerializer(contact).data,
        }
    except Exception as e:
        data = {
            'success': False,
            'error': f'{e}'
        }
        sta = status.HTTP_500_INTERNAL_SERVER_ERROR
    return Response(data, sta)


@api_view(['POST'])
def send_post(request):
    try:
        title = request.POST.get('title')
        text = request.POST.get('text')
        img = request.FILES.get('img')
        date = request.POST.get('date')
        tags = Tags.objects.get(id=request.POST.get('tag_id'))
        category = Category.objects.get(id=request.POST.get('category_id'))
        author = Profile.objects.get(id=request.POST.get('author_id'))
        post = Post.objects.create(
            title=title,
            text=text,
            img=img,
            date=date,
            category=category,
            author=author,
        )
        post.tags.add(tags)
        post.save()
        sta = status.HTTP_201_CREATED
        data = {
            'success': True,
            'post': PostSerializer(post).data,
        }
    except Exception as e:
        data = {
            'success': False,
            'error': f'{e}'
        }
        sta = status.HTTP_500_INTERNAL_SERVER_ERROR
    return Response(data, sta)


@api_view(['POST'])
def create_post_video(request):
    try:
        title = request.POST.get('title')
        text = request.POST.get('text')
        date = request.POST.get('date')
        tags = Tags.objects.get(id=request.POST.get('tag_id'))
        video = request.POST.get('video')
        author = Profile.objects.get(id=request.POST.get('author_id'))
        post_video = PostVideos.objects.create(
            title=title,
            text=text,
            date=date,
            video=video,
            author=author,
        )
        post_video.tags.add(tags)
        post_video.save()
        sta = status.HTTP_201_CREATED
        data = {
            'success': True,
            'post': PostVideosSerializer(post_video).data,
        }
    except Exception as e:
        data = {
            'success': False,
            'error': f'{e}'
        }
        sta = status.HTTP_500_INTERNAL_SERVER_ERROR
    return Response(data, sta)


@api_view(['POST'])
def saved_post(request):
    try:
        profile = Profile.objects.get(id=request.POST.get('author_id'))
        post = Post.objects.get(id=request.POST.get('post_id'))
        saved_post = SavedPost.objects.create(profile=profile)
        saved_post.post.add(post)
        saved_post.save()
        data = {
            'success': True,
            'message': SavedPostSerializer(saved_post).data
        }
        sta = status.HTTP_201_CREATED
    except Exception as e:
        sta = status.HTTP_500_INTERNAL_SERVER_ERROR
        data = {
            'success': False,
            'error': f'{e}'
        }
    return Response(data, sta)


@api_view(['GET'])
def get_top(request):
    top_post = SavedPost.objects.all()
    ser = SavedPostSerializer(top_post, many=True)
    sta = status.HTTP_200_OK
    return Response(ser.data, sta)


@api_view(['GET'])
def get_trendy(request):
    top_post = SavedPost.objects.all()
    ser = SavedPostSerializer(top_post, many=True)
    sta = status.HTTP_200_OK
    return Response(ser.data, sta)


@api_view(['GET'])
def get_popular(request):
    popular_post = Post.objects.all().order_by('-viewed')
    ser_data = PostSerializer(popular_post, many=True).data
    return Response(ser_data, status.HTTP_200_OK)


@api_view(['PATCH'])
def update_profile(request, pk):
    try:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        username = request.POST.get('username')
        banner = request.FILES.get('banner')
        explanation = request.POST.get('explanation')
        img = request.FILES.get('img')
        old_password = request.POST.get('old_password')
        profile = Profile.objects.get(pk=pk)
        if old_password == profile.password:
            if first_name:
                profile.first_name = first_name
            if last_name:
                profile.last_name = last_name
            if email:
                profile.email = email
            if password:
                profile.password = password
            if username:
                profile.username = username
            if banner:
                profile.banner = banner
            if explanation:
                profile.explanation = explanation
            if img:
                profile.img = img
            profile.save()
            data = {
                'success': True,
            }
        else:
            data = {
                'success': False,
                'message': 'invalid password'
            }
    except Exception as e:
        data = {
            'success': True,
            'error': f'{e}'
        }
    return Response(data)