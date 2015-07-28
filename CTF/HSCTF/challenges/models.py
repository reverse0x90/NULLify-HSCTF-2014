from django.db import models
from django.contrib.auth.models import User

class Challenges(models.Model):
	web_name = models.CharField(max_length=20)
	popup_name = models.CharField(max_length=20, unique=True)
	fullname = models.CharField(max_length=100)
	flag = models.CharField(max_length=100, unique=True)
	tile_icon = models.CharField(max_length=100)
	description = models.TextField()
	points = models.IntegerField()
	num_solved = models.IntegerField()

	def __unicode__(self):
		return self.fullname

class ChallengesSolved(models.Model):
	user = models.ForeignKey(User)
	challenge = models.ForeignKey(Challenges)

	class Meta:
		unique_together = ('user', 'challenge',)

	def __unicod__(self):
		return self.challenge.fullname + '_' + self.user.username
		
class ChallengeSubmissions(models.Model):
	user = models.ForeignKey(User, unique=True)
	correct_flags = models.IntegerField()
	wrong_flags = models.BigIntegerField()


class ScoreBoard(models.Model):
	team = models.ForeignKey(User, unique=True)
	score = models.IntegerField()
	modified = models.DateTimeField(auto_now=True)

	def __unicod__(self):
		return self.team.username

