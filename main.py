from tkinter import *
import math
import numpy as np 
import os
class Eay(Frame):
    board=[]
    profits={}#黑方每个点的收益
    profits_={}#白方每个点的收益
    P=[]#每个点的各项指标
    def search(self,x,y):

        padding = 4
        x1, y1 = max(0, x - padding), max(0, y - padding)
        x2, y2 = min(14, x + padding), min(14, y + padding)
        line_strs = {}
        line_strs['horizontal'] = ''.join(str(self.a[y, x]) for x in range(x1, x2 + 1))
        line_strs['vertical'] = ''.join(str(self.a[y, x]) for y in range(y1, y2 + 1))
        line_strs['diagonal1'] = ''.join(str(self.a[j, i]) for i, j in zip(range(x1, x2 + 1), range(y1, y2 + 1)))
        line_strs['diagonal2'] = ''.join(str(self.a[j, i]) for i, j in zip(range(x1, x2 + 1), reversed(range(y1, y2 + 1))))
        for key, line in line_strs.items():
            print(line)
            if '00000' in line:
                print('黑棋胜！')
                break
            elif '11111' in line:
                print('白棋胜！')
                break
        else:
            print('未分胜负！')
        s=np.array(self.a)#打印数字棋盘
        os.system("cls")#清屏
        print('board \n',s.T)
   
        
    def analyse(self):
        for i in Eay.board:
            self.a[int(i[0])][int(i[1])]=Eay.board.index(i)%2#根据奇偶分配黑白
        #print(self.a)
    def createWidgets(self):
        self.draw = Canvas(self, width=313, height=313)
        self.ball = self.draw.create_image(313,313,image=img,anchor=SE)
        self.draw.pack(side=LEFT)
    def justy(self,x,y):#定位
        self.x_1=math.ceil((x-18)/20)*20+18
        self.x_2=math.floor((x-18)/20)*20+18
        self.y_1=math.ceil((y-18)/20)*20+18
        self.y_2=math.floor((y-18)/20)*20+18
        if abs(self.x_1-x)<abs(self.x_2-x):
            x_=self.x_1
        else:
            x_=self.x_2
        if abs(self.y_1-y)<abs(self.y_2-y):
            y_=self.y_1
        else:
            y_=self.y_2
        return x_,y_
    def mouseMove(self, event):
        self.mouse_x = event.x
        self.mouse_y = event.y
        x=(self.justy(event.x,event.y)[0]-18)/20
        y=(self.justy(event.x,event.y)[1]-18)/20
        #print(self.justy(event.x,event.y)[0],self.justy(event.x,event.y)[1])
        print('当前棋子的坐标为：({}, {})'.format(x,y))
        if [x,y] not in Eay.board:
            if len(Eay.board)%2==0:
                self.draw.create_image(x*20+18,y*20+18,image=img_b)
            else:
                self.draw.create_image(x*20+18,y*20+18,image=img_w)
            Eay.board.append([x,y])
        print(Eay.board)
        print('扫描每个空点的价值')
        self.analyse()
        s=np.array(self.a)#打印数字棋盘
        s=s.T
        #print('数字棋盘',s)
        for i in range(15):
            for j in range(15):
                if s[i][j]==3:
                    self.scan(i,j)
        l,m=Eay.profits[max(Eay.profits)][0][0],Eay.profits[max(Eay.profits)][0][1]
        print('b_max  ',max(Eay.profits),'\n',Eay.profits[max(Eay.profits)])#对黑来说获得最大收益坐标
        l,m=l*20+18,m*20+18
        self.draw.create_oval(m-10, l-10, m+10, l+10)
        
        h=Eay.profits_[max(Eay.profits_)]

        l,m=h[0][0],h[0][1]
        l,m=l*20+18,m*20+18
        self.draw.create_rectangle(m-10, l-10, m+10, l+10)
        
        print('w_max ',max(Eay.profits_),'\n',Eay.profits_[max(Eay.profits_)])#对白来说获得最大收益坐标
        #self.search(int(x),int(y))#判断输赢
        Eay.profits={}#清空
        Eay.profits_={}#清空
        Eay.P=[]#清空
    def move_ball(self, *args):
        #当鼠标在窗口中单击的时候执行
        Widget.bind(self.draw, "<Button-1>", self.mouseMove)
    def length(self,p):#求能够形成的最大子串长度
        
        h=[]
        length_b=0
        length_w=0
        h.append(p[3][::-1]+p[4])#上下连线
        h.append(p[1][::-1]+p[6])#左右连线
        h.append(p[2][::-1]+p[5])#左下右上连线
        h.append(p[0][::-1]+p[7])#左上右下连线
        for s in h:
            for j in range(6):
                if j*'1' in s and j>=length_w:
                    length_w=j
                elif j*'0' in s and j>=length_b:
                    length_b=j

        return length_b,length_w
    def scan(self,x,y):
        self.a=np.array(self.a).T
        d=[-1,0,1]
        group=[]
        distance=0#点-群体距离
        distance_=0#点-中心（7,7）距离
        bs=0#最大连续子串长度
        
        for w in range(3):
            for u in range(3):
                t=''
                if u==1 and w==1:#跳过这种情况
                    continue
                for i in range(1,5):#步长4，不包含本身
                    if x+i*d[w]<15 and x+i*d[w]>-1 and y+i*d[u]>-1 and y+i*d[u]<15:
                        t+=str(self.a[x+i*d[w]][y+i*d[u]])
                        x_,y_=x+i*d[w],y+i*d[u]
                        if self.a[x_][y_]!=3:
                            distance+=(x-x_)**2+(y-y_)**2
                group.append(t)
        distance_=(x-7)**2+(y-7)**2
        score=self.value(group,distance,distance_,(x,y))
        #print(x,y,'价值',score)
        if score in Eay.profits.keys():
            Eay.profits[score[0]].append((x,y))
            Eay.profits_[score[1]].append((x,y))
        else:
            Eay.profits[score[0]]=[(x,y)]
            Eay.profits_[score[1]]=[(x,y)]
        #print(x,y,self.value(group))
        
    def value(self,p,d,d_,f):#计算点的价值
        s=''
        for i in p:
            s+=i
        Eay.P.append([f,((np.array([s.count('0'),(-1)*s.count('1'),(-1)*d,(-1)*d_,self.length(p)[0]])*self.params).sum(),\
                        (np.array([s.count('1'),(-1)*s.count('0'),(-1)*d,(-1)*d_,self.length(p)[1]])*self.params).sum() ),s.count('0'),(-1)*s.count('1'),(-1)*d,(-1)*d_,self.length(p)])
  
        return (np.array([s.count('0'),(-1)*s.count('1'),(-1)*d,(-1)*d_,self.length(p)[0]])*self.params).sum(),\
    (np.array([s.count('1'),(-1)*s.count('0'),(-1)*d,(-1)*d_,self.length(p)[1]])*self.params).sum() #black profits,white profits
    def test(self):
        #print(len(Eay.P))

        print('Test:',self.scan(7,7),self.length(self.scan(7,7)))
        
    def __init__(self, master=None):
        Frame.__init__(self, master)
        Pack.config(self)
        self.createWidgets()
        self.after(10, self.move_ball)
        self.params=np.array([1,0.7,0.05,0.08,2])#参数：己方数量、敌方数量、点-群距离、点-中心距离、最长子串
        self.a=np.array([3]*225).reshape(15,15)
        
root=Tk()
img=PhotoImage(file="mokugo.png")
img_b=PhotoImage(file="黑棋.png")
img_w=PhotoImage(file="白棋.png")
game = Eay(root)
game.mainloop()
