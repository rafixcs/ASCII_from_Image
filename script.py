from PIL import Image
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('--img_path', required=True, type=str, help='Image path')
parser.add_argument('--new_width', type=int, help='New ascii image width')
parser.add_argument('--new_ascii', default=False, action='store_true',help='New ascii format')
args = parser.parse_args()

if args.new_ascii:
    NEW_ASCII_CHARS = [219, 178, 177, 176]
    ASCII_CHARS = list(map(chr, NEW_ASCII_CHARS))
else:
    ASCII_CHARS = ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.']

def resize_image(image, new_width=100):
    
    w, h = image.size
    
    ratio = h / w / 1.65
    
    new_height = int(new_width * ratio)
    resized_img = image.resize((new_width, new_height))
    
    return resized_img

def image_toGrayScale(image):
    grayscale_image = image.convert('L')
    return grayscale_image

def image_toASCII(image):
    pixels = image.getdata()
    #characters = "".join(ASCII_CHARS[pixel//65] for pixel in pixels)
    characters = "".join(ASCII_CHARS[pixel//65] for pixel in pixels)
    return characters

def main(img_path, new_width=100):

    try:
        img = Image.open(img_path)
    except:
        print('Failed loading the image! Image path invalid.')
        return

    print('Resizing image...')
    rs_img = resize_image(img, new_width=new_width)
    print('Image to gray scale...')
    gray_img = image_toGrayScale(rs_img)
    print('Image to ASCII...')
    ascii_img = image_toASCII(gray_img)

    pixel_count = len(ascii_img)
    new_ascii_img = '\n'.join(ascii_img[i:(i+new_width)] for i in range(0, pixel_count, new_width))

    print('Printing new ASCII image...')
    print(new_ascii_img)

    with open('./' + img_path.split(os.sep)[-1].split('.')[0] + '_ascii.txt', 'w') as fp:
        fp.writelines(new_ascii_img)

    

if __name__ == '__main__':
    if args.new_width:
        main(args.img_path, args.new_width)
    else:
        main(args.img_path)
