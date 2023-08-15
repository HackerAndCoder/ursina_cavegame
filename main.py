import ursina, time, random, items, itemstack
from ursina.prefabs.first_person_controller import FirstPersonController
from blocks import *

app = ursina.Ursina()

ursina.window.borderless = False
ursina.window.title = "Cave Game"
ursina.window.size = (1000, 700)

world = {}
last_tick_time = time.time()

ticks_alive = 0
hotbar_selected_slot = 0
hotbar_items = [
                itemstack.ItemStack(items.GRASS_BLOCK_ITEM, 1), 
                itemstack.ItemStack(items.STONE_BLOCK_ITEM, 1), 
                None, 
                None, 
                None, 
                None, 
                None, 
                None, 
                None
                ]

hotbar = None
hand_item = None

def update_hand():
    global hotbar_items, hand_item, hotbar_selected_slot
    ursina.destroy(hand_item)
    hand_item = None
    if hotbar_items[hotbar_selected_slot]:
        stack = hotbar_items[hotbar_selected_slot]
        hand_item = ursina.Entity(parent = ursina.camera.ui, 
                                texture = stack.item.texture, 
                                #texture = 'brick',
                                model = stack.item.model,
                                position = (0.7, -0.8),
                                )
        hand_item.rotation_y = 260
        hand_item.rotation_x = 0
        hand_item.rotation_z = -10
    
    update_hotbar()

def update():
    global last_tick_time, ticks_alive, hand_item
    if last_tick_time + 0.05 < time.time(): # tick 20 times per second?
        last_tick_time = time.time()
        ticks_alive += 1
        

    if ursina.held_keys['escape']:
        #ursina.mouse.locked = not ursina.mouse.locked
        quit()
    
def input(key):
    global hotbar_selected_slot, hotbar_items
    if key == 'left mouse down':
        if ursina.mouse.hovered_entity:
            if ursina.distance(player.world_position, ursina.mouse.hovered_entity.world_position) <= 5:
                ursina.destroy(ursina.mouse.hovered_entity)

    elif key == 'right mouse down':
        hit_info = ursina.raycast(ursina.camera.world_position, ursina.camera.forward, 5)
        if hit_info.hit:
            if type(hotbar_items[hotbar_selected_slot].item) == items.BlockItem:
                set_block(
                        hit_info.entity.position + hit_info.normal, 
                        hotbar_items[hotbar_selected_slot].item.block
                        )
    
    elif key in ('1', '2', '3', '4', '5', '6', '7', '8', '9'):
        try:
            hotbar_selected_slot = int(key) - 1
            update_hand()
        except:
            pass

class Voxel(ursina.Button):
    def __init__(self, position=(0,0,0), type = GRASS_BLOCK):
        super().__init__(parent=ursina.scene,
            position=position,
            model=type.model,
            origin_y=.5,
            texture=type.texture,
            color=ursina.color.color(0, 0, random.uniform(.9, 1.0)),
            #highlight_colors=ursina.color.lime,
        )

def set_block(pos = (1, 1, 1), block = GRASS_BLOCK):
    world[pos] = Voxel(position = pos, type = block)

def remove_block(pos):
    try:
        ursina.destroy(world[pos])
        del world[pos]
    except:
        pass

def update_hotbar():
    global hotbar
    ursina.destroy(hotbar)
    hotbar = ursina.Entity(parent = ursina.camera.ui, 
                    texture = 'hotbar', 
                    position = (0, -0.46), 
                    scale = 0.5, 
                    model = 'quad')

world_size = 30

for y in range(3):
    for x in range(world_size):
        for z in range(world_size):
            pos = (x - world_size // 2, y - 5, z - world_size // 2)
            set_block(pos, STONE_BLOCK if y < 2 else GRASS_BLOCK)

ursina.camera.fov = 100

player = FirstPersonController()
player.jump_height = 1.2
player.mouse_sensitivity = (80, 80)
player.gravity = 0.5
player.jump_up_duration = 0.7

update_hand()

app.run(False)