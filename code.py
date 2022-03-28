# This is the code for OIM 3640 Problem Solving & Software Design Assignment 2

# Install Package for Pulling Data
import urllib.request
import string
# import sys
# from unicodedata import category

# Install Natural Language Toolkit
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Install Visualization Package
import matplotlib.pyplot as plt


# Open the Stopwords.txt file and store stopwords.txt into a list
stop_words = open('stopwords.txt')
stop_words_list = []
for line in stop_words:
    stop_words_list.append(line.strip())
# print(stop_words_list) # for testing


# The following code is adapted and modified from Session 15: analyze_book_solution.py
def process_file(filename, skip_header):
    """Makes a histogram that contains the words from a file.
    filename: string
    skip_header: boolean, whether to skip the Gutenberg header
    returns: map from each word to the number of times it appears.
    """
    book = {}
    fp = open(filename, encoding='utf8')

    if skip_header:
        skip_gutenberg_header(fp)

    strippables = string.punctuation + string.whitespace
    # via: https://stackoverflow.com/questions/60983836/complete-set-of-punctuation-marks-for-python-not-just-ascii

    # strippables = ''.join(
    #     [chr(i) for i in range(sys.maxunicode) if category(chr(i)).startswith("P")]
    # )

    for line in fp:
        if line.startswith('*** END OF THE PROJECT'):
            break

        line = line.replace('-', ' ')
        # line = line.replace(
            # chr(8212), ' '
        # )  # Unicode 8212 is the HTML decimal entity for em dash

        for word in line.split():
            # remove punctuation and convert to lowercase
            word = word.strip(strippables)
            word = word.lower()

            if word in stop_words_list:
                continue
            else:
            # update the histogram
                book[word] = book.get(word, 0) + 1

    return book


def skip_gutenberg_header(fp):
    """Reads from fp until it finds the line that ends the header.
    fp: open file object
    """
    for line in fp:
        if line.startswith('*** START OF THE PROJECT'):
            break


# Analysis:
def total_words(book):
    """
    a function that returns the total number of words in the book by summing the values of the dictionary.
    """
    return sum(book.values())


# The following function is created to sort the book dictionary, but since the sorting mechamism is already incorporated in computing the top_10_word function, 
# the result of sort_word function will not be printed in the main function.
def sort_words(dict):
    """
    a function that takes a dictionary from the count_word function as a parameter and sort the dictionary from key with the largest value to key with the lower value (desceding order).
    """
    sorted_values = sorted(dict.values(), reverse=True)
    sorted_dict = {}
    for i in sorted_values:
        for k in dict.keys():
            if dict[k] == i:
                sorted_dict[k] = dict[k]
    return sorted_dict


def top_10_words(dict):
    """
    a function that takes the dictionary as a parameter, sort the dictionary in desceding order and returns the top 10 words with the most frequent appearance.
    """
    sorted_values = sorted(dict.values(), reverse=True)
    sorted_dict = {}
    sorted_top_10 = []
    for i in range(10):
        sorted_top_10.append(sorted_values[i])
    for i in sorted_top_10:
        for k in dict.keys():
            if dict[k] == i:
                sorted_dict[k] = dict[k]
    return sorted_dict


def compare_top_10(book_1, book_2):
    """
    a function that takes the top 10 words dictionary from both books as the parameter and compare them against each other.
    The function should return the top 10 non-overlapping words from  books.
    """
    d1 = top_10_words(book_1)
    d2 = top_10_words(book_2)
    lst = []
    for key in d1:
        if key not in d2.keys():
            lst.append(key)
    for key in d2:
        if key not in d1.keys():
            lst.append(key)
    list_with_no_duplicate = []
    for i in lst:
        if i not in list_with_no_duplicate:
            list_with_no_duplicate.append(i)
    return list_with_no_duplicate


def sentiment_analysis(nltk_text):
    """
    a function that takes the nltk_text as a paremeter and returns the Sentiment Analysis score.
    """
    score = SentimentIntensityAnalyzer().polarity_scores(nltk_text)
    return score


def compare_sentiment_analysis(nltk_text_1, nltk_text_2):
    """
    a function that takes two parameters nltk_text_1 and nltk_text_2 and returns the difference of their Sentiment Analysis scores.
    """
    dict_1 = sentiment_analysis(nltk_text_1)
    dict_2 = sentiment_analysis(nltk_text_2)
    dict_result = {}
    for key in dict_1:
        dict_result [key] = dict_2 [key] - dict_1 [key]
    return dict_result


# The following function is created based on class material and adaptations from https://pythonbasics.org/matplotlib-bar-chart/
# The code is written by myself, not directly copied.
def plot(nltk_text):
    """
    a function that takes the nltk_text dictionary as a parameter and plot the corresponding sentiment analysis score.
    The x-axis consists of the keys to the dictionary from the sentiment analysis:
    ['negative', 'neutral', 'positive', 'compound']
    The y-axis consists of the values to the dictionary from the sentiment analysis.
    """
    name_list = ['negative', 'neutral', 'positive', 'compound']
    num_list = dict.values(sentiment_analysis(nltk_text))
    plt.bar(range(len(num_list)), num_list, tick_label = name_list)
    plt.show
    return plt.show()


# The following function is adapted and modified from https://towardsdatascience.com/overview-of-text-similarity-metrics-3397c4601f50
# This function is discovered and cited as research beyond content presented in the instructions.md file.
# The code is written by myself, not directly copied.
def jaccard_similarity(book1, book2):
    """
    a function that takes book1 and book2 as parameters and return the jaccard similarity coefficient.
    """
    a = set(book1.split())
    b = set(book2.split())
    c = a.intersection(b)
    return float(len(c)) / (len(a) + len(b) - len(c))


def main():
    # please keep the following four lines of code UN-commented when running the main function
    book_Smith = process_file('An Inquiry into the Nature and Causes of the Wealth of Nations.txt', skip_header=True)
    book_Hamilton = process_file('The Federalist Papers.txt', skip_header=True)
    nltk_Smith = open('An Inquiry into the Nature and Causes of the Wealth of Nations.txt', 'r', encoding='utf-8').read()
    nltk_Hamilton = open('The Federalist Papers.txt', 'r', encoding='utf-8').read()

    # print(f'The total number of words in the book from Adam Smith are: {total_words(book_Smith)}')
    # print(f'The total number of words in the book from Alexander Hamilton are: {total_words(book_Hamilton)}')

    print(f'The top 10 words that have the most occurences in the book from Adam Smith are: {top_10_words(book_Smith)}')
    print(f'The top 10 words that have the most occurences in the book from Alexander Hamilton are: {top_10_words(book_Hamilton)}')

    print(f'The difference between Smith\'s book and Hamilton\'s book is: {compare_top_10(book_Smith, book_Hamilton)}')

    # print(f'The Score for sentiment analysis for Smith\'s book is {sentiment_analysis(nltk_Smith)}')
    # print(f'The Score for sentiment analysis for Hamilton\'s book is {sentiment_analysis(nltk_Hamilton)}')

    # print(f'The difference in score between Smith\'s book and Hamilton\'s book is {compare_sentiment_analysis(nltk_Smith, nltk_Hamilton)}')

    # print(plot(nltk_Smith))
    # plt.savefig('Smith.png')

    # print(plot(nltk_Hamilton))
    # plt.savefig('Hamilton.png')

    print(f'The Jaccard Similarity Score between the two books is {jaccard_similarity(nltk_Smith, nltk_Hamilton): 0.5f}')

if __name__ == "__main__":
    main()