import pygame
import sys
from time import time, sleep
import asyncio
import simpleaudio
from glob import glob
from random import randint

# config
clock = pygame.time.Clock()
pygame.mixer.pre_init(44100, 16, 2, 1024)
pygame.mixer.init()
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


class LoopButton(Object):
    def __init__(self, rect, color, bar):
        Object.__init__(self, rect, color)
        self.clicked = False
        self.bar = bar

class Sample:
    def __init__(self, name):
        self.name = name
        self.short_name = None
        self.path = "samples/" + name
        self.layer = None
        self.waveObj = simpleaudio.WaveObject.from_wave_file(self.path)
        self.sound = pygame.mixer.Sound(self.path)
        self.rectsPos = []
        self.color = (randint(100,120),randint(150,250),randint(200,255))
        self.rects_list = []

# buttons
play_button = pygame.Rect(590, 15, 30, 30)
pause_button = pygame.Rect(625, 15, 30, 30)
restart_button = pygame.Rect(660, 15, 30, 30)
loop_buttons_4bar = [LoopButton(pygame.Rect(238+256-3, 52, 8, 8), (153, 219, 255), 2),
                LoopButton(pygame.Rect(238+512-3, 52, 8, 8), (153, 219, 255), 3),
                LoopButton(pygame.Rect(238+768-3, 52, 8, 8), (153, 219, 255), 4),
                LoopButton(pygame.Rect(238+1024-3, 52, 8, 8), (153, 219, 255), 5)]
loop_buttons_8bar = [LoopButton(pygame.Rect(238+128-3, 52, 8, 8), (153, 219, 255), 2),
                LoopButton(pygame.Rect(238+256-3, 52, 8, 8), (153, 219, 255), 3),
                LoopButton(pygame.Rect(238+384-3, 52, 8, 8), (153, 219, 255), 4),
                LoopButton(pygame.Rect(238+512-3, 52, 8, 8), (153, 219, 255), 5),
                LoopButton(pygame.Rect(238+640-3, 52, 8, 8), (153, 219, 255), 6),
                LoopButton(pygame.Rect(238+768-3, 52, 8, 8), (153, 219, 255), 7),
                LoopButton(pygame.Rect(238+896-3, 52, 8, 8), (153, 219, 255), 8),
                LoopButton(pygame.Rect(238+1024-3, 52, 8, 8), (153, 219, 255), 9)]
refresh_button = pygame.Rect(186, 674, 30, 30)
four_bar_button = pygame.Rect(320, 15, 30, 30)
eight_bar_button = pygame.Rect(360, 15, 30, 30)
help_button = pygame.Rect(1220-80, 15, 60, 30)
settings_button = pygame.Rect(1220-15, 15, 60, 30)
# screen objects
line = Line(pygame.Rect(238, 100, 1, 600), (155, 0, 0), 238)
bar_line = Line(pygame.Rect(238, 65, 1, 20), (155, 0, 0), 238)

play_button_img = pygame.image.load("img/play_button.png")
play_button_img.set_colorkey((255, 255, 255))

pause_button_img = pygame.image.load("img/pause_button.png")
pause_button_img.set_colorkey((255, 255, 255))

restart_button_img = pygame.image.load("img/restart_button.png")
restart_button_img.set_colorkey((255, 255, 255))

loop_icon_img = pygame.image.load("img/loop_icon.png")
loop_icon_img.set_colorkey((255, 255, 255))

sample_warning_icon_img = pygame.image.load("img/sample_warning_icon.png")
sample_warning_icon_img.set_colorkey((255, 255, 255))

refresh_button_img = pygame.image.load("img/refresh_button.png")
refresh_button_img.set_colorkey((255, 255, 255))

lines_visible_icon_img = pygame.image.load("img/lines_visible_icon.png")
lines_visible_icon_img.set_colorkey((255, 255, 255))

four_bar_button_img = pygame.image.load("img/4bar_button.png")
four_bar_button_img.set_colorkey((255, 255, 255))

eight_bar_button_img = pygame.image.load("img/8bar_button.png")
eight_bar_button_img.set_colorkey((255, 255, 255))

help_button_img = pygame.image.load("img/help_button.png")
help_button_img.set_colorkey((255, 255, 255))

settings_button_img = pygame.image.load("img/settings_button.png")
settings_button_img.set_colorkey((255, 255, 255))

# program objects
states = {"isPlaying": False, "ended": False, "playButtonClicked": False,
          "pauseButtonClicked": False, "restartButtonClicked": False, "actualSix": 1, "actualBeats": 1, "actualBars": 1,
          "sampleOverload": False, "linesVisible": False, "length": 4, "helpVisible": False}
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
playobjs = []

