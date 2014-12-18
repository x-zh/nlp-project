# coding=UTF-8

"""
Created on 12/17/14

@author: 'johnqiao'
"""
from collections import defaultdict
import re


class QuestionUtil:
    def __init__(self, log=False):
        self.log = log
        self.rules = defaultdict(list)  # rules of question type

    def load_rules(self, filenames):
        if isinstance(filenames, tuple) or isinstance(filenames, list):
            for filename in filenames:
                self.load_rules(filename)
        elif isinstance(filenames, str):
            with open(filenames, 'r') as f:
                for line in f:
                    line = line.replace('\n', '').split(',')
                    rule_name = line[0]
                    rule_pattern = line[1]
                    rule_answer_type = line[2]
                    self.rules[rule_name].append((rule_pattern, rule_answer_type))
            if self.log:
                print self.rules

    def question_type(self, query):
        # Apply rules for annotation
        question_types = []
        for rule_name, rule_patterns in self.rules.items():
            for (rule_pattern, rule_answer_type) in rule_patterns:
                p = re.compile(rule_pattern)
                if p.search(query):
                    question_types.append(rule_answer_type)
        return question_types

if __name__ == '__main__':
    rule_files = ['rules/main.qr']
    q_util = QuestionUtil(log=False)
    q_util.load_rules(rule_files)
    question_types = q_util.question_type('Q. What is the address of Othmer Hall?')
    print question_types
