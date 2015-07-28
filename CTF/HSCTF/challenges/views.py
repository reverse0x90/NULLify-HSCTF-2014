import hashlib
import logging
import random
from challenges.models import *
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User
from HSCTF.utils import *

# Setup logger to backup the queries we made
logger = logging.getLogger('Backup')

# Playboard View
# This view gets the available challenges from the database and gives them to the index.html template.
@login_required
def playboard(request, pageName):

	isIE = checkUserAgent(request.META['HTTP_USER_AGENT'])

	tiles = []
	tilesInfo = Challenges.objects.filter(web_name__exact=pageName).order_by('popup_name')

	for tileInfo in tilesInfo:
		tile = {}
		tile['popup_name'] = str(tileInfo.popup_name)
		tile['tile_icon'] = str(tileInfo.tile_icon)
		tile['points'] = str(tileInfo.points)
		try:
			userSolved = ChallengesSolved.objects.get(user=request.user, challenge=tileInfo)
		except:
			userSolved = False

		if userSolved:
			tile['color'] = 'bg-lightGreen'
		else:
			tile['color'] = 'bg-lightBlue'

		tiles.append(tile)


	return render(request, 'index.html', {'category': pageName, 'tiles': tiles, 'isIE':isIE})

# CheckFlag View
# This view checks if the flag is correct if so it saves the information to the database and logs the result, else will log the fail.
@login_required
def checkFlag(request):
	m = hashlib.sha256()
	m.update(request.POST['flag'].replace(' ', '').lower())
	inputFlag = m.hexdigest()

	flagList = Challenges.objects.values_list('flag', flat=True)
	
	if inputFlag in flagList:
		solvedChallenge = Challenges.objects.get(flag__exact=inputFlag)
		try:
			# Add this team to the challenges solved table
			teamSolved = ChallengesSolved(user=request.user,challenge=solvedChallenge)
			teamSolved.save()
						
			logger.info("ChallengesSolved(user=User.objects.get(username='%s'),challenge=Challenges.objects.get(flag__exact='%s')).save()\n\n" % (request.user.username, inputFlag))
			
			teamPoints = ScoreBoard.objects.get(team=request.user)
			teamPoints.score += solvedChallenge.points
			teamPoints.save()
						
			logger.info("teamPoints = ScoreBoard.objects.get(team=User.objects.get(username='%s')); teamPoints.score += Challenges.objects.get(flag__exact='%s').points; teamPoints.save()\n\n" % (request.user.username, inputFlag))
			
			solvedChallenge.num_solved += 1
			solvedChallenge.save()
			
			logger.info("solvedChallenge = Challenges.objects.get(flag__exact='%s'); solvedChallenge.num_solved += 1; solvedChallenge.save()\n\n" % ( inputFlag))
			
			correctSubmission = ChallengeSubmissions.objects.get(user=request.user)
			correctSubmission.correct_flags += 1
			correctSubmission.save()
			
			logger.info("correctSubmission = ChallengeSubmissions.objects.get(user=User.objects.get(username='%s')); correctSubmission.correct_flags += 1; correctSubmission.save()\n\n" % (request.user.username))
			
		except:
			return HttpResponse('<div style="color:green">You have already solved: ' + solvedChallenge.fullname + '</div>')
		return HttpResponse('<div style="color:green">' + solvedChallenge.fullname + ': Wow such correct flag! The force is strong with this one.</div>')
	else:
		correctSubmission = ChallengeSubmissions.objects.get(user=request.user)
		correctSubmission.wrong_flags += 1
		correctSubmission.save()
		
		logger.info("correctSubmission = ChallengeSubmissions.objects.get(user=User.objects.get(username='%s')); correctSubmission.wrong_flags += 1; correctSubmission.save()\n\n" % (request.user.username))
			
		randResponse = random.randint(1,20)
		returnString = ''
		if randResponse == 1:
			returnString = '<div style="color:red">No. Try not. Do... or do not. There is no try.</div>'
		elif randResponse == 2:
			returnString = '<div style="color:red">Sir, the possibility of successfully brute forcing the flag is approximately 3,720 to 1.</div>'
		elif randResponse == 3:
			returnString = '<div style="color:red">A Jedi uses the Force for knowledge and defense, never for attack.</div>'
		elif randResponse == 4:
			returnString = '<div style="color:red">I sense a disturbance in the force.</div>'
		elif randResponse == 5:
			returnString = '<div style="color:red">Good. Use your aggressive feelings, boy. Let the hate flow through you.</div>'
		elif randResponse == 6:
			returnString = '<div style="color:red">I really don\'t see how that is going to help! Surrender is a perfectly acceptable alternative in extreme circumstances!</div>'
		elif randResponse == 7:
			returnString = '<div style="color:red">Wow such wrong flag! Try again. May the force be with you.</div>'
		elif randResponse == 8:
			returnString = '<div style="color:red">You wanna buy some death sticks?</div>'
		elif randResponse == 9:
			returnString = '<div style="color:red">WAGRRRRWWGAHHHHWWWRRGGAWWWWWWRR. - chewbacca</div>'
		elif randResponse == 10:
			returnString = '<div style="color:red">I have you now!</div>'
		elif randResponse == 11:
			returnString = '<div style="color:red">The Dark Side of the Force is the pathway to many abilities some consider to be... Unnatural.</div>'
		elif randResponse == 12:
			returnString = '<div style="color:red">Great, kid. Don\'t get cocky.</div>'
		elif randResponse == 13:
			returnString = '<div style="color:red">You can\'t win, Darth.</div>'
		elif randResponse == 14:
			returnString = '<div style="color:red">Aren\'t you a little short for a storm trooper?</div>'
		elif randResponse == 15:
			returnString = '<div style="color:red">Mmm. Lost a planet, Master Obi-Wan has. How embarrassing.</div>'
		elif randResponse == 16:
			returnString = '<div style="color:red">Traveling through hyperspace ain\'t like dusting crops, farm boy.</div>'
		elif randResponse == 17:
			returnString = '<div style="color:red">Fear is the path to the dark side.</div>'
		elif randResponse == 18:
			returnString = '<div style="color:red">Anakin, you\'re breaking my heart! And you\'re going down a path I cannot follow!</div>'
		elif randResponse == 19:
			returnString = '<div style="color:red">You disappoint me. Yoda holds you in such high esteem. Surely you can do better!</div>'
		elif randResponse == 20:
			returnString = '<div style="color:red">You were the chosen one! It was said that you would destroy the Sith, not join them.</div>'
		return HttpResponse(returnString)

