# coding=UTF-8

"""
Created on 12/17/14

@author: 'johnqiao'
"""
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
base_path = os.path.abspath(os.path.dirname(__file__))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nlp_question_answer.settings")
django.setup()

from qa.ann.ann import AnnotationUtil, Page
from qa.models import Paragraph, Pages


def add_context():
    Paragraph.objects.filter(content__icontains='JavaScript').delete()
    # delete All rights reserved.
    return
    for p in Paragraph.objects.filter():
        # page = Pages.objects.get(url=p.url)
        if len(p.content) < 10:
            try:
                prev = Paragraph.objects.get(pk=p.pk-1)
                nxt = Paragraph.objects.get(pk=p.pk+1)
                prev.content += ' ' + p.content + ' ' + nxt.content
                prev.save()
                p.delete()
                nxt.delete()
            except Paragraph.DoesNotExist:
                pass
        # else:
            # p.context = page.div
            # p.save()


def export_anns_to_db():
    lst_files = [
        'lst/city.lst',
        'lst/day.lst',
        'lst/day_cap.lst',
        'lst/months.lst',
        'lst/numbers.lst',
        'lst/person.lst',
        'lst/stat_us.lst',
        'lst/time.lst',
        'lst/year.lst',
    ]
    rule_files = ['rules/main.ar']
    ann_util = AnnotationUtil(log=False)
    for i in range(len(lst_files)):
        lst_files[i] = os.path.join(base_path, lst_files[i])
    for i in range(len(rule_files)):
        rule_files[i] = os.path.join(base_path, rule_files[i])

    ann_util.load_annotations(lst_files)
    ann_util.load_rules(rule_files)

    # paragraphs = Paragraph.objects.filter()
    # for p in paragraphs:
    #     page = Page(ann_util.apply_annotation(p.content))
    #     annotations = ''
    #     for key, val in page.ann_counter.items():
    #         annotations += str((key + ' ') * int(val))
    #     p.annotations = annotations
    #     p.save()

    txt = '%22 Office of Undergraduate Admissions New York University 665 Broadway, 11th Floor test@email.com New York, NY 10012-2339 $222,000,000 (172)823-1922'
    page = Page(ann_util.apply_annotation(txt))
    print txt, '\n'
    page.print_sentences()


if __name__ == '__main__':
    add_context()
    export_anns_to_db()
