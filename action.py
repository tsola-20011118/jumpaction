import pyxel

import pyxel


class App:
    def __init__(self):
        pyxel.init(256, 256)
        pyxel.load("action.pyxres")
        # playerをインスタンス化
        self.player = Player()
        self.time = 0
        self.normalGround = [];
        self.placeY = 0;
        self.groundNum = 4;
        self.fallFlag = 0;
        # self.groundCheck = True;
        for i in range(self.groundNum):
            self.normalGround.append(NormalGround(i, 256 - (i + 1) * 64))
        pyxel.run(self.update, self.draw);
        

    def update(self):
        
        # self.placeY = 192  + 16 - self.player.y;
        # if self.placeY < 0:
        #     self.placeY = 0;
        self.player.update()
        if self.placeY % 64 <= len(self.normalGround):
            self.normalGround.append(NormalGround(len(self.normalGround), 256 - (len(self.normalGround) + 1) * 64));
            self.groundNum += 1;
        for i in range(self.groundNum):
            self.normalGround[i].update()
            if BottomHitCheck(self.player.x, self.player.y, self.normalGround[i]) == False:
                self.player.jumpUpDown = 0;
                self.player.y = self.normalGround[i].y - 16;
                self.player.jumpFlag = False;
                self.player.spaceTime = 0;
                self.fallFlag = False;
            elif TopHitCheck(self.player.x, self.player.y, self.normalGround[i]) == False:
                self.player.jumpUpDown = -1
                self.player.y = self.normalGround[i].y - 16;
            
            if OnCheck(self.player.x, self.player.y, self.normalGround[i]) == -1:
                self.fallFlag = True;
        if self.fallFlag == True:
            if self.player.y > self.normalGround[0].y + 64 -16:
                self.player.y = self.normalGround[0].y + 64 - 16;
                self.fallFlag = False;
            self.player.y += 5
        self.time += 1

    def draw(self):
        pyxel.cls(1)
        self.player.draw()
        for i in range(self.groundNum):
            if self.normalGround[i].y >= -8 and self.normalGround[i].y <= 256:
                self.normalGround[i].draw();
        pyxel.line(0, 64, 256, 64, 4)
        pyxel.line(0, 128, 256, 128, 4)
        pyxel.line(0, 192, 256, 192, 4)
        pyxel.text(0, 10, str(OnCheck(self.player.x, self.player.y, self.normalGround[0])), 0)
        pyxel.text(0, 20, str(OnCheck(self.player.x, self.player.y, self.normalGround[1])), 0)
        pyxel.text(0, 30, str(OnCheck(self.player.x, self.player.y, self.normalGround[2])), 0)
        pyxel.text(0, 40, str(OnCheck(self.player.x, self.player.y, self.normalGround[3])), 0)
        pyxel.text(0, 50, str(self.player.y), 0)
        pyxel.text(0, 60, str(self.normalGround[0].y), 0)
        pyxel.text(0, 70, str(self.normalGround[0].y + 64 - 16), 0)
        pyxel.text(0, 80, str(self.fallFlag), 0)



class Player:
    def __init__(self):
        # 飛んでいる状態True , 飛んでいない状態False
        self.jumpFlag = False
        # 上に飛んでいる状態-1 , 下に飛んでいる状態1;
        self.jumpUpDown = 0
        # playerの位置（左上）(スタート地点は中心)
        self.x = (256 - 16) / 2
        self.y = 256 - 16
        # playerが右端にはみ出ている時のflag
        self.moveOutR = False
        # playerが左端にはみ出ている時のflag
        self.moveOutL = False
        # 飛ぶときの初期位置
        self.startY = 0
        # spaceを押した時間
        self.spaceTime = 0
        # imageの番号
        self.imageNum = 0

    def update(self):
        # 常に行う処理
        # 右左に動く
        self.moveRL()
        # 左右にはみ出た時反対側に移動する
        self.moveOut()
        # 飛んでいない時にする処理
        if self.jumpFlag == False:
            self.jumpStart()
        # 飛んでいる時にする処理
        if self.jumpFlag == True:
            self.jump()
        self.imageChange()

    def draw(self):
        pyxel.blt(self.x, self.y, 0, self.imageNum, 0, 16, 16, 0)
        if self.moveOutL == True:
            pyxel.blt(256 + self.x, self.y, 0, self.imageNum, 0, 16, 16, 0)
        if self.moveOutR == True:
            pyxel.blt(self.x - 256, self.y, 0, self.imageNum, 0, 16, 16, 0)

        # pyxel.text(0, 10, str(self.jumpUpDown), 0)

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
            self.moveOutR = True
        if self.moveOutR == True:
            if self.x > 256:
                self.x = self.x - 256
                self.moveOutR = False
            if self.x < 256 - 16:
                self.moveOutR = False

    def moveRL(self):
        if pyxel.btnp(pyxel.KEY_RIGHT, 1, 1):
            self.x += 3
        if pyxel.btnp(pyxel.KEY_LEFT, 1, 1):
            self.x -= 3

    def jumpStart(self):
        # スペースキーが話されたら上に飛んでいることにする
        if pyxel.btnp(pyxel.KEY_SPACE, 1, 1):
            if self.spaceTime <= 20:
                self.spaceTime += 1
        if (not pyxel.btnp(pyxel.KEY_SPACE, 1, 1)) and self.spaceTime != 0:
            # 上向に飛ぶ指標
            self.jumpUpDown = 1
            # スタート位置を記録
            self.startY = self.y
            # 飛んでいる状態に
            self.jumpFlag = True

    def jump(self):
        self.y += (self.startY - self.spaceTime *
                   9 - self.y) * self.jumpUpDown / 8
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
        self.boxNum = pyxel.rndi(2, 7)
        self.x = 16;
        self.y = y
        self.tempY = y
        if self.direction == 1:
            self.x = 256 - 16 *(self.boxNum + 1)

    def update(self):
        pass;

    def draw(self):
        for x in range(self.boxNum):
            if self.direction == 2 and x == self.boxNum - 1:
                pyxel.blt(self.x + x * 16, self.y, 0, 32, 16, 16, 8, 0)
            elif self.direction == 1 and x == 0:
                pyxel.blt(self.x + x * 16, self.y, 0, 0, 16, 16, 8, 0)
            else:
                pyxel.blt(self.x + x * 16, self.y, 0, 16, 16, 16, 8, 0)


def TopHitCheck(playerX, playerY, ground):
    if playerY < ground.y + 8 and playerY + 16 > ground.y and playerX > ground.x - 15 and playerX < ground.x + ground.boxNum * 16 - 1:
        return False
    return True


def BottomHitCheck(playerX, playerY, ground):
    if playerY < ground.y and playerY + 16 > ground.y and playerX > ground.x - 15 and playerX < ground.x + ground.boxNum * 16 - 1:
        return False
    return True


def OnCheck(playerX, playerY, ground):
    if playerY + 16 != ground.y:
        return 0
    elif playerY + 16 == ground.y and (playerX < ground.x - 15 or playerX > ground.x + ground.boxNum * 16 - 1):
        return -1;
    
    return 1;


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

