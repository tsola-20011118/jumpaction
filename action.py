import pyxel

import pyxel


class App:
    def __init__(self):
        pyxel.init(256, 256, fps=30)
        pyxel.load("action.pyxres")
        # playerをインスタンス化
        self.player = Player()
        self.time = 0
        # groundのインスタンス化
        self.normalGround = [];
        
        # self.placeY = 0;
        #groundの個数
        self.groundNum = 4;
        # self.fallFlag = False;
        # self.bottomBottomHit = False;
        # self.groundFallNum = -1;
        # self.groundCheck = True;
        for i in range(self.groundNum):
            self.normalGround.append(NormalGround(i, 256 - (i + 1) * 32))
        pyxel.run(self.update, self.draw);

    def update(self):
        #playerのアップデート
        self.player.update()
        # self.placeY = 192  + 16 - self.player.y;
        # if self.placeY < 0:
        #     self.placeY = 0;
        # if self.placeY % 64 <= len(self.normalGround):
        #     self.normalGround.append(NormalGround(len(self.normalGround), 256 - (len(self.normalGround) + 1) * 64));
        #     self.groundNum += 1;
        # for i in range(self.groundNum):
        #     self.normalGround[i].update();
        #     if self.normalGround[i].onGround == False and BottomHitCheck(self.player.x, self.player.y, self.normalGround[i]) == True:
        #         self.player.jumpUpDown = 0;
        #         self.player.y = self.normalGround[i].y - 16;
        #         self.player.jumpFlag = False;
        #         self.player.spaceTime = 0;
        #         self.normalGround[i].onGround = True;
        #         # self.fallFlag = False;
        #     if self.player.fallFlag == False and BottomHitCheck(self.player.x, self.player.y, self.normalGround[i]) == False:
                # if self.normalGround[i].onGround == True:
                #     self.groundFallNum = i;
        #         self.normalGround[i].onGround = False;
        #     if TopHitCheck(self.player, self.normalGround[i]) == True:
        #         self.player.jumpUpDown = -1
        #         self.player.y = self.normalGround[i].y + 8;
        # for i in range(self.groundNum):
        #     if self.normalGround[i].onGround == False and self.player.y + 16 == self.normalGround[i].y:
        #         self.player.fallFlag = True;
        #         break;
            # else:
            #     self.player.fallFlag = False;
        # if self.player.fallFlag == False:
        #     self.groundFallNum = -1;
        # 
        # if self.player.fallFlag == True and self.player.y != 240:
        #     self.player.y += 5;
        #     if self.player.y >= 256:
        #         self.player.y = 240;
        #         self.fallFlag = False;
        #     if self.player.y > self.normalGround[0].y + 64 -16:
        #         self.player.y = self.normalGround[0].y + 64 - 16;
        #         
        self.time += 1;

    def draw(self):
        pyxel.cls(1)
        self.player.draw()
        for i in range(self.groundNum):
            if self.normalGround[i].y >= -8 and self.normalGround[i].y <= 256:
                self.normalGround[i].draw();
        pyxel.line(0, 64, 256, 64, 4)
        pyxel.line(0, 128, 256, 128, 4)
        pyxel.line(0, 192, 256, 192, 4)

        pyxel.text(0, 20, str(self.time), 0)
        # pyxel.text(0, 30, str(TopHitCheck(self.player, self.normalGround[0])), 0)
        pyxel.text(0, 40, str(BottomHitCheck(self.player.x, self.player.y, self.normalGround[0])), 0)
        # pyxel.text(0, 50, str(self.normalGround[0].boxNum), 0)
        # pyxel.text(0, 60, str(self.player.speed), 0)
        # pyxel.text(0, 70, str(self.normalGround[0].x + 16 * self.normalGround[0].boxNum), 0)
        pyxel.text(0, 80, str(self.player.fallFlag), 0)



