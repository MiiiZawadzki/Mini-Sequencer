import pygame
import sys
from time import time, sleep
import asyncio
import simpleaudio
from glob import glob
from random import randint

# config
clock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption('8Bar')
screen = pygame.display.set_mode((1280, 720))


class Object:
    def __init__(self, rect , color):
        self.rect = rect
        self.color = color


class Line(Object):
    def __init__(self, rect, color, position_x):
        Object.__init__(self, rect, color)
        self.position_x = position_x


class Sample:
    def __init__(self, name):
        self.name = name
        self.path = "samples/" + name
        self.layer = None
        self.waveObj = simpleaudio.WaveObject.from_wave_file(self.path)
        self.rectsPos = []
        self.color = (randint(100,120),randint(150,250),randint(200,255))
        self.rects_list = []

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
right_mouse_button_clicked = False

# fonts
pygame.font.init()
font = pygame.font.SysFont('calibri', 32)
font_16 = pygame.font.SysFont('calibri', 16)
font_24 = pygame.font.SysFont('calibri', 24)
font_text = font.render("1.1", True, (153, 219, 255))


sample_list = []
chosen_samples = []
async def ControlPlayState():
    if states["isPlaying"]:
        if states["ended"]:
            states["ended"] = False
            states["isPlaying"] = True
            line.rect.x = 238
            line.position_x = 238
            bar_line.rect.x = 238
            bar_line.position_x = 238
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
            states["actualBars"] += 1
            states["actualBeats"] = 1
        if line.rect.x >= 1262:
            line.rect.x = 1262
            bar_line.rect.x = 1262
            states["isPlaying"] = False
            states["ended"] = True
            if CheckLeftMouseButtonCollision(play_button):
                if left_mouse_button_clicked:
                    line.rect.x = 238
                    line.position_x = 238
                    bar_line.rect.x = 238
                    bar_line.position_x = 238
                    states["actualSix"] = 1
                    states["actualBeats"] = 1
                    states["actualBars"] = 1
        await asyncio.sleep(0.25)


def CheckLeftMouseButtonCollision(rect):
    mouse_pos = pygame.mouse.get_pos()
    if rect.left < mouse_pos[0] < rect.right:
        if rect.top < mouse_pos[1] < rect.bottom:
            return True
    return False


async def ControlTopButtons():
    if CheckLeftMouseButtonCollision(play_button):
        if left_mouse_button_clicked:
            states["playButtonClicked"] = True
            states["isPlaying"] = True

    if CheckLeftMouseButtonCollision(pause_button):
        if left_mouse_button_clicked:
            states["pauseButtonClicked"] = True
            states["isPlaying"] = False

    if CheckLeftMouseButtonCollision(restart_button):
        if left_mouse_button_clicked:
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


def ControlSampleSection():
    # adding and removing rects
    for i,s in enumerate(chosen_samples):
        pygame.draw.rect(screen, s.color, pygame.Rect(238, 105 + i * 40, 1024, 40))
        pygame.draw.rect(screen, s.color, pygame.Rect(238, 105+i*40, 1024, 40))
        font_16_text = font_16.render(str(s.name), True, (0, 0, 0))
        screen.blit(font_16_text, (240, 108 + i * 40))
        for rect in s.rects_list:
            pygame.draw.rect(screen, (0, 66, 102), rect)
        # if clicked on rect
            if CheckLeftMouseButtonCollision(rect) and left_mouse_button_clicked:
                if rect not in s.rectsPos:
                    s.rectsPos.append(rect)
            if CheckLeftMouseButtonCollision(rect) and right_mouse_button_clicked:
                if rect in s.rectsPos:
                    s.rectsPos.remove(rect)

    # displaying selected rects
    for sample in chosen_samples:
        for rect in sample.rectsPos:
            pygame.draw.rect(screen, (255, 66, 102), rect)

    for sample in chosen_samples:
        for rect in sample.rectsPos:
            if line.rect.colliderect(rect) and states["isPlaying"]:
                sample.waveObj.play()

def ReadSamples():
    # read samples from directory
    sample_names = glob("./samples/*.wav")
    for name in sample_names:
        sample = Sample(name.split("\\")[-1])
        sample.layer = len(sample_list) + 1
        sample_list.append(sample)

ReadSamples()


def UpdateRects(deleted_sample):
    samples_after_sample = []
    j = None
    for i,sample in enumerate(chosen_samples):
        if sample == deleted_sample:
            j = i
    for i,sample in enumerate(chosen_samples):
        if i > j:
            for rect in sample.rects_list:
                rect.y -= 40
    print(samples_after_sample)

sample_rect = []


def ChooseSamples():
    sample_name_rects = []
    global sample_rect
    for i,sample in enumerate(sample_list):
        rect = pygame.Rect(14,14 + i * 44, 202, 40)
        pygame.draw.rect(screen, (33, 39, 48), rect)
        sample_name_rects.append([rect, sample])
        font_text = font_24.render(str(sample.name), True, (153, 219, 255))
        sample.name_pos = (20, 20 + i * 44)
        screen.blit(font_text, (20, 20 + i * 44))
        if CheckLeftMouseButtonCollision(rect) and left_mouse_button_clicked:
            if sample not in chosen_samples:
                for i in range(64):
                    sample.rects_list.append(pygame.Rect(238 + i * 16, 125 + len(chosen_samples) * 40, 10, 10))
                chosen_samples.append(sample)
        if CheckLeftMouseButtonCollision(rect) and right_mouse_button_clicked:
            if sample in chosen_samples:
                sample.rectsPos = []
                UpdateRects(sample)
                sample.rects_list = []
                chosen_samples.remove(sample)


    for list in sample_name_rects:
        if list[1] in chosen_samples:
            pygame.draw.rect(screen,(61, 72, 88), list[0])
            font_text = font_24.render(str(list[1].name), True, (153, 219, 255))
            screen.blit(font_text, list[1].name_pos)


while True:
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
            if event.button == 3:
                right_mouse_button_clicked = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                left_mouse_button_clicked = False
                states["playButtonClicked"] = False
                states["pauseButtonClicked"] = False
                states["restartButtonClicked"] = False
            if event.button == 3:
                right_mouse_button_clicked = False
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

    # draw sample rects and control selecting
    ControlSampleSection()

    # control playing line
    asyncio.run(ControlPlayState())

    # draw playing line
    pygame.draw.rect(screen, line.color, line.rect)
    # draw playing bar line
    pygame.draw.rect(screen, bar_line.color, bar_line.rect)

    # control play/pause/restart buttons
    asyncio.run(ControlTopButtons())

    # control timer
    ControlTimer()

    ChooseSamples()

    pygame.display.update()
    clock.tick(60)