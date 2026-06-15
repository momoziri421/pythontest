import pyxel
import random

class EnemyMush:
    def __init__(self, x, y, move_speed=1, move_range=5,move_probability=5 ):
        self.x = x
        self.y = y
        self.dx = move_speed
        self.direction = 1
        self.start_x = x
        self.move_probability_list = []
        # 1マスが8pxのため
        self.move_range = move_range * 8
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
            if 0 <= tile_x < 256 and 0 <= tile_y < 16:
                tile = pyxel.tilemap(0).pget(tile_x, tile_y)
                if (tile[0] == 0 and tile[1] == 1) or (tile[0] == 0 and tile[1] == 2):
                    return True, tile_y * 8  # 衝突したタイルのY座標も返す
                elif (tile[0] == 2 and tile[1] == 2) or (tile[0] == 0 and tile[1] == 3):  # 地面とオブジェクトのタイル
                    return True, tile_y * 8  # 衝突したタイルのY座標も返す
                elif (tile[0] == 2 and tile[1] == 0) or (tile[0] == 2 and tile[1] == 1):
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

class EnemyBird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dy = 0
        self.direction = 1
        self.is_show = True
        self.on_ground = True
        self.jump_strength = -5.5
        self.gravity = 0.3
        self.max_fall_speed = 1
        self.icon_direction = 0
        self.jump_timer = 0
        self.jump_interval = 60

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
            if 0 <= tile_x < 256 and 0 <= tile_y < 16:
                tile = pyxel.tilemap(0).pget(tile_x, tile_y)
                if (tile[0] == 0 and tile[1] == 1) or (tile[0] == 0 and tile[1] == 2):
                    return True, tile_y * 8  # 衝突したタイルのY座標も返す
                elif (tile[0] == 2 and tile[1] == 2) or (tile[0] == 0 and tile[1] == 3):  # 地面とオブジェクトのタイル
                    return True, tile_y * 8  # 衝突したタイルのY座標も返す
                elif (tile[0] == 2 and tile[1] == 0) or (tile[0] == 2 and tile[1] == 1):
                    return True, tile_y * 8  # 衝突したタイルのY座標も返す
                
        return False, 0    

    def update(self):

        # タイマーで自律的にジャンプ
        self.jump_timer += 1
        if self.jump_timer >= self.jump_interval and self.on_ground:
            self.dy = self.jump_strength
            self.on_ground = False
            self.jump_timer = 0

        if not self.on_ground:
            self.dy += self.gravity
            self.dy = min(self.dy, self.max_fall_speed)

        # y方向位置更新
        next_y = self.y + self.dy

        has_collision, ground_y = self.check_tile_collisions(self.x, next_y)
        if not has_collision:
            self.y = next_y
            # 地面との接触チェック
            if self.dy > 0:
                # 次フレーム
                next_has_collision, next_ground_y = self.check_tile_collisions(self.x, next_y + 1)
                if next_has_collision:
                    self.y = next_ground_y - 8
                    self.dy = 0
                    self.on_ground = True
                else:
                    self.on_ground = False
            else:
                self.on_ground = False
        else:
            # 地面へ着地時
            if self.dy > 0: 
                self.y = ground_y -8
                self.dy = 0
                self.on_ground = True
            # 天井にぶつかった時
            else:
                self.y = ground_y + 8
                self.dy = 0

        if self.icon_direction < 19:
            self.icon_direction += 1
        else:
            self.icon_direction = 0
         

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 8, 16, 8, 8)

