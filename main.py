import pyxel
import random
import enemy
import player

EnemyMush = enemy.EnemyMush
EnemyBird = enemy.EnemyBird
Player = player.Player

class App:
    def __init__(self):
        # Windowサイズ
        pyxel.init(160,128)
        pyxel.load('my_resource.pyxres')
        self.init_game()
        pyxel.run(self.update, self.draw)

    def spawn_enemies_type1(self):
        enemies_type1 = []

        for y in range(16):
            for x in range (63):
                tile = pyxel.tilemap(0).pget(x,y)
                # 敵のタイル
                if tile == (1, 0):
                    move_speed = random.choice([1, 1, 2, 1, 3])
                    move_probability_list = random.randrange(1,10)
                    enemies_type1.append(EnemyMush(x * 8, y * 8, move_speed,move_probability=move_probability_list))
                    # 敵の位置のタイルを透明なタイルに変更
                    pyxel.tilemap(0).pset(x, y, (0, 0))
        return enemies_type1
    
    def spawn_enemies_type2(self):
        enemies_type2 = []

        for y in range(16):
            for x in range (63):
                tile = pyxel.tilemap(0).pget(x,y)
                # 敵のタイル
                if tile == (1, 2):
                    enemies_type2.append(EnemyBird(x * 8, y * 8))
                    # 敵の位置のタイルを透明なタイルに変更
                    pyxel.tilemap(0).pset(x, y, (0, 0))
        return enemies_type2

    
    def init_game(self):
        # タイルマップを初期状態に戻す
        pyxel.load('my_resource.pyxres')
        self.player = Player(0, 0)
        self.enemies_type1 = self.spawn_enemies_type1()
        self.enemies_type2 = self.spawn_enemies_type2()
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
            for enemy in self.enemies_type1:
                if -64 <= enemy.x -self.camera_x <= pyxel.width + 64:
                    enemy.update()
                    if self.player.check_collision(enemy):
                        self.game_over = True

            for enemy in self.enemies_type2:
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
            for enemy in self.enemies_type1:
                real_x = enemy.x - self.camera_x
                # 画面内の敵だけ描写
                if -8 <= real_x <= pyxel.width + 8:
                    if enemy.is_show:
                        pyxel.blt(real_x, enemy.y, 0, 8, 0, 8, 8)
                    else:
                        enemy.y = 128
                        pyxel.blt(real_x, enemy.y, 0, 0, 0, 8, 8)
            
            for enemy in self.enemies_type2:
                real_x = enemy.x - self.camera_x
                # 画面内の敵だけ描写
                if -8 <= real_x <= pyxel.width + 8:
                    if enemy.is_show and enemy.icon_direction <= 10:
                        pyxel.blt(real_x, enemy.y, 0, 8, 16, 8, 8)
                    elif enemy.is_show:
                        pyxel.blt(real_x, enemy.y, 0, 8, 24, 8, 8)
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