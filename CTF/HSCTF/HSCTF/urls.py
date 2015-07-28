from django.conf.urls import patterns, include, url, handler404, handler500
from django.views.generic.base import TemplateView, RedirectView
from HSCTF.views import *
from challenges.views import *

# Set the handler pages for HTTP error 404 and 500 
handler404 = 'HSCTF.views.page404'
handler500 = 'HSCTF.views.page500'

# Allows for fast render of root level documents (robots.txt, favico, etc.)
class TextPlainView(TemplateView):
	def render_to_response(self, context, **kwargs):
		return super(TextPlainView, self).render_to_response(context, content_type='text/plain', **kwargs)

# Router portion of Django application this code ties the web pages to functions
# in the views files (HSCTF.views and challenges.views) 
urlpatterns = patterns('',
	url(r'^$', playboard, {'pageName': 'Recon'}),
	url(r'^recon/$', playboard, {'pageName': 'Recon'}),
	url(r'^trivia/$', playboard, {'pageName': 'Trivia'}),
	url(r'^script/$', playboard, {'pageName': 'Script'}),
	url(r'^web/$', playboard, {'pageName': 'Web'}),
	url(r'^binary/$', playboard, {'pageName': 'Binary'}),
	url(r'^crypto/$', playboard, {'pageName': 'Crypto'}),
	url(r'^forensics/$', playboard, {'pageName': 'Stego/Forensics'}),
	url(r'^network/$', playboard, {'pageName': 'Network'}),
	url(r'^flash/$', playboard, {'pageName': 'Flash'}),
	url(r'^grab_bag/$', playboard, {'pageName': 'Grab Bag'}),
	url(r'^scoreboard/$', scoreboard),
	url(r'^logout/$', logout),
	url(r'^scores/$', scores),
	url(r'^challenge/([a-z]{4}\d{1,2})/$', ctf),
	url(r'^team/(Toaster in the Bathtub|JK|Hack \&\& Axe \|\| Vikings|\@echo off|Digital Synergy|Hawk\'s Leverage|Indestructible Plastic|EZ 011011|All UR flags R belong 2 us|iN Code)/$', team),
	url(r'^tscores/(Toaster in the Bathtub|JK|Hack \&\& Axe \|\| Vikings|\@echo off|Digital Synergy|Hawk\'s Leverage|Indestructible Plastic|EZ 011011|All UR flags R belong 2 us|iN Code)/$', tscores),
	url(r'^tpoints/(Toaster in the Bathtub|JK|Hack \&\& Axe \|\| Vikings|\@echo off|Digital Synergy|Hawk\'s Leverage|Indestructible Plastic|EZ 011011|All UR flags R belong 2 us|iN Code)/$', tpoints),
	url(r'^login/$', login),
	url(r'^submitFlag/$', checkFlag),
	url(r'^auth/$', auth),
	url(r'^robots\.txt$', TextPlainView.as_view(template_name='robots.txt')),
  	url(r'^favicon\.ico$', RedirectView.as_view(url='/images/favicon.ico')),
)
