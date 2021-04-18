import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def mmr(doc_embedding, word_embedding, words, top_n, diversity):

    # Extract similarity within words, and between words and the document
    word_doc_similarity = cosine_similarity(word_embedding, doc_embedding)
    word_similarity = cosine_similarity(word_embedding)

    # init candidates and already choose best keyword or keyphrases
    keywords_idx = [np.argmax(word_doc_similarity)]
    candidates_idx = [i for i in range(len(words)) if i != keywords_idx[0]]

    for _ in range(top_n - 1):
        # Extract similarities within candidates and
        # between candidates and selected keywords or keyphrase.
        candidate_similarities = word_doc_similarity[candidates_idx, :]
        target_similarities = np.max(
            word_similarity[candidates_idx][:, keywords_idx], axis=1)

        # caluclate MMR score
        mmr = (1 - diversity) * (candidate_similarities -
                                 diversity) * target_similarities.reshape(-1,
                                                                          1)
        mmr_idx = candidates_idx[np.argmax(mmr)]

        keywords_idx.append(mmr_idx)
        candidates_idx.append(mmr_idx)

    return [words[index] for index in keywords_idx]
