from utils import *



class Wordle:
    NUM_TRIES = 6
    WORD_LENGTH = 5

    def __init__(self):
        self.__word = get_random_word()
        self.__num_tries_remaining = self.NUM_TRIES

    def get_word(self):
        return self.__word

    def check_guess(self, guess):
        statuses = [LetterStatus.INVALID.value] * self.WORD_LENGTH
        if guess == self.__word:
            statuses = [LetterStatus.CORRECT.value] * self.WORD_LENGTH
        else:
            for i in range(self.WORD_LENGTH):
                ch_guess = guess[i]
                if ch_guess == self.__word[i]:
                    status = LetterStatus.CORRECT
                elif ch_guess in self.__word:
                    status = LetterStatus.PRESENT
                else:
                    status = LetterStatus.ABSENT
                statuses[i] = status

        self.__num_tries_remaining -= 1
        return statuses

    def colorize_guess(self, guess, letter_statues):
        colorized_guess = ""

        for i in range(self.WORD_LENGTH):
            colorized_guess += colored(LetterStatusColor[letter_statues[i]], guess[i])

        return colorized_guess

    def tries_left(self):
        return self.__num_tries_remaining

    def input_guess(self):
        while True:
            guess = input("{} attempt(s) remaining.. \n Your guess: ".format(self.__num_tries_remaining)).lower()
            if guess in LTa:
                return guess
            else:
                print("Ups.. Not a valid word, try again")

    def play(self):
        while self.tries_left():
            guess = self.input_guess()
            letter_statues = self.check_guess(guess)
            colorized_guess = self.colorize_guess(guess, letter_statues)
            print(colorized_guess)
            if all_correct(letter_statues):
                print('You have guessed the right word!')
                return

        print('-- {} -- was the hidden word, good luck next time..'.format(self.__word))