# playing config
step_size = 0.125
six_qty = 65
beats_qty = 17
bars_qty = 5
# Control Bars, Beats, Sixteenhs on different playing states
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
        if states["actualSix"] > 4:
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
        await asyncio.sleep(step_size)

# Move bars and increment sixteenhs
async def ControlPlaying():
    if states["isPlaying"] and not states["helpVisible"]:
        line.position_x += (64/states["length"])
        line.rect.x += (64/states["length"])
        bar_line.position_x += (64/states["length"])
        bar_line.rect.x += (64/states["length"])
        states["actualSix"] += 1

# check if mouse collide with rect given as parameter
def CheckLeftMouseButtonCollision(rect):
    mouse_pos = pygame.mouse.get_pos()
    if rect.left < mouse_pos[0] < rect.right:
        if rect.top < mouse_pos[1] < rect.bottom:
            return True
    return False


# async control play, pause and restart buttons
async def ControlTopButtons():
    if CheckLeftMouseButtonCollision(play_button):
        if left_mouse_button_clicked and not states["helpVisible"]:
            states["playButtonClicked"] = True
            states["isPlaying"] = True

    if CheckLeftMouseButtonCollision(pause_button):
        if left_mouse_button_clicked and not states["helpVisible"]:
            states["pauseButtonClicked"] = True
            states["isPlaying"] = False

    if CheckLeftMouseButtonCollision(restart_button):
        if left_mouse_button_clicked and not states["helpVisible"]:
            states["restartButtonClicked"] = True
            states["isPlaying"] = False
            line.rect.x = 238
            line.position_x = 238
            bar_line.rect.x = 238
            bar_line.position_x = 238
            states["actualSix"] = 1
            states["actualBeats"] = 1
            states["actualBars"] = 1

# Display Bars, beats and sixteenhs on screen
def ControlTimer():
    global font_text
    bar_str = str(str(states["actualBars"]) + "." + str(states["actualBeats"])+ "." + str(states["actualSix"]))
    font_text = font.render(bar_str, True, (153, 219, 255))
    screen.blit(font_text, (230, 15))


def ControlSampleSection():
    if states["sampleOverload"]:
        screen.blit(sample_warning_icon_img, (1100-70, 5))
    if states["linesVisible"]:
        screen.blit(lines_visible_icon_img, (1155-70, 5))
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

    # old version of playing audio
    # # stop and play audio
    # global playobjs
    # for sample in chosen_samples:
    #     for rect in sample.rectsPos:
    #         if line.rect.colliderect(rect) and states["isPlaying"]:
    #             playobjs.append(sample.waveObj.play())
    # for po in playobjs:
    #     if not states["isPlaying"]:
    #         simpleaudio.PlayObject.stop(po)
    #         playobjs.remove(po)

    # stop and play audio
    for sample in chosen_samples:
        for rect in sample.rectsPos:
            if line.rect.colliderect(rect) and states["isPlaying"]:
                sample.sound.play()
        if not states["isPlaying"]:
            sample.sound.stop()



# Read samples from catalog and append it to sample_list
def ReadSamples():
    # read samples from directory
    sample_names = glob("./samples/*.wav")
    for name in sample_names:
        sample_name = name.split("\\")[-1]
        if len(sample_name) > 18:
            sample_name = sample_name[0:15]
            sample_name = sample_name + "..."
        sample = Sample(name.split("\\")[-1])
        sample.short_name = sample_name
        sample.layer = len(sample_list) + 1
        if len(sample_list) < 15:
            sample_list.append(sample)
            states["sampleOverload"] = False
        else:
            states["sampleOverload"] = True

ReadSamples()

# after removing sample from chosen samples update sample rects y position
def UpdateRects(deleted_sample):
    j = None
    for i,sample in enumerate(chosen_samples):
        if sample == deleted_sample:
            j = i
    for i,sample in enumerate(chosen_samples):
        if i > j:
            for rect in sample.rects_list:
                rect.y -= 40


# Clear sample list
def ClearSamples():
    global sample_list
    sample_list = []

