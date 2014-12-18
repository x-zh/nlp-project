# coding=UTF-8

"""
Created on 12/17/14

@author: 'johnqiao'
"""
from collections import defaultdict, Counter
import re
import nltk
from nltk.tokenize import BlanklineTokenizer, RegexpTokenizer
from nltk.tokenize.punkt import PunktWordTokenizer


class Page:
    def __init__(self, sentences):
        self.sentences = sentences
        _ann_list = []
        for sentence in self.sentences:
            for token, anns in sentence.annotated:
                if anns:
                    _ann_list.extend(anns)
        self.ann_counter = Counter(_ann_list)
        # print self.ann_counter

    def print_sentences(self):
        for sentence in self.sentences:
            # print sentence.origin, '\n'
            # print sentence.tokenized, '\n'
            print sentence.annotated, '\n'
            print '\n\n\n'


class Sentence:
    def __init__(self):
        self.origin = ''
        self.tokenized = []
        self.annotated = []


class AnnotationSet:
    def __init__(self):
        self.ann_map = {}


class Annotation:
    def __init__(self):
        # Two ways to get the string
        self.string_index = -1  # the way to save memory
        self.string_length = -1
        self.string = ''  # the way to save time

        self.major_types = []
        self.minor_types = []


class AnnotationUtil:
    def __init__(self, log=False):
        """
            db: key/value pairs
                key     - token
                value   - annotation name list, major type and minor types
        """
        self.anns = defaultdict(list)
        self.rules = defaultdict(list)  # rules of annotation
        self.log = log

    def load_annotations(self, filenames):
        if isinstance(filenames, tuple) or isinstance(filenames, list):
            for filename in filenames:
                self.load_annotations(filename)
        elif isinstance(filenames, str):
            ann_name = ''
            with open(filenames, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and line != '\n':
                        if not ann_name:
                            ann_name = line
                        elif line in self.anns:
                            print 'Error: token[%s] with annotation[%s] already exists.' % (line, ann_name)
                        else:
                            # find the minor types
                            if ':' in line:
                                db_key = line.split(':')[0]
                                self.anns[db_key].append(ann_name)  # add the major annotation
                                # add remaining minor annotations
                                for minor_type in line.split(':')[1:]:
                                    db_value = ann_name + '.' + minor_type  # {ANN_NAME}.{MINOR_NAME}={MINOR_VALUE}
                                    self.anns[db_key].append(db_value)
                            else:
                                self.anns[line].append(ann_name)
            if self.log:
                print self.anns

    def load_rules(self, filenames):
        if isinstance(filenames, tuple) or isinstance(filenames, list):
            for filename in filenames:
                self.load_rules(filename)
        elif isinstance(filenames, str):
            with open(filenames, 'r') as f:
                for line in f:
                    line = line.strip()
                    rule_name = line.split()[0]
                    rule_pattern = line.split()[1]
                    self.rules[rule_name].append(rule_pattern)
            if self.log:
                print self.rules

    def apply_annotation(self, text):
        sentences_of_page = []
        sentences = nltk.sent_tokenize(text)
        # Apply annotations
        for sentence in sentences:
            s = Sentence()
            s.origin = sentence
            # s.tokenized = PunktWordTokenizer().tokenize(sentence)
            s.tokenized = RegexpTokenizer('\s+', gaps=True).tokenize(sentence)
            s_annotated = []
            for token in s.tokenized:
                annotations = []
                if token[-1] in ('.', ',', '!', ':', ';', '?',):
                    token = token[:-1]
                anns_of_token = self.anns.get(token.replace(',', ''))
                if anns_of_token:
                    annotations.extend(anns_of_token)
                # Apply rules for annotation
                for rule_name, rule_patterns in self.rules.items():
                    for rule_pattern in rule_patterns:
                        p = re.compile(rule_pattern)
                        if p.match(token):
                            annotations.append(rule_name)
                s_annotated.append((token, annotations))
            s.annotated = s_annotated
            sentences_of_page.append(s)

        print '\n\n'

        # Apply rules
        for rule_name, rule_patterns in self.rules.items():
            for rule_pattern in rule_patterns:
                p = re.compile(rule_pattern)
                text, n = p.subn('(\g<0>, _%s_)' % rule_name, text)
                if self.log:
                    print 'Replaced %d annotations[%s]' % (n, rule_name)

        return sentences_of_page


if __name__ == '__main__':
    lst_files = [
        'lst/city.lst',
        'lst/day.lst',
        'lst/months.lst',
        'lst/person.lst',
        'lst/stat_us.lst',
        'lst/time.lst',
        'lst/year.lst',
    ]
    rule_files = ['rules/main.ar']
    ann_util = AnnotationUtil(log=False)
    ann_util.load_annotations(lst_files)
    ann_util.load_rules(rule_files)

    # === test annotation === #
    txt = ''
    with open('test_data/test2_cleaned_small.txt', 'r') as f:
        for line in f:
            txt += line.strip() + ' '

    page = Page(ann_util.apply_annotation(txt))
    page.print_sentences()
