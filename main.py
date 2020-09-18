import pygame
import sys
from time import time, sleep
import asyncio
import simpleaudio
from glob import glob
from random import randint
import json

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
        # self.color = (randint(100,120),randint(150,250),randint(200,255))
        c = randint(100, 120)
        self.color = (110, c, c)
        self.rects_list = []

# color themes
dark_theme = {"Background":(25, 29, 36), "Main": (42, 49, 60), "Second":(33, 39, 48), "Selected":(120, 49, 58),
              "six":(0, 66, 102), "beat": (0, 133, 204), "bar": (153, 219, 255), "HelpWindow":(42, 48, 60)}
light_theme = {"Background":(160, 160, 160), "Main": (173, 173, 173), "Second":(150, 150, 150), "Selected":(148, 95, 158),
              "six":(230, 230, 230), "beat": (112, 51, 83), "bar": (106, 17, 69), "HelpWindow":(120, 120, 120)}
theme = dark_theme
# buttons
play_button = pygame.Rect(590, 15, 30, 30)
pause_button = pygame.Rect(625, 15, 30, 30)
restart_button = pygame.Rect(660, 15, 30, 30)
loop_buttons_4bar = [LoopButton(pygame.Rect(238+256-3, 52, 8, 8), theme["bar"], 2),
                LoopButton(pygame.Rect(238+512-3, 52, 8, 8), theme["bar"], 3),
                LoopButton(pygame.Rect(238+768-3, 52, 8, 8), theme["bar"], 4),
                LoopButton(pygame.Rect(238+1024-3, 52, 8, 8), theme["bar"], 5)]
loop_buttons_8bar = [LoopButton(pygame.Rect(238+128-3, 52, 8, 8), theme["bar"], 2),
                LoopButton(pygame.Rect(238+256-3, 52, 8, 8), theme["bar"], 3),
                LoopButton(pygame.Rect(238+384-3, 52, 8, 8), theme["bar"], 4),
                LoopButton(pygame.Rect(238+512-3, 52, 8, 8), theme["bar"], 5),
                LoopButton(pygame.Rect(238+640-3, 52, 8, 8), theme["bar"], 6),
                LoopButton(pygame.Rect(238+768-3, 52, 8, 8), theme["bar"], 7),
                LoopButton(pygame.Rect(238+896-3, 52, 8, 8), theme["bar"], 8),
                LoopButton(pygame.Rect(238+1024-3, 52, 8, 8), theme["bar"], 9)]
refresh_button = pygame.Rect(186, 674, 30, 30)
four_bar_button = pygame.Rect(320, 15, 30, 30)
eight_bar_button = pygame.Rect(360, 15, 30, 30)
help_button = pygame.Rect(1220-79, 16, 58, 28)
settings_button = pygame.Rect(1220-14, 16, 58, 28)
save_button = pygame.Rect(710, 16, 58, 28)
load_button = pygame.Rect(710+65, 16, 58, 28)
save_file_button = pygame.Rect(710, 96, 58, 28)
load_file_button = pygame.Rect(721, 161, 118, 28)
project_buttons = []
select_project_scroll_button = pygame.Rect(695, 62, 15, 35)
scroll_area = pygame.Rect(695, 62, 15, 638)
selected_project = None

# screen objects
line = Line(pygame.Rect(238, 100, 1, 600), (155, 0, 0), 238)
bar_line = Line(pygame.Rect(238, 65, 1, 20), (155, 0, 0), 238)
error_area = pygame.Rect(1000, 100, 260, 50)
error_close_rect = pygame.Rect(1242, 100, 18, 16)

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

save_button_img = pygame.image.load("img/save_button.png")
save_button_img.set_colorkey((255, 255, 255))

load_button_img = pygame.image.load("img/load_button.png")
load_button_img.set_colorkey((255, 255, 255))

load_project_button_img = pygame.image.load("img/load_project_button.png")
load_project_button_img.set_colorkey((255, 255, 255))

# program objects
states = {"isPlaying": False, "ended": False, "playButtonClicked": False,
          "pauseButtonClicked": False, "restartButtonClicked": False, "actualSix": 1, "actualBeats": 1, "actualBars": 1,
          "sampleOverload": False, "linesVisible": False, "length": 4, "helpVisible": False, "settingsVisible": False,
          "errorVisible": False, "saveVisible": False, "loadVisible": False}
