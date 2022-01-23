import string
import random

# Define function which loads wordlist. 
# https://github.com/dwyl/english-words
# https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt
def load_words():
    with open('words_alpha.txt') as word_file:
        valid_words = set(word_file.read().split())
    return valid_words


# Define globals
VALID_CHARS = string.ascii_lowercase
MAX_ATTEMPTS = 6
SOLUTION_LENGTH = 5
VALID_WORDS = filter(lambda word: len(word) == SOLUTION_LENGTH, load_words())
SOLUTION = random.choice(list(VALID_WORDS))
# VALID_WORDS = ['testy', 'zesty', 'messy', 'chess', 'fussy']
# SOLUTION = 'zesty'


def is_valid_guess(guess):
	# Length
	if len(guess) != SOLUTION_LENGTH: return False
	# Valid word
	if guess not in VALID_WORDS: return False
	# Chars
	# if not all([char in VALID_CHARS for char in guess]): return False
	return True


def evalutate_guess(guess):
	# Return a dictionary evaluating the guess against the solution. 
	if guess == SOLUTION: return {'success': True}
	if not is_valid_guess(guess): exit('Not a valid guess.')

	evaluation = {'success': False, 'positions': {}}
	for position in range(SOLUTION_LENGTH):
		char_in_solution = guess[position] in SOLUTION
		char_in_right_position = guess[position] == SOLUTION[position]		

		evaluation['positions'][position] = \
			{
				'in_solution': char_in_solution,
				'in_right_position': char_in_right_position,
				'char': guess[position],
			}
	return evaluation


def solve():
	# Solve world
	# Our initial universe of possible solutions if the list of valid words.
	possible_solutions = VALID_WORDS
	attempt = 0
	while attempt < MAX_ATTEMPTS:
		attempt += 1 

		# We make a random guess from the solutions which are still possible.
		# This algorithm can be made more efficient by making our guess intelligently
		# instead of randomly.
		guess = random.choice(possible_solutions)
		print('Attempt: ' + str(attempt) + ', Guess: ' + guess + ', Possible solutions remaining: ' + str(len(possible_solutions)))
		
		evaluation = evalutate_guess(guess)
		if evaluation['success']: exit('Solved: ' + guess)
		
		# Once we have the results of our evaluation, we want to prune words from the list of possible solutions:
		for position in range(SOLUTION_LENGTH):
			possible_solutions = filter(lambda possible_solution: (guess[position] in possible_solution) == (evaluation['positions'][position]['in_solution']), possible_solutions)
			possible_solutions = filter(lambda possible_solution: (guess[position] == possible_solution[position]) == (evaluation['positions'][position]['in_right_position']), possible_solutions)
	exit('Failed. Could not solve within ' + str(MAX_ATTEMPTS) + ' attempts.')


def main():
	print('Sssshhhh... the solution is: ' + SOLUTION + '\n\nRunning solver...')
	solve()

if __name__ == "__main__":
	main()
