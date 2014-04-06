from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    # Home
    url(r'^$', TemplateView.as_view(template_name='survey/index.html'), name='home'),
    
    # Commuterform
    url(r'^commuterform/$', 'survey.views.commuter', name='commuterform'),
    url(r'^commuterform/complete/$', TemplateView.as_view(template_name='survey/thanks.html'), name='complete'),

    # Leaderboard
    url(r'^leaderboard/$', 'leaderboard.views.new_leaderboard'),
    url(r'^leaderboard-bare/$', 'leaderboard.views.leaderboard_bare'),
    url(r'^test-chart/$', 'leaderboard.views.testchart'),
    url(r'^emplbreakdown/(?P<month>[-\w]+)/$', 'leaderboardlist.views.empBreakDown'),
    url(r'^emplbreakdown/$', 'leaderboardlist.views.chooseMonth'),
    url(r'^nvobreakdown/$', 'leaderboard.views.nvobreakdown'),
    url(r'^nvobreakdown/(?P<selEmpID>[-\w]+)/$', 'leaderboard.views.nvobreakdown'),

    # data api
    url(r'^api/survey/$', 'survey.views.api', name='survey_api'),


    # Examples:
    # url(r'^$', 'django_test.views.home', name='home'),
    # url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
	url(r'^leaderboard/([^/]+)/(\d)/$', 'leaderboard.views.new_leaderboard'),
	url(r'^leaderboard/(\d)/$', 'leaderboard.views.leaderboard_detail'),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
