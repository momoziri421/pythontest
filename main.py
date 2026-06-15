import pyxel
import random
import enemy
import player
import item

EnemyMush = enemy.EnemyMush
EnemyBird = enemy.EnemyBird
EnemyDossunTypeUnder = enemy.EnemyDossunTypeUnder
EnemyDossunTypeLeft = enemy.EnemyDossunTypeLeft
JumpItem = item.JumpItem
SpeedItem = item.SpeedItem
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
            for x in range (256):
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
            for x in range (256):
                tile = pyxel.tilemap(0).pget(x,y)
                # 敵のタイル
                if tile == (1, 2):
                    enemies_type2.append(EnemyBird(x * 8, y * 8))
                    # 敵の位置のタイルを透明なタイルに変更
                    pyxel.tilemap(0).pset(x, y, (0, 0))
        return enemies_type2
    
    def spawn_enemies_type3(self):
        enemies_type3 = []

        for y in range(16):
            for x in range (256):
                tile = pyxel.tilemap(0).pget(x,y)
                # 敵のタイル
                if tile == (2, 0):
                    enemies_type3.append(EnemyDossunTypeUnder(x * 8, y * 8))
                    # 敵の位置のタイルを透明なタイルに変更
                    pyxel.tilemap(0).pset(x, y, (0, 0))
        return enemies_type3
    
    def spawn_enemies_type4(self):
        enemies_type4 = []

        for y in range(16):
            for x in range (256):
                tile = pyxel.tilemap(0).pget(x,y)
                # 敵のタイル
                if tile == (2, 1):
                    enemies_type4.append(EnemyDossunTypeLeft(x * 8, y * 8))
                    # 敵の位置のタイルを透明なタイルに変更
                    pyxel.tilemap(0).pset(x, y, (0, 0))
        return enemies_type4
    
    def spawn_jump_items(self):
        jump_items = []

        for y in range(16):
            for x in range (256):
                tile = pyxel.tilemap(0).pget(x,y)
                # アイテムのタイル
                if tile == (3, 3):
                    jump_items.append(JumpItem(x * 8, y * 8))
                    # アイテムの位置のタイルを透明なタイルに変更
                    pyxel.tilemap(0).pset(x, y, (0, 0))
        return jump_items

    def spawn_speed_items(self):
        speed_items = []

        for y in range(16):
            for x in range (256):
                tile = pyxel.tilemap(0).pget(x,y)
                # アイテムのタイル
                if tile == (3, 1):
                    speed_items.append(SpeedItem(x * 8, y * 8))
                    # アイテムの位置のタイルを透明なタイルに変更
                    pyxel.tilemap(0).pset(x, y, (0, 0))
        return speed_items

    
    def init_game(self):
        # タイルマップを初期状態に戻す
        pyxel.load('my_resource.pyxres')
        self.player = Player(0, 0)
        self.enemies_type1 = self.spawn_enemies_type1()
        self.enemies_type2 = self.spawn_enemies_type2()
        self.enemies_type3 = self.spawn_enemies_type3()
        self.enemies_type4 = self.spawn_enemies_type4()
        self.jump_items = self.spawn_jump_items()
        self.speed_items = self.spawn_speed_items()
        self.game_over = False
        self.game_clear = False
        # カメラのx座標
        self.camera_x = 0
        # スコア・タイマー
        self.score = 0
        self.timer = 0

    def update(self):
        if not self.game_over and not self.game_clear:
            self.player.update()
            self.timer += 1
            # 進行距離に応じてスコア加算(60フレームに1回)
            if self.timer % 60 == 0:
                self.score += int(self.player.x / 8)

            # クリア判定(2016 = 252タイル目)
            if self.player.x >= 2016:
                self.game_clear = True
                self.score += max(0, (300 - self.timer // 60)) * 10
            
            # カメラ位置追従
            target_camera_x = self.player.x - pyxel.width // 2
            self.camera_x = max(0, min(target_camera_x, 2048 - pyxel.width))

            # 当たり安定更新
            for enemy in self.enemies_type1:
                if -64 <= enemy.x - self.camera_x <= pyxel.width + 64:
                    enemy.update()
                    self.player.check_collision(enemy)

            for enemy in self.enemies_type2:
                if -64 <= enemy.x - self.camera_x <= pyxel.width + 64:
                    enemy.update()
                    self.player.check_collision(enemy)

            for enemy in self.enemies_type3:
                if -64 <= enemy.x - self.camera_x <= pyxel.width + 64:
                    enemy.update(self.player)
                    self.player.check_collision_dossun(enemy)

            for enemy in self.enemies_type4:
                if -64 <= enemy.x - self.camera_x <= pyxel.width + 64:
                    enemy.update(self.player)
                    self.player.check_collision_dossun(enemy)

            for item in self.jump_items:
                if -64 <= item.x - self.camera_x <= pyxel.width + 64:
                    item.update(self.player)
                    self.player.check_collision_item(item)

            for item in self.speed_items:
                if -64 <= item.x - self.camera_x <= pyxel.width + 64:
                    item.update(self.player)
                    self.player.check_collision_item(item)

            # ライフ0でゲームオーバー
            if not self.player.is_alive:
                self.game_over = True

            # 落下判定(ライフ減少、残機あれば復活)
            if self.player.y > 127:
                if self.player.take_damage():
                    if self.player.is_alive:
                        # 直前のカメラ左端付近に復活
                        self.player.x = max(0, self.camera_x)
                        self.player.y = 0
                        self.player.dy = 0
                    else:
                        self.game_over = True

            
        else:
            # リスタート
            if pyxel.btnp(pyxel.KEY_R):
                self.init_game()
    
    def draw(self):
        pyxel.cls(0)
        pyxel.bltm(0, 0, 0, self.camera_x, 0, 2048, 128)

        if not self.game_over and not self.game_clear:
            # プレイヤーの描写(無敵中は点滅)
            real_x = self.player.x - self.camera_x
            if self.player.invincible_timer == 0 or self.player.invincible_timer % 6 < 3:
                pyxel.blt(real_x, self.player.y, 0, 8, 8, 8 if self.player.direction == 1 else -8, 8, 0)

            # HUD
            pyxel.text(2, 2, f"SCORE:{self.score}", 7)
            time_sec = self.timer // 30
            pyxel.text(2, 10, f"TIME:{time_sec}", 7)
            for i in range(self.player.lives):
                pyxel.blt(130 + i * 10, 2, 0, 8, 8, 8, 8, 0)

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
            
            for enemy in self.enemies_type3:
                real_x = enemy.x - self.camera_x
                # 画面内の敵だけ描写
                if -8 <= real_x <= pyxel.width + 8:
                    if enemy.is_show:
                        pyxel.blt(real_x, enemy.y, 0, 16, 0, 8, 8)
                    else:
                        enemy.y = 128
                        pyxel.blt(real_x, enemy.y, 0, 0, 0, 8, 8)

            for enemy in self.enemies_type4:
                real_x = enemy.x - self.camera_x
                # 画面内の敵だけ描写
                if -8 <= real_x <= pyxel.width + 8:
                    if enemy.is_show:
                        pyxel.blt(real_x, enemy.y, 0, 16, 8, 8, 8)
                    else:
                        enemy.y = 128
                        pyxel.blt(real_x, enemy.y, 0, 0, 0, 8, 8)
            
            for item in self.jump_items:
                real_x = item.x - self.camera_x
                if -8 <= real_x <= pyxel.width + 8:
                    if item.is_getted:
                        pyxel.blt(real_x, item.y, 0, 0, 0, 8, 8, 0)
                    elif item.is_show:
                        pyxel.blt(real_x, item.y, 0, 24, 16, 8, 8, 0)
                    else:
                        pyxel.blt(real_x, item.y, 0, 24, 24, 8, 8, 0)

            for item in self.speed_items:
                real_x = item.x - self.camera_x
                if -8 <= real_x <= pyxel.width + 8:
                    if item.is_getted:
                        pyxel.blt(real_x, item.y, 0, 0, 0, 8, 8, 0)
                    elif item.is_show:
                        pyxel.blt(real_x, item.y, 0, 24, 0, 8, 8, 0)
                    else:
                        pyxel.blt(real_x, item.y, 0, 24, 8, 8, 8, 0)


        elif self.game_clear:
            # クリア画面
            pyxel.text(57, 54, "GAME CLEAR!", 11)
            pyxel.text(50, 64, f"SCORE: {self.score}", 10)
            time_sec = self.timer // 30
            pyxel.text(50, 72, f"TIME:  {time_sec}s", 7)
            pyxel.text(42, 82, "PRESS R TO RESTART", 8)
        else:
            # ゲームオーバー画面
            pyxel.text(60, 58, "GAME OVER", 8)
            pyxel.text(50, 68, f"SCORE: {self.score}", 7)
            pyxel.text(42, 78, "PRESS R TO RESTART", 8)
App()