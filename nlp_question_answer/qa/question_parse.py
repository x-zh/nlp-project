# coding = utf-8
import nltk


MAPPING = {
    'who': 'PERSON',
    'what': 'OBJECT',
    'where': 'LOC',
    'when': 'DATETIME',
    'why': 'ABSTRACT',
    'how': 'VBP'
}

WORDNET = [
    ['master', 'ms', 'm.s.', 'm.s'],
    ['bachelor', 'bs', 'b.s.', 'b.s'],
    ['doctor', 'phd', 'ph.d'],
    ['financial aid', 'scholarship'],
    ['dentistry', 'dental'],
    ['earn', 'receive'],
    ['created', 'started',]
]

IGNORE = [
    'a', 'able', 'about', 'above', 'across', 'after', 'again', 'against',
    "ain't", 'all', 'almost', 'also', 'am', 'among', 'an', 'and', 'any', 'are',
    "aren't", 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below',
    'between', 'both', 'but', 'by', 'can', "can't", 'cannot', 'could',
    "could've", "couldn't", 'dear', 'did', "didn't", 'do', 'does', "doesn't",
    'doing', "don't", 'down', 'during', 'each', 'either', 'else', 'ever',
    'every', 'few', 'for', 'from', 'further', 'get', 'got', 'had', "hadn't",
    'has', "hasn't", 'have', "haven't", 'having', 'he', "he'd", "he'll", "he's",
    'her', 'here', "here's", 'hers', 'herself', 'him', 'himself', 'his', 'how',
    "how'd", "how'll", "how's", 'however', 'i', "i'd", "i'll", "i'm", "i've",
    'if', 'in', 'into', 'is', "isn't", 'it', "it's", 'its', 'itself', 'just',
    'least', 'let', "let's", 'like', 'likely', 'may', 'me', 'might', "might've",
    "mightn't", 'more', 'most', 'must', "must've", "mustn't", 'my', 'myself',
    'neither', 'no', 'nor', 'not', 'of', 'off', 'often', 'on', 'once', 'only',
    'or', 'other', 'ought', 'our', 'ours', 'ourselves', 'out', 'over', 'own',
    'rather', 'said', 'same', 'say', 'says', 'shall', "shan't", 'she', "she'd",
    "she'll", "she's", 'should', "should've", "shouldn't", 'since', 'so',
    'some', 'such', 'than', 'that', "that'll", "that's", 'the', 'their',
    'theirs', 'them', 'themselves', 'then', 'there', "there's", 'these', 'they',
    "they'd", "they'll", "they're", "they've", 'this', 'those', 'through',
    'tis', 'to', 'too', 'twas', 'under', 'until', 'up', 'us', 'very', 'wants',
    'was', "wasn't", 'we', "we'd", "we'll", "we're", "we've", 'were', "weren't",
    'what', "what'd", "what's", 'when', "when'd", "when'll", "when's", 'where',
    "where'd", "where'll", "where's", 'which', 'while', 'who', "who'd",
    "who'll", "who's", 'whom', 'why', "why'd", "why'll", "why's", 'will',
    'with', "won't", 'would', "would've", "wouldn't", 'yet', 'you', "you'd",
    "you'll", "you're", "you've", 'your', 'yours', 'yourself', 'yourselves']

WEIGHT_MAPPING = {
    'CD': 1.3,
    'NN': 1,
    'JJ': 1,
    'NNS': 1,
    'VBD': 1,
    'VBN': 1,
    'VBP': 1,
    'NNP': 1,
}


class Question():

    def __init__(self, question):
        if question[-1] in ['?', '.', '!']:
            question = question[:-1]
        self.question = question
        self.words = question.split()
        self.question_type = None
        self.kw = None

    def get_type(self):
        if self.question_type is None:
            self.parse_question()
        return self.question_type

    def parse_type(self):
        q = self.words
        if len(q) < 2:
            self.question_type = 'UNKNOWN'
        elif q[0].lower() in ['is', 'was', 'do', 'does', 'did',
                              'will', 'did', 'can', 'must']:
            self.question_type = 'CHECKIF'
        elif q[0].lower() == 'how':
            if q[1].lower() in ['many', 'much', 'long']:
                self.question_type = 'NUM'
            elif q[1].lower() in ['often', 'frequent']:
                self.question_type = 'DATETIME'
        elif q[0].lower() in MAPPING:
            self.question_type = MAPPING.get(q[0].lower(), 'UNKNOWN')
        else:
            self.question_type = 'UNKNOWN'

    def ie_preprocess(self, document):
        sentences = nltk.sent_tokenize(document)
        sentences = [nltk.word_tokenize(sent) for sent in sentences]
        sentences = [nltk.pos_tag(sent) for sent in sentences]
        return sentences

    def apply_wordnet(self):
        document = self.question.lower()
        for wordgroup in WORDNET:
            for word in wordgroup:
                if (word.lower() in document and word.lower() not in IGNORE):
                        for word2 in wordgroup:
                            if word2.lower() != word.lower():
                                self.kw[word2.lower()] = 1
                        break

    def weight_keywords(self):
        if self.kw is None:
            document = self.question
            kw = {}
            tagged_sentences = self.ie_preprocess(document)

            for k, sent in enumerate(tagged_sentences):
                sent = nltk.ne_chunk(sent)
                print sent
                for i in sent:
                    if isinstance(i, nltk.tree.Tree):
                        for j in i.leaves():
                            if j[0] in IGNORE:
                                continue
                            kw[j[0]] = 1.4
                    else:
                        if i[0] not in IGNORE and i[1] in WEIGHT_MAPPING:
                            kw[i[0]] = WEIGHT_MAPPING.get(i[1], 1)
            self.kw = kw
            if self.question_type == 'OBJECT':
                self.kw['which'] = 1
        return self.kw

    def parse_question(self):
        self.parse_type()
        self.weight_keywords()
        self.apply_wordnet()
