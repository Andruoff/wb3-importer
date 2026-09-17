# Add a function that checks when this was most recently updated.
# fix capitalization stuff

# note to self. python -m auto_py_to_exe to export this
# "C:\Users\andre\AppData\Local\Python\pythoncore-3.14-64\fribidi.dll"

import gspread
import csv
import PIL
from PIL import Image, ImageGrab, ImageDraw, ImageText, ImageFont

import random
import textwrap

import sys
import os

# Yoinked code

def resource_path(relative_path):
    # Get absolute path to resource, works for dev and for PyInstaller
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

CARD_WIDTH = 250
CARD_HEIGHT = 350

SHEET_CARD_HEIGHT = 4
SHEET_CARD_WIDTH = 10
SHEET_SIZE = SHEET_CARD_HEIGHT * SHEET_CARD_WIDTH
SHEET_HEIGHT = CARD_HEIGHT * SHEET_CARD_HEIGHT
SHEET_WIDTH = CARD_WIDTH * SHEET_CARD_WIDTH

main_dims = {"card_height": SHEET_CARD_HEIGHT, "card_width": SHEET_CARD_WIDTH, "size": SHEET_SIZE, "height": SHEET_HEIGHT, "width": SHEET_WIDTH}

E_SHEET_CARD_HEIGHT = 2
E_SHEET_CARD_WIDTH = 10
E_SHEET_SIZE = E_SHEET_CARD_HEIGHT * E_SHEET_CARD_WIDTH
E_SHEET_HEIGHT = CARD_HEIGHT * E_SHEET_CARD_HEIGHT
E_SHEET_WIDTH = CARD_WIDTH * E_SHEET_CARD_WIDTH

extra_dims = {"card_height": E_SHEET_CARD_HEIGHT, "card_width": E_SHEET_CARD_WIDTH, "size": E_SHEET_SIZE, "height": E_SHEET_HEIGHT, "width": E_SHEET_WIDTH}


reader = gspread.api_key("AIzaSyDOsvY1riiBGMfHEN4m0oLA2V4TENxn2OU")
sheet = reader.open_by_key("1RyVuXuTbjReXnPB0BYGq-aMEtmI_Z3HK2iEkngKHFN4")
filename = resource_path("card_data.csv")
fontfilename = resource_path("times-new-roman.ttf")
decklistfile = resource_path("decklist_here.txt")

huge_font = ImageFont.truetype(fontfilename, 28)
big_font = ImageFont.truetype(fontfilename, 22)
medium_font = ImageFont.truetype(fontfilename, 18)
small_font = ImageFont.truetype(fontfilename, 16)

missing_cards = []

def find_card(name):
    
    with open(filename, "r") as f:

        data = csv.DictReader(f, delimiter="|")


        for row in data:
            if row["Name"].lower() == str(name).lower():

                return row

    
    #raise Exception("Card \"" + name + "\"does not exist.")

def decklist_checker(decklist):

    print("Have you pasted your decklist into \"decklist_here\" properly? (Y/N)")
    answer = input()
    match answer:
        case "N" | "n" | "no" | "No":
            print("Please do that before running the program thank you.")
            input("Input anything to quit. ")
            quit()
        case _:
            pass

    with open(decklist) as f:
            lines = f.readlines()
    
            if lines[0].strip() == "PASTE HERE":
                print("You forgot to paste your decklist, or pasted it to the wrong spot! Please start over.")
                exit()
    
            if lines[0].strip() == "Main Deck:":
                print("You forgot the deck name! Please check  your formatting against example_decklist.txt. Please start over.")
                decklist_checker(decklist)
    
            deck_name = lines[0].strip()
    
            if lines[1].strip() == "Main Deck:":
                print("Main Deck found.")
            else:
                print("Main Deck not found! Please check  your formatting against example_decklist.txt. Please start over.")
                decklist_checker(decklist)
    
            extra_index = 0
    
            for index in range(len(lines)):
                if lines[index].strip() == "Extra Deck:":
                    extra_index = index
                    print("Extra Deck found.")
                    return extra_index
            if extra_index == 0:
                print("Extra Deck not found! Please check  your formatting against example_decklist.txt. Please start over.")
                decklist_checker(decklist)

    pass

def gen_from_decklist(decklist):

    main_deck = []
    extra_deck = []

    
    extra_index = decklist_checker(decklist)

    with open(decklist) as f:
        lines = f.readlines()


        deck_name = lines[0].strip()


        for index in range(2, extra_index - 1):
            
            count = int(lines[index][0])

            unfinished_name = lines[index].strip()
            #print(unfinished_name)
            unfinished_name = unfinished_name.replace(unfinished_name[0], "", 1)
            name = unfinished_name.replace(unfinished_name[0], "", 1)
            #print(name)
            for i in range(count):

                main_deck.append(name)

        for index in range(extra_index + 1, len(lines)):

            count = int(lines[index][0])
            
            unfinished_name = lines[index].strip()
            #print(unfinished_name)
            unfinished_name = unfinished_name.replace(unfinished_name[0], "", 1)
            name = unfinished_name.replace(unfinished_name[0], "", 1)
            #print(name)

            for i in range(count):

                extra_deck.append(name)

    if getattr(sys, "frozen", False):
        exe_dir = os.path.dirname(sys.executable)
    else:
        exe_dir = os.path.dirname(os.path.abspath(__file__))
    print(exe_dir + "\\" + deck_name + "_main.jpg")

    # deck splitter

    main_1 = []
    main_2 = []
    for i in range(0, 39):
        #print(i)
        if len(main_deck) >= i:
            main_1.append(main_deck[i])
    for i in range(40, 79):
        #print(i)
        if len(main_deck) >= i:
            main_2.append(main_deck[i])

    
    generate_sheet(main_1, main_dims, exe_dir + "\\" + deck_name + "_main_1.jpg")
    generate_sheet(main_2, main_dims, exe_dir + "\\" + deck_name + "_main_2.jpg")
    print("Main Decks made.")
    generate_sheet(extra_deck, extra_dims, exe_dir + "\\" + deck_name + "_extra.jpg")
    print("Extra Deck made")

    return

