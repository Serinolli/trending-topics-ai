from wordcloud import WordCloud
import matplotlib.pyplot as plt


def outputClusterInfo(clusters):
    for cluster, terms in clusters.items():
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(terms))
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.title(cluster + ' Word Cloud')
        plt.axis('off')
        plt.show()

    for cluster, terms in clusters.items():
        term_freq = {}  
        for term in terms:
            term_freq[term] = term_freq.get(term, 0) + 1

        sorted_terms = sorted(term_freq.items(), key=lambda x: x[1], reverse=True)[:10]  # Get top 10 terms
        terms, frequencies = zip(*sorted_terms)

        plt.figure(figsize=(10, 5))
        plt.bar(terms, frequencies)
        plt.title(cluster + ' Top Terms')
        plt.xlabel('Terms')
        plt.ylabel('Frequency')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()
