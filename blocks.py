import os

class Block:
    def __init__(self, model = 'cube', texture = None):
        self.model = model
        self.texture = os.path.join('assets', texture)

GRASS_BLOCK = Block(model = 'grass_block', texture='grass_block')
STONE_BLOCK = Block(model = 'stone', texture='stone')