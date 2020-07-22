import pygame
import sys
from time import time, sleep
import asyncio
import multiprocessing as mp

# config
clock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption('8Bar')
screen = pygame.display.set_mode((1280, 720))
pygame.mixer.init(44100, 16, 2, 4096)
pool = mp.Pool(mp.cpu_count())


class Object:
    def __init__(self, rect , color):
        self.rect = rect
        self.color = color


class Line(Object):
    def __init__(self, rect, color, position_x):
        Object.__init__(self, rect, color)
        self.position_x = position_x


# buttons
play_button = pygame.Rect(590, 15, 30, 30)
pause_button = pygame.Rect(625, 15, 30, 30)
restart_button = pygame.Rect(660, 15, 30, 30)

# screen objects
line = Line(pygame.Rect(238, 100, 1, 600), (155, 0, 0), 238)
bar_line = Line(pygame.Rect(238, 65, 1, 20), (155, 0, 0), 238)

play_button_img = pygame.image.load("img/play_button.png")
play_button_img.set_colorkey((255, 255, 255))

pause_button_img = pygame.image.load("img/pause_button.png")
pause_button_img.set_colorkey((255, 255, 255))

restart_button_img = pygame.image.load("img/restart_button.png")
restart_button_img.set_colorkey((255, 255, 255))

# program objects
states = {"isPlaying": False, "ended": False, "playButtonClicked": False,
          "pauseButtonClicked": False, "restartButtonClicked": False, "actualSix": 1, "actualBeats": 1, "actualBars": 1}
left_mouse_button_clicked = False
start_time = time()

# fonts
pygame.font.init()
font = pygame.font.SysFont('calibri', 32)
font_text = font.render("1.1", True, (153, 219, 255))

sample = pygame.mixer.Sound('samples/1.wav')
sample2 = pygame.mixer.Sound('samples/2.wav')

async def ControlPlayState():
    global start_time
    if states["isPlaying"]:
        start_time = time()
        if states["ended"]:
            line.rect.x = 238
            line.position_x = 238
            bar_line.rect.x = 238
            bar_line.position_x = 238
            states["ended"] = False
            states["actualSix"] = 1
            states["actualBeats"] = 1
            states["actualBars"] = 1
        line.position_x += 16
        line.rect.x += 16
        bar_line.position_x += 16
        bar_line.rect.x += 16
        states["actualSix"] += 1
        if states["actualSix"] > 2:
            states["actualBeats"] += 1
            states["actualSix"] = 1
        if states["actualBeats"] > 4:
            sample.play()
            states["actualBars"] += 1
            states["actualBeats"] = 1
        if line.rect.x >= 1262:
            line.rect.x = 1262
            bar_line.rect.x = 1262
            states["isPlaying"] = False
            states["ended"] = True
        await asyncio.sleep(0.25)


def CheckLeftMouseButtonCollision(rect):
    mouse_pos = pygame.mouse.get_pos()
    if rect.left < mouse_pos[0] < rect.right:
        if rect.top < mouse_pos[1] < rect.bottom:
            return True
    return False


async def ControlTopButtons():
    if CheckLeftMouseButtonCollision(play_button):
        if left_mouse_button_clicked and not states["playButtonClicked"]:
            states["playButtonClicked"] = True
            states["isPlaying"] = True

    if CheckLeftMouseButtonCollision(pause_button):
        if left_mouse_button_clicked and not states["pauseButtonClicked"]:
            states["pauseButtonClicked"] = True
            states["isPlaying"] = False

    if CheckLeftMouseButtonCollision(restart_button):
        if left_mouse_button_clicked and not states["restartButtonClicked"]:
            states["restartButtonClicked"] = True
            states["isPlaying"] = False
            states["ended"] = True
            line.rect.x = 238
            line.position_x = 238
            bar_line.rect.x = 238
            bar_line.position_x = 238
            states["actualSix"] = 1
            states["actualBeats"] = 1
            states["actualBars"] = 1


def ControlTimer():
    global font_text

    bar_str = str(str(states["actualBars"]) + "." + str(states["actualBeats"])+ "." + str(states["actualSix"]))
    font_text = font.render(bar_str, True, (153, 219, 255))
    screen.blit(font_text, (230, 15))


while True:
    print(states)
    screen.fill((25, 29, 36))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        if event.type == pygame.KEYDOWN:
            actual_key = event.key
            if event.key == pygame.K_SPACE:
                states["isPlaying"] = not states["isPlaying"]
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                left_mouse_button_clicked = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                left_mouse_button_clicked = False
                states["playButtonClicked"] = False
                states["pauseButtonClicked"] = False
                states["restartButtonClicked"] = False
    ## screen objects
    # left rect section
    pygame.draw.rect(screen, (42, 49, 60), pygame.Rect(10, 10, 210, 700))
    # top rect section
    pygame.draw.rect(screen, (42, 49, 60), pygame.Rect(585, 10, 110, 40))

    pygame.draw.rect(screen, (33, 39, 48), play_button)
    screen.blit(play_button_img, (590, 15))

    pygame.draw.rect(screen, (33, 39, 48), pause_button)
    screen.blit(pause_button_img, (625, 15))

    pygame.draw.rect(screen, (33, 39, 48), restart_button)
    screen.blit(restart_button_img, (660, 15))
    # middle rect section
    pygame.draw.rect(screen, (42, 49, 60), pygame.Rect(230, 60, 1040, 650))
    # draw bar display
    pygame.draw.rect(screen, (33, 39, 48), pygame.Rect(238, 65, 1024, 20))
    # draw lines on bar display
    for i in range(65):
        pygame.draw.line(screen, (0, 66, 102), (238+i*16, 65), (238+i*16, 85))
    for i in range(37):
        pygame.draw.line(screen, (0, 133, 204), (238+i*32, 65), (238+i*32, 85))
    for i in range(9):
        pygame.draw.line(screen, (153, 219, 255), (238+i*128, 65), (238+i*128, 85))
    # draw main middle container
    pygame.draw.rect(screen, (33, 39, 48), pygame.Rect(238, 100, 1024, 600))

    # control playing line
    asyncio.run(ControlPlayState())
    # draw playing line
    pygame.draw.rect(screen, line.color, line.rect)
    # draw playing line
    pygame.draw.rect(screen, bar_line.color, bar_line.rect)

    # control play/pause/restart buttons
    asyncio.run(ControlTopButtons())

    ControlTimer()
    pygame.display.update()
    clock.tick(60)