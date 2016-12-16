from random import random

gravity = int(random()*20) + 1
wind = int(random()*40) + 1
answer = gravity * wind
tries = 0

print("Your starship is ready to takeoff.")
print("Gravity =", gravity)
print("Wind = UNKNOWN\n")

while tries < 10:
	force = int(input("Input force: "))
	if force < answer:
		print("Too low")
	if force > answer:
		print("Too high")
	if force == answer:
		print("Good takeoff, you escaped the aliens.")
		quit()
	tries += 1

print("You failed - the aliens got you.")
