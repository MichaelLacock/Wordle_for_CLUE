# =================================
# ======== WORDLE for CLUE ========
# ===== Michael Lacock, 2022 ======
# =================================

# UPDATED on 2-17-2022, made with new and modified word list.

# Optional use of the BBQ10 Keyboard library by arturo182.
# Works with the SolderParty and TTGO T-Watch BBQ10 keyboard driver board.

# You can also use the A and B buttons on the Clue to select letters.

import board
import time
import random
import terminalio
import displayio
from adafruit_clue import clue
from adafruit_datetime import datetime, date
import busio
from bbq10keyboard import BBQ10Keyboard, STATE_PRESS, STATE_RELEASE, STATE_LONG_PRESS
from adafruit_display_text import label

def letter_square (row, placement, mode, letter):
    size = (30, 30)

    if (row == 1):
        letter_y = 30
    if (row == 2):
        letter_y = 65
    if (row == 3):
        letter_y = 100
    if (row == 4):
        letter_y = 135
    if (row == 5):
        letter_y = 170
    if (row == 6):
        letter_y = 205

    if (placement == 1):
        letter_x = (35 + letter_select_offset)
    if (placement == 2):
        letter_x = (70 + letter_select_offset)
    if (placement == 3):
        letter_x = (105 + letter_select_offset)
    if (placement == 4):
        letter_x = (140 + letter_select_offset)
    if (placement == 5):
        letter_x = (175 + letter_select_offset)

    if (mode == 0):  #blank
        if letter == 0:
            inner_bitmap = displayio.Bitmap(size[0], size[1], 1)
            inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=color_grey, x=letter_x, y=letter_y)
            screen.append(inner_sprite)

            inner_bitmap = displayio.Bitmap((size[0] - 4), (size[1] - 4), 1)
            inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=color_dark, x=(letter_x + 2), y=(letter_y + 2))
            screen.append(inner_sprite)

    if (mode == 1):  #grey
        inner_bitmap = displayio.Bitmap(size[0], size[1], 1)
        inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=color_grey, x=letter_x, y=letter_y)
        screen.append(inner_sprite)

    if (mode == 2):  #yellow
        inner_bitmap = displayio.Bitmap(size[0], size[1], 1)
        inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=color_yellow, x=letter_x, y=letter_y)
        screen.append(inner_sprite)

    if (mode == 3):  #green
        inner_bitmap = displayio.Bitmap(size[0], size[1], 1)
        inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=color_green, x=letter_x, y=letter_y)
        screen.append(inner_sprite)

    if not mode == 0: #This makes sure there isn't an annoying memory overflow.
        if (delete_under == 1):
            del screen[2]
            del screen[2]

    if not letter == 0:
        #text_group = displayio.Group(scale=1, x=(letter_x + 7), y=(letter_y + 14))
        #text = letter
        #text_area = label.Label(font, text=text, color=0xd8dadc)
        #text_group.append(text_area)
        #screen.append(text_group)

        text_group = displayio.Group(scale=2, x=(letter_x + 9), y=(letter_y + 14))
        text = letter
        text_area = label.Label(terminalio.FONT, text=text, color=0xd8dadc)
        text_group.append(text_area)
        screen.append(text_group)

def blank_squares ():
    letter_square(1, 1, 0, 0)
    letter_square(1, 2, 0, 0)
    letter_square(1, 3, 0, 0)
    letter_square(1, 4, 0, 0)
    letter_square(1, 5, 0, 0)

    letter_square(2, 1, 0, 0)
    letter_square(2, 2, 0, 0)
    letter_square(2, 3, 0, 0)
    letter_square(2, 4, 0, 0)
    letter_square(2, 5, 0, 0)

    letter_square(3, 1, 0, 0)
    letter_square(3, 2, 0, 0)
    letter_square(3, 3, 0, 0)
    letter_square(3, 4, 0, 0)
    letter_square(3, 5, 0, 0)

    letter_square(4, 1, 0, 0)
    letter_square(4, 2, 0, 0)
    letter_square(4, 3, 0, 0)
    letter_square(4, 4, 0, 0)
    letter_square(4, 5, 0, 0)

    letter_square(5, 1, 0, 0)
    letter_square(5, 2, 0, 0)
    letter_square(5, 3, 0, 0)
    letter_square(5, 4, 0, 0)
    letter_square(5, 5, 0, 0)

    letter_square(6, 1, 0, 0)
    letter_square(6, 2, 0, 0)
    letter_square(6, 3, 0, 0)
    letter_square(6, 4, 0, 0)
    letter_square(6, 5, 0, 0)

