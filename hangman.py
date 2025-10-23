import random
def hangman():
    lives = 6
    print("  o ")
    print(" /|\ ")
    print(" / \ ")
    print("The Word Has 5 Letters")
    words = ["river", "plant", "dream", "sound", "light", "chair", "smile", "phone", "world", "laugh", "drink", "music", "green", "money", "house", "dance", "beach", "sleep", "story", "apple", "stone", "clock", "table", "cloud", "bread", "water", "heart", "paper", "happy"]
    chosen_word = random.choice(words)
    display = ["_" for _ in chosen_word]
    guessed_letter = []
    while lives > 0 and "_" in display:
        print(display)
        user_option = input("Choose a letter:   ")
        if user_option in guessed_letter:
            lives = (lives -1)
            print("You have lost a life for guessing an already guessed. You have", lives, "lives left.")
            continue
                
        guessed_letter.append(user_option)

        if user_option in chosen_word:
            for i in range(len(chosen_word)):
                if user_option == chosen_word[i]:
                    display[i] = user_option

        elif not user_option in chosen_word:
            lives = (lives -1)
            print("You guessed wrong, you have", lives, "lives left.")

            if lives == 5:
                print("  o ")
                print(" /|\ ")
                print(" /  ")
            elif lives == 4:
                print("  o ")
                print(" /|\ ")
            elif lives == 3:
                print("  o ")
                print(" /| ")
            elif lives == 2:
                print("  o ")
                print("  | ")
            elif lives == 1:
                print("  o ")
                    
    if "_" not in display:

        print("You Win!")

        print(display)

if __name__== "__main__":
    hangman()



    