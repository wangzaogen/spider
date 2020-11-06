import pytesseract as pt
from PIL import Image,ImageFilter,ImageDraw,ImageEnhance
# from spider_315.lib.utility.pytesseract import image_to_string

def convert_img(img, threshold):
    img = img.convert("L")  # 处理灰度
    pixels = img.load()
    for x in range(img.width):
        for y in range(img.height):
            if pixels[x, y] > threshold:
                pixels[x, y] = 255
            else:
                pixels[x, y] = 0
    return img

def clearNoise(image,G,N,Z):
    draw = ImageDraw.Draw(image)

    for i in range(0,Z):
        for x in range(1,image.size[0] - 1):
            for y in range(1,image.size[1] - 1):
                color = getPixel(image,x,y,G,N)
                if color != None:
                    draw.point((x,y),color)

def getPixel(image,x,y,G,N):
    L = image.getpixel((x,y))
    if L > G:
        L = True
    else:
        L = False

    nearDots = 0
    if L == (image.getpixel((x - 1,y - 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x - 1,y)) > G):
        nearDots += 1
    if L == (image.getpixel((x - 1,y + 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x,y - 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x,y + 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x + 1,y - 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x + 1,y)) > G):
        nearDots += 1
    if L == (image.getpixel((x + 1,y + 1)) > G):
        nearDots += 1

    if nearDots < N:
        return image.getpixel((x,y-1))
    else:
        return None

def ModifyImg(img_name):
    print('准备去除验证码干扰线----------')

    img = Image.open(img_name)
    img = img.filter(ImageFilter.MedianFilter())
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2)
    img = img.convert('1')

    width, height = img.size
    data = []
    for i in range(height):
        tmp=[]
        for j in range(width):
            if(img.getpixel((j,i)) == 255 ):
                tmp.append(1)
            else:
                tmp.append(0)
        data.append(tmp)

    img2 = Image.new("P",img.size, 255)
    for y in range(height):
        for a in range(len(data[y])):

            o = y+1
            t = y+2
            #s = y+3
            z = a+1
            x = a+2
            try:
                if data[o][a] == 0 and data[t][a] == 0 and data[y][z] == 0  and data[y][x] == 0:#and data[s][a] == 0
                    img2.putpixel((a,y),1)
                    img2.save('new_code'+'.png')


            except:
                pass
    img2_path = 'new_code'+'.png'

    image = Image.open(img2_path)
    image = image.convert("L")
    clearNoise(image,53,4,8)
    image.save('new_code2.png')
    image.show()



# image = Image.open('D:\\workspace\\gitlab\\tech_platform_content\\spider_315\\lib\\spider\\code.jpg')
# removeLine('D:\\workspace\\gitlab\\tech_platform_content\\spider_315\\lib\\spider\\code.jpg')
# captcha = convert_img(image, 150)
# captcha.show()
# captcha.save("threshold.jpg")

# result = pt.image_to_string(captcha)
# print(result)  #3n3D

if __name__ == '__main__':
    ModifyImg("threshold.jpg")
    print(pt.image_to_string('new_code2.png'))