class EnemyDossunTypeUnder:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dy = 0
        self.init_y = y
        self.direction = 1
        self.is_show = True
        self.on_ground = False
        self.jump_strength = 5.5
        self.gravity = 0.3
        self.max_fall_speed = 10
        self.min_fall_speed = -4
        self.icon_direction = 0
        self.is_move = False
        self.is_down = True
        self.up_wait_flame = 0
        self.down_wait_flame = 0

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
            if 0 <= tile_x < 256 and 0 <= tile_y < 16:
                tile = pyxel.tilemap(0).pget(tile_x, tile_y)
                if (tile[0] == 0 and tile[1] == 1) or (tile[0] == 0 and tile[1] == 2):
                    return True, tile_y * 8
                elif (tile[0] == 2 and tile[1] == 2) or (tile[0] == 0 and tile[1] == 3):
                    return True, tile_y * 8
                elif (tile[0] == 2 and tile[1] == 0) or (tile[0] == 2 and tile[1] == 1):
                    return True, tile_y * 8
        return False, 0


    def update(self, player):
        if not self.is_move and self.down_wait_flame < 30:
            self.down_wait_flame += 1

        if abs(self.x - player.x) < 24 and not self.is_move and self.down_wait_flame >= 30:
            self.is_move = True
            self.is_down = True
            self.down_wait_flame = 0

        if self.is_move:
            if self.is_down:
                self.dy + self.jump_strength if self.dy == 0 else self.dy
                self.dy += self.gravity
                self.dy = min(self.dy, self.max_fall_speed)
                next_y = self.y + self.dy
            # 硬直
            elif self.up_wait_flame < 30:
                self.up_wait_flame += 1
                next_y = self.y
            else:
                self.dy -= self.gravity
                self.dy = max(self.dy, self.min_fall_speed)
                next_y = self.y + self.dy

            has_collision, ground_y = self.check_tile_collisions(self.x, next_y)
            if not has_collision:
                self.y = next_y
                # 地面との接触チェック
                if self.dy > 0:
                 # 次フレーム
                    next_has_collision, next_ground_y = self.check_tile_collisions(self.x, next_y + 1)
                    if next_has_collision:
                        self.y = next_ground_y - 8
                        self.dy = 0
                        self.is_down = False
                elif self.dy < 0 and self.y <= self.init_y:
                    self.y = self.init_y 
                    self.dy = 0
                    self.is_move = False
                    self.up_wait_flame = 0
            else:
                # 地面へ着地時
                if self.dy > 0: 
                    self.y = ground_y -8
                    self.dy = 0
                    self.is_down = False

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 8, 16, 8, 8)    

class EnemyDossunTypeLeft:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dx = 0
        self.init_x = x
        self.distance = 150
        self.direction = 1
        self.is_show = True
        self.on_ground = False
        self.jump_strength = 5.5
        self.gravity = 0.3
        self.max_fall_speed = 10
        self.min_fall_speed = -4
        self.icon_direction = 0
        self.is_move = False
        self.is_down = True
        self.up_wait_flame = 0
        self.down_wait_flame = 0

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
            if 0 <= tile_x < 256 and 0 <= tile_y < 16:
                tile = pyxel.tilemap(0).pget(tile_x, tile_y)
                if (tile[0] == 0 and tile[1] == 1) or (tile[0] == 0 and tile[1] == 2):
                    return True, tile_x * 8  # 衝突したタイルのY座標も返す
                elif (tile[0] == 2 and tile[1] == 2) or (tile[0] == 0 and tile[1] == 3):  # 地面とオブジェクトのタイル
                    return True, tile_x * 8  # 衝突したタイルのY座標も返す
                elif (tile[0] == 2 and tile[1] == 0) or (tile[0] == 2 and tile[1] == 1):
                    return True, tile_y * 8  # 衝突したタイルのY座標も返す
        return False, 0    
    

    def update(self, player):
        if not self.is_move and self.down_wait_flame < 30:
            self.down_wait_flame += 1

        if  0 < player.x - self.x < 36 and abs(self.y - player.y) < 60 and not self.is_move and self.down_wait_flame >= 30:
            self.is_move = True
            self.is_down = True
            self.down_wait_flame = 0

        if self.is_move:
            if self.is_down:
                self.dx + self.jump_strength if self.dx == 0 else self.dx
                self.dx += self.gravity
                self.dx = min(self.dx, self.max_fall_speed)
                next_x = self.x + self.dx
            # 硬直
            elif self.up_wait_flame < 30:
                self.up_wait_flame += 1
                next_x = self.x
            else:
                self.dx -= self.gravity
                self.dx = max(self.dx, self.min_fall_speed)
                next_x = self.x + self.dx
                
            if next_x - self.init_x >= self.distance:
                next_x = self.x
                self.dx = 0
                self.is_down = False

            has_collision, ground_x = self.check_tile_collisions(next_x, self.y)
            if not has_collision :
                self.x = next_x
                # 右オブジェとの接触チェック
                if self.dx > 0:
                 # 次フレーム
                    next_has_collision, next_ground_x = self.check_tile_collisions(next_x + 1, self.y)
                    if next_has_collision:
                        self.x = next_ground_x - 8
                        self.dx = 0
                        self.is_down = False
                elif self.dx < 0 and self.x <= self.init_x:
                    self.x = self.init_x 
                    self.dx = 0
                    self.is_move = False
                    self.up_wait_flame = 0
            else:
                # 地面へ着地時
                if self.dx > 0: 
                    self.x = ground_x -8
                    self.dx = 0
                    self.is_down = False

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 8, 24, 8, 8)    