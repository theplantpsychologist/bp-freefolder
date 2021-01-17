import random
import math
from tkinter import *
import tkinter.filedialog
from tkinter.filedialog import askopenfile
from tkinter.ttk import *
import pathlib
from intersections import *
import numpy as np
import sys

root = Tk()
canvas1 = Canvas(root,width = 800, height = 600)
canvas1.pack()

class Vertex():
    def __init__(self,x,y):
        self.x = x
        self.y = y

class Crease():
    def __init__(self,x1,y1,x2,y2,mv,angle):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.mv = mv #store as 1 2 or 3, for the cp file.
        if self.mv == 1:
            self.color = 'black'
        if self.mv == 2:
            self.color = 'red'
        if self.mv == 3:
            self.color = 'blue'
        self.length = ((self.x1-self.x2)**2+(self.y1-self.y2)**2)**0.5
        '''try:
            self.angle = math.degrees(math.atan((self.y1-self.y2)/(self.x1-self.x2)))
        except:
            self.angle = 90'''
        self.angle = angle
tkx = lambda x: x*500 + 50
tky = lambda y: 550 - y*500
cpx = lambda x: x*400 - 200
cpy = lambda y: y*-400 + 200

gridsize = 12
#hardcoded for now


creases = []
edge_vertices = []
cpfile = []
#canvas1.create_rectangle(tkx(0),tky(0),tkx(1),tky(1),outline='black',width = 3)

def drawgrid():
    for l in range(0,gridsize):
        canvas1.create_line(tkx(0),tky(l/gridsize),tkx(1),tky(l/gridsize),fill = 'light grey')
        canvas1.create_line(tkx(l/gridsize),tky(0),tkx(l/gridsize),tky(1),fill='light grey')

def start():
    canvas1.delete('all')
    #canvas1.create_rectangle(tkx(0),tky(0),tkx(1),tky(1),outline='black',width = 3)
    global creases,vertices,cpfile
    creases = [Crease(0,0,1,0,1,0),
               Crease(1,0,1,1,1,90),
               Crease(1,1,0,1,1,180),
               Crease(0,1,0,0,1,270)]
    cpfile = []
    vertices = [(0,0),(0,1),(1,1),(1,0)]
    draw_creases(creases)

def generate_crease():
    angle = 0
    mv = random.randint(2,3)
    v1 = Vertex(0,0) #just put it here by default
    v1.edge = random.randint(1,4) #side numbers go counter clockwise, with 1 at the 3 o clock position
    def edge_assignment(v):
        if v.edge == 1:
            v.x = 1
            v.y = random.randint(1,gridsize-1)/gridsize
            angle = random.randint(3,5)*math.pi/4
        if v.edge == 2:
            v.y = 1
            v.x = random.randint(1,gridsize-1)/gridsize
            angle = random.randint(5,7)*math.pi/4
        if v.edge == 3:
            v.x = 0
            v.y = random.randint(1,gridsize-1)/gridsize
            angle = random.randint(-1,1)*math.pi/4  #probably should convert these to degrees
        if v.edge == 4:
            v.y = 0
            v.x = random.randint(1,gridsize-1)/gridsize
            angle = random.randint(1,3)*math.pi/4 
        return math.degrees(angle)
    angle = edge_assignment(v1)
    #print(v1.x,v1.y,angle)
    fold(v1.x,v1.y,angle,mv)        


