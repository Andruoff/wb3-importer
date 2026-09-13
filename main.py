import gspread
import csv
import PIL
from PIL import Image, ImageGrab, ImageDraw, ImageText, ImageFont

import random

CARD_WIDTH = 250
CARD_HEIGHT = 350
SHEET_CARD_HEIGHT = 4
SHEET_CARD_WIDTH = 5
SHEET_SIZE = SHEET_CARD_HEIGHT * SHEET_CARD_WIDTH
SHEET_HEIGHT = CARD_HEIGHT * SHEET_CARD_HEIGHT
SHEET_WIDTH = CARD_WIDTH * SHEET_CARD_WIDTH

reader = gspread.api_key("AIzaSyDOsvY1riiBGMfHEN4m0oLA2V4TENxn2OU")
sheet = reader.open_by_key("1RyVuXuTbjReXnPB0BYGq-aMEtmI_Z3HK2iEkngKHFN4")
filename = "card_data.csv"


def find_card(name):

    with open(filename, "r") as f:

        data = csv.DictReader(f, delimiter="|")


        for row in data:
            if row["Name"] == name:

                return row

    return None 

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


    new_card = PIL.Image.new("RGB", (CARD_WIDTH, CARD_HEIGHT), (255, 255, 255))
    #(random.randint(100, 255), random.randint(100, 255), 255)
    big_font = ImageFont.truetype("times-new-roman.ttf", 22)
    medium_font = ImageFont.truetype("times-new-roman.ttf", 18)


    row_data = find_card(card_name)

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
    rules_text = ImageText.Text(row_data['Oracle Text'], medium_font, "RGB", 4, "ltr")
    
    #print("This is before the rules text gets wrapped")
    #print(row_data["Oracle Text"])
    wrapped_rules = rules_text.wrap(CARD_WIDTH * .8, CARD_HEIGHT * .4)
    if wrapped_rules:
        print("This is " + row_data["Name"])
        print("These are the rules text after they are wrapped.")
        print(wrapped_rules.text)
    #drawer.multiline_text((CARD_WIDTH / 2, CARD_HEIGHT * .55), wrapped_rules, "BLACK", anchor="ms", align="center")

    # Expend Value
    expend_text = ImageText.Text(row_data['Expend Value'], big_font, "RGB", 4, "ltr")
    drawer.text((CARD_WIDTH / 2, CARD_HEIGHT * .95), expend_text, "BLACK", anchor="ms", align="center")

    return new_card

def set_up():

    with open(filename, 'w') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL, delimiter="|")
        writer.writerows(sheet.sheet1.get_all_values())   
        
def generate_sheet(list):

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


    new_sheet.save("new_sheet.jpg")

def main(): 

    #set_up()


    #example_sheet = ["Paranoid Puppy", "Paranoid Puppy", "Lifewield"]


    new_list = generate_card_list(30, 0)

    generate_sheet(new_list)
    

    # medium_font = ImageFont.truetype("times-new-roman.ttf", 18)

    # img = Image.new('RGB', (128, 48), color='black')
    # img.textsize = 20
    # fit_text(img, 'LongerTextGoesHere', (255,255,0), medium_font)
    # img.show()



    #print(find_card("Paranoid Puppy"))

    print("Complete.")

if __name__ == '__main__':
    main()
