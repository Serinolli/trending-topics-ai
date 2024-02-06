from wordcloud import WordCloud
import matplotlib.pyplot as plt

def outputClustersInfo(clusters):
    global_unique_topics = set()
    for cluster in clusters:
        cluster_unique_topics = set()
        for topic in cluster:
            if isinstance(topic, tuple):
                cluster_unique_topics.add(' '.join(topic))
            else:
                cluster_unique_topics.add(topic)
        unique_topics_in_cluster = cluster_unique_topics - global_unique_topics
        if unique_topics_in_cluster:
            print(unique_topics_in_cluster)
            global_unique_topics.update(cluster_unique_topics)
        else:
            print("No unique topics found for this cluster.")