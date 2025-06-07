from PIL import Image

width = 840
length = 160


canvas = Image.new('RGB', (width, length))
pixels = canvas.load()

with open('savefile.txt', 'r') as f:
    for y in range(length):
        line = f.readline().strip()
        values = line.split(' ')
        for x in range(width):
            red = int(values[x * 3])
            green = int(values[x * 3 + 1])
            blue = int(values[x * 3 + 2])
            pixels[x, y] = (red, green, blue)
            
canvas.save('output.png')