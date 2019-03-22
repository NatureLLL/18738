from django.db import models
from django.db.models import Max
from django.contrib.auth.models import User
import datetime


# Create your models here.

class Post(models.Model):
	time = models.DateTimeField(auto_now_add=True)
	content = models.CharField(max_length=42)
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')

	def __str__(self):
		return self.content

	# Returns all recent additions to the posts
	@staticmethod
	def get_changes(time="1970-01-01T00:00+00:00"):
		return Post.objects.filter(time__gt=time).distinct()

	@staticmethod
	def get_max_time():
		return Post.objects.all().aggregate(Max('time'))['time__max'] or datetime.datetime(1970, 1, 1)


class Comment(models.Model):
	time = models.DateTimeField(auto_now_add=True)
	content = models.CharField(max_length=42)
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments_user')
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments_post')


class Profile(models.Model):
	user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
	avatar = models.ImageField(upload_to='images/%Y/%m/%d/', default='images/profile.png', blank=True)
	age = models.PositiveIntegerField(default=0)
	bio = models.CharField(max_length=42, default='')
	followers = models.ManyToManyField(User, related_name='followings', symmetrical=False)

	def get_followings(self):
		followings = self.user.followings.all()
		return followings
