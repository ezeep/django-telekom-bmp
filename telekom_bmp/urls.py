from django.conf.urls import patterns, include

from .views import Event

urlpatterns = patterns(
    '',
    (r'^event$', Event.as_view()),
    (r'^openid/', include('social.apps.django_app.urls', namespace='social')),
)
