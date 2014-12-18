# coding = utf-8
from django.shortcuts import render
from haystack.query import SearchQuerySet
from haystack.query import SQ

from .question_parse import Question


def ask_me_anything(request):
    context = {}
    if request.method == 'POST':
        q = request.POST.get('q', '')
        q = Question(q)
        sq = SearchQuerySet()
        if q.get_type() in ('DATETIME', 'NUM', 'PERSON'):
            sq = sq.narrow('ann:' + q.get_type())
        for k in q.weight_keywords():
            sq = sq.filter_or(SQ(content=k) | SQ(title=k) | SQ(context=k))
        context = {
            'q': q,
            'result': sq[:10],
        }
    return render(request, 'ask_me_anything.html', context)
