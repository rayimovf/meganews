from django.urls import path
from .views import get_category, get_banner, lasts_post, lasts_videos, single_post, get_tag, single_category, get_about, \
    get_information, get_team, create_contact, send_post, create_post_video, saved_post, update_profile, get_popular

urlpatterns = [
    path('get-category/', get_category, name='get-category'),
    path('get-banner/', get_banner, name='get-banner'),
    path('lasts-post/', lasts_post, name='lasts-post'),
    path('lasts-videos/', lasts_videos, name='lasts'),
    path('single-post/<int:pk>/', single_post, name='single-post'),
    path('get-tag/', get_tag, name='get-tag'),
    path('single-category/<int:pk>/', single_category, name='single-category'),
    path('get-about/', get_about, name='get-about'),
    path('get-information/', get_information, name='get-information'),
    path('get-team/', get_team, name='get-team'),
    path('create-contact/', create_contact, name='create-contact'),
    path('send-post/', send_post, name='send-post'),
    path('create-post-video/', create_post_video, name='create'),
    path('saved-post/', saved_post, name='saved-post'),
    path('get-popular/', get_popular, name='get-popular'),
    path('update-profile/<int:pk>/', update_profile, name='update-profile')
]
