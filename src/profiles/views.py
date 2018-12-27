from django.shortcuts import render , get_object_or_404
from .models import Profile
from matches.models import Matches
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .forms import UserJobForm
from .models import UserJob
from django.forms import modelformset_factory
# Create your views here.

User = get_user_model()

@login_required
def profile_view(request,username):
	user = get_object_or_404(User,username=username)
	profile,created = Profile.objects.get_or_create(user=user)
	user_job = user.userjob_set.all()
	match,created = Matches.objects.get_or_create_match(user_a=request.user,user_b=user)
	context = {
		"profile" : profile,
		"match" : match,
		"jobs" : user_job
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

	return render(request,"job/update.html",context)