from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from questions.models import Question
from .forms import ContactForm, SignUpForm
from .models import SignUp
from matches.models import ( Matches , LocationMatch , PositionMatch , EmployerMatch )
from questions.models import Question
from jobs.models import ( Job , Employer , Location)
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.
def home(request):
	title = 'Sign Up Now'
	form = SignUpForm(request.POST or None)
	context = {
		"title": title,
		"form": form
	}
	if form.is_valid():
		#form.save()
		#print request.POST['email'] #not recommended
		instance = form.save(commit=False)

		full_name = form.cleaned_data.get("full_name")
		if not full_name:
			full_name = "New full name"
		instance.full_name = full_name
		instance.save()
		context = {
			"title": "Thank you"
		}

	if request.user.is_authenticated:
		matches = Matches.objects.get_queryset_with_percent(request.user)[:6]
		for u in User.objects.exclude(username=request.user):
			Matches.objects.get_or_create_match(user_a=request.user,user_b=u)
		#PositionMatch.objects.update_matches(request.user,20)
		position = PositionMatch.objects.filter(user = request.user)[:6]
		employer = EmployerMatch.objects.filter(user = request.user)[:6]
		location = LocationMatch.objects.filter(user = request.user)[:6]
		queryset = Question.objects.all().order_by('-timestamp') 
		print(location , employer , position)
		context = {
			"queryset": queryset,
			"matches": matches,
			"positions" : position,
			"employers" : employer,
			"locations" : location 
		}

		return render(request,"question/home.html",context)
		

	return render(request, "home.html", context)



def contact(request):
	title = 'Contact Us'
	title_align_center = True
	form = ContactForm(request.POST or None)
	if form.is_valid():
		# for key, value in form.cleaned_data.iteritems():
		# 	print key, value
		# 	#print form.cleaned_data.get(key)
		form_email = form.cleaned_data.get("email")
		form_message = form.cleaned_data.get("message")
		form_full_name = form.cleaned_data.get("full_name")
		# print email, message, full_name
		subject = 'Site contact form'
		from_email = settings.EMAIL_HOST_USER
		to_email = [from_email, 'youotheremail@email.com']
		contact_message = "%s: %s via %s"%( 
				form_full_name, 
				form_message, 
				form_email)
		some_html_message = """
		<h1>hello</h1>
		"""
		send_mail(subject, 
				contact_message, 
				from_email, 
				to_email, 
				html_message=some_html_message,
				fail_silently=True)

	context = {
		"form": form,
		"title": title,
		"title_align_center": title_align_center,
	}
	return render(request, "forms.html", context)
















