# coding=UTF-8

"""
Created on 11/8/14

@author: 'johnqiao'

Base class to generate page from the data which crawled by Scrapy.
"""
import collections
import json
import operator

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from unidecode import unidecode

from qa.indexer import get_punkt_sent_detector, tokenizer, regularize


class Paragraph(object):
    """Container that holds sentences and their tokens.

    Attributes:
        text: The original unaltered text string of the paragraph.
        sentences: A list of unaltered strings for each sentence in the
            paragraph.
        sentence_tokens: A list of sentences that contains a list of
            string tokens for each sentence.
    """

    def __init__(self, text):
        """Initialize the Paragraph object."""
        self.text = text
        self.sentences = None
        self.sentence_tokens = None

    def segment_sentences(self):
        """Segment the Paragraph text into a list of sentences."""
        # We already use '\n' to separate the paragraph.
        # Sentence segmentation
        # if '\n' in self.text:
        # self.sentences = [sent for sent in self.text.split('\n')]
        # else:
        # TODO(sqiao): use other method to separate the sentences.
        sent_detector = get_punkt_sent_detector()
        self.sentences = sent_detector.tokenize(self.text,
                                                realign_boundaries=True)

    def tokenize_sentences(self):
        """Tokenize each sentence in the list into a list of tokens."""
        if not self.sentences:
            self.segment_sentences()
        # self.sentence_tokens = tokenizer.batch_tokenize(self.sentences)
        self.sentence_tokens = tokenizer.tokenize_sents(self.sentences)


class Page(object):
    """Holds all text and metadata (ID, title) of a page from the corpus.

    Attributes:
        ID: An integer corresponding to the ID of the page in the corpus.
        title: A string of the document title.
        link: The original page link.
        start: The integer offset this document begins at in the corpus.
            Used to seek in the corpus file when retrieving a Page ID.
        paragraphs: A list of Paragraph objects for this document.
        token_count: A defaultdict(int) providing {token -> count},
            where count is the number of times the token appears in the
            document (in all of the document's paragraphs).
        cosine_sim: If present, represents the similarity score for the
            query that was used to retrieve this document. This value
            is set by an Index object.
    """

    def __init__(self, ID, title, link, text, start=None):
        """Initialize the Page object."""
        self.ID = ID
        self.title = title
        self.link = link
        self.text = text
        self.start = start
        self.paragraphs = None
        self.token_count = None
        self.cosine_sim = None

    def remove_markup(self):
        """Remove extra markup and leave just the plain-text."""
        pass

    def unidecode(self):
        """Convert non-ascii to closest ASCII equivalent."""
        print 'title:', self.title
        # print 'link:', self.link
        # print 'content:', self.text
        self.title = unidecode(self.title).strip()
        self.text = unidecode(self.text).strip()

    def preprocess(self):
        """Convenience method that removed markup does unidecode."""
        self.remove_markup()
        self.unidecode()

    def segment_paragraphs(self):
        """Segment the Page text into a list of paragraphs."""
        self.paragraphs = [Paragraph(text) for text in self.text.split('\n')]

    def segment_sentences(self):
        """Segment each Paragraph into a list of sentences."""
        if not self.paragraphs:
            self.segment_paragraphs()
        for paragraph in self.paragraphs:
            paragraph.segment_sentences()

    def tokenize_sentences(self):
        """Tokenize the sentence list in the paragraphs into list of tokens."""
        if not self.paragraphs:
            self.segment_sentences()
        for paragraph in self.paragraphs:
            paragraph.tokenize_sentences()

    def regularize_text(self):
        """Regularizes all tokens for each sentence in each paragraph."""
        if not self.paragraphs:
            self.tokenize_sentences()
        for i, para in enumerate(self.paragraphs):
            for j, sent in enumerate(para.sentence_tokens):
                self.paragraphs[i].sentence_tokens[j] = regularize(sent)
            # Remove empty sentences
            self.paragraphs[i].sentence_tokens = [x for x in self.paragraphs[i].sentence_tokens if x]

    def count_tokens(self):
        """Count the frequency of text's tokens in a bag-of-words style."""
        token_count = collections.defaultdict(int)
        for paragraph in self.paragraphs:
            for sentence in paragraph.sentence_tokens:
                for token in sentence:
                    token_count[token] += 1
        self.token_count = []
        for (token, count) in sorted(token_count.iteritems(),
                                     key=operator.itemgetter(1),
                                     reverse=True):
            self.token_count.append((token, count))

    def __str__(self):
        """Creates a string including ID, title, and original text."""
        self.preprocess()
        f = StringIO()
        f.write('=' * 79 + '\n')
        f.write(str(self.ID) + ' ' + self.title + '\n')
        f.write('-' * 79 + '\n')
        f.write(self.text.encode('utf-8') + '\n')
        f.write('=' * 79 + '\n')
        output = f.getvalue()
        f.close()
        return output

        # def __eq__(self, other):
        # return self.ID == other.ID

        # def __ne__(self, other):
        # return not self.__eq__(other)

        # def __hash__(self):
        # return hash((self.ID,))


def page_generator(file_obj):
    """Parses a Wikipedia dump file and yields individual pages."""
    pos = 0
    data = json.load(file_obj)
    for d in data:
        pos += 1
        yield Page(pos, d['title'], d['link'], d['content'], pos)


def plain_page_generator(file_obj):
    """Yields individual pages from a generated plain-text corpus file."""
    next_pos = 0
    for line in file_obj:
        # Keep track of file pos for later start of page seeking
        pos = next_pos
        next_pos += len(line)
        line = line.decode('utf-8')
        ID, title, link, text = line.split('\t')
        yield Page(int(ID), title, link, text, pos)
