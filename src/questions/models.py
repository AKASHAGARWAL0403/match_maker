from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save
# Create your models here.

class Question(models.Model):
	text = models.TextField()
	active = models.BooleanField(default=True)
	draft = models.BooleanField(default=False)
	timestamp = models.DateTimeField(auto_now = False , auto_now_add = True)

	def __str__(self):
		return self.text[:10]

class Answer(models.Model):
	question = models.ForeignKey(Question,on_delete=models.CASCADE)
	text = models.TextField()
	active = models.BooleanField(default=True)
	draft = models.BooleanField(default=False)
	timestamp = models.DateTimeField(auto_now = False , auto_now_add = True)

	def __str__(self):
		return self.text[:10]

LEVELS = (
			('Mandatory', 'Mandatory'), 
			('Very Important', 'Very Important'),
			('Somewhat Important', 'Somewhat Important'),
			('Not Important','Not Important'),
		)

class UserAnswer(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	question = models.ForeignKey(Question,on_delete=models.CASCADE)
	my_answer = models.ForeignKey(Answer,on_delete=models.CASCADE,related_name="my_answer")
	my_answer_importance = models.CharField(max_length=50,choices=LEVELS)
	input_point = models.IntegerField(default=-1)
	there_answer = models.ForeignKey(Answer,on_delete=models.CASCADE,related_name="match_answer",null=True,blank=True)
	there_answer_importance = models.CharField(max_length=50,choices=LEVELS)
	there_input_point = models.IntegerField(default=-1)
	timestamp = models.DateTimeField(auto_now = False , auto_now_add = True)

def input_value(importance_field):
	if importance_field == 'Mandatory':
		return 300
	elif importance_field == 'Very Important':
		return 200
	elif importance_field == 'Somewhat Important':
		return 100
	elif importance_field == 'Not Important':
		return 0
	else:
		return 0


def pre_save_set_point(sender,instance,*args,**kwargs):
	my_point = input_value(instance.my_answer_importance)
	there_point = input_value(instance.there_answer_importance)
	instance.input_point = my_point
	instance.there_input_point = there_point

pre_save.connect(pre_save_set_point,sender=UserAnswer)