def clear_screen ():
    for i in range(len(screen)):
        del screen[-1]

    bitmap_fullscreen = displayio.Bitmap(240, 240, 1)
    background = displayio.TileGrid(bitmap_fullscreen, pixel_shader=color_dark, x=0, y=0)
    screen.append(background)

    logo = displayio.OnDiskBitmap("/local/logo_small.bmp")
    tile_grid = displayio.TileGrid(logo, pixel_shader=logo.pixel_shader, x=66, y=6)
    screen.append(tile_grid)

def capitalize (letter):
    letter = letter.replace("a", "A")
    letter = letter.replace("b", "B")
    letter = letter.replace("c", "C")
    letter = letter.replace("d", "D")
    letter = letter.replace("e", "E")
    letter = letter.replace("f", "F")
    letter = letter.replace("g", "G")
    letter = letter.replace("h", "H")
    letter = letter.replace("i", "I")
    letter = letter.replace("j", "J")
    letter = letter.replace("k", "K")
    letter = letter.replace("l", "L")
    letter = letter.replace("m", "M")
    letter = letter.replace("n", "N")
    letter = letter.replace("o", "O")
    letter = letter.replace("p", "P")
    letter = letter.replace("q", "Q")
    letter = letter.replace("r", "R")
    letter = letter.replace("s", "S")
    letter = letter.replace("t", "T")
    letter = letter.replace("u", "U")
    letter = letter.replace("v", "V")
    letter = letter.replace("w", "W")
    letter = letter.replace("x", "X")
    letter = letter.replace("y", "Y")
    letter = letter.replace("z", "Z")

    return (letter)

def check (current_attempt, current_row):
    good_count = 0
    for i in range(5): # Makes it so that only 62 elements are displayed at any given time.
        del screen[-1]
    for i in range(5):

        current_letter_check = current_attempt[i]
        if (current_attempt[i] == word[i]):
            good_count = (good_count + 1)
            letter_square(current_row, (i + 1), 3, current_attempt[i])
        elif (current_attempt[i] in word):
            letter_square(current_row, (i + 1), 2, current_attempt[i])
        else:
            letter_square(current_row, (i + 1), 1, current_attempt[i])

    if (good_count == 5):
        return (1)
    else:
        return (0)

