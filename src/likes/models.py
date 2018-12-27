from django.db import models
from django.conf import settings
# Create your models here.

User = settings.AUTH_USER_MODEL

class UserLikeManager(models.Manager):
	def get_all_mutual_like(self,user):
		try:
			user_liked =  user.liker.liked_user.all()
		except:
			user_liked = []
		mutual_like = []
		for like in user_liked:
			try:
				if like.liker.get_mutual_like(user):
					mutual_like.append(like)
			except:
				pass
		return mutual_like

class UserLike(models.Model):
	user = models.OneToOneField(User,related_name="liker",on_delete=models.CASCADE)
	liked_user = models.ManyToManyField(User,related_name="liked_user",blank=True)

	objects = UserLikeManager()

	def __str__(self):
		return self.user.username

	def get_mutual_like(self,user):
		i_like = False
		user_like = False

		if user in self.liked_user.all():
			i_like = True

		user_liked = UserLike.objects.get_or_create(user=user)
		if self.user in user_liked[0].liked_user.all():
			user_like = True

		if i_like and user_like:
			return True
		return False

#from django.contrib.auth import get_user_model
#User  = get_user_model()
#user_a  = User.objects.get(username="aka")
#from likes.models import UserLike
#like_aka  = UserLike.objects.get_all_mutual_like(user_a)