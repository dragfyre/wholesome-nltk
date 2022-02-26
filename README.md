# wholesome-nltk
An nltk-based AI filter to identify "wholesome" content.

It does this using a fairly simplistic algorithm that takes into account the presence of keywords of interest, an NLP sentiment analysis, and a naive Bayes classifier that determines what should be considered "wholesome". The classifier is trained on various sentences, marking them with `True` or `False` depending on whether they should be considered wholesome or not.

As input, you must define a URL leading to an RSS feed with articles to be evaluated. The algorithm parses and summarizes the articles, runs the sentiment analysis, the "wholesome" classifier, and the regex checks, and uses the results to assign an overall score to the article. Articles that score the highest are considered to be the most wholesome.

In practice, this system has a whole lot of holes in it and often doesn't work as expected. It works best when the feed it's given already contains a lot of wholesome material and still seems to come up with a lot of false positives. Definitely a work in progress...

## Dependencies

To run this filter, you should have Python >=3.7 installed with the newspaper3k, feedparser and regex modules. To install these, use pip3:

```
pip3 install newspaper3k
pip3 install feedparser
pip3 install regex
```

