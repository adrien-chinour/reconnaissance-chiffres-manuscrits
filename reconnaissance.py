#!/usr/bin/env python

from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL.ImageTk import *
from PIL.Image import *
from tkinter.messagebox import *

def carreDistanceEuclidienne(t1,t2): #Calcul carre distance euclidienne
	s = 0
	for i in range(len(t1)):
		s = s + pow((t1[i] - t2[i]),2)
	return s

def profilHorizontal(image): #Profil Horizontal
	t = []
	(l,h) = image.size
	for i in range(h):
		t.append(0)
		for j in range(l):
			c = Image.getpixel(image, (j,i))
			t[i] = t[i] + c
	return t

def profilVertical(image): #Profil Vertical
	t = []
	(l,h) = image.size
	for i in range(l):
		t.append(0)
		for j in range(h):
			c = Image.getpixel(image, (i,j))
			t[i] = t[i] + c
	return t

def calculerCaracteristiques(image): #Calcul caracteristique : concatenation profils vertical/horizontal
	t1 = profilVertical(image)
	t2 = profilHorizontal(image)
	return t1+t2

def donnees(): #Calcul caracteristique des images pour algo sans zonning
	M = [[[0 for i in range(10)] for j in range(1000)] for k in range(56)]
	for i in range(10):
		for j in range (1000):
			tmpFichierImage = ("%s_%s.pgm" %(i,j))
			donneesImage = open("donnees2/%s" %(tmpFichierImage))
			M[i][j] = calculerCaracteristiques(donneesImage)
	return M

def donneesZoning(): #Calcul caracteristique des images pour algo avec zonning
	M = [[[0 for i in range(10)] for j in range(1000)] for k in range(49)] 
	for i in range(10):
		for j in range (1000):
			tmpFichierImage = ("%s_%s.pgm" %(i,j))
			donneesImage = open("donnees2/%s" %(tmpFichierImage))
			M[i][j-1] = zoning(donneesImage)
	return M

def plusProcheExemple(img): #Cherche la caracterisique la plus proche pour algo sans zonning
	x,y = img.size
	if (x > 28 or y > 28 ):
		showerror("Erreur", "Image non normalisée")
		return None
	t = calculerCaracteristiques(img)
	M = donnees()
	correspondance = carreDistanceEuclidienne(t,M[0][0])
	for i in range(10):
		for j in range(1000):
			if (carreDistanceEuclidienne(t,M[i][j]) < correspondance):
				correspondance = carreDistanceEuclidienne(t,M[i][j])
				meilleurCorrespondance = (i,j)
	i, j = meilleurCorrespondance
	showinfo("Meilleur corespondance", ("%s_%s.pgm" %(i,j)))
	if askyesno('Meilleur corespondance', 'Voulez-vous ouvrir l\'image ?'):
		img = open("donnees2/%s_%s.pgm" %(i,j))
		img.show()
	return ("%s_%s.pgm" %(i,j))

def zoning(img): #Creer les zones d'image pour algo de zonning
	l,h = img.size
	v = []
	p = l//6
	for i in range(6):
		for j in range(4):
			t = []
			m = 0
			for k in range(i*p,i*p+p):
				for l in range(j*p,j*p+p):
					t.append(Image.getpixel(img, (k,l)))
			for h in range(len(t)):
				m = m + t[h]
			v = v + [m//len(t)]
	return v

def plusProcheExemple2(img): #Cherche la caracterisque la plus proche pour algo avec zonning
	x,y = img.size
	t = zoning(img)
	M = donneesZoning()
	correspondance = carreDistanceEuclidienne(t,M[0][0])
	for i in range(10):
		for j in range(1000):
			if (carreDistanceEuclidienne(t,M[i][j]) < correspondance):
				correspondance = carreDistanceEuclidienne(t,M[i][j])
				meilleurCorrespondance = (i,j)
	i, j = meilleurCorrespondance
	showinfo("Meilleur corespondance", ("%s_%s.pgm" %(i,j)))
	if askyesno('Meilleur corespondance', 'Voulez-vous ouvrir l\'image ?'):
		img = open("donnees2/%s_%s.pgm" %(i,j))
		img.show()
	return ("%s_%s.pgm" %(i,j))