# Scores View
# Gets the scores from the database and returns them in json format.
@login_required
def scores(request):

	TeamScores = ScoreBoard.objects.order_by('-score', 'modified')[:10]
	retJSON = ''
	teams = '{"teams":['
	scores = '"scores":['

	count = 1
	color = ''
	for team in TeamScores:
		teams += '"' + team.team.first_name + '",'

		if count == 1:
			color = 'gold'
		elif count == 2:
			color = 'silver'
		elif count == 3:
			color = '#FF7F00'
		else:
			color = 'black'

		scores += '{"y": ' + str(team.score) + ',' + ' "color": ' + '"' + color + '"'+ ',' + ' "url": ' + '"' + '/team/' + team.team.first_name +'/' + '"' +'},'
		count += 1


	teams = teams[:-1] + '],'
	scores = scores[:-1] + ']}'

	retJSON = teams + scores

	return HttpResponse(retJSON)

# Tscores View
# Gets the team scores from the database and returns them in json format.
@login_required
def tscores(request, teamName):
	try:
		Team = User.objects.get(first_name__exact=teamName)
		TeamChallengeSolved = ChallengesSolved.objects.filter(user=Team)
		recon = 0
		trivia = 0
		script = 0
		web = 0
		binary = 0
		crypto = 0
		stego = 0
		network = 0
		grab_bag = 0
		flash = 0

		for fkchallenge in TeamChallengeSolved:
			if fkchallenge.challenge.tile_icon == 'icon-google':
				recon += fkchallenge.challenge.points
			elif fkchallenge.challenge.tile_icon == 'icon-book':
				trivia += fkchallenge.challenge.points
			elif fkchallenge.challenge.tile_icon == 'icon-github-3':
				script += fkchallenge.challenge.points
			elif fkchallenge.challenge.tile_icon == 'icon-chrome':
				web += fkchallenge.challenge.points
			elif fkchallenge.challenge.tile_icon == 'icon-console':
				binary += fkchallenge.challenge.points
			elif fkchallenge.challenge.tile_icon == 'icon-locked':
				crypto += fkchallenge.challenge.points
			elif fkchallenge.challenge.tile_icon == 'icon-puzzle':
				stego += fkchallenge.challenge.points
			elif fkchallenge.challenge.tile_icon == 'icon-cloud':
				network += fkchallenge.challenge.points
			elif fkchallenge.challenge.tile_icon == 'icon-basket':
				grab_bag += fkchallenge.challenge.points
			elif fkchallenge.challenge.tile_icon == 'icon-lightning':
				flash += fkchallenge.challenge.points


		retJSON = '{"recon": ' + str(recon) + ',' + '"trivia": '  + str(trivia) + ',' + '"script": ' + str(script) + ',' + '"web": ' + str(web) + ',' + '"binary": ' + str(binary) + ',' + '"crypto": ' + str(crypto) + ',' + '"stego": ' + str(stego) + ',' + '"network": ' + str(network) + ',' + '"grab_bag": ' + str(grab_bag) + ',' + '"flash": ' + str(flash) +'}'
		
		return HttpResponse(retJSON)
	except:
		return HttpResponse('False')

# Tpoints View
# Gets the team submissions from the database and returns them in json format.		
@login_required
def tpoints(request, teamName):
	try:
		Team = User.objects.get(first_name__exact=teamName)
		TeamSubmissions = ChallengeSubmissions.objects.get(user=Team)

		retJSON = '{"correct_flags": ' + str(TeamSubmissions.correct_flags) + ',' + '"wrong_flags": '  + str(TeamSubmissions.wrong_flags) + '}'
		
		return HttpResponse(retJSON)
	except:
		return HttpResponse('False')

# Scoreboard View
# Returns the scoreboard.html template.		
@login_required
def scoreboard(request):
	isIE = checkUserAgent(request.META['HTTP_USER_AGENT'])

	return render(request, 'scoreboard.html', {'isIE':isIE})