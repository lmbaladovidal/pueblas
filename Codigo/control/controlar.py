#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3 as bdapi
import gtk,os

class control():

	def buscar(self,widget):
		contenido = self.entry_filtro.get_text()
		filtro = self.combobox_filtro.get_active_text()
		ruta = os.getcwd()
		self.liststore.clear()
		bbdd=bdapi.connect(ruta+'/Base_Datos/bd_stock.db')
		cursor=bbdd.cursor()
		if contenido != "":
			cursor.execute("SELECT * FROM bd_stock WHERE "+filtro.lower()+" LIKE '"+contenido+"%'")
			tupla_resultado = cursor.fetchall()
			if tupla_resultado != []:
				for tupla in tupla_resultado:
					self.liststore.append([int(tupla[1]),tupla[2],tupla[3],tupla[5],tupla[6],tupla[7],tupla[8]])
		else:
			cursor.execute("SELECT * FROM bd_stock")
			tupla_resultado = cursor.fetchall()
			if tupla_resultado != []:
				for tupla in tupla_resultado:
					self.liststore.append([int(tupla[1]),tupla[2],tupla[3],tupla[4],tupla[5],tupla[6],tupla[7]])

	def desbloquear_entry(self,widget):
		self.entry_filtro.set_sensitive(True)

	def focusear_cantidad(self,widget):
		self.tupla = []
		for x in range(6):
			self.tupla.append(self.liststore[0][x])
		self.entry_descripcion.set_text(self.tupla[1])
		self.entry_cantidad.set_property("is-focus",1)

	def restar_cantidad(self,widget):
		ruta = os.getcwd()
		self.tupla[4]= self.tupla[4]-int(self.entry_cantidad.get_text())
		if self.tupla[5] >= self.tupla[4]:
			self.tupla.append(True)
		else:
			self.tupla.append(False)
		bbdd=bdapi.connect(ruta+'/Base_Datos/bd_stock.db')
		cursor=bbdd.cursor()
		cursor.execute("UPDATE bd_stock SET stk_disp = ?, aviso = ? WHERE codigo = ?",(self.tupla[4],self.tupla[6],self.tupla[0]))
		self.tupla = []
		bbdd.commit()
		cursor.close()
		bbdd.close()
		self.liststore.clear()
		self.entry_filtro.set_text("")
		self.entry_descripcion.set_text("")
		self.entry_cantidad.set_text("")

	def delete_event(self,widget,event,self_padre):
		self.window.destroy()

	def cerrar(self,widget,self_padre):
		self.window.destroy()

	def __init__(self,self_padre):
		self.tupla = []
		self.archivo_glade = "./control/ventana_control.glade"
		self.glade = gtk.Builder()
		self.glade.add_from_file(self.archivo_glade)
		self.window = self.glade.get_object("window_control")
		self.button_cerrar = self.glade.get_object("button_cerrar")
		self.table = self.glade.get_object("table1")
		self.liststore = self.glade.get_object("liststore_control")
		self.entry_filtro = self.glade.get_object("entry_filtro")
		self.entry_descripcion = self.glade.get_object("entry_descripcion")
		self.entry_cantidad = self.glade.get_object("entry_cantidad")
		self.combobox_filtro = gtk.combo_box_new_text()
		self.table.attach(self.combobox_filtro,1,2,0,1)
		self.combobox_filtro.append_text("Codigo")
		self.combobox_filtro.append_text("Nro Art")
		self.combobox_filtro.append_text("Marca")
		self.combobox_filtro.connect("changed",self.desbloquear_entry)
		self.entry_filtro.connect("changed",self.buscar)
		self.entry_filtro.connect("activate",self.focusear_cantidad)
		self.entry_cantidad.connect("activate",self.restar_cantidad)
		self.window.connect("delete_event",self.delete_event,self_padre)
		self.button_cerrar.connect("clicked",self.cerrar,self_padre)
		self.combobox_filtro.show()
