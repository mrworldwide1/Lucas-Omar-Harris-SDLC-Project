# Name: ByteFight
# Description: ICS4U SDLC summative project, a fun educational computer science game inspired by Math prodigy.
# Date: November 28, 2023
# By: Omar S, Lucas L, Harris V
# some features like soundtrack dont work on replit - check the github

import pygame
import sys
import random
from button import Button
from cs_questions import computer_science_questions

## Setup ##

# Other variables so fewer values are hardcoded
game_name = "ByteFight"

# Setup display
pygame.init()
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption(game_name)
programIcon = pygame.image.load('battle_arena.png').convert_alpha() # load icon image as a Surface then change icon
pygame.display.set_icon(programIcon)
clock = pygame.time.Clock()

# Get fonts
title_font_size = 72
title_font = pygame.font.Font('Retro Gaming.ttf', title_font_size)
button_font_size = 36
button_font = pygame.font.Font('Retro Gaming.ttf', button_font_size)
tiny_font_size = 18
tiny_font = pygame.font.Font('Retro Gaming.ttf', tiny_font_size)
character_font_size = 14 
character_font = pygame.font.Font('Retro Gaming.ttf', character_font_size)

# Health bar RGB colors
health_bar_colour_enemy = ("purple")
health_bar_colour_player = (0, 255, 0)

# Music that may play in battle - randomly chosen each battle
battleSoundtracks = ["xDeviruchi - Decisive Battle.wav", "xDeviruchi - And The Journey Begins .wav", "xDeviruchi - The Icy Cave .wav", "xDeviruchi - Exploring The Unknown.wav"]

# Enemy/player names
player_name = "Wizard"
enemy_name = "Earth Creature"

# Retrieve save data file with wins/losses, put each line in list
save_file = open("save.txt", "r+")
lines = save_file.readlines()
wins = lines[1]
losses = lines[4]
save_file.close()

# Displays text onto screen surface
def display_text(text, font, x, y, colour):
    text_surface = font.render(text, True, colour)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

# Custom function that fits background image onto entire screen
def display_background(image):
    bg = pygame.image.load(image).convert_alpha()
    bg = pygame.transform.scale(bg, (screen_width, screen_height))
    screen.blit(bg, (0, 0))

# Custom function to play soundtracks
def play_soundtrack(file):
    pygame.mixer.music.load(file)
    pygame.mixer.music.play(-1, 0, 4000)

# Custom function that fades out whatevers currently playing
def stop_soundtrack():
    pygame.mixer.music.fadeout(1000)

# Tell player to keep console open
print("Please don't close this console, you'll need it to answer the questions!")

## Game States ##

def title_screen():
  stop_soundtrack()
  play_soundtrack("xDeviruchi - Title Theme .wav")

  while True:
      # Show title, background, score
      display_background('title_screen_bg.jpg')
      display_text(game_name, title_font, screen_width/2, screen_height/6, 'white')
      display_text("By: Lucas L, Omar S, Harris V - for ICS4U", tiny_font, screen_width/2, screen_height/1.08, 'white')
      display_text(f"Wins: {wins}", tiny_font, screen_width/2, screen_height/1.25, 'white')
      display_text(f"Losses: {losses}", tiny_font, screen_width/2, screen_height/1.18, 'white')

    # Menu choices
      computer_science_button = Button("Play", button_font, screen_width/14, screen_height/2.5, "green", "white", 120, 50)
      quit_button = Button("Quit", button_font, screen_width/14, screen_height/1.8, "red", "white", 120, 50)
      computer_science_button.display()
      quit_button.display()

      # Pygame event queue
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              pygame.quit()
              sys.exit()
        # Switch game state if buttons clicked 
          elif event.type == pygame.MOUSEBUTTONUP:
              if computer_science_button.collide():
                  computer_science_arena()
              elif quit_button.collide():
                  pygame.quit()
                  sys.exit()

      # Updates everything
      pygame.display.update()
      clock.tick(60)