class Player:
    def __init__(self):
        # 飛んでいる状態True , 飛んでいない状態False
        self.jumpFlag = False;
        # 上に飛んでいる状態-1 , 下に飛んでいる状態1;
        self.jumpUpDown = 0;
        # playerの位置（左上）(スタート地点は中心)
        self.x = (256 - 16) / 2;
        self.y = 256 - 16;
        # playerが右端にはみ出ている時のflag
        self.moveOutR = False;
        # playerが左端にはみ出ている時のflag
        self.moveOutL = False;
        # 飛ぶときの初期位置
        self.startY = 0;
        # spaceを押した時間
        self.spaceTime = 0;
        # imageの番号
        self.imageNum = 0;
        #落ちているかの管理
        # self.fallFlag = False;
        # self.speed = 0;
        # groundの上にいる時　１,下にいる時-1
        self.groundHit = -1;

    def update(self):
        # 常に行う処理
        # 右左に動く
        self.moveRL()
        # 左右にはみ出た時反対側に移動する
        self.moveOut();
        # if fallFlag == False:
        #     pass;
        # 飛んでいない時にする処理
        if self.jumpFlag == False:
            self.jumpStart();
        # 飛んでいる時にする処理
        if self.jumpFlag == True:
            self.jump();
        self.imageChange();
        # if self.fallFlag == True:
        #     self.y += 5;

    def draw(self):
        pyxel.blt(self.x, self.y, 0, self.imageNum, 0, 16, 16, 0)
        if self.moveOutL == True:
            pyxel.blt(256 + self.x, self.y, 0, self.imageNum, 0, 16, 16, 0)
        if self.moveOutR == True:
            pyxel.blt(self.x - 256, self.y, 0, self.imageNum, 0, 16, 16, 0)

    def moveOut(self):
        if self.x < 0 and self.x + 16 > 0:
            self.moveOutL = True
        if self.moveOutL == True:
            if self.x < -16:
                self.x = 256 + self.x
                self.moveOutL = False
            if self.x > 0:
                self.moveOutL = False
        if self.x < 256 and self.x + 16 > 256:
            self.moveOutR = Trueaaaaa
        if self.moveOutR == True:
            if self.x > 256:
                self.x = self.x - 256
                self.moveOutR = False
            if self.x < 256 - 16:
                self.moveOutR = False

    def moveRL(self):
        if pyxel.btnp(pyxel.KEY_RIGHT, 1, 1):
            self.x += 3;
        if pyxel.btnp(pyxel.KEY_LEFT, 1, 1):
            self.x -= 3;

    def jumpStart(self):
        # スペースキーが話されたら上に飛んでいることにする
        if pyxel.btnp(pyxel.KEY_SPACE, 1, 1) or pyxel.btnp(pyxel.KEY_UP, 1, 1):
            if self.spaceTime <= 20:
                self.spaceTime += 1
            # self.spaceTime = 17;#13,17,18,
        if ((not pyxel.btnp(pyxel.KEY_SPACE, 1, 1)) and (not pyxel.btnp(pyxel.KEY_UP, 1, 1))) and self.spaceTime != 0:
            self.spaceTime = 10 if self.spaceTime == 13 else self.spaceTime;
            self.spaceTime = 16 if self.spaceTime == 17 or self.spaceTime == 18 else self.spaceTime;
            # 上向に飛ぶ指標
            self.jumpUpDown = 1
            # スタート位置を記録
            self.startY = self.y
            # 飛んでいる状態に
            self.jumpFlag = True

    def jump(self):
        self.speed = (self.startY - self.spaceTime * 9 - self.y) * self.jumpUpDown / 8
        self.y += self.speed;
        if self.jumpUpDown == 1 and self.y < self.startY - self.spaceTime * 8:
            self.jumpUpDown = -1
        if self.jumpUpDown == -1 and self.y > self.startY:
            self.y = self.startY
            self.jumpUpDown = 0
            self.spaceTime = 0
            self.jumpFlag = False

    def imageChange(self):
        if self.jumpUpDown == 0 and self.spaceTime != 0:
            self.imageNum = 16
        elif self.jumpUpDown != 0:
            self.imageNum = 32
        else:
            self.imageNum = 0


class NormalGround:
    def __init__(self, i, y):
        self.direction = i % 2;
        self.boxNum = pyxel.rndi(0, 16)
        self.x = 16;
        self.y = y
        self.tempY = y
        # self.hit
        if self.direction == 1:
            self.x = 256 - 16 * (self.boxNum + 1);
        # bottomcheckの回避用
        self.onGround = False;

    def update(self):
        pass;

    def draw(self):
        for x in range(self.boxNum):
            # if self.direction == 2 and x == self.boxNum - 1:
                pyxel.blt(self.x + x * 16, self.y, 0, 32, 16, 16, 8, 0)
            # elif self.direction == 1 and x == 0:
            #     pyxel.blt(self.x + x * 16, self.y, 0, 0, 16, 16, 8, 0)
            # else:
            #     pyxel.blt(self.x + x * 16, self.y, 0, 16, 16, 16, 8, 0)


# def TopHitCheck(player, ground):
#     if ground.y <= player.y and player.y <= ground.y + 8 and ground.x - 16 < player.x and player.x < ground.x + ground.boxNum * 16:
#         return True;
#     return False;


# def BottomHitCheck(playerX, playerY, ground):
#     if ground.y <= playerY + 17 and playerY + 17 <= ground.y + 8 and ground.x - 16 < playerX and playerX < ground.x + ground.boxNum * 16:
#         return True;
#     return False;


# def OnCheck(playerX, playerY, ground):
#     #groundより下にいる時
#     if playerY > ground.y:
#         return False
#     #groundの上にいて
#     elif playerY == ground.y - 16:
#         # groundに乗ってない時
#         if BottomHitCheck(playerX, playerY, ground) == False:
#             return -1;
#         # groundに乗ってる時
#         else:
#             return 1;
#     else:
#         return True;


# class nomalGround:
#     def __init__(self, y):
#         self.direction = pyxel.rndi(1, 2)
#         self.boxNum = pyxel.rndi(2, 6);
#         self.x = 0;
#         self.y = y;
#         if self.direction == 1:
#             self.x = 256 - 16 * self.boxNum;

#     def update(self):
#         pass;

#     def draw(self):
#         for x in range(self.boxNum):
#             if self.direction == 2 and x == self.boxNum - 1:
#                 pyxel.blt(self.x + x * 16, self.y, 0, 32, 16, 16, 8, 0)
#             elif self.direction == 1 and x == 0:
#                 pyxel.blt(self.x + x * 16, self.y, 0, 0, 16, 16, 8, 0)
#             else:
#                 pyxel.blt(self.x + x * 16, self.y, 0, 16, 16, 16, 8, 0)


# def TopHitCheck(playerX, playerY, ground):
#     if playerY - 1 > ground.y and playerY - 8 < ground.y and playerX > ground.x - 8 and playerX < ground.x + ground.boxNum * 16 - 8:
#         return False;
#     return True;

# def BottomHitCheck(playerX, playerY, ground):
#     if playerY < ground.y and playerY + 16 > ground.y and playerX > ground.x - 3 and playerX < ground.x + ground.boxNum * 16 - 13:
#         return False
#     return True


App()

