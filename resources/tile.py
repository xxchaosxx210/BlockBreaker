import pygame
import json
import objects.block as block
import os


EMPTY_TILE = 0
RED_TILE = 1
GREEN_TILE = 5
ORANGE_TILE = 9
PINK_TILE = 13
BLUE_TILE = 17
GREY_TILE_1 = 21
GREY_TILE_2 = 22
GREY_TILE_3 = 23

LEVEL_MAPS = {"file_paths": [], "offset": 0}

with os.scandir('.\\resources\\levels') as it:
    for entry in it:
        if os.path.isfile(entry.path) and entry.name.endswith(".json"):
            LEVEL_MAPS["file_paths"].append(entry.path)


def load_next_level():
    global LEVEL_MAPS
    try:
        LEVEL_MAPS["offset"] += 1
        offset = LEVEL_MAPS["offset"]
        level = load_level(LEVEL_MAPS["file_paths"][offset])
        return level
    except IndexError as err:
        print(err.__str__())
    return []


def load_level(map_file: str):
    blocks = []
    map_data = json.loads(open(map_file, "r").read())
    x = 0
    y = 0
    tile_width = map_data["tilewidth"]
    tile_height = map_data["tileheight"]
    max_cols = map_data["width"]
    max_rows = map_data["height"]
    current_col = 0
    current_row = 0
    layer = map_data["layers"][0]
    for tile in layer["data"]:
        if tile == RED_TILE:
            blocks.append(block.Block(x, y, False, True, "red"))
        elif tile == GREEN_TILE:
            blocks.append(block.Block(x, y, False, True, "green"))
        elif tile == ORANGE_TILE:
            blocks.append(block.Block(x, y, False, True, "orange"))
        elif tile == BLUE_TILE:
            blocks.append(block.Block(x, y, False, True, "blue"))
        elif tile == PINK_TILE:
            blocks.append(block.Block(x, y, False, True, "pink"))
        elif tile == GREY_TILE_1:
            blocks.append(block.Block(x, y, False, False, "grey", 0, True))
        elif tile == GREY_TILE_2:
            blocks.append(block.Block(x, y, False, False, "grey", 1, True))
        elif tile == GREY_TILE_3:
            blocks.append(block.Block(x, y, False, False, "grey", 2, False))
        x += tile_width
        current_col += 1
        if current_col >= max_cols:
            current_col = 0
            current_row += 1
            x = 0
            y += tile_height
    return blocks
