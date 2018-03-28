from nlpia.data.loaders import get_data
from nltk.tokenize import casual_tokenize
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem import PorterStemmer

# import nltk
# nltk.download('wordnet')  # noqa
# from nltk.stem.wordnet import WordNetLemmatizer

corpus = get_data('cats_and_dogs')

STOPWORDS = 'a and the be do is are was with on in to he her she him I it me my we our you your ? , . !'.split()
tfidfer = TfidfVectorizer(min_df=2, max_df=.6)
docs = [doc.lower() for doc in corpus]
docs = [casual_tokenize(doc) for doc in docs]
stemmer = PorterStemmer()
docs = [[stemmer.stem(w) for w in words if w not in STOPWORDS] for words in docs]
docs = [[w for w in words if w not in STOPWORDS] for words in docs]
docs = [' '.join(words) for words in docs]


tfidfer = TfidfVectorizer(min_df=2, max_df=.6)
df = pd.DataFrame(tfidfer.fit_transform(docs).todense())
id_words = [(i, w) for (w, i) in tfidfer.vocabulary_.items()]
df.columns = list(zip(*sorted(id_words)))[1]

pd.set_option('display.width', 150)
df.round(1)
#     ate  can  car  cat  chase  cute  die  dog  ferret  flower  ...    ran  squirrel  struck  took  tree  trick  turtl   up  vet  water
# 0   0.0  0.0  0.0  0.4    0.0   0.0  0.0  0.0     0.0     0.0  ...    0.0       0.0     0.0   0.0   0.0    0.0    0.0  0.0  0.0    0.0
# 1   0.9  0.0  0.0  0.5    0.0   0.0  0.0  0.0     0.0     0.0  ...    0.0       0.0     0.0   0.0   0.0    0.0    0.0  0.0  0.0    0.0
# 2   0.0  0.0  0.0  0.5    0.8   0.0  0.0  0.0     0.0     0.0  ...    0.0       0.0     0.0   0.0   0.0    0.0    0.0  0.0  0.0    0.0
# ...
# 56  0.0  0.0  0.9  0.5    0.0   0.0  0.0  0.0     0.0     0.0  ...    0.0       0.0     0.0   0.0   0.0    0.0    0.0  0.0  0.0    0.0
# 57  0.0  0.0  0.7  0.0    0.0   0.0  0.0  0.0     0.0     0.0  ...    0.0       0.0     0.0   0.0   0.0    0.0    0.0  0.0  0.0    0.0
# 58  0.0  0.0  0.0  0.0    0.0   0.0  0.0  0.5     0.0     0.0  ...    0.0       0.0     0.0   0.9   0.0    0.0    0.0  0.0  0.0    0.0
# [59 rows x 26 columns]

df.T.sum()
# 0     1.334096
# ...
# 20    0.000000
# 21    1.000000
# 22    0.000000
# ...
# 30    0.000000
# ...
# 34    0.000000
# ...
# 46    0.000000
# 47    1.000000
# 48    0.000000
# ...
[corpus[i] for i in [20, 22, 30, 34, 46, 48]]
['Sit Ubu, sit.',
 'I flew a kite.',
 'The catbird seat',
 "I painted Turtle's shell with nail polish.",
 'Moon lept into my lap.',
 'The lizard aquarium was moist.']


from sklearn.decomposition import PCA
pcaer = PCA(n_components=3)

doc_topic_vectors = pd.DataFrame(pcaer.fit_transform(df.values), columns='A B C'.split())
doc_topic_vectors.round(1)
#            A         B         C
# 0   0.176454  0.278185 -0.118654
# 1   0.146159  0.336665 -0.055871
# 2  -0.057432  0.355008  0.144430
# ...
# 56  0.134689  0.267813 -0.089800
# 57 -0.005008 -0.269208 -0.159880
# 58 -0.409417 -0.080740  0.138035


def tokenize(text):
    text = text.lower()
    tokens = casual_tokenize(text)
    stemmer = PorterStemmer()
    stems = [stemmer.stem(w) for w in tokens if w not in STOPWORDS]
    stems = [w for w in stems if w not in STOPWORDS]
    return stems


def search(text):
    """ search for the most relevant document """
    tokens = tokenize(text)
    topic_vector_query = pd.np.array(tfidfer.transform([' '.join(tokens)]).todense())[0]
    query_series = pd.Series(topic_vector_query, index=df.columns)

    return corpus[query_series.dot(df.T).values.argmax()]


search('Hello world, do you have a cat?')
# 'Do you have a pet?'

search('The quick brown fox jumped over the lazy dog')
# 'The dog sat on the floor.'

search('A dog barked at my car incessantly.')
# 'A dog chased the car, barking.'
tokenize('A dog barked at my car incessantly.')
# ['dog', 'bark', 'at', 'car', 'incessantli']

search('A Rotweiller barked at my car incessantly.')
# 'The cat hated getting in the car.'
tokenize('A Rotweiller barked at my car incessantly.')
# ['rotweil', 'bark', 'at', 'car', 'incessantli']

list(df.columns)
# ['ate', 'can', 'car', 'cat', 'chase', 'cute', 'die', 'dog', 'ferret', 'flower', 'hair', 'hat', 'have', 'it', 'kitten', 'pet', 'ran',
#   'squirrel', 'struck', 'took', 'tree', 'trick', 'turtl', 'up', 'vet', 'water'],
