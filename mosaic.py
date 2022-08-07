import os
from argparse import ArgumentParser
from typing import Dict, List, Tuple

import numpy as np
from PIL import Image

parser = ArgumentParser()
parser.add_argument(
    "-t",
    "--target",
    help="path to the target image to create a mosaic of",
    required=True,
    type=str,
)
parser.add_argument(
    "-c",
    "--collection",
    help="path to a directory of images to create the mosaic from",
    required=True,
    type=str,
)
parser.add_argument(
    "-ts",
    "--tile-size",
    help="x and y dimensions of the target image",
    required=True,
    type=int,
)


def calc_avg_rgb_per_img(collection_path: str) -> Dict[str, Tuple[int, int, int]]:
    files = os.listdir(collection_path)
    if len(files) == 0:
        raise Exception("collection is empty")

    avg_rgb_per_img = dict()
    for file in files:
        file_path = "{}/{}".format(collection_path, file)
        img = Image.open(file_path)
        avg_rgb = np.mean(np.array(img), axis=(0, 1))
        avg_rgb_per_img[file_path] = avg_rgb

    return avg_rgb_per_img


def calc_avg_rgb_per_tile(target_path: str, tile_size: int) -> List[List[int]]:
    img = np.array(Image.open(target_path))

    avg_rgb_per_tile = list()
    for i in range(0, len(img) // tile_size):
        avg_rgb_per_row = list()
        for j in range(0, len(img[0]) // tile_size):
            tile = img[
                i * tile_size : (i + 1) * tile_size, j * tile_size : (j + 1) * tile_size
            ]
            avg_rgb = np.mean(tile, axis=(0, 1))
            avg_rgb_per_row.append(avg_rgb)
        avg_rgb_per_tile.append(avg_rgb_per_row)

    return avg_rgb_per_tile


def calc_distance(rgb1: Tuple[int, int, int], rgb2: Tuple[int, int, int]) -> float:
    return (
        (rgb1[0] - rgb2[0]) ** 2 + (rgb1[1] - rgb2[1]) ** 2 + (rgb1[2] - rgb2[2]) ** 2
    )


def calc_closest_fit(
    rgb: Tuple[int, int, int], avg_rgb_per_img_map: Dict[str, Tuple[int, int, int]]
) -> str:
    best_fit = 256**2
    best_img_path = None
    for img_path, img_rgb in avg_rgb_per_img_map.items():
        distance = calc_distance(rgb, img_rgb)
        if distance < best_fit:
            best_fit = distance
            best_img_path = img_path

    return best_img_path


def calc_mosaic(
    avg_rgb_per_tile_list: List[List[int]],
    avg_rgb_per_img_map: Dict[str, Tuple[int, int, int]],
) -> List[List[str]]:
    mosaic = list()
    for tile_row in avg_rgb_per_tile_list:
        mosaic_row = list()
        for tile_rgb in tile_row:
            img_path = calc_closest_fit(tile_rgb, avg_rgb_per_img_map)
            mosaic_row.append(img_path)
        mosaic.append(mosaic_row)

    return mosaic


def assemble_mosaic(
    mosaic_list: List[List[str]], width: int, height: int, tile_size: int
) -> Image:
    img_arr = np.zeros((height, width, 3), dtype=np.uint8)

    for i in range(0, height // tile_size):
        for j in range(0, width // tile_size):
            tile = Image.open(mosaic_list[i][j])
            img_arr[
                i * tile_size : (i + 1) * tile_size,
                j * tile_size : (j + 1) * tile_size,
                0:3,
            ] = tile

    img = Image.fromarray(img_arr)

    return img


def main(target_path: str, collection_path: str, tile_size: List[int]):
    # assumptions:
    # * collection images are squared
    # * collection images are all of the same size
    # * target image is a multiple of the collection image

    # calc average RGB of collection images
    avg_rgb_per_img_map = calc_avg_rgb_per_img(collection_path)

    # tile target image and calc average RGB of each tile
    avg_rgb_per_tile_list = calc_avg_rgb_per_tile(target_path, tile_size)

    # get closest fit for every tile
    mosaic_list = calc_mosaic(avg_rgb_per_tile_list, avg_rgb_per_img_map)

    # assemble
    mosaic_width, mosaic_height = Image.open(target_path).size
    mosaic_img = assemble_mosaic(mosaic_list, mosaic_width, mosaic_height, tile_size)

    # save
    mosaic_img_name = "mosaic.png"
    mosaic_img.save(mosaic_img_name, "png")


if __name__ == "__main__":
    args = parser.parse_args()
    main(args.target, args.collection, args.tile_size)
