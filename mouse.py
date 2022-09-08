from settings import *
from worldgen import Tile
from chunks import get_tile
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

    def key_press_handler(self, pressed_keys, deltatime, player):
        if pressed_keys[0] == True:
            tile = get_tile(self.mouse_pos[0], self.mouse_pos[1])
            if tile[1].tile_type != "empty" and player.selected_slot == 0:
                tile[1].update_tile("empty", False)
            elif player.selected_slot == 1 and deltatime%5==1:
                tile[1].update_tile("rock", True)