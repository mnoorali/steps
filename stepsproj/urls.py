from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

import stepsapp.views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', stepsapp.views.IndexView,
        name='enter_steps',),
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^register/$', stepsapp.views.RegisterView, name='register'),
    url(r'^enter_steps/', stepsapp.views.StepsView, name='enter_steps'),
    url(r'^steps_list/', stepsapp.views.StepsList, name='steps_list'),
    url(r'^profile/', stepsapp.views.Profile, name='profile'),
    url(r'^password_reset_form/$', 
        'django.contrib.auth.views.password_reset', 
        {'post_reset_redirect' : '/user/password/reset/done/'},
        name="password_reset"),
        (r'^user/password/reset/done/$',
        'django.contrib.auth.views.password_reset_done'),
        (r'^user/password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', 
        'django.contrib.auth.views.password_reset_confirm', 
        {'post_reset_redirect' : '/user/password/done/'}),
        (r'^user/password/done/$', 
        'django.contrib.auth.views.password_reset_complete'),
)

urlpatterns += staticfiles_urlpatterns()
