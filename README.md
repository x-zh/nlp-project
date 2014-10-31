nlp-project
===========

for NLP course

Required Libraries
------------------

### nltk

Natural Language Processing (NLP) functions such as sentence
segmentation, word tokenization, and more.

* <http://nltk.org/install.html>

#### nltk resources

In addition, you will need to download several nltk resources using
nltk.download() after you have the nltk library installed.

* 'taggers/maxent_treebank_pos_tagger/english.pickle'

### gensim

Some useful Information Retrieval (IR) algorithms including string to
vector functions and similarity queries such as TF-IDF. Also implements
topic modelling such as Latent Semantic Analysis.

* <http://radimrehurek.com/gensim/install.html>

* <https://github.com/piskvorky/gensim/>

For successfully installing gensim, you need Fortran compiler. Run the following command to install it. (It might take you a while...) Also, you may need to update your brew first. (See 'Troubleshooting' section for how to update brew)

`brew install gfortran`

If the above command fails, try [Install freetype and scipy - Issue installing GCC using homebrew (scipy package dependency)](http://apple.stackexchange.com/questions/142308/issue-installing-gcc-using-homebrew-scipy-package-dependency) in the Troubleshooting section.

### Django

Python web framework

* <https://www.djangoproject.com/>

### DB (PostgreSQL / MySQL / SQLite)

### Wiki Data

* [simple english-wikipedia-6/10/10 (6/10/10)](https://archive.org/details/simplewiki_20100610)


References
------------------

* [causeofwhy](https://github.com/bwbaugh/causeofwhy)

* [如何计算两个文档的相似度](http://www.52nlp.cn/%E5%A6%82%E4%BD%95%E8%AE%A1%E7%AE%97%E4%B8%A4%E4%B8%AA%E6%96%87%E6%A1%A3%E7%9A%84%E7%9B%B8%E4%BC%BC%E5%BA%A6%E4%B8%80)

* [Setting up Django with MongoDB](http://petrkout.com/programming/setting-up-django-with-mongodb/)

* [Using MongoDB with Django](http://www.ibm.com/developerworks/library/os-django-mongo/)

* [Entry point hook for Django projects](http://eldarion.com/blog/2013/02/14/entry-point-hook-django-projects/)


Troubleshooting
------------------

* [How to update brew](http://apple.stackexchange.com/questions/153790/how-to-fix-brew-after-its-upgrade-to-yosemite)

* [numpy and scipy need fortran compiler](http://stackoverflow.com/questions/11442970/numpy-and-scipy-for-preinstalled-python-2-6-7-on-mac-os-lion)

* [Installing GCC on OS X Yosemite via Homebrew - make[1]: [stage2-bubble] Error 2 make: [bootstrap] Error 2](http://bordoni.me/environment/gcc-os-x-yosemite-via-homebrew/)

* [Install freetype and scipy - Issue installing GCC using homebrew (scipy package dependency)](http://apple.stackexchange.com/questions/142308/issue-installing-gcc-using-homebrew-scipy-package-dependency)
