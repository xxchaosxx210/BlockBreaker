import pygame
import json
from resources.spritesheet import SpriteSheet
import os
import re


# Use this regular expression to split the tileset key into spritesheet name and offset
TILE_SET_SPLIT = re.compile(r'^(.+?)([0-9]+)$')

LEVELS_PATH_NAME = os.path.join("resources", "levels")


class LevelManager:

    def __init__(self):
        self.paths = get_level_paths()
        self.tile_sets = {}
        self.offset = 0
        self.data = {}
        self.width = 0
        self.height = 0


def get_level_paths():
    paths = []
    with os.scandir(LEVELS_PATH_NAME) as it:
        for entry in it:
            if os.path.isfile(entry.path) and entry.name.endswith(".json"):
                paths.append(entry.path)
    return paths


def load_game_background(level: LevelManager):
    """

    Args:
        level: level object must load level before calling this function

        if image loaded then buffer stored in level.background_surface. Use that surface to blit every frame

    """
    bck_surface = pygame.Surface((level.width, level.height))
    x, y = (0, 0)
    col = 0
    bck_layer = level.data["layers"][0]
    for gid in bck_layer["data"]:
        # due to my lack of understanding of the Tile App Ive constructed a hack to associate tiled generated data
        # GIDs with my spritesheet offsets this allows me to load in large tilesets and not have to code every tile
        # if statement by hand
        for tile_key, tile_value in level.tile_sets.items():
            if gid == level.tile_sets[tile_key]:
                match = TILE_SET_SPLIT.match(tile_key)
                tile_name, tile_offset = (match.group(1), int(match.group(2)))
                img = SpriteSheet.block[tile_name].parse(tile_offset)
                bck_surface.blit(img, pygame.rect.Rect(x, y, img.get_width(), img.get_height()))
                break
        x += level.data["tilewidth"]
        col += 1
        if col >= level.data["width"]:
            x = 0
            col = 0
            y += level.data["tileheight"]
    return bck_surface


def load_level(level: LevelManager, level_file: str):
    data = _load_json(level_file)
    if data:
        level.width = data["tilewidth"] * data["width"]
        level.height = data["tileheight"] * data["height"]
        level.data = data
        level.tile_sets = load_gids(data["tilesets"])
    return True


def load_gids(tile_sets: list):
    """

    Args:
        tile_sets: list loaded from map json file compiled from Tiled program

    Returns:
        returns a dictionary containing tilename and GID which is used in the map file data list
    """
    gids = {}
    for tile_set in tile_sets:
        path = os.path.join(f".{os.path.sep}resources{os.path.sep}tilesets", os.path.split(tile_set["source"])[1])
        tile_info = json.loads(open(path, "r").read())
        tile_gid = tile_set["firstgid"]
        for index, tile in enumerate(tile_info["tiles"]):
            key = f"{tile_info['name']}{index}"
            gids[key] = tile_gid
            tile_gid += 1
    return gids


def _load_json(filename: str):
    with open(filename, "r") as fp:
        return json.loads(fp.read())


def load_first_level(level_manager: LevelManager):
    return load_level(level_manager, level_manager.paths[0])


def load_next_level(level_manager: LevelManager):
    try:
        load_level(level_manager, level_manager.paths[level_manager.offset+1])
        level_manager.offset += 1
        return True
    except IndexError:
        return False


# def load_blocks(layer: dict):
#     blocks = []
#     x = 0
#     y = 0
#     tile_width = layer["tilewidth"]
#     tile_height = layer["tileheight"]
#     max_cols = layer["width"]
#     max_rows = layer["height"]
#     current_col = 0
#     current_row = 0
#     layer = layer["layers"][0]
#     for tile in layer["data"]:
#         if tile == RED_TILE:
#             blocks.append(block.Block(x, y, False, True, "red"))
#         elif tile == GREEN_TILE:
#             blocks.append(block.Block(x, y, False, True, "green"))
#         elif tile == ORANGE_TILE:
#             blocks.append(block.Block(x, y, False, True, "orange"))
#         elif tile == BLUE_TILE:
#             blocks.append(block.Block(x, y, False, True, "blue"))
#         elif tile == PINK_TILE:
#             blocks.append(block.Block(x, y, False, True, "pink"))
#         elif tile == GREY_TILE_1:
#             blocks.append(block.Block(x, y, False, False, "grey", 0, True))
#         elif tile == GREY_TILE_2:
#             blocks.append(block.Block(x, y, False, False, "grey", 1, True))
#         elif tile == GREY_TILE_3:
#             blocks.append(block.Block(x, y, False, False, "grey", 2, False))
#         x += tile_width
#         current_col += 1
#         if current_col >= max_cols:
#             current_col = 0
#             current_row += 1
#             x = 0
#             y += tile_height
#     return blocks