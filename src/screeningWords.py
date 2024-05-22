"""
CSCI 720 : Project - A

Author: Shrunjala Mul

Usage: python screeningWords.py -file .\file
"""
import argparse
import math

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import warnings
from collections import Counter

def read_file(file_loc):
    """
    reads the file in pandas and returns a dataframe.

    :param file_loc: the location of the file in the system
    :return: pandas dataframe
    """
    words = list()
    with open(file_loc) as f:
        lines = f.readlines()
        for line in lines:
            words.append(line[:-1])

    return words


def parse_args():
    """
    parses the arguments.
    :return: location of the file
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("-file")
    args = parser.parse_args()  # parse arguments
    return args  # return file location given


def frequency_of_letters(words):
    """
    counts the number of times a letter occurs in this list
    :param words: list of words
    :return: dictionary with key as the letter and value as the count
    """
    count = {}
    for word in words:
        for letter in word:
            if letter not in count:
                count[letter] = 1
            else:
                count[letter] += 1
    return count

def cost_of_letters(count, total_words):
    """
    calculates the cost of each letter (probability)
    :param count: dictionary of count of each occurance of the letter
    :param total_words: total words in the list
    :return: dictionary as the cost or the probability as value and letter as key
    """
    cost = {}
    for letter in count:
        cost_of_letter = int(count[letter])/total_words
        cost[letter] = cost_of_letter
    return cost


def isUniqueChars(string):
    """
    checks if the string is made of unique characters
    :param string: string to check
    :return: boolean True if unique
    """
    # Counting frequency
    freq = Counter(string)

    if (len(freq) == len(string)):
        return True
    else:
        return False

def words_with_unique_letters(words):
    """
    gets all the words with different letters
    :param words: list of words
    :return: words with unqiue letters
    """
    unique_words = []
    for word in words:
        if isUniqueChars(word) == True:
            unique_words.append(word)
    return unique_words

def cost_of_words(cost_letters, words):
    """
    calculates the cost of each word by adding cost of each letter
    :param cost_letters: cost of each letter
    :param words: list of words
    :return: cost of words as dict
    """
    cost_words = {}
    for word in words:
        cost = 0
        for letter in word:
            cost += cost_letters[letter]
        cost_words[word] = cost
    return cost_words

def starting_frequency(words):
    """
    counts the number of times a letter has occured at the start of a word
    :param words: list of words
    :return: letter as key and count that it has occured at the start as value
    """
    count = {}
    for word in words:
        letter = word[0]
        if letter not in count:
            count[letter] = 1
        else:
            count[letter] += 1
    return count

def ending_frequency(words):
    """
    counts the number of times a letter has occured at the end of a word
    :param words: list of words
    :return: letter as key and count that it has occured at the end as value
    """
    count = {}
    for word in words:
        letter = word[-1]
        if letter not in count:
            count[letter] = 1
        else:
            count[letter] += 1
    return count

def break_ties(cost_words, starting, ending):
    """
    cosiders the starting and ending letter frequency in the cost to break ties
    :param cost_words: cost of words based on probability
    :param starting: dictionary of starting letter probabilities
    :param ending: dictionary of ending letter probabilities
    :return: updated costs with starting and ending letter considered
    """
    costs = {}
    for word in cost_words:
        cost = cost_words[word]
        cost += starting[word[0]]/26
        cost += ending[word[-1]]/26
        costs[word] = cost
    return costs

def process_next_choice(words, unique_words, cost):
    """
    takes the words guessed so far, list of possible words and costs of each letter to give the next best word.
    :param words: words guessed so far
    :param unique_words: list of possible words
    :param cost: cost of each letter
    :return: next best word
    """
    letters = []
    for word in words:
        l = list(word)
        letters += l
    next_options = list(unique_words)
    for word in unique_words:
        for i in letters:
            if i in word:
                if word in next_options:
                    next_options.remove(word)
    costs = cost_of_words(cost, next_options)
    costs = sort_dict(costs)
    return list(costs.keys())[0]



def sort_dict(d):
    """
    sort the dictionary by values in decending to maximize cost
    :param d: dictionary to sort
    :return:
    """
    sorted_dict = dict(sorted(d.items(), key=lambda x: x[1], reverse=True))
    return sorted_dict

def main():
    """
    main function
    :return:
    """
    args = parse_args()
    words = read_file(args.file)
    count = frequency_of_letters(words)
    cost = cost_of_letters(count, 26)
    #get words with unique letters only, remove all double letter words
    unique_words = words_with_unique_letters(words)
    cost_words = cost_of_words(cost, unique_words)
    cost_words = dict(sorted(cost_words.items(), key=lambda x:x[1], reverse=True))

    # break ties with most common starting and ending
    updated_cost = break_ties(cost_words,starting_frequency(words), ending_frequency(words))
    updated_cost = dict(sorted(updated_cost.items(), key=lambda x:x[1], reverse=True))

    #first
    first_choice = list(updated_cost.keys())[0]
    final_words = []
    final_words.append(first_choice)

    #second
    unique_words.remove(first_choice)
    next_choice = process_next_choice(final_words, unique_words, cost)
    final_words.append(next_choice)

    #third
    unique_words.remove(next_choice)
    last_choice = process_next_choice(final_words, unique_words, cost)
    final_words.append(last_choice)

    print("Cost Function = letter frequency (objective function) +"
          " best starting and ending letters (regularization)")

    print("\nThe top 3 words are :")
    for w in final_words:
        print(w)







if __name__ == '__main__':
    main()