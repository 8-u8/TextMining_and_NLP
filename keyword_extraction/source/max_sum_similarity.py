import numpy as np
import itertools

from sklearn.metrics.pairwise import cosine_similarity


def max_sum_sim(doc_embedding, word_embedding, words, top_n, nr_candidates):
    # Caluculate distances and extract keywords

    distances = cosine_similarity(doc_embedding, word_embedding)
    distances_candidates = cosine_similarity(word_embedding, word_embedding)

    # get top_n words as candidates based on cosine similarity
    words_idx = list(distances.argsort()[0][-nr_candidates:])
    words_vals = [words[index] for index in words_idx]

    distances_candidates = distances_candidates[np.ix_(words_idx, words_idx)]

    min_sim = np.inf
    candidate = None

    for combination in itertools.combinations(range(len(words_idx)), top_n):
        sim = sum([distances_candidates[i][j]
                  for i in combination for j in combination if i != j])
        if sim < min_sim:
            candidate = combination
            min_sim = sim

    return [words_vals[idx] for idx in candidate]