def get_day ():
    clear_screen()

    text_group = displayio.Group(scale=2, x=20, y=80)
    text = "Month"
    text_area = label.Label(terminalio.FONT, text=text, color=0xd8dadc)
    text_group.append(text_area)
    screen.append(text_group)

    text_group = displayio.Group(scale=2, x=105, y=80)
    text = "Day"
    text_area = label.Label(terminalio.FONT, text=text, color=0xd8dadc)
    text_group.append(text_area)
    screen.append(text_group)

    text_group = displayio.Group(scale=2, x=165, y=80)
    text = "Year"
    text_area = label.Label(terminalio.FONT, text=text, color=0xd8dadc)
    text_group.append(text_area)
    screen.append(text_group)

    size = (60, 30)
    inner_bitmap = displayio.Bitmap(size[0], size[1], 1)
    inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=color_grey, x=20, y=100)
    screen.append(inner_sprite)

    inner_bitmap = displayio.Bitmap((size[0] - 4), (size[1] - 4), 1)
    inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=color_dark, x=22, y=102)
    screen.append(inner_sprite)

    size = (60, 30)
    inner_bitmap = displayio.Bitmap(size[0], size[1], 1)
    inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=color_grey, x=90, y=100)
    screen.append(inner_sprite)

    inner_bitmap = displayio.Bitmap((size[0] - 4), (size[1] - 4), 1)
    inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=color_dark, x=92, y=102)
    screen.append(inner_sprite)

    size = (60, 30)
    inner_bitmap = displayio.Bitmap(size[0], size[1], 1)
    inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=color_grey, x=160, y=100)
    screen.append(inner_sprite)

    inner_bitmap = displayio.Bitmap((size[0] - 4), (size[1] - 4), 1)
    inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=color_dark, x=162, y=102)
    screen.append(inner_sprite)

    Month = 0
    Day = 0
    Year = 0

    press_number = 0
    digit_placement = 1
    all_numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

    current_input = []
    current_text = ""
    MDY_placement = 1
    date_set = 0
    while date_set == 0:
        if (keyboard_available == 1):
            key_count = kbd.key_count
            if key_count > 0:
                key = kbd.key
                state = 'pressed'
                if key[0] == STATE_LONG_PRESS:
                    state = 'held down'
                elif key[0] == STATE_RELEASE:
                    state = 'released'

                if (state == 'pressed'):
                    if (key[1] == "\x08"): #delete
                        if (len(current_input)) > 0:
                            del screen[-1]
                            del current_input[-1]

                    elif (key[1] == "\n"): #enter
                        if (MDY_placement == 1):
                            Month_str = current_text
                            if not Month_str == "":
                                try:
                                    Month = int(Month_str)
                                except:
                                    Month = 0
                            else:
                                Month = 0

                            current_input = []
                            MDY_placement = 2
                        elif (MDY_placement == 2):
                            Day_str = current_text
                            if not Day_str == "":
                                try:
                                    Day = int(Day_str)
                                except:
                                    Day = 0
                            else:
                                Day = 0

                            current_input = []
                            MDY_placement = 3
                        elif (MDY_placement == 3):
                            Year_str = current_text
                            if not Year_str == "":
                                try:
                                    Year = int(Year_str)
                                except:
                                    Year = 0
                            else:
                                Year = 0

                            current_input = []
                            current_text = ""
                            date_set = 1
                        else:
                            print("[-] Could not set date.")
                            date_set = 1

                    else:
                        current_number = (key[1])
                        current_input.append(current_number)
                        current_text = ""
                        for i in range(len(current_input)):
                            current_text += current_input[i]

                        if (MDY_placement == 1):
                            length = len(current_text)
                            current_x = (25 + (length * 12))
                            current_y = 112

                        if (MDY_placement == 2):
                            length = len(current_text)
                            current_x = (97 + (length * 12))
                            current_y = 112

                        if (MDY_placement == 3):
                            length = len(current_text)
                            current_x = (157 + (length * 12))
                            current_y = 112

                        text_group = displayio.Group(scale=2, x=current_x, y=current_y)
                        text = current_number
                        text_area = label.Label(terminalio.FONT, text=text, color=0xd8dadc)
                        text_group.append(text_area)
                        screen.append(text_group)


        else:
            if clue.button_a:
                if not press_number == 0:
                    del screen[-1]
                    del current_input[-1]

                press_number = (press_number + 1)
                time.sleep(0.3)
                if (press_number > 10):
                    press_number = 1

                current_number = all_numbers[(press_number - 1)]
                current_input.append(current_number)

                current_text = ""
                for i in range(len(current_input)):
                    current_text += current_input[i]

                if (MDY_placement == 1):
                    length = len(current_text)
                    current_x = (25 + (length * 12))
                    current_y = 112

                if (MDY_placement == 2):
                    length = len(current_text)
                    current_x = (97 + (length * 12))
                    current_y = 112

                if (MDY_placement == 3):
                    length = len(current_text)
                    current_x = (157 + (length * 12))
                    current_y = 112

                text_group = displayio.Group(scale=2, x=current_x, y=current_y)
                text = current_number
                text_area = label.Label(terminalio.FONT, text=text, color=0xd8dadc)
                text_group.append(text_area)
                screen.append(text_group)

            if clue.button_b:
                if (MDY_placement == 1):
                    if (digit_placement == 2):
                        press_number = 0
                        digit_placement = 1
                        time.sleep(0.5)
                        MDY_placement = (MDY_placement + 1)

                        Month_str = current_text
                        try:
                            Month = int(Month_str)
                        except:
                            Month = 0

                        current_input = []

                    else:
                        press_number = 0
                        digit_placement = (digit_placement + 1)
                        time.sleep(0.3)

                elif (MDY_placement == 2):
                    if (digit_placement == 2):
                        press_number = 0
                        digit_placement = 1
                        time.sleep(0.5)
                        MDY_placement = (MDY_placement + 1)

                        Day_str = current_text
                        try:
                            Day = int(Day_str)
                        except:
                            Day = 0

                        current_input = []
                    else:
                        press_number = 0
                        digit_placement = (digit_placement + 1)
                        time.sleep(0.3)

                elif (MDY_placement == 3):
                    if (digit_placement == 4):
                        press_number = 0
                        digit_placement = 1
                        time.sleep(0.5)
                        MDY_placement = (MDY_placement + 1)

                        Year_str = current_text
                        try:
                            Year = int(Year_str)
                        except:
                            Year = 0

                        current_input = []
                        current_text = ""
                        date_set = 1
                    else:
                        press_number = 0
                        digit_placement = (digit_placement + 1)
                        time.sleep(0.3)

                else:
                            print("[-] Could not set date.")
                            date_set = 1

    if not Year == 0:
        today = datetime(Year, Month, Day)
        start_date = datetime(2021, 06, 18)

        day = (today - start_date).days
    else:
        day = random.randint(0, 2000)
    print(day)

    time.sleep(2)

    return (day)

