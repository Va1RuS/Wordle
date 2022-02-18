import random
import string

from data import *
from colorama import Fore, Style
from enum import Enum


class LetterStatus(Enum):
    CORRECT = 2
    PRESENT = 1
    ABSENT = 0
    INVALID = -1


LetterStatusColor = {
    LetterStatus.CORRECT: Fore.GREEN,
    LetterStatus.PRESENT: Fore.YELLOW,
    LetterStatus.ABSENT: Fore.BLUE,
    LetterStatus.INVALID: Fore.RED}


def get_random_word():
    return random.choice(La)


def colored(color: Fore, text: str):
    return f'{color}{text}{Style.RESET_ALL}'


def all_correct(letter_statues):
    for status in letter_statues:
        if status != LetterStatus.CORRECT:
            return False
    return True


def get_frequencies(words):
    char_frequencies = {}
    for ch in list(string.ascii_lowercase):
        char_frequencies[ch] = [0, 0, 0, 0, 0]
    for word in words:
        for i, ch in enumerate(word):
            freqs = char_frequencies.get(ch, [0, 0, 0, 0, 0])
            freqs[i] += 1
            char_frequencies[ch] = freqs
    return char_frequencies


def word_scores(words, frequencies):
    words_scores = {}
    max_freq = [0] * 5
    for ch in frequencies:
        for i in range(5):
            if max_freq[i] < frequencies[ch][i]:
                max_freq[i] = frequencies[ch][i]
    for word in words:
        score = 1
        for i in range(5):
            ch = word[i]
            score *= 1 + (frequencies[ch][i] - max_freq[i]) ** 2
        words_scores[word] = score
    return words_scores


def pick_best_word(possible_words, allowed_words):

    frequencies = get_frequencies(possible_words)
    words = word_scores(possible_words, frequencies)
    return min(words, key=words.get)
