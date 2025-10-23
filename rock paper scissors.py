
list = ['Rock',' Paper',' Scissors',]
user_option = input("Choose rock, paper, or scissors:   ").lower()
from random import randint
if user_option == "rock":
   computer_option = ("paper")
elif user_option == "paper":
    computer_option = ("scissors")
elif user_option == "scissors":
    computer_option = ("rock")

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


   




