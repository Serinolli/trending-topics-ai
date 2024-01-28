def GetClusterMainTopics(cluster_id, post_titles, cluster_data, tokenized_posts, n_top_topics=5):
    cluster_tf = {}
    for i, title in enumerate(post_titles):
        if cluster_data == cluster_id:
            for term in tokenized_posts[i]:
                cluster_tf[term] = cluster_tf.get(term, 0) + 1

    total_terms = sum(cluster_tf.values())
    cluster_term_weights = {term: freq / total_terms for term, freq in cluster_tf.items()}

    top_terms = sorted(cluster_term_weights, key=cluster_term_weights.get, reverse=True)[:n_top_topics]
    return top_terms