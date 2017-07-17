![baeML](https://i.imgur.com/rHwT8uD.png)

# Relevant Information/Links
+ [The Skip-gram Model](https://www.tensorflow.org/tutorials/word2vec)
	+ Backbone and base inspiration for this project
+ [Word Embeddings](http://colah.github.io/posts/2014-07-NLP-RNNs-Representations/)
	+ Math
+ [Object Serialization](https://docs.python.org/2/library/pickle.html)
	+ This makes everything cheaper
+ [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs3/documentation.html#Parsing%20HTML)
	+ Python package for web scraping
+ [Synonym Clustering with KMeans](http://cs229.stanford.edu/proj2013/DaoKellerBejnood-AlternateEquivalentSubstitutes.pdf)
	+ Due to computational restrictions, our implementation for synonym clustering relied on a cascading-style approach, loosely inspired by binary search.
+ [Skip-thoughts for Sentiment Analysis](https://github.com/tensorflow/models/tree/master/skip_thoughts)
	+ For future improvements, we can use this to detect sentiment bias in article content, and perhaps make modifications for political bias detection.

# Project Overview
![Project Overview](https://i.imgur.com/NZzHoOD.png)
	+ Note: A little outdated, but still generally correct

## Important Requirements (continously updated)
+ Python 2.7
+ TensorFlow 1.0.1+
+ scikit-learn 
+ matplotlib 
+ scipy 
+ numpy 
+ BeautifulSoup 
+ Django
+ TBD

## Frontend Components
+ Basic UI allowing user login with Facebook
+ API to dictate communication between frontend and backend controllers
+ ReactJS

## Backend Components
+ Skip-gram model to vectorize and train on semantics of words
+ Django backend with PostgreSQL DB
+ Webcrawler to find and classify new data using the model, then feed the user relevant info

