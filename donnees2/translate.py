# -*- coding:utf-8 -*-

import struct

def creer_fichier(l,h,nom,type):
	file = open(nom,'w')
	file.write(type + '\n')
	file.write(str(l) + ' ' + str(h) + '\n')
	file.write('255\n')
	file.close()

def creer_image_pgm_binaire():
	for l in range(10):
		cp = 0
		t = []
		binary = open(("data%s" %(l)), 'rb')
		for i in range(784000):
			o = binary.read(1)
			t.append(struct.unpack("B", o)[0])
		binary.close()
		for k in range(1000):
			creer_fichier(28, 28, ("%s_%s.pgm" %(l,k)),'P5')
			file = open(("%s_%s.pgm" %(l,k)),'ab')
			for i in range(28):
				for j in range(28):
					file.write(bytes([255-t[cp]]))
					cp = cp + 1
		file.close()

creer_image_pgm_binaire()