# {"nameOfError": [is error active, was displayed]}
errors = {"sampleLimit": [False, False], "notSelectedProject": [False, False]}
left_mouse_button_clicked = False
right_mouse_button_clicked = False

# fonts
pygame.font.init()
font = pygame.font.SysFont('calibri', 32)
font_16 = pygame.font.SysFont('calibri', 16)
font_24 = pygame.font.SysFont('calibri', 24)
font_text = font.render("1.1", True, theme["bar"])


sample_list = []
chosen_samples = []
playobjs = []
project_names = []

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
    if states["isPlaying"] and not states["helpVisible"] and not states["settingsVisible"]:
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
        if left_mouse_button_clicked and not states["helpVisible"] and not states["settingsVisible"]:
            states["playButtonClicked"] = True
            states["isPlaying"] = True

    if CheckLeftMouseButtonCollision(pause_button):
        if left_mouse_button_clicked and not states["helpVisible"] and not states["settingsVisible"]:
            states["pauseButtonClicked"] = True
            states["isPlaying"] = False

    if CheckLeftMouseButtonCollision(restart_button):
        if left_mouse_button_clicked and not states["helpVisible"] and not states["settingsVisible"]:
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
    font_text = font.render(bar_str, True, theme["bar"])
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
            pygame.draw.rect(screen, theme["six"], rect)
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
            pygame.draw.rect(screen, theme["Selected"], rect)

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
                if not states["helpVisible"] and not states["settingsVisible"]:
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

        errors["sampleLimit"][0] = states["sampleOverload"]

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
        pygame.draw.rect(screen, theme["Second"], rect)
        sample_name_rects.append([rect, sample])
        font_text = font_24.render(str(sample.name), True, theme["bar"])
        if sample.short_name is not None:
            font_text = font_24.render(str(sample.short_name), True, theme["bar"])
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
    pygame.draw.rect(screen, theme["Second"], refresh_button)
    screen.blit(refresh_button_img, (184, 674))
    if CheckLeftMouseButtonCollision(refresh_button) and left_mouse_button_clicked:
        ClearSamples()
        ReadSamples()

    for list in sample_name_rects:
        if list[1] in chosen_samples:
            pygame.draw.rect(screen,theme["Selected"], list[0])
            font_text = font_24.render(str(list[1].name), True, theme["bar"])
            if list[1].short_name is not None:
                font_text = font_24.render(str(list[1].short_name), True, theme["bar"])
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
            button.color = theme["Selected"]
            button.clicked = True
        if CheckLeftMouseButtonCollision(button.rect) and right_mouse_button_clicked:
            button.color = theme["bar"]
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
        pygame.draw.rect(screen, theme["Selected"], four_bar_button)
        screen.blit(four_bar_button_img, (320, 15))
    if states["length"] == 8:
        pygame.draw.rect(screen, theme["Selected"], eight_bar_button)
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
            if states["settingsVisible"]:
                states["settingsVisible"] = False
            states["helpVisible"] = True
        if right_mouse_button_clicked:
            states["helpVisible"] = False
    if states["helpVisible"]:
        states["settingsVisible"] = False
        states["saveVisible"] = False
        states["loadVisible"] = False
        pygame.draw.rect(screen, theme["Selected"], help_button)
        screen.blit(help_button_img, (1220-80, 15))
        pygame.draw.rect(screen, theme["HelpWindow"], pygame.Rect(230, 52, 1040, 658))
        font_text = font.render("About:", True, theme["bar"])
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
            font_text = font_24.render(text, True, theme["bar"])
            screen.blit(font_text, (235, 100+i*30))
            last_y_pos =  100+i*30
        font_text = font.render("Legend:", True, theme["bar"])
        screen.blit(font_text, (235, last_y_pos+60))
        icons_text = [[loop_icon_img, "- Loop mode active icon:"],
                      [sample_warning_icon_img, "- There are over 15 wav files in the sample directory:"],
                      [lines_visible_icon_img, "- Guides line are visible:"]]
        for i, text in enumerate(icons_text):
            font_text = font_24.render(text[1], True, theme["bar"])
            screen.blit(font_text, (235, last_y_pos+100+i*60))
            screen.blit(text[0], (235+len(text[1])*10, last_y_pos+85+i*60))
        ending_text = "[ To go back to the main screen click the right mouse button on the Help button ]"
        font_text = font_16.render(ending_text, True, theme["bar"])
        screen.blit(font_text, (720, 65))


