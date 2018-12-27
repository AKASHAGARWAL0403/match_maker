import datetime
from decimal import Decimal
from django.utils import timezone
from django.db import models
from django.conf import settings
from .utils import get_match
from django.urls import reverse
from jobs.models import ( Job , Location , Employer)
# Create your models here.


class MatchUser(models.query.QuerySet):
	def matches(self,user):
		q1 = self.filter(user_a = user).exclude(user_b=user)
		q2 = self.filter(user_b = user).exclude(user_a=user)
		return (q1 | q2).distinct()


class MatchesManager(models.Manager):

	def get_queryset(self):
		return MatchUser(self.model,using=self._db)

	def get_or_create_match(self,user_a=None,user_b=None):
		try:
			obj1 = self.get(user_a=user_a,user_b=user_b)
		except:
			obj1 = None
		try:
			obj2 = self.get(user_a=user_b,user_b=user_a)
		except:
			obj2 = None
		if obj1 and not obj2:
			obj1.check_update()
			return obj1,False
		elif not obj1 and obj2:
			obj2.check_update()
			return obj2,False
		elif obj1 and obj2:
			obj1.check_update()
			return obj1,False			
		else:
			print(user_a.username,user_b.username,"dfsdasa")
			new_obj = Matches()
			new_obj.user_b = user_b
			new_obj.user_a = user_a
			#match_percent,ques = get_match(user_a,user_b)
			new_obj.do_match()
			return new_obj,True

	def update_all(self):
		queryset = self.all()
		now = timezone.now()
		offset = now - datetime.timedelta(hours=36)
		offset2 = now - datetime.timedelta(hours=12)
		queryset = queryset.filter(updated__gt=offset).filter(updated__lte=offset2)
		if queryset.count > 0:
			for i in queryset:
				i.check_update()

	def matches_all(self,user):
		return self.get_queryset().matches(user)

	def get_queryset_with_percent(self,user):
		matches = []
		match_set = self.matches_all(user).order_by('-match_percent')
		for match in match_set:
			if match.user_a == user:
				items_wanted = [match.user_b, match.get_percent]
				matches.append(items_wanted)
			elif match.user_b == user:
				items_wanted = [match.user_a, match.get_percent]
				matches.append(items_wanted)
			else:
				pass
		return matches



class Matches(models.Model):
	user_a = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='user_a_model')
	user_b = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='user_b_model')
	match_percent =  models.DecimalField(decimal_places=8,max_digits=16,default=0.00)
	total_ques = models.IntegerField()
	timestamp = models.DateTimeField(auto_now_add=True,auto_now = False)
	updated = models.DateTimeField(auto_now_add=False,auto_now=True)

	def __str__(self): #__str__(self)
		return "%.2f" %(self.match_percent)

	objects = MatchesManager()

	@property
	def get_percent(self):
		new_decimal=0.000 
		if self.match_percent != 0.0:
			new_decimal = self.match_percent * Decimal(100)
		return "%.2f%%" %(new_decimal)


	def do_match(self):
		user_a = self.user_a
		user_b = self.user_b
		match_percent,ques = get_match(user_a,user_b)
		self.match_percent = match_percent
		self.total_ques = ques
		self.save()


	def check_update(self):
		offset = timezone.now() - datetime.timedelta(hours=12)
		if self.updated < offset or self.match_percent == 0:
			self.do_match()
			PositionMatch.objects.update_matches(self.user_a,10)
			PositionMatch.objects.update_matches(self.user_b,10)
		else:
			print("Already Updated")

class PostionMatchManager(models.Manager):
	def update_matches(self,user ,match_no):
		matches = Matches.objects.get_queryset_with_percent(user = user)
		for match in matches:
			userjob = match[0].userjob_set.all()
			if userjob.count() > 0:
				for job in userjob:
					try:
						the_job = Job.objects.get(text__iexact=job.position)
						jobmatch , created = self.get_or_create(user = user , job=the_job)
					except:
						pass
					try:
						the_location = Location.objects.get(name__iexact=job.location)
						locationmatch , created = LocationMatch.objects.get_or_create(user = user , location=the_location)
					except:
						pass
					try:
						the_emoloyer = Employer.objects.get(name__iexact= job.employer_name)
						employermatch , created = EmployerMatch.objects.get_or_create(user = user , employer=the_emoloyer)
					except Employer.MultipleObjectsReturned:
						the_emoloyer = Employer.objects.filter(name__iexact=job.employer_name).first()
						employermatch , created = EmployerMatch.objects.get_or_create(user = user , employer=the_emoloyer)
					except:
						pass



class PositionMatch(models.Model):
	user = 	models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	job  = models.ForeignKey(Job,on_delete=models.CASCADE)	
	hidden = models.BooleanField(default=False)
	liked = models.NullBooleanField()
	updated = models.DateTimeField(auto_now=True,auto_now_add=False)

	objects = PostionMatchManager()

	def check_update(self,match_int):
		past = datetime.timedelta(hours=12)
		now =  timezone.now()
		offset = now - past
		if self.updated < offset:
			PositionMatch.objects.update_matches(self.user,match_int) 

	def __str__(self):
		return self.user.username

	@property
	def get_match_url(self):
		return reverse("position_match" , kwargs={"slug" : self.job.slug})

class LocationMatch(models.Model):
	user = 	models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	location = models.ForeignKey(Location,on_delete=models.CASCADE)	
	hidden = models.BooleanField(default=False)
	liked = models.NullBooleanField()

	def __str__(self):
		return self.user.username

	@property
	def get_match_url(self):
		return reverse("location_match" , kwargs={"slug" : self.location.slug})


class EmployerMatch(models.Model):
	user = 	models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	employer  = models.ForeignKey(Employer,on_delete=models.CASCADE)	
	hidden = models.BooleanField(default=False)
	liked = models.NullBooleanField()

	def __str__(self):
		return self.user.username

	@property
	def get_match_url(self):
		return reverse("employer_match" , kwargs={"slug" : self.employer.slug})