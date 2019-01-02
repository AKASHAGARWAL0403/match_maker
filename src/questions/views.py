from django.shortcuts import render , get_object_or_404 , redirect
# Create your views here.
from .forms import UserAnswerForm
from .models import ( Question,Answer,UserAnswer )
from django.contrib import messages
from matches.signal import user_matches_update

def home(request):
	queryset = Question.objects.all()
	instance = queryset.first()
	form = UserAnswerForm(request.POST or None)
	if form.is_valid():
		print(form.cleaned_data)
		question_id = form.cleaned_data.get("question_id")
		answer_id = form.cleaned_data.get("answer_id")
		question_ins = Question.objects.get(id=question_id)
		answer_ins = Answer.objects.get(id=answer_id)
		#rand = Question.objects.all().order_by("?").first()
		return redirect("question")
	context = {
		"instance" : instance,
		"form" : form
	}
	#print(instance.cleaned_data)
	return render(request,"question/home.html",context)


def single(request,id=None):
	if request.user.is_authenticated:
		form = UserAnswerForm(request.POST or None)
		instance = get_object_or_404(Question,id=id)
		try:
			new_user = UserAnswer.objects.get(user=request.user,question=instance)
			updated_q = True
		except UserAnswer.DoesNotExist:
			new_user = UserAnswer()
			updated_q = False
		except UserAnswer.MultipleObjectsReturned:
			new_user = UserAnswer.objects.get(user=request.user,question=instance).first()
			updated_q = True
		except:
			new_user = UserAnswer()
			updated_q = False
		if form.is_valid():
			print(form.cleaned_data)
			question_id = form.cleaned_data.get("question_id")
			answer_id = form.cleaned_data.get("answer_id")
			answer_id_importance = form.cleaned_data.get("importance_level")
			there_answer_id = form.cleaned_data.get("there_answer_id")
			there_answer_id_importace = form.cleaned_data.get("there_importance_level")

			question_ins = Question.objects.get(id=question_id)
			answer_ins = Answer.objects.get(id=answer_id)

			#new_user = UserAnswer()
			new_user.question = question_ins
			new_user.my_answer = answer_ins
			new_user.my_answer_importance = answer_id_importance
			new_user.user = request.user
			if there_answer_id != -1:
				there_answer_ins = Answer.objects.get(id=there_answer_id)
				new_user.there_answer = there_answer_ins
				new_user.there_answer_importance = there_answer_id_importace
			else:
				new_user.there_answer = None
				new_user.there_answer_importance = "Not Important"
			new_user.save()

			if updated_q:
				messages.success(request,"Your answer was updated successfully")
			else:
				messages.success(request,"Your answer was saved successfully")

			user_matches_update.send(user=request.user, sender=new_user.__class__)

			rand = Question.objects.get_unanswered(request.user).order_by("?")
			if rand.count() > 0:
				rand_instance = rand.first()
				return redirect("question_single" , id=rand_instance.id)
			else:
				return redirect("home")
		context = {
			"instance" : instance,
			"form" : form,
			"new_user" : new_user
		}
		#print(instance.cleaned_data)
		return render(request,"question/single.html",context)