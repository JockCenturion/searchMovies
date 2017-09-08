#Autores: Jock, Daiane e Romeu
#Pyhton: 3.6
#Main Libraries: Pillow, Tkinter


#Importações
from tkinter import *
from PIL import Image, ImageTk
import urllib.request
import json
import io


#Class Buscar Filme
class Search:
	def __init__(self, key):
		link           = "http://www.omdbapi.com/?t="       		        #API omdb
		yourkey        =  key.replace(' ', '+')             		        #Busca pelo filme     
		decode_format  = "utf-8"                            		        #encodings 
		resp           = urllib.request.urlopen(link + yourkey).read() 
		inf_movies     = json.loads(resp.decode(decode_format)) 		#dicionário com as informaçoes do filme

                #Resposta = True (encontrou) | Resposta = False (não encontrou)
		if list(inf_movies.values()).count('False') == 0:
			window2(inf_movies)						#window de Resultados
		else:	
			window3()							#window de Erro
		

#window Principal do Programa 
class window1:
	def __init__(self):
		self.window = Tk()
		
		'''permitir fullscreen
		self.window.title("Search Movies") 
		self.window.attributes ('-fullscreen', True) 
		'''
		
		#Carrega o Background com um canva
		canva1 		= Canvas(self.window, bg="blue", height=0, width=0)
		bg_picture 	= PhotoImage(file="death-note.png")
		bg_label   	= Label(self.window, image=bg_picture, bg="black").place(x=0, y=0, relwidth=1, relheight=1)
		canva1.pack()

		#Titulo
		self.lb_title = Label(self.window, text="Movies Search", font=('Mv Boli','50'), bg="black", fg="white")
		self.lb_title.place(x=395, y=120)

		#Nome do inbox
		self.lb_input1 = Label(self.window, text="Movie Name", font=('Mv Boli','20'), bg="black", fg="white")
		self.lb_input1.place(x=350, y=285)

		self.lb_input2 = Label(self.window, text="Movie Year", font=('Mv Boli', 20), bg="black", fg="white")
		self.lb_input2.place(x=350, y=327)

		#Inbox
		self.ed1 = Entry(self.window, width=40)
		self.ed1.place(x=550, y=300)

		self.ed2 = Entry(self.window, width=40)
		self.ed2.place(x=550, y=340)

		#Botao Search
		self.bt = Button(self.window, width=20, text="SEARCH", command=self.bt_click1)
		self.bt.place(x=595, y=370)

		#Botão Quit - adicionado
		self.btquit = Button(self.window, width=10, text="QUIT", command=self.bt_click2)
		self.btquit.place(x= 630, y=400)
		
		#Mantem a window a espera de eventos
		self.window.geometry("1366x768+0+0")
		self.window.mainloop()

	#Metodo para capturar eventos do botão search
	def bt_click1(self):
                #Captura o input do Nome(ed1)
		busca = str(self.ed1.get()).lower().replace ("ç", "c")                                  #se o campo de ano for deixado vazio mando apenas o 1º campo

		#Captura o input do Ano(ed2)
		if (str(self.ed2.get()).isnumeric()):							#captura a mensagem do inbox ed2 e verifica se é numerico
			busca = str(busca) + "&y=" + str(self.ed2.get())	                        #se for numero será realizado uma concatenação
											        
		self.window.destroy()                                                                   #Destroi a Frame window1
		Search(busca)										#passa para a classe search(lógica da aplicaçao) a key
		
	#Metodo para capturar eventos do botão quit
	def bt_click2(self):
		self.window.destroy()			

#window de Exibição de Resultados		
class window2:
	def __init__(self, inf_movies):

		self.window = Tk()
		self.window.title("Movie")
		
		#Carrega a foto no Background (Criando um canvas)
		canva1 		= Canvas(self.window, bg="blue", height=0, width=0)
		bg_picture 	= PhotoImage(file="bg_cat.png")
		bg_label   	= Label(self.window, image=bg_picture).place(x=0, y=0, relwidth=1, relheight=1)
		canva1.pack()
		
		#Nome do Filme
		lb_text = Label(self.window, text=inf_movies["Title"], font=('Mv Boli','28'), bg="grey", fg="white")
		lb_text.pack()

		#Verifica se há Poster (Capa)
		if "N/A" not in inf_movies["Poster"]:
			image_url = inf_movies["Poster"]
		else:
			image_url = "https://goo.gl/gkZpZ1" 
		
		#Carrega o Poster
		my_page     = urllib.request.urlopen(image_url)
		my_picture  = io.BytesIO(my_page.read())
		pil_img     = Image.open(my_picture)
		tk_img 	    = ImageTk.PhotoImage(pil_img)
		label 	    = Label(self.window, image=tk_img, bg="grey").place(x=50, y=160) 
		
		#informaçoes do Filme
		canva2 = Canvas(self.window, width=600, height=550, bd=5, bg="grey")
		canva2.place(x=360, y=160)
		count = 0	
		for item in inf_movies:
			if (str(item) != "Poster" and str(item) != "Ratings" and str(item) != "Response" and str(item) != "Title" and str(item) != "Plot"):
				texto = (str(item) + "    " + str(inf_movies[item]))
				canva2.create_text(20, 20 + count, text=texto, font=('Arial','10','bold'), anchor=SW, fill='white')
				count += 27														
		 
		#Informaçoes do Poster ou Sinopse
		lb_poster1 = Label(self.window, text="POSTER", bg="grey", fg="white", font=('Arial','10','bold')).place(x=51, y = 610)
		lb_poster2 = Label(self.window, text=inf_movies["Plot"], wraplength=300, bg="grey", fg="white", font=('Arial','10','bold')).place(x=51, y = 635)

		#Botão Quit 
		self.btquit = Button(self.window, width=20, text="QUIT", command=self.bt_click2).pack (side = BOTTOM, anchor=SE)
		
		#Botao de voltar
		bt = Button(self.window, width=20, text="BACK", command=self.bt_click1).pack(side=RIGHT, anchor=SE)
		self.window.geometry("1366x768+0+0")
		self.window.mainloop()
		
	#Metodo para capturar eventos do botão voltar
	def bt_click1(self):
		self.window.destroy()
		window1()
		
	#Metodo para capturar eventos do botão quit
	def bt_click2(self):
		self.window.destroy()

#window ERROr
class window3:
	def __init__(self):

		self.window = Tk()
		self.window.title("Not Found")
		
		##Carrega a foto no Background (Criando um canvas)
		canva1 		= Canvas(self.window, bg="blue", height=0, width=0)
		bg_picture 	= PhotoImage(file="not_found.png")
		bg_label   	= Label(self.window, image=bg_picture, bg="white").place(x=0, y=0, relwidth=1, relheight=1)
		canva1.pack()

		self.lb = Label(self.window, text="Movie Not Found!", font=('Mv Boli','30'), bg="white")
		self.lb.pack()

		#Botão Quit 
		self.btquit = Button(self.window, width=20, text="QUIT", command=self.bt_click2).pack (side = BOTTOM, anchor=SE)
		
		#Botão de voltar
		bt = Button(self.window, width=20, text="BACK", command=self.bt_click1).pack(side=RIGHT, anchor=SE)

		self.window.geometry("1366x768+0+0")
		self.window.mainloop()

	#Metodo para capturar eventos do botão voltar
	def bt_click1(self):
		self.window.destroy()
		window1()
		
	#Metodo para capturar eventos do botão quit
	def bt_click2(self):
		self.window.destroy()

#Classe Principal do Programa
window1()


