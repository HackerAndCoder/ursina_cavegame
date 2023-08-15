import ursina, time, random
from ursina.prefabs.first_person_controller import FirstPersonController
from blocks import *

app = ursina.Ursina()

ursina.window.borderless = False
ursina.window.title = "Cave Game"
ursina.window.size = (1000, 700)

world = {}
last_tick_time = time.time()

ticks_alive = 0

def update():
    global last_tick_time, ticks_alive
    if last_tick_time + 0.05 < time.time(): # tick 20 times per second?
        last_tick_time = time.time()
        ticks_alive += 1

    if ursina.held_keys['escape']:
        #ursina.mouse.locked = not ursina.mouse.locked
        quit()
    
def input(key):
    if key == 'left mouse down':
        if ursina.mouse.hovered_entity:
            if ursina.distance(player.world_position, ursina.mouse.hovered_entity.world_position) <= 5:
                ursina.destroy(ursina.mouse.hovered_entity)

    elif key == 'right mouse down':
        hit_info = ursina.raycast(ursina.camera.world_position, ursina.camera.forward, 5)
        if hit_info.hit:
            set_block(hit_info.entity.position + hit_info.normal)

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

hotbar = ursina.Entity(parent = ursina.camera.ui, texture = 'hotbar', position = (0, -0.46), scale = 0.5, model = 'quad')

world_size = 20

for x in range(16):
    for z in range(16):
        pos = (x - world_size // 2, -4, z - world_size // 2)
        set_block(pos, GRASS_BLOCK)

ursina.camera.fov = 100

player = FirstPersonController()
player.jump_height = 1.2
player.gravity = 0.5
player.jump_up_duration = 0.7

app.run(False)