from haystack import indexes
from .models import Pages, Paragraph


# class PagesIndex(indexes.SearchIndex, indexes.Indexable):
#     text = indexes.CharField(document=True, use_template=True)
#     title = indexes.CharField(model_attr='title')
#
#     def get_model(self):
#         return Pages

class ParagraphIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(use_template=True, document=True)
    title = indexes.CharField(model_attr='title', boost=0.7)
    context = indexes.CharField(model_attr='context', boost=0.1)
    ann = indexes.CharField(model_attr='annotations')

    def get_model(self):
        return Paragraph
