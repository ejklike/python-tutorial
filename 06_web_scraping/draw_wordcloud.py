import itertools
from collections import Counter

import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd
from konlpy.tag import Okt


def get_words_ko(okt, text, stopwords=None):
    tagged = okt.pos(text, 
                     stem=True, 
                     norm=True)
    filtered = [w for w, pos in tagged if pos[0] == 'N']
    filtered = [w for w in filtered if len(w) > 1]  # Remove single-character words
    
    if stopwords is not None:
        filtered = [w for w in filtered if w not in stopwords]
    return filtered


def flatten_list(list_of_lists):
    return list(itertools.chain.from_iterable(list_of_lists))


def draw_wordcloud(words, title=None, save_path=None):
    word_freq = Counter(words)
    wordcloud = WordCloud(
        font_path='./NanumSquareRoundR.ttf', 
        width=800, 
        height=400, 
        background_color='white').generate_from_frequencies(word_freq)
    
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud)
    if title:
        plt.title(title)
    plt.axis('off')
    if save_path:
        plt.savefig(save_path)
    else:
        plt.show()


if __name__ == '__main__':

    # load data
    df = pd.read_csv('./soccer_news.csv')

    # define NLP parser
    okt = Okt()

    # extract words
    stopwords = ['기자', '축구', '통해']
    df['words'] = df['text'].apply(lambda x: get_words_ko(okt, x, stopwords=stopwords))

    # concatenate all lists of words into a single list
    words_all = flatten_list(df['words'])

    # draw word cloud
    draw_wordcloud(words_all, 
                   title='Daum Sports: Breaking News', 
                   save_path='wordcloud.png')