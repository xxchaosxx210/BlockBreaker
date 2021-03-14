import pygame
import json
from resources.spritesheet import SpriteSheet
import os
import re

from objects.block import Block


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


def load_game_background(level_manager: LevelManager):
    """

    Args:
        level_manager: level_manager object must load level before calling this function

        if image loaded then buffer stored in level_manager.background_surface. Use that surface to blit every frame

    """
    bck_surface = pygame.Surface((level_manager.width, level_manager.height))
    x, y = (0, 0)
    col = 0
    layer = list(filter(lambda l: l["name"] == "background", level_manager.data["layers"]))[0]
    for gid in layer["data"]:
        # due to my lack of understanding of the Tile App Ive constructed a hack to associate tiled generated data
        # Grid IDs with my spritesheet offsets this allows me to load in large tilesets and not have to code every tile
        # if statement by hand
        for tile_key, tile_value in level_manager.tile_sets.items():
            if gid == level_manager.tile_sets[tile_key]:
                match = TILE_SET_SPLIT.match(tile_key)
                tile_name, tile_offset = (match.group(1), int(match.group(2)))
                img = SpriteSheet.block[tile_name].parse(tile_offset)
                bck_surface.blit(img, pygame.rect.Rect(x, y, img.get_width(), img.get_height()))
                break
        x += level_manager.data["tilewidth"]
        col += 1
        if col >= level_manager.data["width"]:
            x = 0
            col = 0
            y += level_manager.data["tileheight"]
    return bck_surface


def load_level(level_manager: LevelManager, level_file: str):
    data = _load_json(level_file)
    if data:
        level_manager.width = data["tilewidth"] * data["width"]
        level_manager.height = data["tileheight"] * data["height"]
        level_manager.data = data
        level_manager.tile_sets = load_global_ids(data["tilesets"])
        background_surface = load_game_background(level_manager)
        blocks = load_blocks(level_manager)
        return background_surface, blocks
    return None


def load_first_level(level_manager: LevelManager):
    return load_level(level_manager, level_manager.paths[0])


def load_next_level(level_manager: LevelManager):
    try:
        load_level(level_manager, level_manager.paths[level_manager.offset+1])
        level_manager.offset += 1
        return True
    except IndexError:
        return False


def load_global_ids(tile_sets: list):
    """

    Args:
        tile_sets: list loaded from map json file compiled from Tiled program

    Returns:
        returns a dictionary containing tilename and GID which is used in the map file data list
    """
    glob_ids = {}
    for tile_set in tile_sets:
        path = os.path.join(f".{os.path.sep}resources{os.path.sep}tilesets", os.path.split(tile_set["source"])[1])
        tile_info = json.loads(open(path, "r").read())
        tile_gid = tile_set["firstgid"]
        for index, tile in enumerate(tile_info["tiles"]):
            key = f"{tile_info['name']}{index}"
            glob_ids[key] = tile_gid
            tile_gid += 1
    return glob_ids


def _load_json(filename: str):
    with open(filename, "r") as fp:
        return json.loads(fp.read())


def load_blocks(level_manager: LevelManager):
    blocks = []
    x, y = (0, 0)
    col = 0
    layer = list(filter(lambda l: l["name"] == "blocks", level_manager.data["layers"]))[0]
    for gid in layer["data"]:
        for key, value in level_manager.tile_sets.items():
            if gid == level_manager.tile_sets[key]:
                match = TILE_SET_SPLIT.match(key)
                tile_name, tile_offset = (match.group(1), int(match.group(2)))
                blocks.append(Block(x, y, tile_name, tile_offset, False, True))
        x += level_manager.data["tilewidth"]
        col += 1
        if col >= level_manager.data["width"]:
            x = 0
            col = 0
            y += level_manager.data["tileheight"]
    return blocks