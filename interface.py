#!/usr/bin/env python

from tkinter import *
from PIL import Image
from PIL import ImageTk
from tkinter.filedialog import *
from tkinter.messagebox import *

from reconnaissance import *
from traitement import *

fenetre = Tk()
fenetre.title("Fenetre principale")
canvas_selection = Canvas(fenetre)
image = None

# < FONCTIONS D'AFFICHAGES
def placementFen(fen): #Place la fenetre principale au centre de l'ecran
	l, h = fen.winfo_screenwidth(), fen.winfo_screenheight()
	x, y = (l//2-150) , (h//2-150)
	fen.geometry("%dx%d%+d%+d" % (300,300,x,y))
placementFen(fenetre)

def fermer(): #Ferme le programme
	global image
	image.destroy()

def ouvrir(): #Ouverture de la fenetre de l'image importee et ouverture de l'image depuis fichier
	global img_tk, image, canvas, img_pil, rect
	if(image != None):
		image.destroy()
	image = Toplevel()
	image.title("image importée")
	filepath = askopenfilename(title="Ouvrir une image",filetypes=[('jpg files','.jpg'),('all files','.*')])
	img_pil = open(filepath)
	img_tk = ImageTk.PhotoImage(img_pil)
	canvas = Canvas(image, width=img_tk.width(), height=img_tk.height(), cursor="cross")
	canvas.create_image(0, 0, anchor=NW, image=img_tk)
	rect = None
	canvas.pack()
	canvas.bind("<ButtonPress-1>", debut)
	canvas.bind("<ButtonRelease-1>", fin)
	canvas.bind("<Button-4>", resizeM)
	canvas.bind("<Button-5>", resizeP)

def rectangle(): #Creer le rectangle de selction image
	global x1, y1, x2, y2, canvas, img_pil, img_select_tk, img_select_pil, canvas_selection, rect
	if(rect != None):
		canvas.delete(rect)
	rect = canvas.create_rectangle(x1,y1,x2,y2)
	if(x1 < x2):
		afficher(img_pil.crop((x1,y1,x2,y2)))
	else:
		afficher(img_pil.crop((x2,y2,x1,y1)))

def afficher(img): #Affiche l'image sélectionné
	global img_select_tk, canvas_selection, img_select_pil
	img_select_pil = img
	img_select_tk = ImageTk.PhotoImage(img)
	canvas_selection.delete(ALL)
	x,y = img_select_pil.size
	if(x < 300 or y < 300):
		if(x < 300 and y > 300):
			canvas_selection.configure(height=y, width=300)
			canvas_selection.create_image(150, y//2, anchor=CENTER, image=img_select_tk)
		if(y < 300 and x > 300):
			canvas_selection.configure(height=300, width=x)
			canvas_selection.create_image(x//2, 150, anchor=CENTER, image=img_select_tk)
		else:
			canvas_selection.configure(height=y, width=x)
			canvas_selection.create_image(x//2, y//2, anchor=CENTER, image=img_select_tk)
	else:
		canvas_selection.configure(height=y, width=x)
		canvas_selection.create_image(0, 0, anchor=NW, image=img_select_tk)
	canvas_selection.pack(expand=Y)
# >

# < FONCTIONS BIND
def resizeP(event):
	global img_tk, img_pil, canvas
	x,y = img_pil.size
	img_pil = img_pil.resize((x+x//10,y+y//10), ANTIALIAS)
	img_tk = ImageTk.PhotoImage(img_pil)
	canvas.create_image(0, 0, anchor=NW, image=img_tk)
	canvas.configure(height=img_tk.height(), width=img_tk.width())

def resizeM(event):
	global img_tk, img_pil, canvas
	x,y = img_pil.size
	img_pil = img_pil.resize((x-x//10,y-y//10), ANTIALIAS)
	img_tk = ImageTk.PhotoImage(img_pil)
	canvas.create_image(0, 0, anchor=NW, image=img_tk)
	canvas.configure(height=img_tk.height(), width=img_tk.width())

def debut(event):
	global x1, y1
	x1, y1 = (event.x, event.y)

def fin(event): 
	global x2, y2
	x2, y2 = (event.x, event.y)
	rectangle()
# >

# < CALLBACK BAR MENU
def callNormalisation(n): #Lance la normalisation
	global img_select_tk, img_select_pil, canvas_selection
	imageSelect()
	afficher(normalisation(img_select_pil, n))

def callZoom(n): #Lance le zoom ou dezoom de l'image sélectionné
	global img_select_tk,img_select_pil, canvas_selection
	imageSelect()
	afficher(zoom(img_select_pil, n))

def callRotation(n): #Lance la rotation de l'image sélectionné
	global img_select_tk,img_select_pil, canvas_selection
	imageSelect()
	afficher(rotation(img_select_pil, n))

def callAlgo1(): #Lance l'algo 1 (sans zoning)
	global img_select_pil
	imageSelect()
	print(plusProcheExemple(img_select_pil))

def callAlgo2(): #Lance l'algo 2 (zoning)
	global img_select_pil
	imageSelect()
	print(plusProcheExemple2(img_select_pil))

def imageSelect():
	try:
		img_select_pil
	except:
		showerror("Erreur", "Aucune image sélectionnée")
# >

# < PARAMETRE BAR MENU
menubar = Menu(fenetre)

menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label="Ouvrir", command=ouvrir)
menu1.add_command(label="Fermer", command=fermer)
menu1.add_separator()
menu1.add_command(label="Quitter", command=fenetre.quit)
menubar.add_cascade(label="Fichier", menu=menu1)

# lambda permet d'utiliser les paramètres des fonctions 

menu2 = Menu(menubar, tearoff=0)
menu2.add_command(label="Zoom +", command=lambda:callZoom(True)) 
menu2.add_command(label="Zoom -", command=lambda:callZoom(False))
menu2.add_separator()
menu2.add_command(label="Rotation droite", command=lambda:callRotation(True))
menu2.add_command(label="Rotation gauche", command=lambda:callRotation(False))
menu2.add_separator()
menu2.add_command(label="Normaliser + taille", command=lambda:callNormalisation(True))
menu2.add_command(label="Normaliser", command=lambda:callNormalisation(False))
menubar.add_cascade(label="Modifier", menu=menu2)

menu3 = Menu(menubar, tearoff=0)
menu3.add_command(label="Algorithme 1", command=callAlgo1)
menu3.add_command(label="Algorithme 2", command=callAlgo2)
menubar.add_cascade(label="Trouver", menu=menu3)
# >

#configure la fenetre avec une taille 500x300
fenetre.config(menu=menubar, width=500, height=300)

#affiche la fenetre en boucle
fenetre.mainloop()