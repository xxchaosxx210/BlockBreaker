import pygame
import json
import objects.block as block


LEVEL_ONE_MAP = ".\\resources\\levels\\one.json"

EMPTY_TILE = 0
RED_TILE = 1
GREEN_TILE = 5


def load_map(map_file: str):
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
        x += tile_width
        current_col += 1
        if current_col >= max_cols:
            current_col = 0
            current_row += 1
            x = 0
            y += tile_height
    return blocks
