import PIL.Image as Image
import numpy
from sys import argv
def braille_char(number):
    if number < 0 or number > 255:
        print("ay o what the fuck")
    return chr(0x2800+int(number))


html_top = """<!doctype html>
<html>
<head>
<title>Braille Image</title>
<style type="text/css">
@font-face {font-family: "CascadiaMono"; src: url("./CascadiaMono.ttf");}
body {font-size:2px; background-color: black; color: white; font-family: "CascadiaMono";}
</style>
</head>
<body>
<pre>
"""
html_bot = """</pre>
</body>
</html>"""

def dither(m:list):
    for y in range(len(m)):
        for x in range(len(m[y])):
            casted = 0.0
            if m[y][x] > 128: casted = 1
            delta =  m[y][x] - casted * 255
            m[y][x] = casted
            if x+1 < len(m[y]):
                m[y    ][x + 1] += delta * 7 / 16
            if (y+1 < len(m)):
                if x != 0: m[y + 1][x - 1] += delta * 3 / 16
                m[y + 1][x    ] += delta * 5 / 16
                if x+1 < len(m[y]): m[y + 1][ x + 1]+= delta * 1 / 16
    return m

def brailleify(m):
    with open("result.html", "w", encoding="utf-8") as html_f:
        with open("result.txt", "w", encoding="utf-8") as txt_f:
            html_f.write(html_top)
            for y in range(0,len(m)//4*4,4):
                for x in range(0,len(m[y])//2*2,2):
                    s = braille_char(m[y][x]+m[y+1][x]*2+m[y+2][x]*4+m[y][x+1]*8+m[y+1][x+1]*16+m[y+2][x+1]*32+m[y+3][x]*64+m[y+3][x+1]*128)
                    html_f.write(s)
                    txt_f.write(s)
                html_f.write("\n")
                txt_f.write("\n")
            html_f.write(html_bot)


def main():    
    image=Image.open(argv[1])
    
    match argv:
        case [*_, "--resize", scale]:
            image = image.resize(map(lambda x:int(x*float(scale)), image.size))
    
    
    image = image.convert("L")
    image_array = numpy.asarray(image.getdata()).astype(numpy.float32)
    image_array.shape = (image.size[1], image.size[0])
    
    brailleify(dither(image_array))

if __name__ == "__main__":
    main()
