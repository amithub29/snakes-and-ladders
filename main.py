import pygame
from sys import exit
from random import randint

board_size = (800, 600)
window_title = "Snakes&Ladders"
font_name = "fonts/MagicSaturday-rg1OA.ttf"
font_size = 50
text_position = (625, 50)
main_board_image = "images/background-main.jpg"
game_over_image = "images/background-reset.png"
side_panel_size = (200, 600)
side_panel_color = (0, 20, 40)
side_panel_text = "Player 1"
side_panel_text_color = "Grey"
play_button_image = "resources/Play.png"
play_pressed_image = "resources/Play_down.png"
play_button_position = (700, 550)
dice_position = (700, 400)
player1_image = "resources/Pieces/player1.png"
player2_image = "resources/Pieces/player2.png"
static_player1_image = "resources/Pieces/player1.png"
static_player2_image = "resources/Pieces/player2.png"
ladders = {4: 14, 9: 31, 20: 38, 28: 84, 40: 59, 51: 67, 63: 81}
snakes = {17: 7, 64: 60, 89: 26, 95: 75, 99: 78}


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
    def __init__(self, screen, image, location):
        self.image = image
        self.position = 1
        self.target_pos = 1
        self.switch = False
        self.screen = screen
        self.player_surface = pygame.image.load(self.image).convert_alpha()
        self.player_rect = self.player_surface.get_rect(bottomleft=location)

    def render_player(self):
        self.screen.blit(self.player_surface, self.player_rect)

    def move(self):
        if self.position % 10 == 0:
            self.player_rect.bottom -= 5
            if self.player_rect.bottom % 60 == 0:
                self.position += 1
                print(self.position)
        else:
            if (self.position // 10) % 2 == 0:
                self.player_rect.left += 5
            else:
                self.player_rect.left -= 5

            if self.player_rect.left % 60 == 0:
                self.position += 1
                print(self.position)

    def check_ladders(self):
        for key in ladders:
            if self.position == key:
                self.target_pos = ladders[key]
                break

    def check_snakes(self):
        for key in snakes:
            if self.position == key:
                self.target_pos = snakes[key]
                break

    def reverse_move(self):
        if (self.position - 1) % 10 == 0:
            self.player_rect.bottom += 5
            if self.player_rect.bottom % 60 == 0:
                self.position -= 1
        else:
            if ((self.position - 1) // 10) % 2 == 0:
                self.player_rect.left -= 5
            else:
                self.player_rect.left += 5

            if self.player_rect.left % 60 == 0:
                self.position -= 1


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
    def __init__(self, screen, image):
        self.image = image
        self.turn = True
        self.screen = screen
        self.running = True
        self.board_surface = pygame.image.load(main_board_image).convert()  # Main board surface
        self.side_panel_surface = pygame.Surface(side_panel_size).convert()  # Side Panel surface
        self.side_panel_surface.fill(side_panel_color)  # Color of side panel
        self.font = pygame.font.Font(font_name, font_size)  # Font
        self.font_surface = self.font.render(side_panel_text, True, side_panel_text_color)  # Font surface
        self.game_over_surface = pygame.image.load(game_over_image).convert()
        self.static_player_surface = pygame.image.load(image).convert_alpha()

    def render_board(self):
        self.screen.blit(self.board_surface, (0, 0))  # update the board
        self.screen.blit(self.side_panel_surface, (600, 0))  # update the side panel
        self.screen.blit(self.font_surface, text_position)   # update the font

    def render_gameover(self):
        self.screen.blit(self.game_over_surface, (0, 0))

    def render_static_piece(self):
        self.static_player_surface = pygame.image.load(self.image).convert_alpha()
        self.screen.blit(self.static_player_surface, (710, 45))


switch = True
clicked = False
clickable = True
move = False


def main():
    pygame.init()  # Initialize the game
    screen = pygame.display.set_mode(board_size)  # Main screen object
    pygame.display.set_caption(window_title)  # Title for the window
    clock = pygame.time.Clock()  # Clock for the frame rate

    board = Board(screen, static_player1_image)
    button = Button(screen)
    player1 = Player(screen, player1_image, (0, 600))
    player2 = Player(screen, player2_image, (0, 600))
    dice = Dice(screen)
    player = player1

    while True:  # Run the game loop
        for event in pygame.event.get():  # game exit event
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button.play_button_rect.collidepoint(event.pos):
                    button.clicked = True
                    dice.roll_dice()
                    if board.turn:
                        player = player1
                    else:
                        player = player2
                    if dice.number != 6:
                        board.turn = not board.turn
                        if player == player1:
                            print("Player1")
                            board.image = static_player2_image
                        elif player == player2:
                            print("Player2")
                            board.image = static_player1_image

                    if player.position + dice.number <= 100:
                        player.target_pos = player.position + dice.number

            if event.type == pygame.MOUSEBUTTONUP:
                button.clicked = False

        if board.running:
            board.render_board()
            player1.render_player()
            player2.render_player()
            board.render_static_piece()
            button.render_button()
            dice.render_dice()
        else:
            board.render_gameover()

        if player.position == 100:
            board.running = False
        elif player.position == player.target_pos:
            player.check_ladders()
            player.check_snakes()
        elif player.position > player.target_pos:
            player.reverse_move()
        elif player.position < player.target_pos:
            player.move()

        pygame.display.update()  # change the frame
        clock.tick(60)  # upper limit of the frame rate


if __name__ == '__main__':
    main()
