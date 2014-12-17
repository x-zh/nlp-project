import nltk

MAPPING = {
    'CD': 1.2,
    'NN': 1.1,
    'NNS': 1.1,
    'IN': 0.6,
    'DT': 0.6,
    'WP': 0.6,
    'VBZ': 0.6,
    'VBP': 0.6,
    'NNP': 1.1,
}


def ne(document):
    kw = {}
    def ie_preprocess(document):
        sentences = nltk.sent_tokenize(document)
        sentences = [nltk.word_tokenize(sent) for sent in sentences]
        sentences = [nltk.pos_tag(sent) for sent in sentences]
        return sentences

    tagged_sentences = ie_preprocess(document)

    for k, sent in enumerate(tagged_sentences):
        sent = nltk.ne_chunk(sent)
        for i in sent:
            if isinstance(i, nltk.tree.Tree):
                for j in i.leaves():
                    kw[j[0]] = 1.2
            else:
                if i[1] in MAPPING:
                    kw[i[0]] = MAPPING.get(i[1], 1)
    print kw
    print ""

with open('testQuestions.txt', 'r') as f:
    for l in f:
        if l.strip() and l.strip()[0].lower() == 'q':
            ne(l.strip())
