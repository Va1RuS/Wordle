import random
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
