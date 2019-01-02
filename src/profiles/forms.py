from django import forms

from .models import ( UserJob , Profile )

class UserJobForm(forms.ModelForm):
	class Meta:
		model = UserJob
		fields = [
			'position',
			'location',
			'employer_name'
		]

class UserForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = [
			'location',
			'picture'
		]
