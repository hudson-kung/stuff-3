
list = ['Rock',' Paper',' Scissors',]
user_option = input("Choose rock, paper, or scissors: ").lower()
from random import randint
random_number = randint (1, 3)
if random_number == 1:
   computer_option = ("rock")
elif random_number == 2:
    computer_option = ("paper")
elif random_number == 3:
    computer_option = ("scissors")

if user_option == computer_option:
    print("Tie!")
elif user_option == "rock" and computer_option == "scissors":
    print("You Win!")
elif user_option == "rock" and computer_option == "paper":
    print("You Lose!")
elif user_option == "paper" and computer_option == "rock":
    print("You Win!")
elif user_option == "paper" and computer_option == "scissors":
    print("You Lose!")
elif user_option == "scissors" and computer_option == "paper":
    print("You Win!")
else:
    print("You Lose!")


print("My Choice Was", computer_option)




   




