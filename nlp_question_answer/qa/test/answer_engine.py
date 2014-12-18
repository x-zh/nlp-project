# coding=UTF-8

"""
Created on 12/5/14

@author: 'johnqiao'
"""
import os

import django
import nltk
import codecs
from Levenshtein import ratio


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nlp_question_answer.settings")
django.setup()

from qa.models import Pages


def ie_preprocess(document):
    sentences = nltk.sent_tokenize(document)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent) for sent in sentences]
    print sentences


def output_pages_to_text(file_name):
    page_data = Pages.objects.filter()
    with codecs.open(file_name, 'w', 'utf-8') as f:
        for page in page_data.iterator():
            title = page.title.strip()
            f.write(title)
            p = page.p.strip()
            f.write(p)

            # div = page.div.strip()
            # f.write(div)


def process_page_text(file_name):
    text = ''
    for line in codecs.open(file_name, 'r', 'utf-8'):
        line = line.strip()
        if line in ('\n', ''):
            continue
        text += line + ' '

    print '=' * 50
    sentences = nltk.sent_tokenize(text)
    for sentence in sentences:
        print sentence
        sentence = nltk.word_tokenize(sentence)
        print '-->', sentence
        sentence = nltk.pos_tag(sentence)
        print '==>', sentence
        # print '**>', nltk.ne_chunk(sentence)
        print '\n'


def component_pos_tag(txt, log=False):
    # txt = 'What percentage of the tuition for freshman students in 2002 is covered by the financial aid awarded to them?'
    # txt = 'How much did the undergraduate applications rise from 2002 to 2012?'
    # txt = 'How much of the 2013 freshman class is of international origin?'
    sentence = nltk.word_tokenize(txt)
    sentence = nltk.pos_tag(sentence)
    if log:
        print '==>', sentence
    return sentence


def clean_txt_file(file_name):
    text = ''
    for line in codecs.open(file_name, 'r', 'utf-8'):
        line = line.strip()
        if line in ('\n', ''):
            continue
        text += line + ' '

    with codecs.open('test_data/txt_cleaned.txt', 'w', 'utf-8') as f:
        f.write(text)


def break_down_to_sentences(txt, log=False):
    sentences = nltk.sent_tokenize(txt)
    if log:
        for sentence in sentences:
            print '==>', sentence, '\n'
    return sentences
        # sentence = nltk.word_tokenize(sentence)
        # print '==>', sentence, '\n'


def calculate_similarity(str1, str2):
    """
    # Calculate document TF-IDF
    d_tfidf = dict()
    token_counts = self.doci[ID]
    max_count = max(token_counts.itervalues())
    for term in token_counts:
        # TF: Raw frequency divided by the maximum raw frequency
        # of any term in the document.
        tf = token_counts[term] / max_count
        # IDF: Total number of documents in the corpus divided by
        # the number of documents where the term appears.
        idf = math.log(len(self.doci) / self.dict.dfs[term])
        d_tfidf[term] = tf * idf
    # Calculate inner product
    inner_product = 0
    for term in terms:
        if term in token_counts:
            inner_product += q_tfidf[term] * d_tfidf[term]
    # Calculate query length
    query_length = 0
    for term in q_tfidf:
        query_length += q_tfidf[term] ** 2
    query_length = math.sqrt(query_length)
    # Calculate document length
    doc_length = 0
    for term in d_tfidf:
        doc_length += d_tfidf[term] ** 2
    doc_length = math.sqrt(doc_length)
    # Calculate the cosine similarity
    cosine_sim = inner_product / (query_length * doc_length)
    ranked_pages[ID] = cosine_sim
    """
    return ratio(str1, str2)


if __name__ == "__main__":
    # Clean file
    # with open('test_data/test2.txt') as f:
    # f_name = 'test_data/test_data.txt'
    # f_name = 'test_data/test1.txt'
    # output_pages_to_text(f_name)
    # process_page_text(f_name)

    # clean_txt_file('test_data/test2.txt')

    # === break_down_to_sentences === #
    # file_name = 'test_data/test2_cleaned.txt'
    # text = ''
    # for line in codecs.open(file_name, 'r', 'utf-8'):
    #     line = line.strip()
    #     if line in ('\n', ''):
    #         continue
    #     text += line + ' '
    # break_down_to_sentences(text, log=True)

    # === calculate_similarity === #
    file_name = 'test_data/test2_cleaned.txt'
    text = ''
    for line in codecs.open(file_name, 'r', 'utf-8'):
        line = line.strip()
        if line in ('\n', ''):
            continue
        text += line + ' '
    sentences = break_down_to_sentences(text, log=False)
    query = 'How much did the undergraduate applications rise from 2002 to 2012?'
    sentences_with_similarity = []
    for sentence in sentences:
        sentence = sentence.encode('utf-8')
        score = calculate_similarity(str(sentence), str(query))
        sentences_with_similarity.append((score, sentence))
    sentences_with_similarity = sorted(sentences_with_similarity, key=lambda tup: tup[0], reverse=True)
    results = []
    processed_query = 'undergraduate applications rise from 2002 to 2012'
    # Assume we have a component that can pick out the more important words...
    # currently, let's only fetch NN(单数|不可数) and NNS(复数) as the 'important words'
    processed_query_words_with_boosted = []
    for word, tag in component_pos_tag(processed_query):
        if tag in ('NN', 'NNS'):
            processed_query_words_with_boosted.append(word)

    for score, sentence in sentences_with_similarity:
        for word_in_query in processed_query_words_with_boosted:
            if word_in_query in sentence:
                results.append((score, sentence))
                break

    # multiple answers are possible
    answers_from_googler = [
        'There was a 45% rise in undergraduate applications from 2002 to 2012 from .... Part of that investment was a move from leased to owned space, which will result ...',
        'transition to college through programs and services in college readiness and ... rapidly between 2002-03 and 2012-13 than over either of the two preceding decades, but the average annual rate of increase in inflation-adjusted tuition and fees at private ... The average published tuition and fee price for undergraduates.'
        "From 2002-2012, undergraduate applications increased 288% from 9,838 to 28,348. ... Vanderbilt's commitment to teaching the whole student is evident in the many ways it ... The college hall system will bring new energy to the array of campus living ... The substantial increase in faculty honors and awards over the past ten",
        'the UK. Being entrusted with the education of students who will become professional and ... Despite the steady rise in student numbers, the UK remains behind many .... With the exception of enrolments on other undergraduate programmes, ... Patterns and trends in UK higher education 2012. 2002–03. 2003–04. 2004–05',
        "In 2012-2013, 7,968 students participated in the co-op program. ... Northeastern began as a commuter school with many part-time and evening .... The 49,822 undergraduate applications represent a 5.2 percent increase from the previous year. .... In 2002, Northeastern's Center for Subsurface Sensing and Imaging System",
    ]
    final_results = []
    for answer_from_googler in answers_from_googler:
        for _, sentence in results:
            score = calculate_similarity(sentence, answer_from_googler)
            final_results.append((score, sentence))

    final_results = sorted(final_results, key=lambda tup: tup[0], reverse=True)

    index = 1
    no_duplicates = set()
    for score, sentence in final_results:
        if sentence not in no_duplicates:
            print '%d. [%s]\t%s\n' % (index, score, sentence)
            index += 1
            no_duplicates.add(sentence)

            tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
            tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
            # chunked_sentences = nltk.batch_ne_chunk(tagged_sentences, binary=False)






