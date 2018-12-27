from django.contrib import admin
from .models import ( Question , Answer , UserAnswer )
# Register your models here.

class AnswerTabularInline(admin.TabularInline):
	model = Answer

class QuestionModel(admin.ModelAdmin):
	inlines = [AnswerTabularInline]		
	class Meta:
		model = Question


admin.site.register(Question,QuestionModel)
admin.site.register(Answer)
admin.site.register(UserAnswer)