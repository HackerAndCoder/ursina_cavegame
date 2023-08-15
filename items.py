import nbt, blocks

class Item: # the Item class is the base class for all items 
    def __init__(self, display_name, texture, nbt, model = 'quad'):
        self.display_name = display_name
        self.texture = texture
        self.nbt = nbt
        self.model = model

class BlockItem(Item):
    def __init__(self, display_name, block, model = 'cube'):
        self.display_name = display_name
        self.model = block.model
        self.nbt = {}
        self.block = block
        self.texture = block.texture

class Tool(Item): # the Tool class is the base class for all tools. It has added attributes like durability.
    def __init__(self, display_name, texture, max_durability):
        super().__init__(display_name, texture, nbt = nbt.NBT({'max_durability': max_durability, 'durability': max_durability}))

GRASS_BLOCK_ITEM = BlockItem('Grass block', blocks.GRASS_BLOCK)
STONE_BLOCK_ITEM = BlockItem('Stone block', blocks.STONE_BLOCK)