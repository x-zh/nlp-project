# coding=UTF-8

"""
Created on 10/30/14

@author: 'johnqiao'

Configuration of QA system.

"""
import os
import sys
import errno
import ConfigParser

from qa import indexer

index = None

CONFIG_NAME = 'config.ini'
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_dir = os.path.join(BASE_DIR, 'data')

# How many response worker threads to use
# NUMBER_OF_PROCESSES = max(1, multiprocessing.cpu_count() - 1)

# IMPORTANT: We should not use multiple processing because of the following:
# - queues.py
# def qsize(self):
# # Raises NotImplementedError on Mac OSX because of broken sem_getvalue()
#           return self._maxsize - self._sem._semlock._get_value()
#


def create_default_config():
    """Used to create a default config file if one does not exist."""
    config = ConfigParser.SafeConfigParser()
    config.add_section('wiki')
    config.set('wiki', 'location', os.path.join(DATA_dir, 'dump.xml'))
    with open(CONFIG_NAME, mode='w') as f:
        config.write(f)


def read_config():
    """Reads a configuration file from disk."""
    config = ConfigParser.SafeConfigParser()
    try:
        with open(CONFIG_NAME) as f:
            config.readfp(f)
    except IOError as e:
        if e.errno != errno.ENOENT:
            raise
        print 'Configuration file not found! Creating one...'
        create_default_config()
        print 'Please edit the config file named: ' + CONFIG_NAME
        sys.exit(errno.ENOENT)
    return config


def load_index(wiki_location, doci_in_memory=False):
    """Loads an existing Index or creates one if it doesn't exist."""
    try:
        return indexer.Index(wiki_location, doci_in_memory)
    except indexer.IndexLoadError:
        indexer.create_index(wiki_location, progress_count=100, max_pages=20000)
        return indexer.Index(wiki_location, doci_in_memory)


def main():
    global index
    """Loads the Index and starts a web UI according to a config file."""
    config = read_config()
    print 'Loading index'
    index = load_index(config.get('wiki', 'location'))
    print 'Starting web server'

    # pool = multiprocessing.Pool(NUMBER_OF_PROCESSES)
    # Give each pool initial piece of work so that they initialize.
    # ans_eng = AnswerEngine(index, 'bird sing', 0, 1, 2.16)
    # answer_engine.get_answers(ans_eng)
    # for x in xrange(NUMBER_OF_PROCESSES * 2):
    #     pool.apply_async(answer_engine.get_answers, (ans_eng,))
    # del ans_eng
