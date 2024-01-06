from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Account
from random import randint
from django.db import connection


# @login_required
# def confirmView(request):
# 	if request.user.is_authenticated and request.GET.get('csrfmiddlewaretoken'):
# 		print('access granted')
# 		amount = request.session['amount']
# 		to = User.objects.get(username=request.session['to'])
# 		print(request.user)
# 		request.user.account.balance -= amount
# 		to.account.balance += amount
# 		request.user.account.save()

# 		to.account.save()
# 	else:
# 		print('not granted')
# 	return redirect('/')
	
@login_required
def transferView(request):
	if request.method == 'POST':
		request.session['to'] = request.POST.get('to')
		request.session['amount'] = request.POST.get('amount')
		amount = request.session['amount']
		receiver = User.objects.get(username=request.session['to'])
		sender = request.user.account

		try:
			amount = int(request.session['amount'])
			sender.balance -= amount
			amount = receiver.account.balance + amount
			receiver.account.balance = amount
		except:
			pass

		query = f"UPDATE pages_account SET balance = {amount} WHERE user_id = {receiver.id};"
		print(query)
		with connection.cursor() as cursor:
			cursor.execute(query)
		sender.save()
		receiver.account.save()
		# return render(request, 'pages/confirm.html')
	return redirect('/')




@login_required
def homePageView(request):
	request.session['sessionid'] = randint(0, 10)
	accounts = Account.objects.exclude(user_id=request.user.id)
	return render(request, 'pages/index.html', {'accounts': accounts,
											 'sessionid': request.session['sessionid']})
