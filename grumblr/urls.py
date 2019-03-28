from django.urls import path
import django.contrib.auth.views
from django.conf.urls import url
from django.conf import settings
import grumblr.views


urlpatterns = [
        path('', grumblr.views.home),
        path('login', django.contrib.auth.views.LoginView.as_view(redirect_authenticated_user=True),{'template_name': 'grumblr/login.html'}, name='login'),
        path('logout',  django.contrib.auth.views.LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
        path('register', grumblr.views.register, name='register'),
        path('global', grumblr.views.home, name='home'),
        path('add-post', grumblr.views.add_post, name='add'),
        path('add-comment', grumblr.views.add_comment, name = 'comment'),
        path('get-posts', grumblr.views.get_posts, name = 'get-posts'),
        url(r'^get-posts/(?P<last_modified>.+)$', grumblr.views.get_posts, name = 'get-posts'),
        path('profile/<int:user_id>', grumblr.views.profile, name='profile'), 
        path('edit-profile', grumblr.views.edit_profile, name='edit_profile'), 
        path('send-reset-password-email', grumblr.views.send_reset_password_email, name='send_reset_password_email'),
        path('follow/<int:user_id>', grumblr.views.follow, name = 'follow'),
        path('unfollow/<int:user_id>', grumblr.views.unfollow, name = 'unfollow'),
        path('following_stream', grumblr.views.follow_stream, name = 'following_stream'),
        path('statistics', grumblr.views.get_statistics, name = 'statistics'),
        path('indiv_statistics', grumblr.views.get_indiv_statistics, name = 'indiv_statistics'),
        path('fake_data', grumblr.views.fake_data, name = 'fake_data'),
        path('reset_data', grumblr.views.reset_data, name = 'reset_data'),
path('get_data', grumblr.views.get_data, name = 'get_data'),
        # path('make_comment', grumblr.views.make_comment, name = 'make-comment'),
        
    ]