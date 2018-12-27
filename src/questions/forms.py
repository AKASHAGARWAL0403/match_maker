from django import forms

from .models import ( LEVELS , Question , Answer )

class UserAnswerForm(forms.Form):
	question_id = forms.IntegerField()
	answer_id = forms.IntegerField()
	importance_level = forms.ChoiceField(choices=LEVELS)
	there_answer_id = forms.IntegerField()
	there_importance_level = forms.ChoiceField(choices=LEVELS)


	def clean_question_id(self):
		my_question = self.cleaned_data.get('question_id')
		try:
			ques_obj = Question.objects.get(id=my_question)
		except:
			raise forms.ValidationError("There was a problem with the question")
		return my_question


	def clean_answer_id(self):
		my_answer = self.cleaned_data.get('answer_id')
		try:
			ans_obj = Answer.objects.get(id=my_answer)
		except:
			raise forms.ValidationError("There was a problem with your answer")
		return my_answer

	def clean_there_answer_id(self):
		there_answer = self.cleaned_data.get('there_answer_id')
		try:
			ans_obj = Answer.objects.get(id=there_answer)
		except:
			if there_answer == -1:
				return there_answer
			else:
				raise forms.ValidationError("There was a problem with your answer")
		return there_answer	