def generate_card_list(length, index):

    card_list = []

    with open(filename, "r") as f:

        data = csv.DictReader(f, delimiter="|")

        for i in range(index):
            next(data)

        counter = 0

        for row in data:

            if row["Name"]:
                card_list.append(row["Name"])
                #print(row["Name"])
                counter += 1
                if counter > length: 
                    next(data)
            
    
    return card_list
  
def generate_card(card_name):

    # I should make this color depending on what it expends for maybe
    row_data = find_card(card_name)

    if row_data == None:
        return

    color = (245, 245, 245)


    if row_data["Expend Value"].__contains__("R"):
        color = (255, 200, 200)
    if row_data["Expend Value"].__contains__("W"):
        color = (255, 255, 240)
    if row_data["Expend Value"].__contains__("B"):
        color = (180, 150, 220)
    if row_data["Expend Value"].__contains__("G"):
        color = (200, 250, 200)
    if row_data["Expend Value"].__contains__("U"):
        color = (170, 200, 255)
    

    new_card = PIL.Image.new("RGB", (CARD_WIDTH, CARD_HEIGHT), color)
    #(random.randint(100, 255), random.randint(100, 255), 255)
    

    

    drawer = ImageDraw.Draw(new_card)

    # Name
    name_text = ImageText.Text(row_data['Name'], big_font, "RGB", 4, "ltr")
    drawer.text((CARD_WIDTH / 2, CARD_HEIGHT * .1), name_text, "BLACK", anchor="ms", align="center")

    # Mana
    mana_text = ImageText.Text(row_data['Mana Cost'], big_font, "RGB", 4, "ltr")
    drawer.text((CARD_WIDTH / 2, CARD_HEIGHT * .15), mana_text, "BLACK", anchor="ms", align="center")

    # Typeline
    type_text_text = str(row_data['Type'] + " - " + row_data['Subtype'])
    type_text = ImageText.Text(type_text_text, medium_font, "RGB", 4, "ltr")
    drawer.text((CARD_WIDTH / 2, CARD_HEIGHT * .5), type_text, "BLACK", anchor="ms", align="center")

    # Rules Text
    raw_rules_text = row_data['Oracle Text'].strip()

    if len(raw_rules_text) > 50:

        rules_text_list = textwrap.wrap(raw_rules_text, 30)
        wrapped_rules_text = "\n".join(rules_text_list)
        
        rules_text = ImageText.Text(wrapped_rules_text, small_font, "RGB", 4, "ltr")
        drawer.multiline_text((CARD_WIDTH / 2, CARD_HEIGHT * .57), rules_text, "BLACK", anchor="ms", align="center")

    else:

        rules_text_list = textwrap.wrap(raw_rules_text, 20)
        wrapped_rules_text = "\n".join(rules_text_list)
        
        rules_text = ImageText.Text(wrapped_rules_text, medium_font, "RGB", 4, "ltr")
        drawer.multiline_text((CARD_WIDTH / 2, CARD_HEIGHT * .57), rules_text, "BLACK", anchor="ms", align="center")

    # Expend Value
    expend_text = ImageText.Text(row_data['Expend Value'], huge_font, "RGB", 4, "ltr")
    drawer.text((CARD_WIDTH / 2, CARD_HEIGHT * .95), expend_text, "BLACK", anchor="ms", align="center")

    return new_card

def set_up():

    print("Hello and welcome to the deck generator!")

    def reimport():
        print("Would you like to update the card database? (Y/N)")
        answer = input()
        #print("Answer: \"" + answer + "\"")
        match answer:
            case "Y" | "y" | "Yes" | "yes":
                print("Reading sheet...")
                with open(filename, 'w') as f:
                    writer = csv.writer(f, quoting=csv.QUOTE_ALL, delimiter="|")
                    writer.writerows(sheet.sheet1.get_all_values())  
                print("Sheet updated!")
            case "N" | "n" | "No" | "no":
                print("Update declined.")
                return
            case _:
                print("Please enter Y or N!")
                reimport()

    reimport()


    # with open(filename, 'w') as f:
    #     writer = csv.writer(f, quoting=csv.QUOTE_ALL, delimiter="|")
    #     writer.writerows(sheet.sheet1.get_all_values())   
        
def generate_sheet(list, dims, name):

    card_array = []

    for i in range(len(list)):
        if find_card(list[i]):
            card_array.append(generate_card(list[i]))
        else:
            missing_cards.append(list[i])

    if missing_cards != []:
        print("Error! These cards were unable to be found:")
        print(missing_cards)
        print("Please start over and try again.")
        input("Input anything to quit. ")
        quit()

    # for i in list:
    #     card_array.append(generate_card(i))

    new_sheet = Image.new("RGB", (dims["width"], dims["height"]))

    array_counter = 0

    for i in range(dims["card_height"]):
        for k in range(dims["card_width"]):
            if array_counter < len(list):
                to_paste = card_array[array_counter]
                new_sheet.paste(to_paste, (CARD_WIDTH * k, CARD_HEIGHT * i))
                array_counter += 1


    new_sheet.save(name)

def main(): 

    set_up()

    gen_from_decklist(decklistfile)

    print("Complete. Program finishing.")
    input("Say Bye")

if __name__ == '__main__':
    main()
