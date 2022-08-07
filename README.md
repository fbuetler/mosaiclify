# Mosaiclify

A tool to generate a mosaic image.

## Run

```bash
python3 mosaic.py --target target.png --collection collection --tile-size 5
```

The resulting mosaic image will be called `mosaic.png`

## Assumptions

This tool is a POC and therefore some assumptions apply:

- The collection images are squared
- The collection images are all of the same size
- The target image dimensions are a multiple of the collection image dimensions

Further, the implementation does not focus on performance.

### Resize an image

```bash
convert input.png -resize 2500x1550! output.png
```

With the exclamation mark the ratio of the image is ignored.

## Collection

For development purposes a collection of unicolor images with size 5x5 pixels can be generated with:

```bash
python3 generate.py
```

They will be saved in a directory called `collection`