def ControlSettings():
    global theme
    if CheckLeftMouseButtonCollision(settings_button):
        if left_mouse_button_clicked:
            if states["helpVisible"]:
                states["helpVisible"] = False
            states["settingsVisible"] = True
        if right_mouse_button_clicked:
            states["settingsVisible"] = False
    if states["settingsVisible"]:
        states["saveVisible"] = False
        states["helpVisible"] = False
        states["loadVisible"] = False
        pygame.draw.rect(screen, theme["Selected"], settings_button)
        screen.blit(settings_button_img, (1220 - 15, 15))
        pygame.draw.rect(screen, theme["HelpWindow"], pygame.Rect(230, 52, 1040, 658))
        ending_text = "[ To go back to the main screen click the right mouse button on the Settings button ]"
        font_text = font_16.render(ending_text, True, theme["bar"])
        screen.blit(font_text, (720, 65))
        font_text = font.render("Color theme: ", True, theme["bar"])
        screen.blit(font_text, (235, 57))
        dark_rect = pygame.Rect(270, 100, 100, 50)
        pygame.draw.rect(screen, dark_theme["Background"], dark_rect)
        light_rect = pygame.Rect(420, 100, 100, 50)
        pygame.draw.rect(screen, light_theme["Background"], light_rect)
        selected_borders = [pygame.Rect(270,100,100,1), pygame.Rect(270,100,1,50), pygame.Rect(270,150,100,1), pygame.Rect(370,100,1,50)]
        if theme == light_theme:
            selected_borders = [pygame.Rect(420,100,100,1), pygame.Rect(420,100,1,50), pygame.Rect(420,150,100,1), pygame.Rect(520,100,1,50)]
        for border in selected_borders:
            pygame.draw.rect(screen,theme["Selected"],border,3)
        if CheckLeftMouseButtonCollision(dark_rect):
            if left_mouse_button_clicked:
                theme = dark_theme
                # Update color of loop rects
                buttons = loop_buttons_4bar
                if states["length"] == 8:
                    buttons = loop_buttons_8bar
                for button in buttons:
                    button.color = theme["bar"]
        if CheckLeftMouseButtonCollision(light_rect):
            if left_mouse_button_clicked:
                theme = light_theme
                # Update color of loop rects
                buttons = loop_buttons_4bar
                if states["length"] == 8:
                    buttons = loop_buttons_8bar
                for button in buttons:
                    button.color = theme["bar"]


def ControlErrorDisplay():
    error_pos = (1000, 100)
    error_close_rect.y = 100
    if states["loadVisible"]:
        error_pos = (1000, 52)
        error_close_rect.y = 52
    if errors["sampleLimit"][0]:
        error_area.x = error_pos[0]
        error_area.y = error_pos[1]
        if not errors["sampleLimit"][1]:
            states["errorVisible"] = True
            errors["sampleLimit"][1] = True
        if states["errorVisible"]:
            pygame.draw.rect(screen, theme["Selected"], error_area)
            font_text = font_16.render("[x]", True, (0, 0, 0))
            screen.blit(font_text, (1242, error_pos[1]))
            DisplayErrorMessage("Too many samples in 'samples' directory (limit is 15).")
            if CheckLeftMouseButtonCollision(error_close_rect):
                if left_mouse_button_clicked:
                    states["errorVisible"] = False
    if errors["notSelectedProject"][0]:
        error_area.x = error_pos[0]
        error_area.y = error_pos[1]
        if not errors["notSelectedProject"][1]:
            states["errorVisible"] = True
            errors["notSelectedProject"][1] = True
        if states["errorVisible"]:
            pygame.draw.rect(screen, theme["Selected"], error_area)
            font_text = font_16.render("[x]", True, (0, 0, 0))
            screen.blit(font_text, (1242, error_pos[1]))
            DisplayErrorMessage("First, select a project to load.")
            if CheckLeftMouseButtonCollision(error_close_rect):
                if left_mouse_button_clicked:
                    states["errorVisible"] = False

