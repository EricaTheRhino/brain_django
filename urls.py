from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^events/$', 'brain.processor.views.add_event', name='add_event'),
    url(r'^state/$', 'brain.processor.views.get_state', name='get_state'),
    url(r'^register/$', 'brain.processor.views.register_component', name='register_component'),
    url(r'^$', 'brain.website.views.home', name='home'),
    url(r'^mood/$', 'brain.website.views.mood', name='mood'),
    url(r'^mood.json', 'brain.website.views.mood_json', name='mood_json'),
    url(r'^latest_events.json', 'brain.website.views.latest_events_json', name='latest_events_json'),
    url(r'^fullness_message', 'brain.website.views.fullness_message', name='fullness_message'),
    url(r'^tickle_message', 'brain.website.views.tickle_message', name='tickle_message'),
    url(r'^credits/$', 'brain.website.views.credits', name='credits'),
    url(r'^touchscreen/$', 'brain.website.views.touchscreen', name='touchscreen'),
    url(r'^panel/$', 'brain.website.views.panel', name='panel'),
    url(r'^board/$', 'brain.website.views.board', name='board'),
    url(r'^board/play/$', 'brain.website.views.play', name='play'),
    url(r'^board/eyes/$', 'brain.website.views.get_eye_data', name='get_eye_data'),
    url(r'^board/trigger/$', 'brain.website.views.trigger_cmd', name='trigger_cmd'),
    url(r'^board/eyes/(?P<eye>left|right)$', 'brain.website.views.get_eye_image'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^library/test/success.html', 'brain.website.views.success', name='success'),
    url(r'^ncsi.txt', 'brain.website.views.ncsi', name='ncsi'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
)
