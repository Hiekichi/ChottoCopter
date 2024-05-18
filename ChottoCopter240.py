import pyxel
# ブローダーバンドと呼ぶかブローダーボンドと呼ぶかとなどと些細なことで争っていた時代もありました
### グローバル変数
bullet1s = []     # 横向き時の弾
bullet2s = []     # こっち向き時の弾
hiteffect1s = []  # 横向き時の爆発演出
hiteffect2s = []  # こっち向き時の爆発演出
hiteffectt1s = []  # 戦車発砲による爆発演出
hiteffectt2s = []  # 戦車自体の爆発演出
stars = []        # 背景で瞬いている星
rescuers = []     # これから救助される人たち
smilers = []      # ヘリから降りた人たち
cabins = []       # 人質のいる小屋
tanks = []        # 戦車
planes = []       # 戦闘機
missiles = []     # ミサイル(?)
#ufo = None        # 謎の円盤

count_died = 0      # 死亡者数
count_board = 0     # 現在ヘリに搭乗している人数
count_rescued = 0   # 基地に無事帰還できた人数
gameover_cnt = 0  # ゲームオーバー（ヘリ爆発）になった後のメッセージ表示用
gameend_cnt = 0   # ゲームエンド（全員救出か死亡）になった後のメッセージ表示用

def init_global_variable():
    global bullet1s,bullet2s,hiteffect1s,hiteffect2s,hiteffectt1s,hiteffectt2s,stars,rescuers,smilers,cabins,tanks,planes,count_died,count_board,count_rescued,missiles,gameover_cnt,gameend_cnt
    bullet1s = []     # 横向き時の弾
    bullet2s = []     # こっち向き時の弾
    hiteffect1s = []  # 横向き時の爆発演出
    hiteffect2s = []  # こっち向き時の爆発演出
    hiteffectt1s = []  # 戦車発砲による爆発演出
    hiteffectt2s = []  # 戦車自体の爆発演出
    stars = []        # 背景で瞬いている星
    rescuers = []     # これから救助される人たち
    smilers = []      # ヘリから降りた人たち
    cabins = []       # 人質のいる小屋
    tanks = []        # 戦車
    planes = []       # 戦闘機
    missiles = []

    count_died = 0      # 死亡者数
    count_board = 0     # 現在ヘリに搭乗している人数
    count_rescued = 0   # 基地に無事帰還できた人数
    gameover_cnt = 0  # ゲームオーバー（ヘリ爆発）になった後のメッセージ表示用
    gameend_cnt = 0   # ゲームエンド（全員救出か死亡）になった後のメッセージ表示用