def DisplayErrorMessage(message):
    error_pos1 = (1005, 116)
    error_pos2 = (1008, 132)
    if states["loadVisible"]:
        error_pos1 = (1005, 68)
        error_pos2 = (1008, 84)
    text = message
    if len(text) > 55:
        text = text[:55]
        text = text[:-3] + "..."
    text_first_line = ""
    text_second_line = ""
    if len(text) > 32:
        text_first_line = text[:30]
        text_second_line = text[30:]
    else:
        text_first_line = text
    font_text = font_16.render(text_first_line, True, (0, 0, 0))
    screen.blit(font_text, error_pos1)
    font_text = font_16.render(text_second_line, True, (0, 0, 0))
    screen.blit(font_text, error_pos2)

save_is_pressed = False
load_is_pressed = False
def ControlSave():
    global save_is_pressed
    if CheckLeftMouseButtonCollision(save_button):
        if left_mouse_button_clicked:
            states["saveVisible"] = True
        if right_mouse_button_clicked:
            states["saveVisible"] = False
    if states["saveVisible"]:
        states["settingsVisible"] = False
        states["helpVisible"] = False
        states["loadVisible"] = False
        pygame.draw.rect(screen, theme["Selected"], save_button)
        screen.blit(save_button_img, (709, 15))
        pygame.draw.rect(screen, theme["HelpWindow"], pygame.Rect(230, 52, 1040, 658))
        ending_text = "[ To go back to the main screen click the right mouse button on the Save button ]"
        font_text = font_16.render(ending_text, True, theme["bar"])
        screen.blit(font_text, (720, 65))
        pygame.draw.rect(screen, theme["Selected"], save_file_button)

        if CheckLeftMouseButtonCollision(save_file_button):
            if left_mouse_button_clicked:
                if not save_is_pressed:
                    length = states["length"]
                    sample_names = {}
                    loop_button = 10000
                    if length == 4:
                        for button in loop_buttons_4bar:
                            if button.clicked:
                                if loop_button > button.rect.x:
                                    loop_button = button.rect.x
                    else:
                        for button in loop_buttons_8bar:
                            if button.clicked:
                                if loop_button > button.rect.x:
                                    loop_button = button.rect.x
                    for sample in chosen_samples:
                        x_val = []
                        for rect in sample.rectsPos:
                            x_val.append(rect.x)
                        sample_names[sample.name] = x_val
                    data_to_save = {"Length": length, "sample_list": sample_names, "loop_pos":loop_button}
                    with open('saved/new project.json', 'w') as json_file:
                        json.dump(data_to_save, json_file)
                    save_is_pressed = True


def ReadProjects():
    global project_names
    projects = glob("./saved/*.json")
    for proj in projects:
        name = proj.split("\\")[-1]
        short_name = name.split(".json")
        if short_name[0] not in project_names:
            project_names.append(short_name[0])