i2c = board.I2C()

try:
    kbd = BBQ10Keyboard(i2c)
    kbd.backlight = 1

    keyboard_available = 1
except:
    keyboard_available = 0

x_pos = 30
y_pos = 30

display = board.DISPLAY

screen = displayio.Group()
display.show(screen)

color_dark = displayio.Palette(1)
color_dark[0] = (18, 18, 19) #dark

color_light = displayio.Palette(1)
color_light[0] = (216, 218, 220) #light

color_grey = displayio.Palette(1)
color_grey[0] = (58, 58, 60) #grey

color_yellow = displayio.Palette(1)
color_yellow[0] = (178, 159, 76) #yellow

color_green = displayio.Palette(1)
color_green[0] = (96, 139, 85) #green

delete_under = 1
letter_select_offset = 0

day = get_day()

clear_screen()
blank_squares()

count = 1
words_file = open('/local/words_new.txt', 'r')
for line in words_file:
    if (count == day):
        word = line
    count = (count + 1)
words_file.close()

press_letter = 0
all_letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

current_attempt = []
current_row = 1
current_placement = 1
game_over = 0
win = 0
while game_over == 0:
    if (keyboard_available == 1):
        key_count = kbd.key_count
        if key_count > 0:
            key = kbd.key
            state = 'pressed'
            if key[0] == STATE_LONG_PRESS:
                state = 'held down'
            elif key[0] == STATE_RELEASE:
                state = 'released'

            if (state == 'pressed'):
                if (key[1] == "\x08"): #delete
                    current_placement = (len(current_attempt) + 1)
                    if current_placement > 1:
                        del screen[-1]
                        del current_attempt[-1]

                elif (key[1] == "\n"): #enter
                    current_placement = (len(current_attempt) + 1)
                    if current_placement > 5:
                        result = check(current_attempt, current_row)

                        if (result == 0):
                            current_row = (current_row + 1)
                            if (current_row == 7):
                                game_over = 1
                            else:
                                current_attempt = []
                                current_placement = 1

                        if (result == 1):
                            win = 1
                            game_over = 1

                else:
                    current_letter = (key[1])
                    current_letter = capitalize(current_letter)

                    current_placement = (len(current_attempt) + 1)
                    if not current_placement > 5:
                        current_attempt.append(current_letter)
                        letter_square(current_row, current_placement, 0, current_letter)


    else:
        if clue.button_a:
            if not press_letter == 0:
                del screen[-1]
                del current_attempt[-1]

            press_letter = (press_letter + 1)
            time.sleep(0.3)
            if (press_letter > 26):
                press_letter = 1

            current_letter = all_letters[(press_letter - 1)]
            current_placement = (len(current_attempt) + 1)
            if not current_placement > 5:
                current_attempt.append(current_letter)
                letter_square(current_row, current_placement, 0, current_letter)

        if clue.button_b:
            current_placement = (len(current_attempt) + 1)
            if not current_placement > 5:
                press_letter = 0
                time.sleep(0.3)
                current_placement = (current_placement + 1)
            else:
                press_letter = 0
                result = check(current_attempt, current_row)

                if (result == 0):
                    current_row = (current_row + 1)
                    if (current_row == 7):
                        game_over = 1
                    else:
                        current_attempt = []
                        current_placement = 1

                if (result == 1):
                    win = 1
                    game_over = 1


if (win == 1):
    time.sleep(2)
    clear_screen() # Memory overflow tends to occour if this isn't here.
    inner_bitmap = displayio.Bitmap(200, 40, 1)
    inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=color_green, x=20, y=90)
    screen.append(inner_sprite)

    text_group = displayio.Group(scale=2, x=52, y=108)
    text = "You Got It!"
    text_area = label.Label(terminalio.FONT, text=text, color=0xd8dadc)
    text_group.append(text_area)
    screen.append(text_group)

    time.sleep(12000)

else:
    clear_screen()
    inner_bitmap = displayio.Bitmap(200, 40, 1)
    inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=color_yellow, x=20, y=90)
    screen.append(inner_sprite)

    text_group = displayio.Group(scale=2, x=56, y=108)
    text = "Game Over."
    text_area = label.Label(terminalio.FONT, text=text, color=0xd8dadc)
    text_group.append(text_area)
    screen.append(text_group)

    time.sleep(12000)