class Copter():
    def __init__(self) -> None:
        self.is_active = True
        self.is_stay = False
        self.cnt = 0
        self.force_x = 0
        self.force_y = 0
        self.x = 1924  # 絶対座標、世界の中でのx座標
        self.y = 206   # 絶対座標、世界の中でのy座標
        self.crush_flag = False
        self.crush_cnt = 0
        self.landingchecked_flag = False  ## 着地処理を済ませているかどうか
        self.land_flag = False ## 着地中
        self.style = 0  # 0:左向き、1:こっち向き、2:右向き、3:こっち向き
        self.unboard_cnt = 48
    def update(self):
        global count_died,count_board,count_rescued,gameend_cnt
        if self.is_active == False:
            return
        #### 以下はヤラレてない時の処理
        self.cnt += 1
        ### 移動の処理
        if abs(self.force_x) > 4:
            self.force_x = 4 * (self.force_x / abs(self.force_x))
        if abs(self.force_y) > 4:
            self.force_y = 4 * (self.force_y / abs(self.force_y))
        self.x += self.force_x
        self.y += self.force_y
        self.force_x *= 0.9
        self.force_y *= 0.9

        ### 着地の判定と自然落下の処理
        if round(self.y) >= 206:
            self.y = 206
            if self.landingchecked_flag == False:
                self.check_landing()
                if self.x > 1900 and self.x < 1940:
                    self.unboard_cnt = 48
            else: ##self.landingchecked_flag == False:
                if self.x > 1900 and self.x < 1940:
                    self.unboard_cnt -= 1
                    if self.unboard_cnt < 0:
                        self.unboard_cnt = 48
                        if count_board > 0:
                            count_board -= 1
                            count_rescued += 1
                            if self.style == 1:
                                smilers.append(Smiler(self.x + 20))
                            else:
                                smilers.append(Smiler(self.x + 28))
                            if count_died+count_rescued == 56:
                                gameend_cnt = 360
                                copter.is_stay = True
            self.force_y = 0
            self.land_flag = True
        else:
            self.y += 0.5
            self.land_flag = False

        if self.x < 0:
            self.x = 0
        elif self.x > 2016:
            self.x = 2016
        if self.y < 10:
            self.y = 10

    def check_landing(self):
        global rescuers,count_died,count_board,count_rescued,gameover_cnt
        ### 踏みつぶしチェック
        if self.style == 0 or self.style == 2:
            dx1 = -6
            dx2 = 30
        else:
            dx1 = 2
            dx2 = 22
        for rescuer in reversed(rescuers):
            d = rescuer.x - self.x
            if d > dx1 and d < dx2:
                count_died += 1
                rescuers.remove(rescuer)
                pyxel.play(2,8)
        if self.force_y > 1.2:  # 速度超過で着陸失敗
            hiteffectt2s.append(HitEffectT2(self.x-3,self.y-3))
            hiteffectt2s.append(HitEffectT2(self.x-3,self.y+3))
            hiteffectt2s.append(HitEffectT2(self.x+3,self.y-3))
            hiteffectt2s.append(HitEffectT2(self.x+3,self.y+3))
            gameover_cnt = 256
            self.x = 3000
            self.y = 300
            self.is_active = False
            ufo.is_active = False
            count_died += count_board
            count_board = 0
            pyxel.play(2,6)

        self.landingchecked_flag = True

    def draw(self):
        if self.is_active == False:
            return
        ###### 以下はヤラレテないときの処理
        x = self.x - framewin.x  ### 描画位置の計算
        y = self.y
        if self.style == 0: # 左向き
            if self.land_flag:
                pyxel.blt(x,y,0,(self.cnt//8%4)*32,16,32,16,0)
                return
            elif self.force_x < -1: # 左に加速
                pyxel.blt(x,y,0,(self.cnt%4)*32,32,32,16,0)
            elif self.force_x > 1: # 右に加速
                pyxel.blt(x,y,0,(self.cnt%4)*32,48,32,16,0)
            else: #if self.force_x >= -1 and self.force_x <= 1:
                pyxel.blt(x,y,0,(self.cnt%4)*32,16,32,16,0)
        elif self.style == 2: # 右向き
            if self.land_flag:
                pyxel.blt(x,y,0,(self.cnt//8%4)*32,16,-32,16,0)
            elif self.force_x < -1: # 左に加速
                pyxel.blt(x,y,0,(self.cnt%4)*32,48,-32,16,0)
            elif self.force_x > 1: # 右に加速
                pyxel.blt(x,y,0,(self.cnt%4)*32,32,-32,16,0)
            else:
                pyxel.blt(x,y,0,(self.cnt%4)*32,16,-32,16,0)
        else:  # self.style == 1か3: # こっち向き
            if self.land_flag:
                pyxel.blt(x,y,0,(self.cnt//8%4)*32,64,32,16,0)
            elif self.force_x < -1: # 左に加速
                pyxel.blt(x,y,0,(self.cnt%4)*32,80,32,16,0)
            elif self.force_x > 1: # 右に加速
                pyxel.blt(x,y,0,(self.cnt%4)*32,96,32,16,0)
            else:
                pyxel.blt(x,y,0,(self.cnt%4)*32,64,32,16,0)
copter = Copter()

class Framewindow():
    def __init__(self) -> None:
        self.x = 1808  #2048 - 240 # 世界のどの位置を表示中か
    def update(self):
        if self.x <= 0:
            self.x = 0
        elif self.x >= 1808: # 2048-240
            self.x = 1808
    def draw(self):
        pyxel.bltm(0,256-64,0,self.x,0,256,64,0)
framewin = Framewindow()

class HitEffect1():
    def __init__(self,x,y,is_hitground) -> None:
        self.x = x
        self.y = y
        self.cnt = 15
        self.is_alive = True
        self.is_hitground = is_hitground
        pyxel.play(1,2)
    def update(self):
        self.cnt -= 1
        if self.cnt <= 0:
            self.is_alive = False
    def draw(self):
        pyxel.blt(self.x - framewin.x,self.y,0,(10-self.cnt)//5*8,136,8,8,0)

class HitEffect2():
    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y
        self.cnt = 30
        self.is_alive = True
        pyxel.play(1,2)
    def update(self):
        self.cnt -= 1
        if self.cnt <= 0:
            self.is_alive = False
    def draw(self):
        pyxel.blt(self.x - framewin.x,self.y,0,(24-self.cnt)//6*16,128,16,8,0)

class HitEffectT1():
    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y
        self.cnt = 21
        self.is_alive = True
        #pyxel.play(1,9)
    def update(self):
        self.cnt -= 1
        if self.cnt <= 0:
            self.is_alive = False
    def draw(self):
        pyxel.blt(self.x - framewin.x,self.y,0,(14-self.cnt)//7*8,168,8,8,0)

class HitEffectT2():
    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y
        self.cnt = 42
        self.is_alive = True
        pyxel.play(1,9)
    def update(self):
        self.cnt -= 1
        if self.cnt <= 0:
            self.is_alive = False
    def draw(self):
        pyxel.blt(self.x - framewin.x,self.y,0,(42-self.cnt)//14*32,192,32,16,0)

class Bullet1():  ## 横向きに飛ばす弾（小屋の扉、人質、戦闘機、UFOに対応する）
    def __init__(self,x,y,dx,dy) -> None:
        self.is_alive = True
        self.is_hitground = False
        self.cnt = 48
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        pyxel.play(0,1)
    def update(self):
        global planes
        if self.y > 212:   # 地面にHITして消滅
            self.is_alive = False
            self.is_hitground = True
        elif self.cnt < 0 or self.y < -10: # LifeTime終了か画面外に出て消滅
            self.is_alive = False
        else:  # それ以外の時は移動処理
            self.x += self.dx
            self.y += self.dy
            self.cnt -= 1
            for plane in reversed(planes):
                if abs(plane.x - self.x) < 26 and abs(plane.y - self.y) < 12:
                    hiteffect2s.append(HitEffect2(plane.x+8,plane.y))
                    hiteffect2s.append(HitEffect2(plane.x+16,plane.y+3))
                    hiteffect2s.append(HitEffect2(plane.x+24,plane.y))
                    planes.remove(plane)
            
    def draw(self):
        pyxel.circ(self.x - framewin.x,self.y,1,7)

class Bullet2():  ## こっち向きに飛ばす弾（戦車に対応する）
    def __init__(self,x,y,dx,dy) -> None:
        self.is_alive = True
        #self.cnt = 48
        self.hit_height = 212 + (200 - y) //4
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        pyxel.play(0,1)
    def update(self):
        self.x += self.dx
        self.y += self.dy
        #self.cnt -= 1
        if self.y > self.hit_height:
            self.is_alive = False
    def draw(self):
        pyxel.circ(self.x - framewin.x,self.y,1,13)

class Missile():  ## 飛行機の発射弾（ミサイル）
    def __init__(self,x,y,dx,dy) -> None:
        self.is_alive = True
        #self.cnt = 96
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        pyxel.play(2,3)
    def update(self):
        global gameover_cnt,count_died,count_board
        self.x += self.dx
        self.y += self.dy
        #self.cnt -= 1
        if self.y > 210:  # or self.cnt < 0:
            self.is_alive = False
        if abs(copter.x+16 - self.x) < 16 and abs(copter.y+8 - self.y) < 8:
            hiteffectt2s.append(HitEffectT2(copter.x+8,copter.y))
            gameover_cnt = 256
            copter.x = 3000
            copter.y = 300
            copter.is_active = False
            ufo.is_active = False
            count_died += count_board
            count_board = 0
            self.is_alive = False
            pyxel.play(2,6)
    def draw(self):
        pyxel.blt(self.x-framewin.x,self.y,0, 0,232,-8*self.dx,8,0)

class Star():
    def __init__(self) -> None:
        self.x = pyxel.rndi(2,252)
        self.y = pyxel.rndi(2,204)
    def update(self):
        pass
    def draw(self):
        pyxel.pset(self.x,self.y,pyxel.rndi(7,12))

class Rescuer():
    def __init__(self,x) -> None:
        self.x = x
        self.y = 212
        self.is_doing = False
        self.stay_time = 48
        self.speed = pyxel.rndf(1,2)
        self.cnt = pyxel.rndi(0,100)
        self.startdash = pyxel.rndf(-50,50)
        self.startdash_diff = self.startdash / 48
    def update(self):
        if self.stay_time > 0:
            self.stay_time -= 1
            return
        if self.is_doing == False:
            self.x += self.startdash_diff
            self.startdash -= self.startdash_diff
            if round(self.startdash) == 0:
                self.is_doing = True
            return
        self.cnt += 1
        if pyxel.rndi(0,6) > 0:
            pass
        elif copter.x < self.x -12 and (self.x - copter.x) < 72 and copter.y > 160:
            self.x -= self.speed
        elif copter.x > self.x -12 and (copter.x - self.x) < 48 and copter.y > 160:
            self.x += self.speed
        else:
            self.x += pyxel.rndi(-1,1)
    def draw(self):
        if self.stay_time == 0:
            pyxel.blt(self.x - framewin.x,self.y,0,self.cnt//10%6*8,120,8,8,0)

class Smiler():
    def __init__(self,x) -> None:
        self.x = x
        self.y = 210
        self.speed = pyxel.rndf(0.3,0.6)
        self.hello_cnt = 0
        pyxel.play(0,4)
    def update(self):
        if self.hello_cnt > 0:
            self.hello_cnt -= 1
        else:
            if pyxel.rndi(0,200) == 0:
                self.hello_cnt = pyxel.rndi(48,96)
            else:
                self.x += self.speed
    def draw(self):
        if self.hello_cnt > 0:
            pyxel.blt(self.x - framewin.x,self.y,0,48+self.hello_cnt//3%2*8,120,8,8,0)
        else:
            pyxel.blt(self.x - framewin.x,self.y,0,pyxel.frame_count//2%6*8,120,8,8,0)

class Cabin():
    def __init__(self,x,y,status) -> None:
        self.x = x
        self.y = y
        self.status = status  # 0:Close  1:Just-in Open  2:Opened
    def update(self):
        global rescuers
        if self.status == 1: # ただいまオープンになりました
            for i in range(8):
                rescuers.append(Rescuer(self.x+4))
            self.status = 2
    def draw(self):
        if self.status == 0:
            ## クローズ状態の小屋
            pyxel.blt(self.x - framewin.x,208,0,128,0,16,16,0)
        else:
        ## オープン状態の小屋（燃えている）
            pyxel.blt(self.x - framewin.x,208,0,144+pyxel.frame_count//3%3*16,0,16,16,0)

class Tank():
    def __init__(self,x,y) -> None:
        self.x = x
        self.dx = 1
        self.y = y
        self.is_alive = True
        self.cnt = 0
        self.barrel = 2 # 砲塔の向き、0～4 、0,1が左向き2が正面向き3,4が右向き
    def update(self):
        if self.cnt > 0:
            self.cnt -= 1
            self.x += self.dx
        else:
            self.cnt = pyxel.rndi(24,64)
            if abs(copter.x - self.x) < 256 and copter.land_flag:
                if self.x < copter.x:
                    self.barrel = pyxel.rndi(2,4)
                    self.dx = pyxel.rndf(0,1)
                else:
                    self.barrel = pyxel.rndi(0,2)
                    self.dx = pyxel.rndf(-1,0)
            else:
                self.barrel = pyxel.rndi(0,4)
                self.dx = pyxel.rndf(-1,1)
        if pyxel.rndi(0,48) == 0: ### 発砲
            hiteffectt1s.append(HitEffectT1(self.x+self.barrel*8,212))
        if self.x > 1700:
            self.x = 1700
    def draw(self):
        pyxel.blt(self.x- framewin.x,self.y,0,self.barrel*32,144,32,16,0)
    def check_hit(self,x,y):
        if self.x < x and self.x + 24 > x and self.y < y and self.y + 4 > y:
            return True
        else:
            return False
    def __lt__(self, other):
        return self.y < other.y

class Plane():
    def __init__(self,x,y,cop_x,cop_y) -> None:
        self.x = x
        self.y = y
        self.cop_x = cop_x
        self.cop_y = cop_y
        if x <  cop_x:
            self.dx = 1
        else:
            self.dx = -1
        self.status = 0  ## 0:急接近 1:反転準備 2:反転(1) 3:反転(2) 4:ミサイル発射 5:反転完了 6:上昇 7:急上昇 7:退場
        self.is_alive = True
    def update(self):
        if self.status == 0:
            self.x += (self.dx * 3)
            if abs(self.x - self.cop_x) < 10:
                self.status = 1
        elif self.status == 1:
            self.x += (self.dx * 2)
            self.y += 0.5
            if abs(self.x - self.cop_x) > 95:
                self.status = 2
        elif self.status == 2:
            self.x -= (self.dx * 2)
            self.y += 2
            if abs(self.x - self.cop_x) < 84:
                self.status = 3
        elif self.status == 3:
            self.x -= (self.dx * 2)
            self.y += 1
            if abs(self.x - self.cop_x) < 48:
                self.status = 4
        elif self.status == 4:
            ### ミサイル発射
            missiles.append(Missile(self.x,self.y,-self.dx*4,2))
            missiles.append(Missile(self.x,self.y-10,-self.dx*4,2))
            self.status = 5
        elif self.status == 5:
            self.x -= (self.dx * 2)
            if abs(self.x - self.cop_x) > 50:
                self.status = 6
        elif self.status == 6:
            self.x -= (self.dx * 2)
            self.y -= 1
            if abs(self.x - self.cop_x) > 90:
                self.status = 7
        elif self.status == 7:
            self.x -= (self.dx * 5)
            self.y -= 3
            if self.y < -20:
                self.status = 8
                self.is_alive = False
    def draw(self):
        pyxel.blt(self.x-framewin.x,self.y,0,self.status*32,216,32*(-1)*self.dx,16,0)
        #print("status {}   dx {}   plane=({},{})  cop_xy=({},{})".format(self.status,self.dx,self.x-framewin.x,self.y,self.cop_x-framewin.x,self.cop_y))

class Ufo():
    def __init__(self) -> None:
        self.is_active = False
        self.x = 0
        self.y = 0
    def activate(self,x,y):
        self.is_active = True
        self.x = x
        self.y = y
    def update(self):
        if self.is_active:
            if self.x > copter.x+12:
                self.x -= pyxel.rndf(-0.5,2.0)
            else:
                self.x += pyxel.rndf(-0.5,2.0)
            if self.y > copter.y+4:
                self.y -= 0.4
            else:
                self.y += 0.4
    def draw(self):
        if self.is_active:
            pyxel.blt(self.x-framewin.x,self.y,0,0,240,8,8,0)
ufo = Ufo()

class App():
    def __init__(self):
        pyxel.init(240,240,title="チョットコプター（ChottoCopter）",fps=48)
        pyxel.load("copter.pyxres")
        self.init_game()
        pyxel.run(self.update,self.draw)

    def init_game(self):
        global copter,framewin,gameover_cnt,ufo
        init_global_variable()
        copter = Copter()
        framewin = Framewindow()
        for i in range(30):
            stars.append(Star())
        xs = [120,330,360,780,1000,1100,1480]
        for x in xs:
            cabins.append(Cabin(x,208,0))
        cabins[-1].status = 1
        gameover_cnt = 0
        self.gameend_cnt = 0
        self.stage_counter = 0
        pyxel.play(0,0)

    def update(self):
        global count_died,count_board,count_rescued,gameover_cnt,gameend_cnt
        self.stage_counter += 1

        ### ゲームエンド（全員救出か死亡）後に一定時間メッセージを表示
        if gameend_cnt > 0:
            gameend_cnt -= 1
            if gameend_cnt == 0:
                self.init_game()
                return
        elif count_died+count_rescued == 56:
            gameend_cnt = 360
            copter.is_stay = True
            return
        ### ゲームオーバー後に一定時間メッセージを表示
        if gameover_cnt > 0:
            gameover_cnt -= 1
            if gameover_cnt == 0:
                self.init_game()
                return
        ### デバッグ用★★★
        if pyxel.btnp(pyxel.KEY_SPACE):
            planes.append(Plane(copter.x-240,pyxel.rndi(60,120),copter.x,copter.y))
            if pyxel.rndi(0,1)==0:
                ufo.activate(copter.x - 240, pyxel.rndi(-30,0))
            else:
                ufo.activate(copter.x + 240, pyxel.rndi(-30,0))

        ### ジョイパッドの入力判定（自機の移動などに反映）
        ## アナログ左ステックで自機の移動など
        if not copter.is_stay:
            self.gamepad_lx = pyxel.btnv(pyxel.GAMEPAD1_AXIS_LEFTX)
            self.gamepad_ly = pyxel.btnv(pyxel.GAMEPAD1_AXIS_LEFTY)
            if copter.land_flag: # 着地中は左右移動できず、飛び立つとき急加速
                self.gamepad_lx = 0
                self.gamepad_ly *= 100
                if self.gamepad_ly < -1000:
                    copter.landingchecked_flag = False
            copter.force_x += (self.gamepad_lx / 65536 )
            copter.force_y += (self.gamepad_ly / 65536 )
        
        ### AボタンとBボタンは飛行中だけ反応しますよ
        if copter.land_flag == False:
            ### Aボタンで機体の向きを変える
            if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
                if copter.style == 1:
                    if copter.force_x < 0:
                        copter.style = 0
                    else:
                        copter.style = 2
                else:
                    copter.style = 1
            ### Bボタンで弾を発射        
            if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
                if copter.style == 0: # 左向き
                    x = copter.x + 8        #鼻先
                    y = copter.y + 10   #ちょっと下
                    dx = -10
                    dy = -copter.force_x
                    bullet1s.append(Bullet1(x,y,dx,dy))
                elif copter.style == 2: # 右向き
                    x = copter.x + 28        #鼻先
                    y = copter.y + 10   #ちょっと下
                    dx = 10
                    dy = copter.force_x
                    bullet1s.append(Bullet1(x,y,dx,dy))
                else:  # copter.style == 1 or 3: # こっち向き
                    if copter.y > 104:
                        x = copter.x + 16        #鼻先
                        y = copter.y + 10   #ちょっと下
                        dx = (-copter.force_x) / 5
                        dy = 2
                        bullet2s.append(Bullet2(x,y,dx,dy))

        ### 描画範囲（framewin）の設定
        if (copter.x - framewin.x) < 156 and copter.force_x < -0.2:
            framewin.x -= 4
        if (copter.x - framewin.x) >  56 and copter.force_x >  0.2:
            framewin.x += 4

        ### 戦車の出現（仮）
        if pyxel.frame_count%480==0 and copter.x < 1600 and (pyxel.rndi(0,2) == 0 or copter.land_flag):
            r = pyxel.rndi(1,2)
            if len(tanks) < 8:
                for i in range(r):
                    if pyxel.rndi(0,1) == 0:
                        tanks.append(Tank(copter.x - 256,220+pyxel.rndi(-6,6)))
                    else:
                        tanks.append(Tank(copter.x + 256,220+pyxel.rndi(-6,6)))
        ### 戦闘機の出現（仮）
        if len(planes) < 2 and pyxel.frame_count%240==0 and copter.x < 1500 and pyxel.rndi(0,3)==0:
            if pyxel.rndi(0,1) == 0:
                planes.append(Plane(copter.x-240,pyxel.rndi(30,120),copter.x,copter.y))
            else:
                planes.append(Plane(copter.x+240,pyxel.rndi(30,120),copter.x,copter.y))
        ### UFOの出現
        if not ufo.is_active and self.stage_counter > 6000 and pyxel.frame_count%2000==0:
            if pyxel.rndi(0,1)==0:
                ufo.activate(copter.x - 240, pyxel.rndi(-30,0))
            else:
                ufo.activate(copter.x + 240, pyxel.rndi(-30,0))
            

        ### 枠内に表示される背景（地面）の更新
        framewin.update()
        ### 人質小屋の更新
        for cabin in cabins:
            cabin.update()
        ### 救難者の更新
        for rescuer in reversed(rescuers):
            rescuer.update()
            if copter.land_flag and rescuer.is_doing and count_board < 8:
                if copter.style == 0 or copter.style == 2:
                    if (copter.x - rescuer.x) < 8 and (copter.x - rescuer.x) > -32:
                        count_board += 1
                        rescuers.remove(rescuer)
                        pyxel.play(0,5)
                else:
                    if (copter.x - rescuer.x) < 0 and (copter.x - rescuer.x) > -24:
                        count_board += 1
                        rescuers.remove(rescuer)
                        pyxel.play(0,5)
        ### 自機の更新
        copter.update()
        ### 戦車の更新
        for tank in reversed(tanks):
            tank.update()
            if tank.is_alive == False:
                tanks.remove(tank)
                pyxel.play(2,6)
        ### UFOの描画
        ufo.update()
        if ufo.is_active:
            if abs(copter.x+16 - ufo.x) < 16 and abs(copter.y+8 - ufo.y) < 8:
                self.gameover_proc()
        ### 戦闘機の更新
        for plane in reversed(planes):
            plane.update()
            if plane.is_alive == False:
                planes.remove(plane)
        ### 無事に基地に帰還できた人の更新
        for smiler in reversed(smilers):
            smiler.update()
            if smiler.x > 1986:
                smilers.remove(smiler)
        ### 弾とミサイルの更新
        for bullet in reversed(bullet1s):
            bullet.update()
            if bullet.is_alive == False:
                hiteffect1s.append(HitEffect1(bullet.x,bullet.y,bullet.is_hitground))
                bullet1s.remove(bullet)
            elif abs(ufo.x - bullet.x) < 8 and abs(ufo.y - bullet.y) < 8:
                ufo.is_active = False
                hiteffect1s.append(HitEffect1(ufo.x,ufo.y,False))
                bullet1s.remove(bullet)
        for bullet in reversed(bullet2s):
            bullet.update()
            if bullet.is_alive == False:
                hiteffect2s.append(HitEffect2(bullet.x,bullet.y))
                for tank in reversed(tanks):
                    if tank.check_hit(bullet.x,bullet.y):
                        hiteffectt2s.append(HitEffectT2(tank.x,tank.y))
                        tanks.remove(tank)
                bullet2s.remove(bullet)
        for missile in reversed(missiles):
            missile.update()
            if missile.is_alive == False:
                hiteffectt1s.append(HitEffectT1(missile.x,missile.y))
                missiles.remove(missile)
        ### 爆発エフェクトの更新　★当たり判定★　小屋・救助者・戦車・ヘリ
        for hit in reversed(hiteffect1s): ### ヘリからの横向き弾のエフェクト
            hit.update()
            if hit.is_alive == False:
                if hit.is_hitground:
                    for cabin in cabins: ### 小屋の扉
                        if cabin.status == 0:
                            if cabin.x - 2 < hit.x and cabin.x + 10 > hit.x:
                                cabin.status = 1
                    for rescuer in reversed(rescuers): ### 救助者
                        if rescuer.stay_time == 0:
                            if rescuer.x < hit.x and rescuer.x + 8 > hit.x:
                                count_died += 1
                                rescuers.remove(rescuer)
                                pyxel.play(2,8)
                hiteffect1s.remove(hit)
        for hit in reversed(hiteffect2s): ### ヘリからのこっち向き弾のエフェクト
            hit.update()
            if hit.is_alive == False:
                hiteffect2s.remove(hit)
        for hit in reversed(hiteffectt1s): ### 戦車から撃たれた弾のエフェクト
            hit.update()
            if hit.is_alive == False:
                for rescuer in reversed(rescuers): ## 救助者に被弾
                    if abs(rescuer.x - hit.x) < 3:
                        count_died += 1
                        rescuers.remove(rescuer)
                        pyxel.play(2,8)
                for cabin in reversed(cabins): ### 小屋の扉に被弾
                    if cabin.status == 0 and abs(cabin.x - hit.x) < 3:
                        cabin.status = 1
                if copter.land_flag and  copter.x < hit.x-8 and copter.x > hit.x-24:
                    self.gameover_proc()
                    #return
                hiteffectt1s.remove(hit)
        for hit in reversed(hiteffectt2s):
            hit.update()
            if hit.is_alive == False:
                hiteffectt2s.remove(hit)

    def gameover_proc(self):
        global gameover_cnt,count_died,count_board
        hiteffectt2s.append(HitEffectT2(copter.x-3,copter.y-3))
        hiteffectt2s.append(HitEffectT2(copter.x-3,copter.y+3))
        hiteffectt2s.append(HitEffectT2(copter.x+3,copter.y-3))
        hiteffectt2s.append(HitEffectT2(copter.x+3,copter.y+3))
        gameover_cnt = 256
        copter.x = 3000
        copter.y = 300
        copter.is_active = False
        ufo.is_active = False
        count_died += count_board
        count_board = 0
        pyxel.play(2,6)


    def draw(self):
        global count_died,count_board,count_rescued,ufo
        pyxel.cls(0)

        ### 星の描画
        for star in stars:
            star.draw()
        pyxel.blt(190,80,1,0,32,32,32,0)
        ### 枠内に表示される背景（地面）の描画
        framewin.draw()
        ### 旗の描画
        pyxel.blt(2000 - framewin.x,200,0,pyxel.frame_count//6%4*8+16,8,8,8,0)
        ### 人質小屋の描画
        for cabin in cabins:
            cabin.draw()
        ### 救難者の描画
        for rescuer in rescuers:
            rescuer.draw()
        ### 自機の描画
        copter.draw()
        ### 戦車の描画
        for tank in sorted(tanks):
            tank.draw()
        ### 戦闘機の描画
        for plane in reversed(planes):
            plane.draw()
        ### UFOの描画
        ufo.draw()
        ### 無事に基地に帰還できた人の描画
        for smiler in smilers:
            smiler.draw()
        ### 弾とミサイルの描画
        for bullet in bullet1s:
            bullet.draw()
        for bullet in bullet2s:
            bullet.draw()
        for missile in missiles:
            missile.draw()

        ### 爆発エフェクトの描画
        for hit in hiteffect1s:
            hit.draw()
        for hit in hiteffect2s:
            hit.draw()
        for hit in hiteffectt1s:
            hit.draw()
        for hit in hiteffectt2s:
            hit.draw()

        ### 死亡者数、搭乗者数、救助完了者数の描画
        pyxel.blt(32,10,1,0,8,8,8,0)
        pyxel.blt(40,10,1,count_died//10*8,0,8,8,0)
        pyxel.blt(48,10,1,count_died%10*8,0,8,8,0)
        pyxel.blt(112,10,1,8,8,8,8,0)
        pyxel.blt(120,10,1,count_board//10*8,0,8,8,0)
        pyxel.blt(128,10,1,count_board%10*8,0,8,8,0)
        pyxel.blt(192,10,1,16,8,8,8,0)
        pyxel.blt(200,10,1,count_rescued//10*8,0,8,8,0)
        pyxel.blt(208,10,1,count_rescued%10*8,0,8,8,0)
        ### 基地と戦場との境界線
        pyxel.line(1802 - framewin.x,216,(1800-framewin.x)-(framewin.x-1660),400,7)
        pyxel.line(1800 - framewin.x,216,(1800-framewin.x)-(framewin.x-1600),400,7)

        if gameend_cnt > 0:
            #pyxel.text(100,100,"GAME\nEND",7)
            pyxel.blt(92,100,1,0,88,56,40,0)
        elif gameover_cnt > 0:
            #pyxel.text(100,100,"GAME OVER",7)
            pyxel.blt(72,100,1,0,64,104,16,0)

        ### デバッグ用描画
        #pyxel.text(40,50,"gameend_cnt:{}  gameover_cnt:{}".format(gameend_cnt,gameover_cnt),7)
        #pyxel.text(40,30,"Copter ({},{} force_y:{})".format(int(copter.x),int(copter.y),copter.force_y),7)
        #pyxel.text(40,40,"landingchecked_flag:{}".format(copter.landingchecked_flag),7)
        #pyxel.text(40,50,"framewin.x:{}".format(int(framewin.x)),7)
        #pyxel.text(40,60,"len(tanks):{}   len(planes):{}    ufo:({},{})".format(len(tanks),len(planes),int(ufo.x),int(ufo.y)),7)
        #pyxel.text(40,70,"AXISX:{}".format(pyxel.btnv(pyxel.GAMEPAD1_AXIS_LEFTX)),7)
        #pyxel.text(40,80,"AXISY:{}".format(pyxel.btnv(pyxel.GAMEPAD1_AXIS_LEFTY)),7)
App()