def ControlLoad():
    global load_is_pressed, project_names, project_buttons, selected_project, errors
    if CheckLeftMouseButtonCollision(load_button):
        if left_mouse_button_clicked:
            states["loadVisible"] = True
        if right_mouse_button_clicked:
            states["loadVisible"] = False
    if states["loadVisible"]:
        states["settingsVisible"] = False
        states["helpVisible"] = False
        states["saveVisible"] = False
        pygame.draw.rect(screen, theme["Selected"], load_button)
        screen.blit(load_button_img, (709+65, 15))
        pygame.draw.rect(screen, theme["HelpWindow"], pygame.Rect(230, 52, 1040, 658))
        ending_text = "[ To go back to the main screen click the right mouse button on the Load button ]"
        font_text = font_16.render(ending_text, True, theme["bar"])
        screen.blit(font_text, (720, 65))
        load_text = "Selected project: "
        if selected_project is not None:
            load_text += selected_project[0]
        font_text = font_24.render(load_text, True, theme["bar"])
        screen.blit(font_text, (720, 100))

        load_text = "[ To load project click the Load project button ]"
        font_text = font_16.render(load_text, True, theme["bar"])
        screen.blit(font_text, (720, 140))

        pygame.draw.rect(screen, theme["Second"], load_file_button)
        screen.blit(load_project_button_img, (720, 160))

        pygame.draw.rect(screen, theme["Second"], pygame.Rect(235, 57, 480, 648))

        ReadProjects()

        # Display list of available projects
        if len(project_names) < 14:
            for i, proj in enumerate(project_names):
                rect = pygame.Rect(240, 62+i*45, 450, 40)
                if rect not in project_buttons:
                    project_buttons.append(rect)
                pygame.draw.rect(screen, theme["HelpWindow"], rect)
                if selected_project is not None and rect == selected_project[1]:
                    pygame.draw.rect(screen, theme["Selected"], rect)
                if CheckLeftMouseButtonCollision(rect):
                    if left_mouse_button_clicked:
                        selected_project = [proj, rect]
                font_text = font_24.render(proj, True, theme["bar"])
                screen.blit(font_text, (245, 68+i*45))
        else:
            for i, proj in enumerate(project_names):
                if i < 14:
                    rect = pygame.Rect(240, 62+i*45, 450, 40)
                    if rect not in project_buttons:
                        project_buttons.append(rect)
                    pygame.draw.rect(screen, theme["HelpWindow"], rect)
                    if selected_project is not None and rect == selected_project[1]:
                        pygame.draw.rect(screen, theme["Selected"], rect)
                    if CheckLeftMouseButtonCollision(rect):
                        if left_mouse_button_clicked:
                            selected_project = [proj, rect]
                    font_text = font_24.render(proj, True, theme["bar"])
                    screen.blit(font_text, (245, 68+i*45))
            pygame.draw.rect(screen, theme["HelpWindow"], scroll_area)
            pygame.draw.rect(screen, theme["bar"], select_project_scroll_button)
            mouse_pos = pygame.mouse.get_pos()
            if CheckLeftMouseButtonCollision(select_project_scroll_button):
                if left_mouse_button_clicked:
                    select_project_scroll_button.y = mouse_pos[1]-17
            if CheckLeftMouseButtonCollision(scroll_area):
                if left_mouse_button_clicked:
                    select_project_scroll_button.y = mouse_pos[1] - 17
            if select_project_scroll_button.bottom > 700:
                select_project_scroll_button.bottom = 700
            if select_project_scroll_button.top < 62:
                select_project_scroll_button.top = 62
        # Load project if load_project button is clicked or display error
        if CheckLeftMouseButtonCollision(load_file_button):
            if left_mouse_button_clicked:
                pygame.draw.rect(screen, theme["Selected"], load_file_button)
                screen.blit(load_project_button_img, (720, 160))
                if not load_is_pressed:
                    if selected_project is None:
                        errors["notSelectedProject"][0] = True
                    else:
                        LoadProject()
                    load_is_pressed = True



def LoadProject():
    global selected_project, states, six_qty, beats_qty, bars_qty, line, bar_line
    with open('saved/'+str(selected_project[0])+'.json') as json_file:
        data = json.load(json_file)
    states["loadVisible"] = False
    states["length"] = data["Length"]
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
        for button in loop_buttons_4bar:
            if button.rect.x == data["loop_pos"]:
                button.clicked = True
                button.color = theme["Selected"]
            else:
                button.clicked = False
                button.color = theme["bar"]
    if states["length"] == 8:
        six_qty = 129
        beats_qty = 33
        bars_qty = 9
        for button in loop_buttons_8bar:
            if button.rect.x == data["loop_pos"]:
                button.clicked = True
                button.color = theme["Selected"]
            else:
                button.clicked = False
                button.color = theme["bar"]
    for dict in data["sample_list"]:
        print(dict, data["sample_list"][dict])
        for sample in sample_list:
            if sample.name == dict:
                if states["length"] == 4:
                    for i in range(64):
                        sample.rects_list.append(pygame.Rect(238 + i * 16, 125 + len(chosen_samples) * 40, 15, 10))
                    for pos in data["sample_list"][dict]:
                        for rect in sample.rects_list:
                            if rect.x == pos:
                                sample.rectsPos.append(rect)
                    chosen_samples.append(sample)