# Control selecting samples in left panel
def ChooseSamples():
    sample_name_rects = []
    for i,sample in enumerate(sample_list):
        rect = pygame.Rect(14,14 + i * 44, 202, 40)
        pygame.draw.rect(screen, (33, 39, 48), rect)
        sample_name_rects.append([rect, sample])
        font_text = font_24.render(str(sample.name), True, (153, 219, 255))
        if sample.short_name is not None:
            font_text = font_24.render(str(sample.short_name), True, (153, 219, 255))
        sample.name_pos = (20, 20 + i * 44)
        screen.blit(font_text, (20, 20 + i * 44))

        if CheckLeftMouseButtonCollision(rect) and left_mouse_button_clicked:
            if sample not in chosen_samples:
                if states["length"] == 4:
                    for i in range(64):
                        sample.rects_list.append(pygame.Rect(238 + i * 16, 125 + len(chosen_samples) * 40, 15, 10))
                if states["length"] == 8:
                    for i in range(128):
                        sample.rects_list.append(pygame.Rect(238 + i * 8, 125 + len(chosen_samples) * 40, 7, 5))
                chosen_samples.append(sample)
        if CheckLeftMouseButtonCollision(rect) and right_mouse_button_clicked:
            if sample in chosen_samples:
                sample.rectsPos = []
                UpdateRects(sample)
                sample.rects_list = []
                chosen_samples.remove(sample)

    # display refresh button, clear sample list then read samples again
    pygame.draw.rect(screen, (33, 39, 48), refresh_button)
    screen.blit(refresh_button_img, (184, 674))
    if CheckLeftMouseButtonCollision(refresh_button) and left_mouse_button_clicked:
        ClearSamples()
        ReadSamples()

    for list in sample_name_rects:
        if list[1] in chosen_samples:
            pygame.draw.rect(screen,(0, 80, 122), list[0])
            font_text = font_24.render(str(list[1].name), True, (153, 219, 255))
            if list[1].short_name is not None:
                font_text = font_24.render(str(list[1].short_name), True, (153, 219, 255))
            screen.blit(font_text, list[1].name_pos)

# Control loop options
def LoopSelection():
    buttons = loop_buttons_4bar
    if states["length"] == 8:
        buttons = loop_buttons_8bar
    for button in buttons:
        pygame.draw.rect(screen, button.color, button.rect)
        if button.clicked:
            screen.blit(loop_icon_img, (1024-70, 5))
        if CheckLeftMouseButtonCollision(button.rect) and left_mouse_button_clicked:
            button.color = (50, 39, 48)
            button.clicked = True
        if CheckLeftMouseButtonCollision(button.rect) and right_mouse_button_clicked:
            button.color = (153, 219, 255)
            button.clicked = False
        if states["actualBars"] == button.bar and states["actualSix"] == 1 and states["actualBeats"] == 1:
            if button.clicked:
                states["isPlaying"] = True
                states["ended"] = False
                states["actualBars"] = 1
                states["actualSix"] = 1
                states["actualBeats"] = 1
                line.rect.x = 238
                line.position_x = 238
                bar_line.rect.x = 238
                bar_line.position_x = 238

def ControlSelectingLength():
    global step_size, six_qty, beats_qty, bars_qty
    length_changed = False
    if states["length"] == 4:
        pygame.draw.rect(screen, (50, 39, 48), four_bar_button)
        screen.blit(four_bar_button_img, (320, 15))
    if states["length"] == 8:
        pygame.draw.rect(screen, (50, 39, 48), eight_bar_button)
        screen.blit(eight_bar_button_img, (360, 15))
    if CheckLeftMouseButtonCollision(four_bar_button) and left_mouse_button_clicked:
        states["length"] = 4
        length_changed = True
    if CheckLeftMouseButtonCollision(eight_bar_button) and left_mouse_button_clicked:
        states["length"] = 8
        length_changed = True
    if length_changed:
        global chosen_samples
        for sample in chosen_samples:
            sample.rectsPos = []
            sample.rects_list = []
        chosen_samples = []
        states["isPlaying"] = False
        states["actualBars"] = 1
        states["actualSix"] = 1
        states["actualBeats"] = 1
        line.rect.x = 238
        line.position_x = 238
        bar_line.rect.x = 238
        bar_line.position_x = 238
        if states["length"] == 4:
            six_qty = 65
            beats_qty = 17
            bars_qty = 5
        if states["length"] == 8:
            six_qty = 129
            beats_qty = 33
            bars_qty = 9


