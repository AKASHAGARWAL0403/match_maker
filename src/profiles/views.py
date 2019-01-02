from django.shortcuts import render , get_object_or_404 , redirect
from .models import Profile
from matches.models import Matches
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .forms import ( UserJobForm , UserForm )
from .models import UserJob
from django.forms import modelformset_factory
from django.contrib import messages
from likes.models import UserLike
# Create your views here.

User = get_user_model()


@login_required
def profile(request):
	user = get_object_or_404(User,username=request.user.username)
	profile,created = Profile.objects.get_or_create(user=request.user)
	user_job = user.userjob_set.all()
	context = {
		"profile" : profile,
		"jobs" : user_job,
	}
	return render(request,"profile/user_profile.html",context)



@login_required
def profile_edit(request):
	title = "UPDATE PROFILE"
	profile,created = Profile.objects.get_or_create(user=request.user)
	form = UserForm(request.POST or None , request.FILES or None , instance=profile )
	context = {
		"form" : form,
		"title" : title
	}

	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		instance.save()
		messages.success(request,"Your Profile was updated")

	return render(request,"forms.html",context)

@login_required
def profile_view(request,username):
	user = get_object_or_404(User,username=username)
	profile,created = Profile.objects.get_or_create(user=user)
	user_job = user.userjob_set.all()
	user_like  =  UserLike.objects.get_or_create(user=request.user)
	i_like = False
	if user in user_like[0].liked_user.all():
		i_like = True
	mutual_like = user_like[0].get_mutual_like(user)
	match,created = Matches.objects.get_or_create_match(user_a=request.user,user_b=user)
	context = {
		"profile" : profile,
		"match" : match,
		"jobs" : user_job,
		"mutual_like" : mutual_like,
		"i_like" : i_like
	}
	return render(request,"profile/profile_view.html",context)


@login_required
def job_create(request):
	title = "ADD JOB"
	form = UserJobForm(request.POST or None)
	context = {
		"form" : form,
		"title" : title
	}

	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		instance.save()

	return render(request,"forms.html",context)

@login_required
def job_edit(request):
	title ="UPDATES JOB"
	UserFormData = modelformset_factory(UserJob,form=UserJobForm)
	queryset = UserJob.objects.filter(user=request.user)
	formset = UserFormData(request.POST or None , queryset=queryset)
	context = {
		"formset" : formset,
		"title" : title
	}
	if formset.is_valid():
		instances = formset.save(commit=False)
		for instance in instances:
			instance.user = request.user
			instance.save()
		print("rgdsdfcecsgrdfsd")
		return redirect("user_profile")

	return render(request,"job/update.html",context)