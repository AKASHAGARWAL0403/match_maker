from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from questions.models import Question
from newsletter.forms import ContactForm, SignUpForm
from newsletter.models import SignUp
from matches.models import ( Matches , LocationMatch , PositionMatch , EmployerMatch )
from questions.models import Question
from jobs.models import ( Job , Employer , Location)
from django.contrib.auth import get_user_model
from likes.models import UserLike
User = get_user_model()

# Create your views here.
def home(request):
	if request.user.is_authenticated:
		for u in User.objects.exclude(username=request.user):
			Matches.objects.get_or_create_match(user_a=request.user,user_b=u)
		matches = Matches.objects.get_queryset_with_percent(request.user)[:6]
		if matches:
			if matches[0][1] == "0.00%":
				matches = []
		position = PositionMatch.objects.filter(user = request.user)[:6]
		employer = EmployerMatch.objects.filter(user = request.user)[:6]
		location = LocationMatch.objects.filter(user = request.user)[:6]
		mutual_likes = UserLike.objects.get_all_mutual_like(request.user)[:4]
		context = {
			"matches": matches,
			"positions" : position,
			"employers" : employer,
			"locations" : location,
			"mutual_likes" : mutual_likes
		}

		return render(request,"dashboard/home.html",context)
	context = {

	}

	return render(request, "home.html", context)