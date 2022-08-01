from settings import *
from worldgen import Tile
class Mouse:
    def __init__(self):
        self.mouse_pos = [0,0]

    def get_selected_tile(self, mouse_pos, player):
        player.position_x - player.position_x%TILE_SIZE

        mouse_pos_x = mouse_pos[0]  + player.position_x - 320
        mouse_pos_y = mouse_pos[1]-19  + player.position_y - 160

        self.mouse_pos[0] = mouse_pos_x - mouse_pos_x%TILE_SIZE
        self.mouse_pos[1] = mouse_pos_y - mouse_pos_y%TILE_SIZE

        return self.mouse_pos

    def key_press_handler(self, pressed_keys, chunks):
        if pressed_keys[0] == True:
            chunk = chunks.get_tile(self.mouse_pos[0], self.mouse_pos[1])
            if chunk[1].tile_type != "empty":
                chunk[1] = Tile(chunk[1].position_x, chunk[1].position_y)