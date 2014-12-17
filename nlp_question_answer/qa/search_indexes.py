from haystack import indexes
from .models import Pages, Paragraph


class PagesIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')

    def get_model(self):
        return Pages

# class ParagraphIndex(indexes.SearchIndex, indexes.Indexable):
#     text = indexes.CharField(model_attr='content', document=True)
#     title = indexes.CharField(model_attr='title')
#
#     def get_model(self):
#         return Paragraph
