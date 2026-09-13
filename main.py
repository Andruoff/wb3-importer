import gspread
import csv
import PIL
from PIL import Image, ImageGrab, ImageDraw, ImageText, ImageFont

import random
import textwrap

CARD_WIDTH = 250
CARD_HEIGHT = 350
SHEET_CARD_HEIGHT = 8
SHEET_CARD_WIDTH = 10
SHEET_SIZE = SHEET_CARD_HEIGHT * SHEET_CARD_WIDTH
SHEET_HEIGHT = CARD_HEIGHT * SHEET_CARD_HEIGHT
SHEET_WIDTH = CARD_WIDTH * SHEET_CARD_WIDTH

reader = gspread.api_key("AIzaSyDOsvY1riiBGMfHEN4m0oLA2V4TENxn2OU")
sheet = reader.open_by_key("1RyVuXuTbjReXnPB0BYGq-aMEtmI_Z3HK2iEkngKHFN4")
filename = "card_data.csv"

huge_font = ImageFont.truetype("times-new-roman.ttf", 28)
big_font = ImageFont.truetype("times-new-roman.ttf", 22)
medium_font = ImageFont.truetype("times-new-roman.ttf", 18)
small_font = ImageFont.truetype("times-new-roman.ttf", 16)

def find_card(name):
    
    with open(filename, "r") as f:

        data = csv.DictReader(f, delimiter="|")


        for row in data:
            if row["Name"] == name:

                return row

    raise Exception("Card \"" + name + "\"does not exist.")

def gen_from_decklist(decklist):

    main_deck = []
    extra_deck = []

    with open(decklist) as f:
        lines = f.readlines()

        if lines[0].strip() == "PASTE HERE":
            raise Exception("You forgot to paste your decklist, or pasted it to the wrong spot!")

        if lines[0].strip() == "Main Deck:":
            raise Exception("You forgot the deck name! Please check  your formatting against example_decklist.txt")

        deck_name = lines[0].strip()

        if lines[1].strip() == "Main Deck:":
            print("Main Deck found.")
        else:
            raise Exception("Main Deck not found! Please check  your formatting against example_decklist.txt")

        extra_index = 0

        for index in range(len(lines)):
            if lines[index].strip() == "Extra Deck:":
                extra_index = index
                print("Extra Deck found.")
                break
        if extra_index == 0:
            raise Exception("Extra Deck not found! Please check  your formatting against example_decklist.txt")


        for index in range(2, extra_index - 1):
            
            count = int(lines[index][0])

            unfinished_name = lines[index].strip()
            print(unfinished_name)
            unfinished_name = unfinished_name.replace(unfinished_name[0], "", 1)
            name = unfinished_name.replace(unfinished_name[0], "", 1)
            print(name)
            for i in range(count):

                main_deck.append(name)

        for index in range(extra_index + 1, len(lines)):

            count = int(lines[index][0])
            
            unfinished_name = lines[index].strip()
            print(unfinished_name)
            unfinished_name = unfinished_name.replace(unfinished_name[0], "", 1)
            name = unfinished_name.replace(unfinished_name[0], "", 1)
            print(name)

            for i in range(count):

                extra_deck.append(name)
        
        generate_sheet(main_deck, deck_name + "_main.jpg")
        print("main_deck.jpg made.")
        generate_sheet(extra_deck, deck_name + "_extra.jpg")
        print("extra_deck.jpg made.")

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
                    break
            next(data)
            

    return card_list
  
def generate_card(card_name):

    # I should make this color depending on what it expends for maybe
    row_data = find_card(card_name)

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

    with open(filename, 'w') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL, delimiter="|")
        writer.writerows(sheet.sheet1.get_all_values())   
        
def generate_sheet(list, name):

    card_array = []

    for i in list:
        card_array.append(generate_card(i))

    new_sheet = Image.new("RGB", (SHEET_WIDTH, SHEET_HEIGHT))

    array_counter = 0

    for i in range(SHEET_CARD_HEIGHT):
        for k in range(SHEET_CARD_WIDTH):
            if array_counter < len(list):
                to_paste = card_array[array_counter]
                new_sheet.paste(to_paste, (CARD_WIDTH * k, CARD_HEIGHT * i))
                array_counter += 1


    new_sheet.save(name)

def main(): 

    set_up()

    gen_from_decklist("example_decklist.txt")

    print("Complete.")

if __name__ == '__main__':
    main()