def fold(vx,vy,angle,mv):   
    intersections = []
    intersection_distances = []
    other_storage = []
    for c in creases:
        intersection = intersect(c.x1,c.y1,c.angle,vx,vy,angle)
        try:
            if intersection == None:
                continue
        except:
            "all good"
        if eq(intersection[0],vx) and eq(intersection[1],vy):# and (eq(vx,0) or eq(vx,1) or eq(vy,0) or eq(vy,1)): #this is our starting edge
            starting_edge = c
            continue
        if between(0,1,intersection[0]) and between(0,1,intersection[1]) and between(c.x1,c.x2,intersection[0]) and between(c.y1,c.y2,intersection[1]):
            #if the intersection is within the square or pretty close
            "gonna have to store all the intersections and see which is the closest to v, then intersection becomes the new v"
            intersections.append(intersection)
            intersection_distances.append(((intersection[0]-vx)**2+(intersection[1]-vy)**2)**0.5)
            if eq(intersection[0],0) or eq(intersection[1],0) or eq(intersection[0],1) or eq(intersection[1],1):
                other_storage.append([True, c.angle,c.x1,c.y1,c.x2,c.y2,c.mv,creases.index(c)]) #def a better way but i'm lazy
                hitedge = True
                other_angle = c.angle
            else:
                other_storage.append([False, c.angle,c.x1,c.y1,c.x2,c.y2,c.mv,creases.index(c)])
                #other_storage will store relevant data for all the possible vertices.
                #local_vertex_number will tell us which list in the other_storage are we gonna look at
    try:
        local_vertex_number = intersection_distances.index(min(intersection_distances)) #find the closest one and store the data about it
    except:
        print(vx,vy,angle,mv,"no intersections found")
    intersection = intersections[local_vertex_number]

    stuff = other_storage[local_vertex_number]
    hitedge = stuff[0]
    other_angle = stuff[1]
    
    canvas1.create_rectangle(tkx(intersection[0])-2,tky(intersection[1])-2,tkx(intersection[0])+2,tky(intersection[1])+2,fill = 'red')
    vertices.append(intersection)
    vertices.append((vx,vy))
    creases.append(Crease(vx,vy,intersection[0],intersection[1],mv,angle))

    del(creases[stuff[-1]])
    creases.append(Crease(intersection[0],intersection[1],stuff[4],stuff[5],stuff[6],stuff[1]))
    creases.append(Crease(stuff[2],stuff[3],intersection[0],intersection[1],stuff[6],stuff[1]))
    try:
        if not(eq(vx,starting_edge.x1) and eq(vy,starting_edge.y1)) and not (eq(vx,starting_edge.x2) and eq(vy,starting_edge.y2)):
            creases.append(Crease(vx,vy,starting_edge.x2,starting_edge.y2,starting_edge.mv,starting_edge.angle))
            creases.append(Crease(starting_edge.x1,starting_edge.y1,vx,vy,starting_edge.mv,starting_edge.angle))
            del(creases[creases.index(starting_edge)])
    except:
        "it's probably fine i think..."
    draw_creases(creases)

    stuff = (hitedge,intersection,other_angle,angle,mv) #stuff to tell if it should repeat or not, and if so from where

    if not stuff[0]:
        if mv == 2:
            mv = 3
        elif mv == 3:
            mv = 2
        angle = 180 - stuff[3] + 2*stuff[2]
        vx = stuff[1][0]
        vy = stuff[1][1]
        fold(vx,vy,angle,mv)


   
def draw_creases(creases):
    canvas1.delete('all')
    drawgrid()
    for c in creases:
        canvas1.create_line(tkx(c.x1),tky(c.y1),tkx(c.x2),tky(c.y2),fill = c.color)
        #cpfile.append(str(c.mv)+' '+str(cpx(c.x1))+' '+str(cpy(c.y1))+' '+str(cpx(c.x2))+' '+str(cpy(c.y2)))
    for v in vertices:
        canvas1.create_rectangle(tkx(v[0])-1,tky(v[1])-1,tkx(v[0])+1,tky(v[1])+1,fill = 'black')








'''        
def draw_edges(vertices,cpfile):
    edge1 = []
    edge2 = []
    edge3 = []
    edge4 = []
    for v in vertices:
        if v[0] == 1:
            edge1.append(v)
        if v[1] == 1:
            edge2.append(v)
        if v[0] == 0:
            edge3.append(v)
        if v[1] == 0:
            edge4.append(v)
    def draw_one_edge(edge,cpfile):
        edge.sort()
        for e in range(0,len(edge)-1):
            try:
                cpfile.append("1 "+str(cpx(edge[e][0]))+' '+str(cpy(edge[e][1]))+' '+str(cpx(edge[e+1][0]))+' '+str(cpy(edge[e+1][1]))+' ')
            except:
                cpfile.append("1 "+str(cpx(edge[e][0]))+' '+str(cpy(edge[e][1]))+' '+str(cpx(edge[0][0]))+' '+str(cpy(edge[0][1]))+' ')
    draw_one_edge(edge1,cpfile)
    draw_one_edge(edge2,cpfile)
    draw_one_edge(edge3,cpfile)
    draw_one_edge(edge4,cpfile)'''

boi = Tk()
boi.withdraw()
def file_save():
    cpfile = []
    for c in creases:
        cpfile.append(str(c.mv)+' '+str(cpx(c.x1))+' '+str(cpy(c.y1))+' '+str(cpx(c.x2))+' '+str(cpy(c.y2)))
    filename = tkinter.filedialog.asksaveasfile(mode='w+', defaultextension=".cp",parent = boi)
    if filename is None: # asksaveasfile return `None` if dialog closed with "cancel".
        boi.withdraw()
        return
    for x in range(0,len(cpfile)):
        #print(cp_file[x])
        filename.write(str(cpfile[x])+"\n")
        
    filename.close()
    boi.withdraw()
enter = Button(root,text ='Restart',command = start)
enter.place(x=600,y=100)
enter = Button(root,text ='Generate another fold',command = generate_crease)
enter.place(x=600,y=200)
enter = Button(root,text ='Export cp file',command = file_save)
enter.place(x=600,y=300)


start()
    
def draw_many_creases(number):
    for x in range(0,number):
        generate_crease()


'''
algorithm 1
add on creases, starting from a random position along the edge and at a random angle.
if the crease bumps into another crease, it reflects angle and switches mv (will have
to break the other crease as well)
problem: will only get a limited kind of vertex


algorithm 2
start with a vertex located in a random point in the square, extend a random even
number of creases out such that the flat foldability rules are satisfied.
then pick one of those creases to build the next vertex on, and watch out for
intersections between the creases of the vertices


Idea: make an origami python module, which would include crease intersection stuff,
storing as a cp file function, as well as crease and vertex classes
'''
