#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3 as bdapi
import gtk,os,time

class cierre():
	
	def guardar_db(self,widget,window):
		nombre = self.entry_nombre.get_text()
		ruta = os.getcwd()
		bbdd=bdapi.connect(ruta+'/Base_Datos/bd_caja.db')
		cursor=bbdd.cursor()
		cursor.execute("INSERT INTO bd_caja (cajera,fecha,venta_bruta,ganancia) VALUES (?,?,?,?)",(nombre,self.fecha,self.total_b,self.total_n))
		bbdd.commit()
		cursor.close()
		bbdd.close()
		resumen = open("./control/resumen.txt","w")
		resumen.close()
		self.cerrar(None,window)
		
		
	def fecha_act(self):
		fecha = time.ctime()
		lista = []
		palabra = ""
		for x in range(len(fecha)):
			if fecha[x] != " ":
				palabra +=fecha[x]
			else:
				lista.append(palabra)
				palabra = ""
		lista.append(palabra)
		print lista
		self.fecha = lista[0]+' '+lista[2]+' '+lista[1]+' '+lista[4]+' '+lista[3]
		
	def convertir_linea_a_dato(self,linea):
		cadena = []
		i = 0
		elementos =0
		elemento = ""
		while elementos < 3:
			while linea[i] != "," and linea[i] != "\n":
				elemento += linea[i]
				i += 1
			cadena.append(elemento)
			elemento = ""
			elementos +=1
			i += 1
		return cadena
	
	def escribir_treeview(self):
		resumen = open("./control/resumen.txt","r+")
		archivo = resumen.readlines()
		for linea in archivo:
			cadena = self.convertir_linea_a_dato(linea)
			self.liststore.append([float(cadena[0]),float(cadena[1]),int(cadena[2])])
			self.total_b += float(cadena[1])*float(cadena[2])
		resumen.close()
		
		
	def completar_entrys(self):
		self.total_n =self.total_b/1.8
		self.entry_ganancia_b.set_text(str(self.total_b))
		self.entry_ganancia_n.set_text(str(self.total_n))
		self.entry_fecha.set_text(self.fecha)
		
	def delete_event(self,widget,event,window):
		window.set_sensitive(True)
		self.window.destroy()

	def cerrar(self,widget,window):
		window.set_sensitive(True)
		self.window.destroy()
		
	def __init__ (self,self_padre):
		self_padre.window.set_sensitive(False)
		self.total_b = 0
		self.total_n = 0
		self.archivo_glade = "./control/ventana_cierre.glade"
		self.glade = gtk.Builder()
		self.glade.add_from_file(self.archivo_glade)
		self.window = self.glade.get_object("window_cierre")
		self.treeview = self.glade.get_object("treeview")
		self.liststore = self.glade.get_object("liststore")
		self.entry_nombre = self.glade.get_object("entry_nombre")
		self.entry_fecha = self.glade.get_object("entry_fecha")
		self.entry_ganancia_b = self.glade.get_object("entry_ganancia_b")
		self.entry_ganancia_n = self.glade.get_object("entry_ganancia_n")
		self.btn_ok = self.glade.get_object("button_ok")
		self.btn_quit = self.glade.get_object("button_quit")
		self.window.connect("delete-event",self.delete_event,self_padre.window)
		self.btn_ok.connect("clicked",self.guardar_db,self_padre.window)
		self.btn_quit.connect("clicked",self.cerrar,self_padre.window)
		self.escribir_treeview()
		self.fecha_act()
		self.completar_entrys()
		

