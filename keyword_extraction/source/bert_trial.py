# %% load libraries
from max_sum_similarity import max_sum_sim
from Maximum_Marginal_Relevance import mmr

# import numpy as np
# import itertools

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from sentence_transformers import SentenceTransformer
# %%
'''
もくてき
docのキーワード抽出(Keyword Extraction)の練習。
from: https://towardsdatascience.com/keyword-extraction-with-bert-724efca412ea
docは単一の文章。これを各センテンスに適用するとすれば面倒そう。
ここでやっているのはある意味生成モデル的な動き。教師あり学習ではなく、
CountVectorizerによる単語頻度での抽出と
学習済みモデル(sentence_transformerを通したDistilBert)を使う
(なんか distilbert-base-nli-stsb-mean-tokens がいいらしい)
多様な表現を持ってくるためにはBERT最強！みたいなところがあるっぽい。
'''
# %% document definition
doc = """
      Supervised learning is the machine learning task of 
      learning a function that maps an input to an output based 
      on example input-output pairs.[1] It infers a function 
      from labeled training data consisting of a set of 
      training examples.[2] In supervised learning, each 
      example is a pair consisting of an input object 
      (typically a vector) and a desired output value (also 
      called the supervisory signal). A supervised learning 
      algorithm analyzes the training data and produces an 
      inferred function, which can be used for mapping new 
      examples. An optimal scenario will allow for the algorithm 
      to correctly determine the class labels for unseen 
      instances. This requires the learning algorithm to  
      generalize from the training data to unseen situations 
      in a 'reasonable' way (see inductive bias).
      """

# %% using CountVectrizer
# memo: it cannot use for dataset.
n_gram_range = (3, 3)
stop_words = 'english'

count = CountVectorizer(ngram_range=n_gram_range,
                        stop_words=stop_words).fit([doc])
candidates = count.get_feature_names()

# %% check count vectorizer
candidates

# %% using Embeddings with sentence transformers.
model = SentenceTransformer('distilbert-base-nli-mean-tokens')

# %% model fitting and encoding
doc_embedding = model.encode([doc])
canditate_embeddings = model.encode(candidates)

# %% check objects
# memo: it returns numeric vectors.
print(doc_embedding)
print(canditate_embeddings)

# %% comparison for Countvectorizer and embeddings
top_n = 5
distances = cosine_similarity(doc_embedding, canditate_embeddings)
keywords = [candidates[index] for index in distances.argsort()[0][-top_n:]]

# %%
print(f'cosine similarity is {distances}')
print(f'keywords top 5 is: {keywords}')

# %%
keywords_mssim = max_sum_sim(
    doc_embedding, canditate_embeddings, candidates, top_n=5, nr_candidates=20)

# %% check keywords_mssim
print(keywords)
print(keywords_mssim)
# %%
# memo: high diversity makes diverse keyphrases.
keywords_mmr = mmr(doc_embedding, canditate_embeddings,
                   words=candidates, top_n=5, diversity=0.7)

# %% check keywords_mssim
print(keywords)
print(keywords_mmr)

# %%
