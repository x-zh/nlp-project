# coding = utf-8
import nltk


MAPPING = {
    'who': 'PERSON',
    'what': 'OBJECT',
    'where': 'LOCATION',
    'when': 'DATETIME',
    'why': 'ABSTRACT',
    'how': 'VBP'
}

WORDNET = [
    ['master', 'ms', 'm.s.', 'm.s'],
    ['bachelor', 'bs', 'b.s.', 'b.s'],
    ['doctor', 'phd', 'ph.d'],
]

WEIGHT_MAPPING = {
    'CD': 1.1,
    'NN': 1,
    'JJ': 1,
    'NNS': 1,
    'VBD': 1,
    # 'IN': 0.1,
    # 'DT': 0.1,
    # 'WP': 0.1,
    # 'VBZ': 0.1,
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
        elif q[0].lower() in MAPPING:
            self.question_type = MAPPING.get(q[0].lower(), 'UNKNOWN')
        else:
            self.question_type = 'UNKNOWN'

    def weight_keywords(self):
        if self.kw is None:
            document = self.question
            kw = {}
            def ie_preprocess(document):
                sentences = nltk.sent_tokenize(document)
                sentences = [nltk.word_tokenize(sent) for sent in sentences]
                sentences = [nltk.pos_tag(sent) for sent in sentences]
                return sentences

            tagged_sentences = ie_preprocess(document)

            for k, sent in enumerate(tagged_sentences):
                sent = nltk.ne_chunk(sent)
                print sent
                for i in sent:
                    if isinstance(i, nltk.tree.Tree):
                        for j in i.leaves():
                            for wordgroup in WORDNET:
                                if j[0].lower() in wordgroup:
                                    for w in wordgroup:
                                        kw[w] = 1
                                    break
                            kw[j[0]] = 1
                    else:
                        if i[1] in WEIGHT_MAPPING:
                            kw[i[0]] = WEIGHT_MAPPING.get(i[1], 1)
            self.kw = kw
        if self.question_type == 'OBJECT':
            self.kw['which'] = 1
        return self.kw

    def parse_question(self):
        self.parse_type()
        self.weight_keywords()

