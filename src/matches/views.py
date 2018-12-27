from django.shortcuts import render
from jobs.models import Job,Location,Employer

def position_match_view(request,slug):
	try:
		instance = Job.objects.get(slug=slug)
	except Job.MultipleObjectsReturned:
		queryset = Job.objects.filter(slug=slug).order_by('-id')
		instance = queryset[0]
	except Job.DoesNotExist:
		raise Http404

	template = "matches/position_match.html"
	context = {
		"instance": instance,
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
	context = {
		"instance": instance,
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
	context = {
		"instance": instance,
	}
	return render(request, template, context)