from django.shortcuts import render
from jobs.models import Job,Location,Employer
from .models import (PositionMatch , LocationMatch , EmployerMatch  , Matches)
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.contrib.auth import get_user_model 
from profiles.models import Profile


User = get_user_model()

@receiver(user_logged_in)
def get_user_match_reciever(sender,request,user,*args,**kwargs):
	for u in User.objects.exclude(username=user):
		Matches.objects.get_or_create_match(user_a=user,user_b=u)
	Profile.objects.get_or_create(user=user)

def position_match_view(request,slug):
	try:
		instance = Job.objects.get(slug=slug)
	except Job.MultipleObjectsReturned:
		queryset = Job.objects.filter(slug=slug).order_by('-id')
		instance = queryset[0]
	except Job.DoesNotExist:
		raise Http404

	template = "matches/position_match.html"
	matches = PositionMatch.objects.filter(job__text__iexact=instance.text).exclude(user=request.user)
	context = {
		"instance": instance,
		"matches" : matches
	}
	return render(request, template, context)

def location_match_view(request,slug):
	try:
		instance = Location.objects.get(slug=slug)
	except Location.MultipleObjectsReturned:
		queryset = Job.objects.filter(slug=slug).order_by('-id')
		instance = queryset[0]
	except Location.DoesNotExist:
		raise Http404

	template = "matches/location_match.html"
	matches = LocationMatch.objects.filter(location__name__iexact=instance.name).exclude(user=request.user)
	context = {
		"instance": instance,
		"matches" : matches
	}
	return render(request, template, context)

def employer_match_view(request,slug):
	try:
		instance = Employer.objects.get(slug=slug)
	except Employer.MultipleObjectsReturned:
		queryset = Employer.objects.filter(slug=slug).order_by('-id')
		instance = queryset[0]
	except Employer.DoesNotExist:
		raise Http404

	template = "matches/employer_match.html"
	matches = EmployerMatch.objects.filter(employer__name__iexact=instance.name).exclude(user=request.user)
	context = {
		"instance": instance,
		"matches" : matches
	}
	return render(request, template, context)