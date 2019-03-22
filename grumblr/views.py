from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.db import transaction
from django.views.decorators.csrf import ensure_csrf_cookie
import datetime

from grumblr.models import *
from grumblr.forms import *
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
# Create your views here.
from django.utils import timezone
from django.urls import reverse

@login_required
@ensure_csrf_cookie  # Gives CSRF token for later requests.
def home(request):
    form = PostForm()
    posts = Post.objects.all().order_by('time').reverse()
    context = {'posts': posts, 'profile': get_object_or_404(Profile, user=request.user), 'user':request.user, 'form':form, 'max_time':datetime.datetime.now()}
    return render(request, 'grumblr/global.html', context)

@login_required
def follow_stream(request):
    form = PostForm()
    follows = request.user.followings.all()
    posts = Post.objects.filter(user__profile__in=follows)
    posts = posts.all().order_by('time').reverse()
    context = {'posts': posts, 'profile': get_object_or_404(Profile, user=request.user), 'user':request.user,  'form':form, 'max_time':datetime.datetime.now()}
    return render(request, 'grumblr/global.html', context)

@login_required
@transaction.atomic
def add_post(request):
    context = {}
    if request.method == 'GET':
        form = PostForm()
        return render(request, 'posts.json', context, content_type='application/json')
    else:
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = Post(content=form.cleaned_data['content'],user=request.user)
            new_post.save()

    posts = Post.objects.filter(id = new_post.id)
    context = {'posts': posts, 'last_modified': new_post.time }
    return render(request, 'posts.json', context, content_type='application/json')
    # max_time = Post.get_max_time()
    # posts = Post.objects.all().order_by('time').reverse()
    # context = {'form':form, 'posts': posts, 'user': request.user, 'profile': get_object_or_404(Profile, user=request.user)}
    # return render(request, 'grumblr/global.html', context)

@login_required
@transaction.atomic
def add_comment(request):
    context = {}
    if request.method == 'GET':
        form = PostForm()
        return render(request, 'posts.json', context, content_type='application/json')

    form = CommentForm(request.POST)

    if form.is_valid():
        post_id = form.cleaned_data['post_id']
        new_comment = Comment(content=form.cleaned_data['content'],user=request.user, post=get_object_or_404(Post, pk=post_id))

        new_comment.save()

    context = {'comment': new_comment}
    return render(request, 'comment.json', context, content_type='application/json')


# Returns all recent additions in the database, as JSON
@login_required
@transaction.atomic
def get_posts(request, last_modified="1970-01-01T00:00+00:00"):
    max_time = Post.get_max_time()
    # todo: validate input

    posts = Post.get_changes(last_modified).order_by('time')

    context = {"last_modified":max_time, "posts":posts}

    return render(request, 'posts.json', context, content_type='application/json')


@transaction.atomic
def register(request):
    context = {}
#    User.objects.all().delete()
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'grumblr/register.html', context)
    
    form = RegistrationForm(request.POST)
    context['form'] = form
    
    # Validates the form.
    if not form.is_valid():
        return render(request, 'grumblr/register.html', context)
    
    new_user = User.objects.create_user(username=form.cleaned_data['username'], first_name=form.cleaned_data['firstname'], 
                                        last_name=form.cleaned_data['lastname'], email = form.cleaned_data['email']
                                        , password=form.cleaned_data['password1'])
    new_user.is_active = False
    new_user.save()
    
    new_profile = Profile(user = new_user)
    new_profile.save()
    
    current_site = get_current_site(request)
    mail_subject = 'Activate your blog account.'
    message = render_to_string('grumblr/email_activation.html', {
                'user': new_user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(new_user.pk)).decode(),
                'token':default_token_generator.make_token(new_user),
            })
    to_email = new_user.email
    # send real email
#    email = EmailMessage(mail_subject, message, to=[to_email])
#    email.send()
    
    # pretend to send email
    send_mail(subject=mail_subject, message=message, from_email="leiyuqia@gmail.com", recipient_list=[to_email])

    return HttpResponse('A confirmarion email has been sent to activate your account. Please click the link in that email to complete the registration')   

@transaction.atomic
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = get_object_or_404(User, pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return render(request, 'grumblr/activation_complete.html', {})
    else:
        return HttpResponse('Activation link is invalid!')


@login_required
def profile(request, user_id):
    context = {}
    context['form'] = PostForm()
    user= get_object_or_404(User, id=user_id)
    posts = Post.objects.filter(user=user).order_by('time').reverse()
    context['posts'] = posts
    context['profile'] = get_object_or_404(Profile, user=user)
    if request.user.id == user_id:
        context['identity'] = True
    else:
        context['identity'] = False

    if request.user in context['profile'].followers.all():
        context['follow'] = True
    else:
        context['follow'] = False
        
    context['user'] = request.user
    return render(request, 'grumblr/profile.html', context)

@login_required
@transaction.atomic
def edit_profile(request):
    profile_to_edit = get_object_or_404(Profile, user = request.user)
    if request.method == 'GET':
        form = ProfileForm(instance = profile_to_edit)
        context = {'form':form}
        return render(request, 'grumblr/edit-profile.html', context)
    
    
    form = ProfileForm(data=request.POST, files=request.FILES, instance = profile_to_edit)
    if not form.is_valid():
        context = {'form':form}
        return render(request, 'grumblr/edit-profile.html', context)
    
    form.save()

    return redirect('profile', user_id = request.user.id)

@login_required
@transaction.atomic
def send_reset_password_email(request):
    user = request.user
    current_site = get_current_site(request)
    mail_subject = 'Reset password for your blog account.'
    message = render_to_string('grumblr/reset-password-email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token':default_token_generator.make_token(user),
            })
    to_email = user.email
    send_mail(subject=mail_subject, message=message, from_email="yuqil1@andrew.cmu.edu", recipient_list=[to_email])
    return HttpResponse('An email has been sent to your email address. Please click the link in that email to reset your password')
    
@transaction.atomic
def reset_password(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'GET':
            form = PasswordForm()
            return render(request, 'grumblr/reset_password.html', {'form': form})
    
        form = PasswordForm(request.POST)
#        user = request.user
        if not form.is_valid():
            return render(request, 'grumblr/reset_password.html', {'form': form})
        if not user.check_password(form.cleaned_data['old_password']):
            messages.error(request, 'Old password is not correct')
            return render(request, 'grumblr/reset_password.html', {'form': form})
        else:
            user.set_password(form.cleaned_data['new_password1'])
            user.save()
            update_session_auth_hash(request, user)
            return render(request, 'grumblr/reset_ps_complete.html', {})
    else:
        return HttpResponse('This link is invalid!')

@login_required
@transaction.atomic
def follow(request, user_id):
    """
    request.user follows the user of user_id
    """
    user2 = get_object_or_404(User, id=user_id)
    user2_profile = get_object_or_404(Profile, user=user2)
    user2_profile.followers.add(request.user)
    return redirect('profile', user_id = user_id)

@login_required
@transaction.atomic
def unfollow(request, user_id):
    user2 = get_object_or_404(User, id=user_id)
    user2_profile = get_object_or_404(Profile, user=user2)
    user2_profile.followers.remove(request.user)
    return redirect('profile', user_id = user_id)
    
        