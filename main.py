from tkinter import *
import math
import numpy as np 
class Eay(Frame):
	counter=0
	board=[]
	def search(self,x,y):
		self.analyse()
		d=[-1,0,1]
		for w in range(3):
			for u in range(3):
				t=''
				if u==1 and w==1:#跳过这种情况
					continue
				for i in range(5):#步长5，包含本身
					if x+i*d[w]<15 and x+i*d[w]>-1 and y+i*d[u]>-1 and y+i*d[u]<15:
						t+=str(self.a[x+i*d[w]][y+i*d[u]])
				print(t)
				if '00000'==t:
					print('白棋胜！')
					break
				elif '11111'==t:
					print('黑棋胜！')
					break
					
		print(self.a)
	def analyse(self):
		for i in Eay.board:
			self.a[int(i[0])][int(i[1])]=i[2]
		print(self.a)
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
		print(self.justy(event.x,event.y)[0],self.justy(event.x,event.y)[1])
		print('棋子的坐标为：({}, {})'.format(x,y))
		if [x,y,Eay.counter%2] not in Eay.board:
			Eay.counter+=1
			if Eay.counter%2:
				self.draw.create_image(x*20+18,y*20+18,image=img_b)
			else:
				self.draw.create_image(x*20+18,y*20+18,image=img_w)
			Eay.board.append([x,y,Eay.counter%2])
		print(Eay.board)
		self.search(int(x),int(y))
	def move_ball(self, *args):
		#当鼠标在窗口中单击的时候执行
		Widget.bind(self.draw, "<Button-1>", self.mouseMove)
	
	def __init__(self, master=None):
		Frame.__init__(self, master)
		Pack.config(self)
		self.createWidgets()
		self.after(10, self.move_ball)
		self.a=np.array([3]*225).reshape(15,15)
		
root=Tk()
img=PhotoImage(file="C:/Users/Administrator/Desktop/python练习/mokugo.png")
img_b=PhotoImage(file="C:/Users/Administrator/Desktop/python练习/黑棋.png")
img_w=PhotoImage(file="C:/Users/Administrator/Desktop/python练习/白棋.png")
game = Eay(root)
game.mainloop()
