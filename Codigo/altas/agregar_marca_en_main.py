#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gtk,os

from validaciones.validacion import caracteres_validos
from validaciones.validacion import es_float
from altas.question import question

import sqlite3 as bdapi

class nueva_marca:

	def add_marca(self,widget,self_padre):
		descripcion=self.entry_descripcion.get_text()
		marca=self.entry_marca.get_text()
		ganancia=float(self.entry_ganancia.get_text() )
		ruta = os.getcwd()
		bbdd=bdapi.connect(ruta+'/Base_Datos/bd_marcas.db')
		cursor=bbdd.cursor()
		cursor.execute(" INSERT INTO marca (nombre,descripcion,coeficiente) VALUES(?,?,?)",(marca,descripcion,ganancia ) )
		bbdd.commit()
		cursor.close()
		bbdd.close()
		self_padre.window.set_sensitive(True)
		self.window.destroy()

	def controlar_marca(self,marca):
		ruta = os.getcwd()
		bbdd=bdapi.connect(ruta+'/Base_Datos/bd_marcas.db')
		cursor=bbdd.cursor()
		cursor.execute("SELECT nombre FROM marca WHERE nombre =?",(marca,))
		tupla = cursor.fetchone()
		print tupla
		if tupla == None:
			return True
		else:
			return False
		cursor.close()
		bbdd.close()

	def aceptar_with_enter(self,widget,event,self_padre):
		if event.keyval ==gtk.keysyms.Return:
			self.add_marca(None,self_padre)

	def validar_descripcion(self,widget):
		self.descripcion_ok=False
		descripcion=self.entry_descripcion.get_text()
		if caracteres_validos(descripcion) and descripcion != "":
			self.entry_descripcion.set_icon_from_stock(1,gtk.STOCK_APPLY)
			self.descripcion_ok=True
		else:
			self.entry_descripcion.set_icon_from_stock(1,gtk.STOCK_DIALOG_ERROR)

	def validar_marca(self,widget):
		self.marca_ok=False
		marca=self.entry_marca.get_text()
		if caracteres_validos(marca) and marca != "":
			if self.controlar_marca(marca):
				self.entry_marca.set_icon_from_stock(1,gtk.STOCK_APPLY)
				self.marca_ok=True
			else:
				self.entry_marca.set_icon_from_stock(1,gtk.STOCK_DIALOG_ERROR)
		else:
			self.entry_marca.set_icon_from_stock(1,gtk.STOCK_DIALOG_ERROR)

	def validar_ganancia(self,widget):
		self.ganancia_ok=False
		ganancia=self.entry_ganancia.get_text()
		if es_float(ganancia):
			self.entry_ganancia.set_icon_from_stock(1,gtk.STOCK_APPLY)
			self.ganancia_ok=True
		else:
			self.entry_ganancia.set_icon_from_stock(1,gtk.STOCK_DIALOG_ERROR)
		if ganancia == "":
		 self.entry_ganancia.set_property("secondary-icon-stock",None)

	def desbloquear_aceptar(self,widget):
		self.btn_ok.set_sensitive(False)
		if self.marca_ok and self.descripcion_ok and self.ganancia_ok:
			self.btn_ok.set_sensitive(True)

	def cancelar(self,widget,self_padre):
		self_padre.window.set_sensitive(True)
		self.window.destroy()

	def delete_event(self,widget,event,self_padre):
		self_padre.window.set_sensitive(True)
		self.window.destroy()

	def __init__(self,self_padre):
		self_padre.window.set_sensitive(False)
		self.archivo="./altas/agregar_marca_en_main.glade"
		self.glade=gtk.Builder()
		self.glade.add_from_file(self.archivo)

		self.window = self.glade.get_object("window")
		self.btn_ok = self.glade.get_object("button_ok")
		self.button_no = self.glade.get_object("button_no")
		self.entry_descripcion = self.glade.get_object("entry_descripcion")
		self.entry_marca = self.glade.get_object("entry_marca")
		self.entry_ganancia = self.glade.get_object("entry_ganancia")
		self.table=self.glade.get_object("table1")

		self.marca_ok,self.descripcion_ok,self.ganancia_ok=False,False,False

		self.window.connect("delete-event",self.delete_event,self_padre)

		self.entry_marca.connect("changed",self.validar_marca)
		self.entry_descripcion.connect("changed",self.validar_descripcion)
		self.entry_ganancia.connect("changed",self.validar_ganancia)

		self.entry_marca.connect("changed",self.desbloquear_aceptar)
		self.entry_descripcion.connect("changed",self.desbloquear_aceptar)
		self.entry_ganancia.connect("changed",self.desbloquear_aceptar)

		self.btn_ok.connect("clicked",self.add_marca,self_padre)
		self.button_no.connect("clicked",self.cancelar,self_padre)

		self.window.connect("key-press-event",self.aceptar_with_enter,self_padre)