# main program loop
while True:
    # draw background
    screen.fill(theme["Background"])
    # control events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        if event.type == pygame.KEYDOWN:
            actual_key = event.key
            if event.key == pygame.K_SPACE:
                if not states["helpVisible"] or not states["settingsVisible"]:
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
                save_is_pressed = False
                load_is_pressed = False
                left_mouse_button_clicked = False
                states["playButtonClicked"] = False
                states["pauseButtonClicked"] = False
                states["restartButtonClicked"] = False
            if event.button == 3:
                right_mouse_button_clicked = False
    ## screen objects
    # left rect section
    pygame.draw.rect(screen, theme["Main"], pygame.Rect(10, 10, 210, 700))

    # top rect section
    # play, pause, restart container
    pygame.draw.rect(screen, theme["Main"], pygame.Rect(585, 10, 110, 40))

    pygame.draw.rect(screen, theme["Second"], play_button)
    screen.blit(play_button_img, (590, 15))

    pygame.draw.rect(screen, theme["Second"], pause_button)
    screen.blit(pause_button_img, (625, 15))

    pygame.draw.rect(screen, theme["Second"], restart_button)
    screen.blit(restart_button_img, (660, 15))

    # save, load container
    pygame.draw.rect(screen, theme["Main"], pygame.Rect(705, 10, 135, 40))
    pygame.draw.rect(screen, theme["Second"], save_button)
    screen.blit(save_button_img, (709, 15))
    pygame.draw.rect(screen, theme["Second"], load_button)
    screen.blit(load_button_img, (709+65, 15))

    # settings, help container
    pygame.draw.rect(screen, theme["Main"], pygame.Rect(1135, 10, 135, 40))
    pygame.draw.rect(screen, theme["Second"], help_button)
    screen.blit(help_button_img, (1220-80, 15))

    pygame.draw.rect(screen, theme["Second"], settings_button)
    screen.blit(settings_button_img, (1220-15, 15))

    # middle rect section
    pygame.draw.rect(screen, theme["Main"], pygame.Rect(230, 60, 1040, 650))
    # draw bar display
    pygame.draw.rect(screen, theme["Second"], pygame.Rect(238, 65, 1024, 20))

    # draw main middle container
    pygame.draw.rect(screen, theme["Second"], pygame.Rect(238, 100, 1024, 600))

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
        end_pos = (238+i*(1024/(six_qty-1)), 84)
        if states["linesVisible"]:
            end_pos = (238+i*(1024/(six_qty-1)), 700)
        pygame.draw.line(screen, theme["six"], (int(238+i*(1024/(six_qty-1))), 65), end_pos)
    for i in range(beats_qty):
        end_pos = (238+i*(1024/(beats_qty-1)), 84)
        if states["linesVisible"]:
            end_pos = (238+i*(1024/(beats_qty-1)), 700)
        pygame.draw.line(screen, theme["beat"], (int(238+i*(1024/(beats_qty-1))), 65), end_pos)

    for i in range(bars_qty):
        end_pos = (238 + i * (1024/(bars_qty-1)), 84)
        if states["linesVisible"]:
            end_pos = (238+i*(1024/(bars_qty-1)), 700)
        pygame.draw.line(screen, theme["bar"], (int(238+i*(1024/(bars_qty-1))), 65), end_pos)

    # draw playing line
    pygame.draw.rect(screen, line.color, line.rect)
    # draw playing bar line
    pygame.draw.rect(screen, bar_line.color, bar_line.rect)

    pygame.draw.rect(screen, theme["Second"], four_bar_button)
    screen.blit(four_bar_button_img, (320, 15))

    pygame.draw.rect(screen, theme["Second"], eight_bar_button)
    screen.blit(eight_bar_button_img, (360, 15))

    ControlSelectingLength()

    ControlHelp()

    ControlSettings()

    ControlSave()

    ControlLoad()

    ControlErrorDisplay()

    pygame.display.update()

    clock.tick(60)
