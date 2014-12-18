# coding=UTF-8

"""
Created on 12/17/14

@author: 'johnqiao'
"""
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nlp_question_answer.settings")
django.setup()

from qa.ann.ann import AnnotationUtil, Page
from qa.models import Paragraph


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
    ann_util.load_annotations(lst_files)
    ann_util.load_rules(rule_files)

    paragraphs = Paragraph.objects.filter()
    for p in paragraphs:
        page = Page(ann_util.apply_annotation(p.content))
        annotations = ''
        for key, val in page.ann_counter.items():
            annotations += str((key + ' ') * int(val))
        p.annotations = annotations
        p.save()


    # page = Page(ann_util.apply_annotation(txt))
    # page.print_sentences()


if __name__ == '__main__':
    export_anns_to_db()