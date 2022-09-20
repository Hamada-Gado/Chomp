# visualize chomp game from Basic computer game book using pygame

from math import pi
from time import sleep
import pygame, random, sys
from pygame.locals import *
pygame.init()

FPS = 30
W_WIDTH, W_HEIGHT = 800, 745
BOX_SIZE = 70
GAP_SIZE = 5
COLUMNS, ROWS = 9, 9
assert COLUMNS * (BOX_SIZE + GAP_SIZE) < W_WIDTH and ROWS * (BOX_SIZE + GAP_SIZE) < W_HEIGHT, 'Widow is too small for the cookie.'
X_MARGIN = int((W_WIDTH - (COLUMNS * (BOX_SIZE + GAP_SIZE)))//2)
Y_MARGIN = int((W_HEIGHT - (ROWS * (BOX_SIZE + GAP_SIZE)))//2)

#               R    G    B
COOKIE      = (230, 206, 160)
GRAY        = (100, 100, 100)
NAVY_BLUE   = ( 60,  60, 100)
WHITE       = (255, 255, 255)
BLACK       = (  0,   0,   0)
GREEN       = (  0, 128,   0)
RED         = (255,   0,   0)
BLUE        = (  0,   0, 255)
BLUE_VIOLET = (138,  43, 226)
PURPLE      = (255,   0, 255)
YELLOW      = (255, 255,   0)

BG_COLOR = NAVY_BLUE
LIGHT_BG_COLOR = GRAY
HIGHLIGHT_COLOR = BLUE

FONT = pygame.font.Font(None, 70)
TITLE_FONT = pygame.font.Font(None, 125)
RULES_FONT = pygame.font.Font(None, 38)
PLAYER_FONT = pygame.font.Font(None, 30)

def make_cookie():
    cookie = [['P']]
    cookie[0] += ['C']*(ROWS-1)
    for _ in range(COLUMNS-1):
        cookie.append(['C']*ROWS)

    return cookie

def draw_cookie(left: int, top: int):
    pygame.draw.rect(WINDOW, COOKIE, (left, top, BOX_SIZE, BOX_SIZE))
    pixObj = pygame.PixelArray(WINDOW)
    for x in range(left, left+BOX_SIZE, BOX_SIZE//4):
        for y in range(top, top+BOX_SIZE, BOX_SIZE//4):
            pixObj[x][y] = BLACK

    del pixObj

def draw_poisoned(left: int, top: int):
    poisoned_surface = pygame.Surface((BOX_SIZE, BOX_SIZE)).convert_alpha()
    poisoned_surface.fill((0, 255, 0, 50))
    pygame.draw.rect(WINDOW, COOKIE, (left, top, BOX_SIZE, BOX_SIZE))
    WINDOW.blit(poisoned_surface, (left, top))

    pixObj = pygame.PixelArray(WINDOW)
    for x in range(left, left+BOX_SIZE, BOX_SIZE//4):
        for y in range(top, top+BOX_SIZE, BOX_SIZE//4):
            pixObj[x][y] = BLACK

    del pixObj

def draw_eaten(left: int, top: int):
    pass

def draw_cookies(cookie: list[list[str]]):
    draw = {'': draw_eaten, 'P': draw_poisoned, 'C': draw_cookie}
    for cookieX in range(COLUMNS):
        for cookieY in range(ROWS):
            left, top = leftTop_coords_of_cookie(cookieX, cookieY)
            draw[cookie[cookieX][cookieY]](left, top)

def chomp(cookie: list[list[str]], cookieX, cookieY):
    for x in range(cookieX, len(cookie)):
        for y in range(cookieY, len(cookie[x])):
            cookie[x][y] = ''

def leftTop_coords_of_cookie(cookieX: int, cookieY: int):
    left = cookieX * (BOX_SIZE + GAP_SIZE) + X_MARGIN
    top = cookieY * (BOX_SIZE + GAP_SIZE) + Y_MARGIN
    return (left, top)

def get_cookie_at_pixel(x: int, y: int):
    for cookieX in range(COLUMNS):
        for cookieY in range(ROWS):
            left, top = leftTop_coords_of_cookie(cookieX, cookieY)
            cookieRect = pygame.Rect(left, top, BOX_SIZE, BOX_SIZE)
            if cookieRect.collidepoint(x, y):
                return (cookieX, cookieY)
    return (None, None)       

def lost_animation(name: str):
    name_surface = TITLE_FONT.render(name+' has lost :(', True, YELLOW)
    
    color1 = LIGHT_BG_COLOR
    color2 = BG_COLOR

    for i in range(13):
        color1, color2 = color2, color1
        WINDOW.fill(color1)
        WINDOW.blit(name_surface, ((WINDOW.get_width()-name_surface.get_width())//2, (WINDOW.get_height()-name_surface.get_height())//2))
        pygame.display.update()
        pygame.time.wait(300)

def main_menu():
        
    play_button = FONT.render('PLAY', True, BLACK, WHITE)
    instruction_button = FONT.render('INSTRUCTIONS', True, WHITE)
    title = TITLE_FONT.render('CHOMP', True, RED, BLUE_VIOLET)

    play_button_rect = play_button.get_rect()
    instruction_button_rect = instruction_button.get_rect()

    play_button_rect.topleft = ((WINDOW.get_width()-play_button_rect.width)//2, WINDOW.get_height()//2)
    instruction_button_rect.topleft = ((WINDOW.get_width()-instruction_button_rect.width)//2 + 20, (WINDOW.get_height()//2+play_button_rect.height+10))

    mouseX = mouseY = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == MOUSEMOTION:
                mouseX, mouseY = event.pos
                if play_button_rect.collidepoint(mouseX, mouseY):
                    play_button = FONT.render('PLAY', True, GREEN, WHITE)
                else:
                    play_button = FONT.render('PLAY', True, BLACK, WHITE)

                if instruction_button_rect.collidepoint(mouseX, mouseY):
                    instruction_button = FONT.render('INSTRUCTION', True, GREEN, WHITE)
                else:
                    instruction_button = FONT.render('INSTRUCTION', True, BLACK, WHITE)

            if event.type == MOUSEBUTTONUP:
                mouseX, mouseY = event.pos
                if play_button_rect.collidepoint(mouseX, mouseY):
                    return
                if instruction_button_rect.collidepoint(mouseX, mouseY):
                    return instruction_menu()



        WINDOW.fill(BLUE_VIOLET)
        WINDOW.blit(title, (WINDOW.get_width()//2 - title.get_width()//2, 50))
        WINDOW.blit(play_button, play_button_rect.topleft)
        WINDOW.blit(instruction_button, instruction_button_rect.topleft)
        pygame.display.update()
        CLOCK.tick(FPS)

def instruction_menu():
    rules = [
            'The board is a big cookie - 9 rows high and', 
            '9 columns wide.',
            'In the upper left corner of the cookie is',
            'a poison square. The one who',
            'chomps the poison square loses.',
            'To take a chomp, type the row',
            'and columns of one of the squares',
            'on the cookie. all of the square below and',
            'to the right of that square',
            '(including that square, too)',
            'disappear -- CHOMP!!',
            'No fair chomping squares that have',
            'already been chomped,',
            'or that are outside the original',
            'dimensions of the cookie.',
            'Press Enter to return to main menu.']
        
    WINDOW.fill(PURPLE)
    for i, rule in enumerate(rules):
        rule_surface = RULES_FONT.render(rule, True, BLACK)
        WINDOW.blit(rule_surface, (10, 28*i+10))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == KEYUP and event.key == K_RETURN:
                return main_menu()

def get_players_name():
    prompt_surface = FONT.render("Enter the players name", True, YELLOW)
    input_box = pygame.Rect(WINDOW.get_width()//2 - 200, WINDOW.get_height()//2 - 25, 400, 50)
    start_button = FONT.render('START', True, BLACK, WHITE)
    start_rect = start_button.get_rect()
    start_rect.topleft = ((WINDOW.get_width() - start_rect.w)//2, input_box.bottom + 20)

    name = ''
    players = []
    while True:
        bg_color = BG_COLOR
        pos = pygame.mouse.get_pos()

        if start_rect.collidepoint(pos):
            start_button = FONT.render('START', True, GREEN, WHITE)
        else:
            start_button = FONT.render('START', True, BLACK, WHITE)

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                
                if event.key == pygame.K_RETURN and len(name.strip()) > 0:
                        players.append(name)
                        name = ''

                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]

                elif len(name) <= 10 and event.unicode != pygame.K_RETURN:
                    name += event.unicode

            if event.type == MOUSEBUTTONUP:
                pos = event.pos
                if start_rect.collidepoint(pos):
                    if players != []:
                        return players
                    bg_color = RED

        name_surface = FONT.render(name, True, BLACK)

        WINDOW.fill(bg_color)
        WINDOW.blit(prompt_surface, ((WINDOW.get_width() - prompt_surface.get_width())//2, 100))
        pygame.draw.rect(WINDOW, WHITE, input_box)
        WINDOW.blit(name_surface, (input_box.x + 16, input_box.centery - name_surface.get_height()//2))
        WINDOW.blit(start_button, start_rect.topleft)
        pygame.display.update()
        CLOCK.tick(FPS)

def main():
    global WINDOW, CLOCK
    WINDOW = pygame.display.set_mode((W_WIDTH, W_HEIGHT))
    pygame.display.set_caption('Chomp')
    CLOCK = pygame.time.Clock()

    main_cookie = make_cookie()
    mouseX = mouseY = 0

    main_menu()
    players = get_players_name()
    random.shuffle(players)

    curr_player = PLAYER_FONT.render(f'{players[0]}\'s chomp', True, BLACK, BG_COLOR)
    
    while True:
        mouse_clicked = False

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == MOUSEMOTION:
                mouseX, mouseY = event.pos

            if event.type == MOUSEBUTTONUP:
                mouseX, mouseY = event.pos
                mouse_clicked = True

        cookieX, cookieY = get_cookie_at_pixel(mouseX, mouseY)

        if mouse_clicked and cookieX != None and cookieY != None:
            if main_cookie[cookieX][cookieY] == 'P':
                lost_animation(players[0])
                return main()
            elif main_cookie[cookieX][cookieY] == 'C':
                chomp(main_cookie, cookieX, cookieY)
                player = players[0]
                players.remove(players[0])
                players.append(player)
                curr_player = PLAYER_FONT.render(f'{players[0]}\'s chomp', True, BLACK, BG_COLOR)

        WINDOW.fill(BG_COLOR)
        WINDOW.blit(curr_player, (10, 10))
        draw_cookies(main_cookie)
        pygame.display.update()
        CLOCK.tick(FPS)

if __name__ == '__main__':
    main()