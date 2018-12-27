from django.shortcuts import render , get_object_or_404 , redirect
from .models import UserLike
from django.contrib.auth import get_user_model
from django.urls import reverse

# Create your views here.

User  = get_user_model()

def like_unlike_view(request,id):
	to_like_unlike = get_object_or_404(User,id=id)
	profile , created = UserLike.objects.get_or_create(user = request.user)
	#profile.liked_user.add(to_like_unlike)
	if to_like_unlike in profile.liked_user.all():
		print(profile.liked_user.all(),"SDAfsasa")
		profile.liked_user.remove(to_like_unlike)
	else:
		print("Dsfadsa")
		profile.liked_user.add(to_like_unlike)

	return redirect("profile",username=to_like_unlike.username)


