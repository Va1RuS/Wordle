from utils import *


class WordleCracker:
    NUM_TRIES = 6
    WORD_LENGTH = 5

    def __init__(self):
        self.__word = get_random_word()
        self.__La = La
        self.__Ta = Ta
        # self.__LTa = self.__La + self.__Ta
        self.__num_tries_remaining = self.NUM_TRIES

    def get_word(self):
        return self.__word

    def set_random_word(self, word):
        self.__word = get_random_word()
        self.__La = La
        self.__Ta = Ta
        # self.__LTa = self.__La + self.__Ta
        self.__num_tries_remaining = self.NUM_TRIES

    def set_new_word(self, word):
        self.__word = word
        self.__La = La
        self.__Ta = Ta
        self.__num_tries_remaining = self.NUM_TRIES

    def tries_left(self):
        return self.__num_tries_remaining

    def input_guess(self):
        while True:
            guess = input("{} attempt(s) remaining.. \n Your guess: ".format(self.__num_tries_remaining)).lower()
            if guess in self.__La or guess in self.__Ta:
                return guess
            else:
                print("Ups.. Not a valid word, try again")

    def discard_extra_words(self, guess, letter_statuses):
        for i in range(len(letter_statuses)):
            ch = guess[i]
            status = letter_statuses[i]
            if status == LetterStatus.CORRECT:
                self.__La = list(filter(lambda word: word[i] == ch, self.__La))
                self.__Ta = list(filter(lambda word: word[i] == ch, self.__Ta))
            elif status == LetterStatus.PRESENT:
                self.__La = list(filter(lambda word: ch in (word[:i] + word[i + 1:]), self.__La))
                self.__Ta = list(filter(lambda word: ch in (word[:i] + word[i + 1:]), self.__Ta))
            elif status == LetterStatus.ABSENT:
                self.__La = list(filter(lambda word: ch not in word, self.__La))
                self.__Ta = list(filter(lambda word: ch not in word, self.__Ta))

        if guess in self.__La:
            self.__La.remove(guess)
        if guess in self.__Ta:
            self.__Ta.remove(guess)

    def check_guess(self, guess):
        statuses = []
        for i in range(self.WORD_LENGTH):
            ch_guess = guess[i]
            if ch_guess == self.__word[i]:
                status = LetterStatus.CORRECT
            elif ch_guess in self.__word:
                status = LetterStatus.PRESENT
            else:
                status = LetterStatus.ABSENT
            statuses.append(status)

        self.__num_tries_remaining -= 1
        return statuses

    def colorize_guess(self, guess, letter_statues):
        colorized_guess = ""
        for i in range(self.WORD_LENGTH):
            colorized_guess += colored(LetterStatusColor[letter_statues[i]], guess[i])

        return colorized_guess

    def crack_interactive(self):
        while self.tries_left():
            guess = self.input_guess()
            letter_statuses = self.check_guess(guess)
            colorized_guess = self.colorize_guess(guess, letter_statuses)
            print(colorized_guess)
            if all_correct(letter_statuses):
                print('You have guessed the right word!')
                return
            if len(self.__La) == 1:
                print('Next guess is 100% correct have guessed the right word! {}'.format(self.__La[0]))
            self.discard_extra_words(guess, letter_statuses)
            print(self.__La)
            print(self.__Ta)
            print("After this attempt Ta length: {}   La length: {}".format(len(self.__Ta), len(self.__La)))

        print('-- {} -- was the hidden word, good luck next time..'.format(self.get_word()))

    def crack(self):
        guesses = 0
        while len(self.__La) != 1:
            guesses += 1
            guess = pick_best_word(self.__La, self.__Ta)
            letter_statuses = self.check_guess(guess)
            if all_correct(letter_statuses):
                break
            self.discard_extra_words(guess, letter_statuses)

        return self.__word, guesses

    def crack_all(self):
        word_guesses = []
        for word in La:
            self.set_new_word(word)
            word, guesses = self.crack()
            word_guesses.append(guesses)
            La.remove(word)
