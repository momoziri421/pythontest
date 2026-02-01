import pyxel
import random

#キノコ型の敵
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

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.is_falling = False
        self.on_ground = False
        self.direction = 1

        #ジャンプ系
        self.jump_count = 0
        self.max_jumps = 2
        self.jump_strength = -5.5
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
            if 0 <= tile_x < 63 and 0 <= tile_y < 16:
                tile = pyxel.tilemap(0).pget(tile_x, tile_y)
                if (tile[0] == 0 and tile[1] == 1) or (tile[0] == 0 and tile[1] == 2):  # 地面とオブジェクトのタイル
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
                self.is_falling = True
                self.on_ground = False
                self.jump_count = 1
            elif self.jump_count < self.max_jumps:
                self.dy = self.jump_strength * 0.7
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
                    self.is_falling = False
                    self.on_ground = True
                    self.jump_count = 0
                else:
                    self.on_ground = False
                    self.is_falling = True
            else:
                self.on_ground = False
                self.is_falling = True
        else:
            # 地面へ着地時
            if self.dy > 0: 
                self.y = ground_y -8
                self.dy = 0
                self.is_falling = False
                self.on_ground = True
                self.jump_count = 0
            # 天井にぶつかった時
            else:
                self.y = ground_y + 8
                self.dy = 0

        # 移動制限
        self.x = max(0,min(self.x , 504 - 8))

    def check_collision(self, enemy):
        # 敵とのあたり判定
        if (abs(self.x - enemy.x) < 7 and
             abs(self.y -enemy.y) < 8):
            self.defeat_enemy(enemy)
            return False
            
        if (abs(self.x - enemy.x) < 8 and
             abs(self.y -enemy.y) < 8):
            self.is_alive = False
            return True
        return False

    def defeat_enemy(self, enemy):
        enemy.is_show = False
        self.dy = self.jump_strength
        self.is_falling = True
        self.on_ground = False
        self.dy += self.gravity
        self.dy = min(self.dy, self.max_fall_speed)

    def draw(self):
        # プレイヤーの向きに応じて反転
        if self.direction == 1:
            pyxel.blt(self.x, self.y, 0, 8, 8, 8, 8, 0)
        else:
            pyxel.blt(self.x, self.y, 0, 8, 8, -8, 8, 0)

class App:
    def __init__(self):
        # Windowサイズ
        pyxel.init(160,128)
        pyxel.load('my_resource.pyxres')
        self.init_game()
        pyxel.run(self.update, self.draw)

    def spawn_enemies(self):
        enemies = []

        for y in range(16):
            for x in range (45):
                tile = pyxel.tilemap(0).pget(x,y)
                # 敵のタイル
                if tile == (1, 0):
                    move_speed = random.choice([1, 1, 2, 1, 3])
                    move_probability_list = random.randrange(1,10)
                    enemies.append(EnemyMush(x * 8, y * 8, move_speed))
                    # 敵の位置のタイルを透明なタイルに変更
                    pyxel.tilemap(0).pset(x, y, (0, 0))
        return enemies
    
    def init_game(self):
        # タイルマップを初期状態に戻す
        pyxel.load('my_resource.pyxres')
        self.player = Player(0, 0)
        self.enemies = self.spawn_enemies()
        self.game_over = False
        self.game_clear = False
        # カメラのx座標
        self.camera_x = 0

    def update(self):
        if not self.game_over and not self.game_clear:
            self.player.update()

            # クリア判定(312 = 39タイル目)
            if self.player.x >= 480:
                self.game_clear = True
            
            # カメラ位置追従
            target_camera_x = self.player.x - pyxel.width // 2
            self.camera_x = max(0, min(target_camera_x, 504 - pyxel.width))

            # 当たり安定更新
            for enemy in self.enemies:
                if -64 <= enemy.x -self.camera_x <= pyxel.width + 64:
                    enemy.update()
                    if self.player.check_collision(enemy):
                        self.game_over = True
            # 落下判定
            if self.player.y > 127 :
                self.game_over = True    


        else:
            # リスタート
            if pyxel.btnp(pyxel.KEY_R):
                self.init_game()
    
    def draw(self):
        pyxel.cls(0)
        pyxel.bltm(0, 0, 0, self.camera_x, 0, 504, 128)

        if not self.game_over and not self.game_clear:
            # プレイヤーの描写
            real_x = self.player.x - self.camera_x
            pyxel.blt(real_x, self.player.y, 0, 8, 8, 8 if self.player.direction == 1 else -8, 8, 0)

            # 敵の描画
            for enemy in self.enemies:
                real_x = enemy.x - self.camera_x
                # 画面内の敵だけ描写
                if -8 <= real_x <= pyxel.width + 8:
                    if enemy.is_show:
                        pyxel.blt(real_x, enemy.y, 0, 8, 0, 8, 8)
                    else:
                        enemy.y = 128
                        pyxel.blt(real_x, enemy.y, 0, 0, 0, 8, 8)

        elif self.game_clear:
            # クリア画面
            pyxel.text(60, 64, "GAME CLEAR!", 11)
            pyxel.text(45, 74, "PRESS R TO RESTART", 8)
        else:
            # ゲームオーバー画面
            pyxel.text(60, 64, "GAME OVER", 8)
            pyxel.text(45, 74, "PRESS R TO RESTART", 8)
App()