def computer_science_arena():
    # Sets enemy and player health points 
    player_health = 100 
    enemy_health = 100

    # Store previously asked questions to prevent repeats
    asked_questions = []

    # Music
    stop_soundtrack()
    play_soundtrack(random.choice(battleSoundtracks))

    while True:
        # Show background
        display_background('battle_arena.png')
      
        # Displays health bars
        pygame.draw.rect(screen, health_bar_colour_player, (20, 20, player_health * 2.2, 30))
        pygame.draw.rect(screen, health_bar_colour_enemy, (400, 20, enemy_health * 2.2, 30))
      
        # Displays player and enemy names 
        display_text(player_name, character_font, 50, 10, 'white')
        display_text(enemy_name, character_font, 465, 10, 'white')
      
        # Displays fight and heal buttons
        fight_button = Button("Fight", button_font, screen_width / 12, screen_height - 100, "brown", "white", 120, 50)
        heal_button = Button("Heal", button_font, 3 * screen_width / 4.10, screen_height - 100, "brown", "white", 120, 50)
        fight_button.display()
        heal_button.display()
  
        # Event queue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                # Ask question when fight clicked
                if fight_button.collide():

                    # Ensures same question is not asked twice
                    while True:
                        question_data = random.choice(computer_science_questions)
                        if question_data["question"] not in asked_questions:
                            asked_questions.append(question_data["question"])  
                            break

                    question = question_data["question"]
                    options = question_data["options"]
                    answer = input(f"{question} ({','.join(options)}\n Answer: ")

                    # Attack enemy if correct answer, otherwise damage player
                    if answer.upper() == question_data["answer"]:
                        enemy_health -= random.randint(10, 20)
                        print("You attacked!")
                    else:
                        damage = random.randint(10, 20)
                        player_health -= damage
                        if damage > 15:
                            print("Enemy lands crit! You missed!") 
                        else:
                            print("Enemy lands hit! You missed!")
                          
                # Ask questions if heal clicked
                elif heal_button.collide():
                    # Ensures same question is not asked twice
                    while True:
                        question_data = random.choice(computer_science_questions)
                        if question_data["question"] not in asked_questions:
                            asked_questions.append(question_data["question"])  
                            break

                    question = question_data["question"]
                    options = question_data["options"]
                    answer = input(f"{question} ({','.join(options)}\n Answer: ")

                    # Heal player up to max health of 100 if answer correct, otherwise harm player
                    if answer.upper() == question_data["answer"]:
                        player_health += random.randint(5, 10)
                        player_health = min(100, player_health)
                        if player_health < 100:
                            print("You healed!")
                        elif player_health >= 100:
                            print("You healed and are at max health!")
                    else:
                        damage = random.randint(15, 60)
                        player_health -= damage
                        if damage > 20:
                            print("You missed!") 
                        else:
                            print("Enemy lands Hit! You missed!") 
                          
        # Game over or victory screen
        if player_health <= 0:
            display_text("Game Over", title_font, screen_width / 2, screen_height / 1.5, 'red')
            pygame.display.update()
            pygame.time.delay(2000)

            # Update save returning list containing each line as an element in read/write mode
            # save_file = open("save.txt", "r+")
            # lines = save_file.readlines()
            # losses += 1
            # lines[4] = losses
            # # update specific line
            # save_file.writelines(lines)
            # save_file.close()

            stop_soundtrack()
            play_soundtrack("xDeviruchi - Title Theme .wav")
            return
        
        elif enemy_health <= 0:
            display_text("You Win!", title_font, screen_width / 2, screen_height / 2, 'green')
            pygame.display.update()
            pygame.time.delay(2000)

            stop_soundtrack()
            play_soundtrack("xDeviruchi - Title Theme .wav")
            return

        # Updates everything
        pygame.display.update()
        clock.tick(60)

# Starts game 
title_screen()
