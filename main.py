import pygame
from sys import exit

class Board:
    def __init__(self):
        self.grid = [['', '', ''],
                     ['', '', ''],
                     ['', '', ''],]
        self.grid_rect_list = []
        self.turns = 0
        self.game_state = 'Xturn'

        for i in range(9):
            x = i // 3
            y = i % 3
            new_rect = pygame.Rect(175 + 150 * x, 75 + 150 * y,150,150)
            self.grid_rect_list.append(new_rect)

    def checkCollision(self, x_turn):
        if pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()
            for i in range(9):
                x = i // 3
                y = i % 3
                if self.grid_rect_list[i].collidepoint(mouse_pos):
                    if not self.grid[x][y]:
                        if x_turn:
                            self.grid[x][y] = 'X'
                            self.turns += 1
                            x_turn = False
                            self.game_state = 'Oturn'
                            move_sound.play()
                            return x_turn
                        else:
                            self.grid[x][y] = 'O'
                            self.turns += 1
                            x_turn = True
                            self.game_state = 'Xturn'
                            move_sound.play()
                            return x_turn
                
        return x_turn
                            
    def displayMoves(self):
 
        main_text = ""
        match self.game_state:
            case "Xturn":
                main_text = "Vez do jogador X"
        match self.game_state:
            case "Oturn":
                main_text = "Vez do jogador O"
        match self.game_state:
            case "draw":
                main_text = "Ihh deu Velha! Aperte espaco para reiniciar!"
        match self.game_state:
            case "X":
                main_text = "X VENCEU! Aperte espaco para reiniciar!"
        match self.game_state:
            case "O":
                main_text = "O VENCEU! Aperte espaco para reiniciar!"
        
        self.text_surf = main_font.render(main_text, False, '#031c29')
        self.text_rect = self.text_surf.get_rect(center = (400, 50))
        screen.blit(self.text_surf, self.text_rect)
            
        for i in range(9):
            x = i // 3
            y = i % 3
            if self.grid[x][y] == 'X':
                screen.blit(playerX_surf, (200 + 150 * x, 100 + 150 * y))
            if self.grid[x][y] == 'O':
                screen.blit(playerO_surf, (200 + 150 * x, 100 + 150 * y))
    
    def checkWin(self):

        diagonal1 = set()
        diagonal2 = set()
        for i in range(len(self.grid)):
            if len(set(self.grid[i])) == 1 and self.grid[i][0]:
                self.game_state = self.grid[i][0]
                return self.grid[i][0]
            column = set()
            r = -i - 1
            diagonal1.add(self.grid[i][i])
            diagonal2.add(self.grid[i][r])
            for j in range(len(self.grid)):
                column.add(self.grid[j][i])
            if len(column) == 1 and self.grid[j][i]:
                self.game_state = self.grid[j][i]
                return self.grid[j][i]
        if len(diagonal1) == 1 and self.grid[i][i]:
            self.game_state = self.grid[i][i]
            return self.grid[i][i]
        if len(diagonal2) == 1 and self.grid[i][r]:
            self.game_state = self.grid[i][r]
            return self.grid[i][r]
    
        if self.turns >= 9:
            self.game_state = 'draw'
            return 'draw'   
         
        return None
        
#initializing pygame and window
pygame.init()
w, h = 800, 600
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("Jogo da velha")
clock = pygame.time.Clock()
board = Board()
#Surfaces
playerX_surf = pygame.image.load(r'graphics\playerX.png').convert_alpha()
playerO_surf = pygame.image.load(r'graphics\playerO.png').convert_alpha()
#text
main_font = pygame.font.Font(r'font\Pixeltype.ttf', 50)

"""color pallete:
    dark blue #031c29
    blue #0a6874
    light blue #88c9d1
    light yellow #fbf7d1
    light pink #d96297
    dark pink #a8275d"""
bg_color = '#fbf7d1'
line_color = '#a8275d'

#sounds
move_sound = pygame.mixer.Sound(r"sounds\moveSound.wav")
bg_music = pygame.mixer.Sound(r'sounds\bgMusic.mp3')
victory_sound = pygame.mixer.Sound(r'sounds\victory.wav')
bg_music.set_volume(0.3)
victory_sound.set_volume(0.5)
bg_music.play(-1)

#game logic
game_active = True
x_turn = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if not game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    board = Board()
                    game_active = True
                    x_turn = True

    screen.fill(bg_color)
    #vertical lines
    pygame.draw.line(screen, line_color, (325, 75), (325, 525), width = 8)
    pygame.draw.line(screen, line_color, (475, 75), (475, 525), width = 8)
    #horizontal
    pygame.draw.line(screen, line_color, (175, 225), (625, 225), width = 8)
    pygame.draw.line(screen, line_color, (175, 375), (625, 375), width = 8)

    if game_active:
        x_turn = board.checkCollision(x_turn)
        board.displayMoves()
        vict = board.checkWin()
        if vict:
            victory_sound.play()
            game_active = False
    else:
        board.displayMoves()

    pygame.display.update()
    clock.tick(60)