import pygame
import json


class SpriteSheet:
    block = {}

    def __init__(self, image_path: str, json_path: str):
        self.image = pygame.image.load(image_path).convert()
        self.data = json.loads(open(json_path, "r").read())["frames"]

    def get(self, x: int, y: int, w: int, h: int):
        sprite = pygame.Surface((w, h))
        sprite.blit(self.image, (0, 0), (x, y, w, h))
        return sprite

    def parse(self, offset: int):
        d = self.data[offset]["frame"]
        return self.get(d["x"], d["y"], d["w"], d["h"])

    @staticmethod
    def load_all():
        SpriteSheet.block["red"] = SpriteSheet(".\\resources\\images\\red_block.png",
                                               ".\\resources\\images\\red_block.json")
        SpriteSheet.block["green"] = SpriteSheet(".\\resources\\images\\green_block.png",
                                                 ".\\resources\\images\\green_block.json")
        SpriteSheet.block["blue"] = SpriteSheet(".\\resources\\images\\blue_block.png",
                                                ".\\resources\\images\\blue_block.json")
        SpriteSheet.block["pink"] = SpriteSheet(".\\resources\\images\\pink_block.png",
                                                ".\\resources\\images\\pink_block.json")
        SpriteSheet.block["orange"] = SpriteSheet(".\\resources\\images\\orange_block.png",
                                                  ".\\resources\\images\\orange_block.json")
        SpriteSheet.block["grey"] = SpriteSheet(".\\resources\\images\\grey_block.png",
                                                ".\\resources\\images\\grey_block.json")
