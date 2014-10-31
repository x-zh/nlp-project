# coding=UTF-8

"""
Created on 10/30/14

@author: 'johnqiao'
"""
import logging
import traceback
from nlp_question_answer import settings

log = logging.getLogger('nlp-qa')


def log_error(exc_info):
    t, v, exc_tb = exc_info
    log.error('Error type: ' + str(t))
    log.error('Error value: ' + str(v))
    for filename, line_num, func_name, source in traceback.extract_tb(exc_tb):
        log.error('\nFile name: %-23s\nLine num: %s\nSource: "%s"\nFunction: %s()\n' % (filename, line_num, source, func_name))
    log.error('=' * 10)

    if settings.DEBUG:
        print 'Error type: ' + str(t)
        print 'Error value: ' + str(v)

        for filename, line_num, func_name, source in traceback.extract_tb(exc_tb):
            print '\nFile name: %-23s\nLine num: %s\nSource: "%s"\nFunction: %s()\n' % (filename, line_num, source, func_name)
        print '=' * 10
