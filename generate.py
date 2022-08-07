from PIL import Image

img_path = "collection/"
x_px = 5
y_px = 5
steps = 64

i = 0
for r in range(0, 256 + 1, steps):
    for g in range(0, 256 + 1, steps):
        for b in range(0, 256 + 1, steps):
            print("generating IMG: ({}, {}, {})".format(r, g, b))
            img = Image.new("RGB", (x_px, y_px), (r, g, b))
            img_name = "{}_{}_{}.png".format(r, g, b)
            img.save(img_path + img_name, "png")
            i += 1
