import pygame
from sys import exit
from random import randint

board_size = (800, 600)
window_title = "Snakes&Ladders"
font_name = "fonts/MagicSaturday-rg1OA.ttf"
font_size = 50
main_board_image = "images/background-main.jpg"
side_panel_size = (200, 600)
side_panel_color = (0, 20, 40)
side_panel_text = "Player 1"
side_panel_text_color = "Grey"
play_button_image = "resources/Play.png"
play_pressed_image = "resources/Play_down.png"
play_button_position = (700, 550)
dice_position = (700, 400)
player_image = "resources/Pieces/player1.png"


class Dice:
    def __init__(self, screen):
        self.number = 0
        self.screen = screen
        self.dice_images = [pygame.image.load(f'resources/Dice/dieRed{i}.png').convert_alpha()
                            for i in range(1, 7)]
        self.current_image = self.dice_images[0]
        self.dice_rect = self.current_image.get_rect(midbottom=dice_position)

    def render_dice(self):
        self.screen.blit(self.current_image, self.dice_rect)

    def roll_dice(self):
        self.number = randint(1, 6)
        self.current_image = self.dice_images[self.number - 1]


class Player:
    def __init__(self, screen):
        self.player_x = 0
        self.player_y = 600
        self.position = 1
        self.target_pos = 0
        self.switch = False
        self.screen = screen
        self.player_surface = pygame.image.load(player_image).convert_alpha()
        self.player_rect = self.player_surface.get_rect(bottomleft=(self.player_x, self.player_y))

    def render_static_player(self):
        self.screen.blit(self.player_surface, (710, 45))
        self.screen.blit(self.player_surface, self.player_rect)

    def move(self):
        if self.position % 10 == 0:
            self.player_rect.bottom -= 1
            if self.player_rect.bottom % 60 == 0:
                self.position += 1
        else:
            if (self.position // 10) % 2 == 0:
                self.player_rect.left += 1
            else:
                self.player_rect.left -= 1

            if self.player_rect.left % 60 == 0:
                self.position += 1


class Button:
    def __init__(self, screen):
        self.screen = screen
        self.clicked = False
        self.clickable = True
        self.play_button_surface = pygame.image.load(play_button_image).convert_alpha()
        self.play_button_rect = self.play_button_surface.get_rect(midbottom=play_button_position)
        self.play_pressed_surface = pygame.image.load(play_pressed_image).convert_alpha()
        self.play_pressed_rect = self.play_pressed_surface.get_rect(midbottom=play_button_position)

    def render_button(self):
        if self.clicked:
            self.screen.blit(self.play_pressed_surface, self.play_pressed_rect)
        else:
            self.screen.blit(self.play_button_surface, self.play_button_rect)


class Board:
    def __init__(self, screen):
        self.screen = screen
        self.board_surface = pygame.image.load(main_board_image).convert()  # Main board surface
        self.side_panel_surface = pygame.Surface(side_panel_size).convert()  # Side Panel surface
        self.side_panel_surface.fill(side_panel_color)  # Color of side panel
        self.font = pygame.font.Font(font_name, font_size)  # Font
        self.font_surface = self.font.render(side_panel_text, True, side_panel_text_color)  # Font surface

    def render_board(self):
        self.screen.blit(self.board_surface, (0, 0))  # update the board
        self.screen.blit(self.side_panel_surface, (600, 0))  # update the side panel
        self.screen.blit(self.font_surface, (625, 50))


switch = True
clicked = False
clickable = True
move = False


def main():
    pygame.init()  # Initialize the game
    screen = pygame.display.set_mode(board_size)  # Main screen object
    pygame.display.set_caption(window_title)  # Title for the window
    clock = pygame.time.Clock()  # Clock for the frame rate

    board = Board(screen)
    button = Button(screen)
    player = Player(screen)
    dice = Dice(screen)

    while True:  # Run the game loop
        for event in pygame.event.get():  # game exit event
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button.play_button_rect.collidepoint(event.pos):
                    button.clicked = True
                    dice.roll_dice()
                    player.target_pos = player.position + dice.number

            if event.type == pygame.MOUSEBUTTONUP:
                button.clicked = False

        board.render_board()
        player.render_static_player()
        button.render_button()
        dice.render_dice()
        if player.position < player.target_pos:
            player.move()

        pygame.display.update()  # change the frame
        clock.tick(60)  # upper limit of the frame rate

        #    screen.blit(dice_surface1, dice_rect1)

        # if clicked:
        #     screen.blit(play_pressed_surface, play_pressed_rect)
        #     if clickable:
        #         clickable = False
        #         num = randint(1, 6)
        #         current_image = dice_images[num - 1]
        #         target_pos = player1_rect.left + (num * 60)
        #         move = True
        #         print(f"current_pos: {player1_rect.left}")
        #         print(f"target pos: {target_pos}")
        #         print(f"move: {move}")
        # else:
        #     screen.blit(play_button_surface, play_button_rect)
        #
        # screen.blit(current_image, dice_rect)
        #
        # if switch:
        #     if move:
        #         if player1_rect.left < target_pos and player1_rect.right > 570:
        #             switch = False
        #         if player1_rect.left < target_pos:
        #             player1_rect.left += 5
        #         else:
        #             move = False
        #             clickable = True
        #             target_pos = 0
        #
        # else:
        #     if move:
        #         if player1_rect.right > target_pos:
        #             player1_rect.left -= 5
        #         else:
        #             move = False

        # if player1_rect.right > 600:
        #     player1_rect.bottom -= 61
        #     switch = False
        # elif player1_rect.left < 0:
        #     player1_rect.bottom -= 60
        #     switch = True


if __name__ == '__main__':
    main()

