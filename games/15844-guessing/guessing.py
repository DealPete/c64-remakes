from random import random

guesses = 0

print("I'm thinking of a number from 1 to 100.")

number = int(random()*100 + 1)

while True:
	guess = int(input("What is your guess: "))
	guesses += 1
	
	if guess < number:
		print("Too low!")
	else:
		if guess > number:
			print("Too high!")
		else:
			break

print("That is correct!!!")
print("That took you", str(guesses), "guesses.")
	
