# 64/128 MATH QUIZ - STEVE KOOPS
# Remake by Peter Deal

from random import random

playing = True

while playing:
	a = int(random()*10)
	b = int(random()*10)

	incorrect = True
	while incorrect:
		print(a, "*", b, "=")
		answer = input("Enter the answer: ")
		if int(answer) == a*b:
			cont = input("Correct!  Do you want another? ")
			incorrect = False
			if cont == 'N' or cont == 'n':
				playing = False
		else:
			print("Wrong")
