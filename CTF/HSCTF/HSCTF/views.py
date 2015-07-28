#!/usr/bin/python
# Imports for program
import re
from django import forms
from challenges.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from HSCTF.utils import *

# 404 Error View
def page404(request):
	isIE = checkUserAgent(request.META['HTTP_USER_AGENT'])
	return render(request, '404.html', {'isIE':isIE})

# 500 Error View
def page500(request):
	isIE = checkUserAgent(request.META['HTTP_USER_AGENT'])
	return render(request, '500.html', {'isIE':isIE})

# Login View
# Checks the user agent and displays the appropriate view. (This bootstrap template nav bar doesn't play nice with windows firefox)  
def login(request):
	isIE = checkUserAgent(request.META['HTTP_USER_AGENT'])
	return render(request, 'login.html', {'isIE':isIE})

# Authentication View
# Checks if the user provided the right username an password else returns an error 
def auth(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username=username, password=password)
	if user is not None:
		if user.is_active:
			auth_login(request, user)
			return HttpResponse('True')
		else:
			return HttpResponse('<div style="color:red">Your Account has been disabled</div>')
	else:
		return HttpResponse('<div style="color:red">Login Failed Please Try Again</div>')

# Logout View
# Logs the user out the auth_logout takes care of destroying all the cookies, etc. 
@login_required
def logout(request):
	auth_logout(request)
	return redirect('/recon/')

# CTF View
# This function gets the challenge information out of the database and passes it the challenge.html template.
@login_required
def ctf(request, cPopup):
	challengeInfo = Challenges.objects.get(popup_name__exact=cPopup)
	total_teams = User.objects.count()


	return render(request, 'challenge.html', {'fullname':challengeInfo.fullname, 'description':challengeInfo.description.replace('$TEAM$', request.user.last_name), 'num_solved':challengeInfo.num_solved, 'total_teams': total_teams})

# Team View
# This function returns the team.html template the database data used by the team.html template is pulled via ajax.
@login_required
def team(request, teamName):
	#challengeInfo = Challenges.objects.get(popup_name__exact=cPopup)
	#total_teams = User.objects.count()

	isIE = checkUserAgent(request.META['HTTP_USER_AGENT'])

	return render(request, 'team.html', {'isIE':isIE, 'teamName':teamName})
