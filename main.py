import gspread
import PIL

CARD_WIDTH = 250
CARD_HEIGHT = 350
key = "AIzaSyDOsvY1riiBGMfHEN4m0oLA2V4TENxn2OU"

def generate_card(card_data: list):
    #new_card = PIL.Image.new("hsv", (CARD_WIDTH, CARD_HEIGHT), (255, 255, 255))
    #new_card.show()
    pass

def main():
    gc = gspread.api_key("AIzaSyDOsvY1riiBGMfHEN4m0oLA2V4TENxn2OU")

    sh = gc.open_by_key("1RyVuXuTbjReXnPB0BYGq-aMEtmI_Z3HK2iEkngKHFN4")

    print(sh.sheet1.get('A1'))
    print("Hi")
    
    generate_card([1])

if __name__ == '__main__':
    main()
