from django.shortcuts import render_to_response

# Create your views here.
from django.template import RequestContext
from qa import config
from qa.answer_engine import AnswerEngine
from qa import answer_engine


def index(request):
    """Handles requests for the query input page."""
    template_values = {}
    if request.method == 'GET':
        return render_to_response('index.html', RequestContext(request, template_values))


def query_handler(request):
    """Gets user query and any args and sends to an AnswerEngine."""
    template_values = {}
    if request.method == 'GET':
        query = request.GET.get('q')
        num_top = request.GET.get('top', 5)
        num = request.GET.get('num', 100)
        start = request.GET.get('start', 0)
        lch = request.GET.get('lch', 2.16)
        log_training = bool(request.GET.get('train', False))
        ans_eng = AnswerEngine(config.index, query, start, num_top, lch)
        answers, ir_query_tagged = answer_engine.get_answers(ans_eng)

        template_values['query'] = query
        template_values['ir_query'] = ' '.join(ans_eng.ir_query)
        template_values['ir_query_tagged'] = ir_query_tagged
        template_values['num_pages'] = ans_eng.num_pages
        template_values['num_answers'] = len(answers)
        template_values['answers'] = answers[:num]

        # Log answer details
        if log_training:
            with open('log_training.txt'.format(num), mode='a') as f:
                f.write('\t'.join([' '.join(ans_eng.ir_query), query]) + '\t0')
                for rank, answer in enumerate(answers, start=1):
                    f.write('\t' + '\t'.join([str(rank)] + [str(x) for x in answer._features]))
                f.write('\n')

        return render_to_response('answer.html', RequestContext(request, template_values))


