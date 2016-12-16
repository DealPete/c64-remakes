from random import random

print("I'm thinking of a number between 1 and one million.")

number = int(random()*1000000 + 1)

guess = int(input("What is your guess: "))

if guess == number:
	print("You win.")
else:
	print("Sorry, the number was", number)
	print("You lose.")
