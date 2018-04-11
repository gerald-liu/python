import random               # Import the 'random' library

# Generate a new integer random number
target = random.randint(1, 100)
print("I am thinking of a number. What number am I thinking of?")

# Do the main game loop
finished = False            # This is true if the game has finished
count = 0
while not finished:
    # Get the user's guess
    guess_input = int(input("Please enter a number between 1 and 100: "))
    count = count + 1
    # Check the user's guess
    if guess_input < 1 or guess_input > 100:
        print("Please enter an integer number between 1 and 100.")
    elif guess_input > target:
        print("Too high.")
    elif guess_input < target:
        print("Too low.")
    else:
        print("You got it! My number is", target, "\nIt took you", count, "times to get the number!")
        finished = True

# At this point, the game is finished
