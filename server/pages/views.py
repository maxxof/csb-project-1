from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Account
from random import randint
from django.db import connection, transaction


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
	
# @login_required
def transferView(request):
	# if request.method == 'GET':
	request.session['from'] = request.GET.get('from')
	request.session['to'] = request.GET.get('to')
	request.session['amount'] = request.GET.get('amount')
	amount = request.session['amount']
	sender = User.objects.get(username=request.session['from'])
	receiver = User.objects.get(username=request.session['to'])

	try:
		amount = int(request.session['amount'])
		sender.account.balance -= amount
		sender.account.save()
		amount = receiver.account.balance + amount
	except:
		pass

	query = f"UPDATE pages_account SET balance = {amount} WHERE user_id = {receiver.id};"
	with connection.cursor() as cursor:
		cursor.execute(query)
	# receiver.account.save()
	# return render(request, 'pages/confirm.html')
	return redirect('/')




@login_required
def homePageView(request):
	request.session['sessionid'] = randint(1, 2)
	accounts = Account.objects.exclude(user_id=request.user.id)
	return render(request, 'pages/index.html', {'accounts': accounts,
											 'sessionid': request.session['sessionid']})
