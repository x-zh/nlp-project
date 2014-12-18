from django.conf.urls import patterns, include, url
# from django.contrib import admin
from django.conf.urls.static import static
from nlp_question_answer import settings


# from qa import views as web
urlpatterns = patterns(
    '',
    url(r'^ask/', include('qa.urls')),
    url(r'^search/', include('haystack.urls')),
)

urlpatterns += static(settings.STATIC_URL,
                      document_root=settings.STATIC_ROOT)
