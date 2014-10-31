from django.conf.urls import patterns, include, url
# from django.contrib import admin
from django.conf.urls.static import static
from nlp_question_answer import settings

urlpatterns = patterns('',
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


from qa import views as web
urlpatterns += patterns('',
                        url(r'^$', web.index, name='web_index'),
                        url(r'^cause/$', web.query_handler, name='web_query'),
                        )