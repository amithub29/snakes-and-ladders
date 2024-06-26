import pygame
from sys import exit
from random import randint

# TODO
# Resize board to 600x600
# Resize player to 60x60
#

pygame.init()   # Initialize the game
screen = pygame.display.set_mode((800, 600))    # Main screen object
pygame.display.set_caption("Snakes&Ladders")    # Title for the window
clock = pygame.time.Clock()                     # clock for the frame rate
font = pygame.font.Font("resources/magic-saturday-font/MagicSaturday-rg1OA.ttf", 50)    # Font

board_surface = pygame.image.load('images/background-main.jpg').convert()   # background image
side_panel_surface = pygame.Surface((200, 600)).convert()
side_panel_surface.fill((0, 20, 40))
font_surface = font.render('Player', True, 'Grey')
play_button_surface = pygame.image.load('resources/Play.png').convert_alpha()
play_button_rect = play_button_surface.get_rect(midbottom=(700, 550))
play_pressed_surface = pygame.image.load('resources/Play_down.png').convert_alpha()
play_pressed_rect = play_pressed_surface.get_rect(midbottom=(700, 550))

dice_images = [pygame.image.load(f'resources/kenney_boardgame-pack/PNG/Dice/dieRed{i}.png').convert_alpha()
               for i in range(1, 7)]
current_image = dice_images[0]
dice_rect = current_image.get_rect(midbottom=(700, 400))

player1_surface = pygame.image.load('resources/kenney_boardgame-pack/PNG/Pieces/player1.png').convert_alpha()
player1_rect = player1_surface.get_rect(bottomleft=(0, 600))

switch = True
clicked = False
clickable = True
move = False
num = 0
target_pos = 0

while True:     # Run the game loop
    for event in pygame.event.get():        # game exit event
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        # if event.type == pygame.MOUSEMOTION:
        #     print(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if play_button_rect.collidepoint(event.pos):
                # print('hit')
                clicked = True

        if event.type == pygame.MOUSEBUTTONUP:
            clicked = False

    screen.blit(board_surface, (0, 0))                # update the board
    screen.blit(side_panel_surface, (600, 0))         # update the side panel
    screen.blit(font_surface, (625, 50))
    screen.blit(player1_surface, (710, 45))
    screen.blit(player1_surface, player1_rect)
#    screen.blit(dice_surface1, dice_rect1)

    if clicked:
        screen.blit(play_pressed_surface, play_pressed_rect)
        if clickable:
            clickable = False
            num = randint(1, 6)
            current_image = dice_images[num - 1]
            target_pos = player1_rect.left + (num * 60)
            move = True
            print(f"current_pos: {player1_rect.left}")
            print(f"target pos: {target_pos}")
            print(f"move: {move}")
    else:
        screen.blit(play_button_surface, play_button_rect)

    screen.blit(current_image, dice_rect)

    if switch:
        if move:
            if player1_rect.left < target_pos and player1_rect.right > 570:
                switch = False
            if player1_rect.left < target_pos:
                player1_rect.left += 5
            else:
                move = False
                clickable = True
                target_pos = 0

    else:
        if move:
            if player1_rect.right > target_pos:
                player1_rect.left -= 5
            else:
                move = False

    # if player1_rect.right > 600:
    #     player1_rect.bottom -= 61
    #     switch = False
    # elif player1_rect.left < 0:
    #     player1_rect.bottom -= 60
    #     switch = True

    pygame.display.update()                 # change the frame
    clock.tick(60)                          # upper limit of the frame rate


# import pygame
#
#
# def main():
#     pygame.init()
#     logo = pygame.image.load("images/logo.jpg")
#     pygame.display.set_icon(logo)
#     pygame.display.set_caption("The game")
#
#     screen = pygame.display.set_mode((800, 600))
#     running = True
#
#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#
#
# if __name__ == '__main__':
#     main()
