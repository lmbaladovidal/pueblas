#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gtk,os
import sqlite3 as bdapi

class question():

	def cargar_lista(self,self_altas):
		self_altas.liststore_marca.clear()
		ruta = os.getcwd()
		bbdd = bdapi.connect(ruta+'/Base_Datos/bd_marcas.db')
		cursor=bbdd.cursor()
		cursor.execute("SELECT * FROM marca")
		for tupla in cursor.fetchall():
			self_altas.liststore_marca.append([tupla[1]])
		cursor.close()
		bbdd.close()

	def aceptar_with_enter(self,widget,event,self_altas,self_padre):
		if event.keyval ==gtk.keysyms.Return:
			self.cargar_again(None,self_altas)
		if event.keyval ==gtk.keysyms.Escape:
			self_altas.window.destroy()
			self_padre.window.set_sensitive(True)

	def cargar_again(self,widget,self_altas):
		self_altas.entry_codigo.set_text("")
		self_altas.entry_descripcion.set_text("")
		self_altas.entry_marca.set_text("")
		self_altas.entry_costo.set_text("")
		self_altas.entry_codigo.set_property("secondary-icon-stock",None)
		self_altas.entry_descripcion.set_property("secondary-icon-stock",None)
		self_altas.entry_marca.set_property("secondary-icon-stock",None)
		self_altas.entry_costo.set_property("secondary-icon-stock",None)
		self_altas.window.set_sensitive(True)
		self_altas.entry_codigo.set_property("is-focus",1)
		self.window.destroy()
		self.cargar_lista(self_altas)

	def cerrar(self,widget,window_altas,window_padre):
		self.window.destroy()
		window_altas.destroy()
		window_padre.set_sensitive(True)

	def __init__(self,self_altas,self_padre):
		self_altas.window.set_sensitive(False)
		self.archivo="./altas/question.glade"
		self.glade=gtk.Builder()
		self.glade.add_from_file(self.archivo)


		self.window=self.glade.get_object("dialog1")
		self.button_aceptar=self.glade.get_object("button_aceptar")
		self.button_cerrar=self.glade.get_object("button_cerrar")

		self.button_aceptar.connect("clicked",self.cargar_again,self_altas)
		self.button_cerrar.connect("clicked",self.cerrar,self_altas.window,self_padre.window)

		self.window.connect("key-press-event",self.aceptar_with_enter,self_altas,self_padre)
