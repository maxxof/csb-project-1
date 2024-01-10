from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Account
from random import randint
from django.db import connection

# A5:2017-Broken Access Control and CSRF vulnerability
@login_required
def transferView(request):
	if request.user.is_authenticated:
		# <-- FIX FOR BROKEN ACCESS CONTROL -->
		# uncomment next row
		# if request.method == 'POST' and request.POST.get('csrfmiddlewaretoken'):
		# in templates/index.html change the method of a transfer from from GET to POST
		# and uncomment {% csrf_token %} line to include csrf tokens with every action
		# uncomment POST-gets and comment out GET-gets
		# request.session['from'] = request.user.username
		# request.session['to'] = request.POST.get('to')
		# request.session['amount'] = request.POST.get('amount')
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
				# return redirect('/')
				pass
			
			# A1:2017-Injection
			# for example typing in the amount box "0; --" resets every account's balance to 0
			query = f"UPDATE pages_account SET balance = {amount} WHERE user_id = {receiver.id};"
			with connection.cursor() as cursor:
				cursor.execute(query)
			
			# <-- FIX FOR INJECTION -->
			# fix the try-catch block so that when user types anything else other than integer it
			# redirects back.
			
			# comment out last 3 rows with sql query and uncomment next two rows
			# with connection.cursor() as cursor:
			# 	cursor.execute("UPDATE pages_account SET balance = %s WHERE user_id = %s", (amount, receiver.id))
			# fixes the SQL-injection vulnerability.
			
			# alternatively there is even better fix, just by using django's in-built object system 
			# receiver.account.balance = amount
			# receiver.account.save()
	return redirect('/')

# A3:2017-Sensitive Data Exposure
@login_required
def balanceView(request, username):
	# <-- FIX FOR SENSITIVE DATA EXPOSURE -->
	# uncomment next two rows
	# if request.user.is_authenticated:
	# 	user = request.user
	# comment out next try-except block

	try:
		user = User.objects.get(username=username)
	except:
		return redirect('/')
	return render(request, 'pages/balance.html', {'user': user, 'balance': user.account.balance})


@login_required
def homePageView(request):
	request.session['sessionid'] = randint(1, 2)
	accounts = Account.objects.exclude(user_id=request.user.id)
	return render(request, 'pages/index.html', {'accounts': accounts,
											 'sessionid': request.session['sessionid']})
