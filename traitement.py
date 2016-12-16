#!/usr/bin/env python

from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL.ImageTk import * 
from PIL.Image import *
from tkinter.messagebox import *

def augmenter_contraste(img): #Augmente le contraste min 1 max 255
	min = 255
	max = 0
	(l,h) = img.size
	for i in range(l):
		for j in range(h):
			c = Image.getpixel(img, (i,j))
			if(min > c):
				min = c
			if(max < c):
				max = c
	for i in range(l):
		for j in range(h):
			c = Image.getpixel(img, (i,j))
			Image.putpixel(img, (i,j), 255/(max-min+1)*(c-min))
	return img

def decouper(img): #Decouper l'image pour avoir marge similaire
	(l,h) = img.size
	horizontale = []
	verticale = []
	for i in range(l):
		for j in range(h):
			if(Image.getpixel(img, (i,j)) < 170):
				horizontale.append(i)
	for i in range(h):
		for j in range(l):
			if(Image.getpixel(img, (j,i)) < 170):
				verticale.append(i)
	img = img.crop((horizontale[0]-6, verticale[0]-6, horizontale[-1]+6, verticale[-1]+6))
	return img

def normalisation(img, n): #Normalisation
	img = img.convert("L")
	augmenter_contraste(img)
	img = decouper(img)
	if(n):
		img = img.resize((28, 28), ANTIALIAS)
		augmenter_contraste(img)
	return img

def zoom(img, n): #Zoom/Dezoom de l'image
	x,y = img.size
	if(n):
		x = 2*x
		y = 2*y
	else:
		x = x//2
		y = y//2
	img = img.resize((x,y), ANTIALIAS)
	return img

def rotation(img, n): #Rotation image
	x,y = img.size
	if(n):
		angle = 90
	else:
		angle = -90
	img = img.rotate(angle)
	return img