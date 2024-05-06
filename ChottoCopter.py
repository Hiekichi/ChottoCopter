import pyxel

### グローバル変数
bullet1s = []
bullet2s = []
hiteffects = []
stars = []

class Copter():
    def __init__(self) -> None:
        self.cnt = 0
        self.force_x = 0
        self.force_y = 0
        self.x = 1924  # 絶対座標、世界の中でのx座標
        self.y = 206   # 絶対座標、世界の中でのy座標
        self.crush_flag = False
        self.land_flag = False
        self.style = 0  # 0:左向き、1:こっち向き、2:右向き、3:こっち向き
    def update(self):
        self.cnt += 1
        #print(str(self.cnt))
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
        #print(self.y)
        if round(self.y) >= 206:
            #print("着地！")
            self.y = 206
            #if self.force_y > 1:
            #    self.crush_flag = True
            self.force_y = 0
            self.land_flag = True
        else:
            self.y += 0.5
            self.land_flag = False


    def draw(self):
        ### 描画位置の計算
        x = self.x - framewin.x
        y = self.y
        if self.style == 0: # 左向き
            if self.land_flag:
                pyxel.blt(x,y,0,(self.cnt//8%4)*32,16,32,16,0)
                #print("着地の描画！！！" + str(self.cnt))
                return
            elif self.force_x < -1: # 左に加速
                pyxel.blt(x,y,0,(self.cnt%4)*32,32,32,16,0)
            elif self.force_x > 1: # 右に加速
                pyxel.blt(x,y,0,(self.cnt%4)*32,48,32,16,0)
            else: #if self.force_x >= -1 and self.force_x <= 1:
                pyxel.blt(x,y,0,(self.cnt%4)*32,16,32,16,0)
                #print("飛行中の描画")
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
        self.x = 2048 - 256   # 世界のどの位置を表示中か
    def update(self):
        if self.x <= 0:
            self.x = 0
        elif self.x >= 1792: # 2048-256
            self.x = 1792
    def draw(self):
        pyxel.bltm(0,256-64,0,self.x,0,256,64,0)
framewin = Framewindow()

class HitEffect():
    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y
        self.cnt = 30
        self.is_alive = True
    def update(self):
        self.cnt -= 1
        if self.cnt <= 0:
            self.is_alive = False
    def draw(self):
        #print("Draw  {},{}  {}  {}".format(self.x - framewin.x,self.y,(24-self.cnt)//6*16,128))
        pyxel.blt(self.x - framewin.x,self.y,0,(24-self.cnt)//6*16,128,16,8,0)
        pyxel.blt(0,0,0,(24-self.cnt)//6*16,128,16,8,0)

class Bullet1():
    def __init__(self,x,y,dx,dy) -> None:
        self.is_alive = True
        self.cnt = 48
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.cnt -= 1
        if self.y > 200 or self.cnt < 0 or self.y < -10:
            self.is_alive = False
    def draw(self):
        #print("{},{}".format(self.x - framewin.x,self.y))
        pyxel.circ(self.x - framewin.x,self.y,1,7)

class Bullet2():
    def __init__(self,x,y,dx,dy) -> None:
        self.is_alive = True
        #self.cnt = 48
        self.hit_height = 216 + (206 - y) //2
        print(self.hit_height)
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
    def update(self):
        self.x += self.dx
        self.y += self.dy
        #self.cnt -= 1
        if self.y > self.hit_height:
            self.is_alive = False
    def draw(self):
        #print("{}  {}  ({},{})".format(self.x,framewin.x,self.x - framewin.x,self.y))
        pyxel.circ(self.x - framewin.x,self.y,1,13)

class Star():
    def __init__(self) -> None:
        self.x = pyxel.rndi(2,252)
        self.y = pyxel.rndi(2,204)
    def update(self):
        pass
    def draw(self):
        pyxel.pset(self.x,self.y,pyxel.rndi(7,12))


class App():
    def __init__(self):
        pyxel.init(256,256,title="チョットコプター（ChottoCopter）",fps=48)
        pyxel.load("copter.pyxres")
        for i in range(30):
            stars.append(Star())
        pyxel.run(self.update,self.draw)

    def update(self):

        ### ジョイパッドの入力判定（自機の移動などに反映）
        ## アナログ左ステックで自機の移動など
        self.gamepad_lx = pyxel.btnv(pyxel.GAMEPAD1_AXIS_LEFTX)
        self.gamepad_ly = pyxel.btnv(pyxel.GAMEPAD1_AXIS_LEFTY)
        if copter.land_flag: # 着地中は左右移動できず、飛び立つとき急加速
            self.gamepad_lx = 0
            self.gamepad_ly *= 100
        copter.force_x += (self.gamepad_lx / 65536 )
        copter.force_y += (self.gamepad_ly / 65536 )
        
        ### AボタンとBボタンは飛行中だけ反応しますよ
        if copter.land_flag == False:
            ### Aボタンで機体の向きを変える
            if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
                copter.style += 1
                if copter.style > 3:
                    copter.style = 0
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
                    if copter.y > 140:
                        x = copter.x + 16        #鼻先
                        y = copter.y + 10   #ちょっと下
                        dx = (-copter.force_x) / 5
                        dy = 2
                        bullet2s.append(Bullet2(x,y,dx,dy))

        if (copter.x - framewin.x) < 156 and copter.force_x < -0.2:
            framewin.x -= 4
        if (copter.x - framewin.x) >  56 and copter.force_x >  0.2:
            framewin.x += 4


        ### 枠内に表示される背景（地面）の更新
        framewin.update()
        ### 自機の更新
        copter.update()
        ### 弾の更新
        for bullet in bullet1s:
            bullet.update()
            #print("{}  {}  {}".format(bullet.x,bullet.y,bullet.cnt))
            if bullet.is_alive == False:
                bullet1s.remove(bullet)
        for bullet in bullet2s:
            bullet.update()
            #print("{},  {},  {}".format(bullet.x,bullet.y,bullet.hit_height))
            if bullet.is_alive == False:
                hiteffects.append(HitEffect(bullet.x,bullet.y))
                bullet2s.remove(bullet)
        ### 爆発エフェクトの更新
        for hit in hiteffects:
            hit.update()
            if hit.is_alive == False:
                hiteffects.remove(hit)

    def draw(self):
        pyxel.cls(0)
        pyxel.text(10,10,"AXIA_LEFTX : {}".format(self.gamepad_lx),7)
        pyxel.text(10,20,"AXIA_LEFTX : {}".format(self.gamepad_ly),7)

        ### デバッグ用
        pyxel.text(10,180,"copter.force_x : {}".format(copter.force_x),7)
        pyxel.text(10,190,"copter.force_y : {}".format(copter.force_y),7)

        ### 星の描画
        for star in stars:
            star.draw()
        ### 枠内に表示される背景（地面）の描画
        framewin.draw()
        ### 自機の描画
        copter.draw()
        ### 弾の描画
        for bullet in bullet1s:
            bullet.draw()
        for bullet in bullet2s:
            bullet.draw()
        ### 爆発エフェクトの描画
        for hit in hiteffects:
            hit.draw()

App()

