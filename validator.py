def GetClusterMainTopics(clusterId, postTitles, clusters, tokenizedPosts, nTopTopics=5):
    cluster_tf = {}
    for i, title in enumerate(postTitles):
        if clusters[i] == clusterId:
            for term in tokenizedPosts[i]:
                cluster_tf[term] = cluster_tf.get(term, 0) + 1

    total_terms = sum(cluster_tf.values())
    cluster_term_weights = {term: freq / total_terms for term, freq in cluster_tf.items()}

    top_terms = sorted(cluster_term_weights, key=cluster_term_weights.get, reverse=True)[:nTopTopics]
    return top_terms