#
# Programmed by: Jake Jongewaard
#
# Provides routines for processing data and gathering useful
# statistics.
#==============================================================


import collections
import operator
import random
import re

import numpy as np

from src import data_loader as loader


def get_population_prob_dist(population, prev_word_array, review_batch):
    """
    Calculates the distribution of the probabilities of each word in the population
    occuring after the previous words that have been generated.

    :param population: Array of words that represents the individuals of a population
    :param prev_word_array: All of the previous words that have been generated
    :param review_batch: The batch of reviews that is being used to calculate the dist.
    :return: The probability distribution of the population
    """
    def prob_of_next_word(next_word):
        """
        Calculates the probability of of a given word occuring after the previously
        generated words.

        :param next_word: Word to calculate the probability of
        :return: The probability of next_word occuring after the previously generated words
        """
        compare_phrase = np.append(prev_word_array, next_word)
        resized_batch = np.resize(review_batch, (len(compare_phrase)))
        count = 0

        for phrase in resized_batch:
            if np.array_equal(phrase, compare_phrase):
                count += 1

        return count / (resized_batch.shape[0] * resized_batch.shape[1])

    prob_dist = {}

    for individual in population:
        prob_dist[individual] = prob_of_next_word(individual)

    return prob_dist


def get_expected_prob_dist(prev_word_array, review_batch):
    """
    Calculate the distribution of probabilities of all the unique words found in the review_batch
    occuring after the previously generated words.

    :param prev_word_array: Previously generated words
    :param review_batch: Batch of reviews used to calculate the distribution
    :return: Expected probability distribution found in the review batch
    """
    prob_dist = {}
    all_words = loader.get_all_words(review_batch)
    all_words_ = list(map(lambda x: len(x), all_words))
    sorted_words = all_words[np.argsort(all_words)]
    count = 0

    for i in range(len(sorted_words)):
        if sorted_words[i] == sorted_words[i+1]:
            count += 1
        else:
            prob_dist[sorted_words[i-1]] = count
            count = 0

    return prob_dist


def calc_substring_freq_dist(population_dist, target_dist, substring_size):
    """


    :param population_dist:
    :param substring_size:
    :return:
    """
    begin = 0
    end = substring_size - 1

    def get_comparison_substrings(substring_array, min_num_substrings=round(len(population_dist))):
        """

        :param substring_array:
        :param min_num_substrings:
        :return:
        """
        for individual in population_dist:
            rand_index = random.randint(0, len(population_dist) - end)
            parent = individual[begin + rand_index:end + rand_index]
            np.append(substring_array, parent)

        substring_array = np.unique(substring_array)
        if len(substring_array) < min_num_substrings:
            get_comparison_substrings(substring_array, min_num_substrings)

    freq_dist = {}
    substring_array = np.array()
    freq = 0

    get_comparison_substrings(substring_array)
    for substring in substring_array:
        freq = len([m.start for m in re.finditer(substring, target_dist)])
        freq_dist[substring] = freq

    ordered_dict = collections.OrderedDict(sorted(freq_dist.items(), key=operator.itemgetter(1)))
    return ordered_dict



