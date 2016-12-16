#!/usr/bin/env python

import struct

def creation():
	return open("data.txt", "w")

def ecriture(fichier, t):
	fichier = open("data.txt", "a")
	for i in range(56):
		fichier.write(str(t[i]))
		fichier.write("\n")
	fichier.close()

def dataExist(fichier):
	try:
		open(fichier, "r")
	except:
		return False
	return True

def lecture(i):
	fichier = open("data.txt", "r")
	t = []
	debut = i*56
	for i in range(debut,debut+56):
		t.append(int(fichier.readline()))
	return t


