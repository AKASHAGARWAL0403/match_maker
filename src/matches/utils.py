from decimal import Decimal
from questions.models import UserAnswer

def get_point(user_a,user_b):
	ans_a = UserAnswer.objects.filter(user=user_a)
	ans_b = UserAnswer.objects.filter(user=user_b)
	total_poss = 0
	total = 0
	ques = 0
	for a in ans_a:
		for b in ans_b:
			a_pref = a.there_answer
			b_ans = b.my_answer
			if a.question.id == b.question.id:
				ques += 1;
				if a_pref == b_ans:
					total += a.there_input_point
				total_poss += a.there_input_point
	percent = 0
	if total_poss != 0:
		percent = total/Decimal(total_poss)
	if percent==0:
		percent = 0.00001
	return percent,ques

def get_match(user_a,user_b):
	ans_a = get_point(user_a,user_b)
	ans_b = get_point(user_b,user_a)
	total_ques = Decimal(ans_a[1])
	if total_ques != 0:
		match_percent = (Decimal(ans_a[0]) * Decimal(ans_b[0]))**(1/Decimal(ans_a[1]))
	else:
		print("Returning 0.00")
		return 0.0000,0
	return match_percent,ans_b[1]