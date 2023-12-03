import pytesseract
from PIL import Image
import cv2
import imutils
from os import listdir

# kuvatiedostot
gen = listdir('./data/general/')
hist = listdir('./data/historical/')

# konfiguraatiot
m = open('modes.txt', 'r')
modes = m.read()
m.close()

# kielet
l = open('langs.txt', 'r')
langs = l.read()
l.close()

# suurennus
zoom_factor = 1.0
def on_mouse_wheel(event, x, y, flags, param):
    global zoom_factor
    if event == cv2.EVENT_MOUSEWHEEL:
        if flags > 0:
            zoom_factor *= 1.1
        else:
            zoom_factor /= 1.1
        img = scaleImg(param, param.shape[1])
        cv2.imshow('result', img)

# skaalaus kuvan näyttämistä varten
def scaleImg(img, width):
    scaled_img = imutils.resize(img, width=int(width * zoom_factor))
    return scaled_img
    
# fontin koko kuvan leveyden mukaan
def scaleFont(width):
    if width <= 400:
        return 0.3
    elif width <= 900:
        return 0.4
    else:
        return 0.8

# kuvanlukija
def reader(params):
    try:
        if params[0] in gen:
            imgurl = f'./data/general/{params[0]}'
        elif params[0] in hist:
            imgurl = f'./data/historical/{params[0]}'
        conf = f'--psm {params[1]} --oem {params[2]}'
        lang = params[3]

        # tekstin tulostus konsoliin
        text = pytesseract.image_to_string(Image.open(imgurl), config=conf, lang=lang)
        print(text)

        try:
            if params[4] == 'b' or params[4] == 'bl':
                # visualisointi
                img = cv2.imread(imgurl)
                height, width, _ = img.shape

                boxes = pytesseract.image_to_boxes(img, lang=lang, config=conf)

                for box in boxes.splitlines():
                    box = box.split(' ')
                    x, y, w, h = int(box[1]), int(box[2]), int(box[3]), int(box[4])
                    cv2.rectangle(img, (x, height - y), (w, height - h), (0, 255, 0), 1)
                    if params[4] == 'bl':
                        cv2.putText(img, box[0], (x, height - y + 13), cv2.FONT_HERSHEY_SIMPLEX, scaleFont(width), (0, 0, 255), 1) # huom fontti ei tue ääkkösiä

                #img = scaleImg(img, width)
                cv2.imshow('result', img)
                cv2.setMouseCallback('result', on_mouse_wheel, img)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
        except:
            print('[ To show visualization, include b (boxes) or bl (boxes and letters) at the end of the command. ]')
    except:
        print('Error: check command')

# käyttöliittymä    
def main():

    command = ''

    while command != 'q':
        print('-------------- Reader --------------')
        print('Help: h')
        print('Quit: q')
        command = input(': ')
        if command == 'q':
            break
        if command == 'h':
            print('--------------- Help ---------------')
            print('Example command: "testi1.jpg 3 3 fin b"')
            print('[filename] [PSM] [OEM] [lang] [visualization]')
            print('Images: i')
            print('Configuration: c')
            print('Languages: l')
            print('Visualization: b = boxes | bl = boxes & letters | empty = none')
        elif command == 'i':
            print('-------------- Images --------------')
            print('General:')
            for file in gen:
                print(f'- {file}')
            print('Historical:')
            for file in hist:
                print(f'- {file}')
        elif command == 'c':
            print('-------------- Config --------------')
            print(modes)
        elif command == 'l':
            print('------------- Language -------------')
            print(langs)
        else:
            print('-------------- Result --------------')
            comm = command.split(' ')
            print(reader(comm))


# käynnistys ajaessa
if __name__ == "__main__":
    main()