def ControlHelp():
    if CheckLeftMouseButtonCollision(help_button):
        if left_mouse_button_clicked:
            states["helpVisible"] = True
        if right_mouse_button_clicked:
            states["helpVisible"] = False
    if states["helpVisible"]:
        pygame.draw.rect(screen, (50, 39, 48), help_button)
        screen.blit(help_button_img, (1220-80, 15))
        pygame.draw.rect(screen, (42, 48, 60), pygame.Rect(230, 52, 1040, 658))
        font_text = font.render("About:", True, (153, 219, 255))
        screen.blit(font_text, (235, 57))
        texts = ["This program is simple audio sequencer that uses samples placed in 'samples' directory.",
                 "- To activate/select objects on screen use left mouse button.",
                 "- To deactivate/unselect objects on screen use right mouse button.",
                 "- To change length click on 4 or 8 icon placed at top of the screen, but this will cause reset of patterns.",
                 "- To display/hide guides line press tab button.",
                 "- Supported audio file format is .wav saved with 16 bit depth.",
                 "- Limit of samples in directory is 15 files.",
                 "- To refresh samples use button placed at bottom of the screen.",
                 "- To activate loop mode, select the area you want to loop, by clicking on light squares above ruler display.",
                 ]
        last_y_pos = 0
        for i, text in enumerate(texts):
            font_text = font_24.render(text, True, (153, 219, 255))
            screen.blit(font_text, (235, 100+i*30))
            last_y_pos =  100+i*30
        font_text = font.render("Legend:", True, (153, 219, 255))
        screen.blit(font_text, (235, last_y_pos+60))
        icons_text = [[loop_icon_img, "- Loop mode active icon:"],
                      [sample_warning_icon_img, "- There are over 15 wav files in the sample directory:"],
                      [lines_visible_icon_img, "- Guides line are visible:"]]
        for i, text in enumerate(icons_text):
            font_text = font_24.render(text[1], True, (153, 219, 255))
            screen.blit(font_text, (235, last_y_pos+100+i*60))
            screen.blit(text[0], (235+len(text[1])*10, last_y_pos+85+i*60))
        ending_text = "[ To go back to the main screen click the right mouse button on the Help button ]"
        font_text = font_16.render(ending_text, True, (153, 219, 255))
        screen.blit(font_text, (720, 65))
# main program loop
while True:
    screen.fill((25, 29, 36))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        if event.type == pygame.KEYDOWN:
            actual_key = event.key
            if event.key == pygame.K_SPACE:
                if not states["helpVisible"]:
                    states["isPlaying"] = not states["isPlaying"]
            if event.key == pygame.K_TAB:
                states["linesVisible"] = not states["linesVisible"]
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

    pygame.draw.rect(screen, (33, 39, 48), help_button)
    screen.blit(help_button_img, (1220-80, 15))

    pygame.draw.rect(screen, (33, 39, 48), settings_button)
    screen.blit(settings_button_img, (1220-15, 15))

    # middle rect section
    pygame.draw.rect(screen, (42, 49, 60), pygame.Rect(230, 60, 1040, 650))
    # draw bar display
    pygame.draw.rect(screen, (33, 39, 48), pygame.Rect(238, 65, 1024, 20))

    # draw main middle container
    pygame.draw.rect(screen, (33, 39, 48), pygame.Rect(238, 100, 1024, 600))


    # draw sample rects and control selecting
    ControlSampleSection()

    # control playing line
    asyncio.run(ControlPlaying())
    asyncio.run(ControlPlayState())

    # control play/pause/restart buttons
    asyncio.run(ControlTopButtons())

    # control timer
    ControlTimer()

    # control left sample section
    ChooseSamples()

    # control loop options
    LoopSelection()

    # draw lines on bar display
    # if lineVisible state is set to True draw lines to the end of the window
    for i in range(six_qty):
        end_pos = (238+i*(1024/(six_qty-1)), 85)
        if states["linesVisible"]:
            end_pos = (238+i*(1024/(six_qty-1)), 700)
        pygame.draw.line(screen, (0, 66, 102), (238+i*(1024/(six_qty-1)), 65), end_pos)
    for i in range(beats_qty):
        end_pos = (238+i*(1024/(beats_qty-1)), 85)
        if states["linesVisible"]:
            end_pos = (238+i*(1024/(beats_qty-1)), 700)
        pygame.draw.line(screen, (0, 133, 204), (238+i*(1024/(beats_qty-1)), 65), end_pos)

    for i in range(bars_qty):
        end_pos = (238 + i * (1024/(bars_qty-1)), 85)
        if states["linesVisible"]:
            end_pos = (238+i*(1024/(bars_qty-1)), 700)
        pygame.draw.line(screen, (153, 219, 255), (238+i*(1024/(bars_qty-1)), 65), end_pos)

    # draw playing line
    pygame.draw.rect(screen, line.color, line.rect)
    # draw playing bar line
    pygame.draw.rect(screen, bar_line.color, bar_line.rect)

    pygame.draw.rect(screen, (33, 39, 48), four_bar_button)
    screen.blit(four_bar_button_img, (320, 15))

    pygame.draw.rect(screen, (33, 39, 48), eight_bar_button)
    screen.blit(eight_bar_button_img, (360, 15))

    ControlSelectingLength()

    ControlHelp()

    pygame.display.update()

    clock.tick(60)