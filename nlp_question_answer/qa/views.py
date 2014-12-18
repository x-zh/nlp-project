# coding = utf-8
from django.shortcuts import render
from haystack.query import SearchQuerySet

from .question_parse import Question
from .models import Pages


def ask_me_anything(request):
    context = {}
    if request.method == 'POST':
        q = request.POST.get('q', '')
        q = Question(q)
        sq = SearchQuerySet()
        for k, v in q.weight_keywords().items():
            if v != 1:
                sq = sq.boost(k, v)
        for k in q.weight_keywords():
            sq = sq.filter_or(content=k)
        context = {'q': q, 'result': sq[:10]}
    return render(request, 'ask_me_anything.html', context)
