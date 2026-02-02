import pyxel
import random

class EnemyMush:
    def __init__(self, x, y, move_speed=1, move_range=5,move_probability=5 ):
        self.x = x
        self.y = y
        self.dx = move_speed
        self.direction = 1
        self.is_alive = True
        self.start_x = x
        self.move_probability_list = []
        # 1マスが8pxのため
        self.move_range = move_range * 8
        self.initial_direction = 1
        self.is_show = True

        for i in range(move_probability):
            self.move_probability_list.append(1)
        for i in range(10 - move_probability):
            self.move_probability_list.append(0)



    def check_tile_collisions(self, x, y):
        # タイルのサイズ（8x8）を考慮して、プレイヤーの四隅のタイル座標をチェック
        tile_coords = [
            #左上
            (int(x / 8), int(y / 8)),
            #右上
            (int((x + 7) / 8), int(y / 8)),
            #左下
            (int(x / 8), int((y + 7) / 8)),
            #右下
            (int((x + 7) / 8), int((y + 7) / 8))
        ]

        for tile_x, tile_y in tile_coords:
            # タイルマップの範囲内かチェック
            if 0 <= tile_x < 63 and 0 <= tile_y < 16:
                tile = pyxel.tilemap(0).pget(tile_x, tile_y)
                if (tile[0] == 0 and tile[1] == 1) or (tile[0] == 0 and tile[1] == 2):  # 地面とオブジェクトのタイル
                    return True, tile_y * 8  # 衝突したタイルのY座標も返す
                
        return False, 0    

    def update(self):
        is_move = random.choice(self.move_probability_list)
        self.next_x = self.x + (self.dx  * is_move)
        has_condition, _ = self.check_tile_collisions(self.next_x, self.y)

        if not has_condition:
            self.x += self.dx  * is_move
        else:    
            self.dx *= -1
            self.direction *= -1

        if self.x >= self.start_x + self.move_range:
            self.x = self.start_x + self.move_range
            self.dx *= -1
            self.direction *= -1
        elif self.x <= self.start_x:
            self.x = self.start_x
            self.dx *= -1
            self.direction *= -1



    def draw(self):
        pyxel.blt(self.x, self.y, 0, 8, 0, 8, 8)