import pyxel

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.on_ground = False
        self.direction = 1

        #ジャンプ系
        self.jump_count = 0
        self.max_jumps = 1
        self.jump_strength = -5
        self.gravity = 0.35
        self.max_fall_speed = 6
        self.accelerration = 1
        
        #成功判定
        self.is_alive = True

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
                if (tile[0] == 0 and tile[1] == 1) or (tile[0] == 0 and tile[1] == 2):  # 地面とオブジェクトのタイル
                    return True, tile_y * 8  # 衝突したタイルのY座標も返す
                elif (tile[0] == 2 and tile[1] == 2) or (tile[0] == 0 and tile[1] == 3):
                    return True, tile_y * 8  # 衝突したタイルのY座標も返す
                elif (tile[0] == 2 and tile[1] == 0) or (tile[0] == 2 and tile[1] == 1):
                    return True, tile_y * 8  # 衝突したタイルのY座標も返す
        return False, 0

    
    def update(self):
        
        # 左右移動
        if pyxel.btn(pyxel.KEY_LEFT):
            self.dx -= self.accelerration
            self.direction = -1
        elif pyxel.btn(pyxel.KEY_RIGHT):
            self.dx += self.accelerration
            self.direction = 1


        # ジャンプ
        if pyxel.btnp(pyxel.KEY_SPACE):
            if self.on_ground:
                self.dy = self.jump_strength
                self.on_ground = False
                self.jump_count = 1
            elif self.jump_count < self.max_jumps:
                self.dy = self.jump_strength
                self.jump_count += 1

        if not self.on_ground:
            self.dy += self.gravity
            self.dy = min(self.dy, self.max_fall_speed)

        # 座標の更新
        next_x = self.x + self.dx
        next_y = self.y

        # 当たり判定
        has_collision, _ = self.check_tile_collisions(next_x, self.y)
        if not has_collision:
            self.x = next_x
            self.dx = 0
        else:
            # 壁と衝突(速度を0に戻す)
            self.dx = 0

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
                    self.jump_count = 0
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
                self.jump_count = 0
            # 天井にぶつかった時
            else:
                self.y = ground_y + 8
                self.dy = 0

        # 移動制限
        self.x = max(0,min(self.x , 2048 - 8))

    def check_collision(self, enemy):
        # 敵とのあたり判定
        if (abs(self.x - enemy.x) < 8 and
             0 > self.y - enemy.y > -8):
            self.defeat_enemy(enemy)
            return False
            
        if (abs(self.x - enemy.x) < 8 and
             abs(self.y -enemy.y) < 8):
            self.is_alive = False
            return True
        return False
    
    def check_collision_dossun(self, enemy):
        # 敵とのあたり判定
        if (abs(self.x - enemy.x) < 7 and
             abs(self.y -enemy.y) < 7):
            self.is_alive = False
            return True
        return False
    
    def check_collision_item(self, item):
        # アイテムとのあたり判定
        if (abs(self.x - item.x) < 5 and
             abs(self.y -item.y) < 5):
            item.get_item(self)


    def defeat_enemy(self, enemy):
        enemy.is_show = False
        self.dy = self.jump_strength * 0.5
        self.on_ground = False
        self.dy += self.gravity
        self.dy = min(self.dy, self.max_fall_speed)

    def draw(self):
        # プレイヤーの向きに応じて反転
        if self.direction == 1:
            pyxel.blt(self.x, self.y, 0, 8, 8, 8, 8, 0)
        else:
            pyxel.blt(self.x, self.y, 0, 8, 8, -8, 8, 0)
