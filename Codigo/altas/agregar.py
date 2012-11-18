#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3 as bdapi
import gtk,os

from validaciones.validacion import caracteres_validos
from validaciones.validacion import codigo_no_repetido
from validaciones.validacion import articulo_no_repetido
from validaciones.validacion import es_int
from validaciones.validacion import es_float
from validaciones.validacion import pintar
from altas.agregar_marca import nueva_marca

from altas.question import question

class altas():

	def cargar_lista(self):
		self.liststore_marca.clear()
		ruta = os.getcwd()
		bbdd=bdapi.connect(ruta+'/Base_Datos/bd_marcas.db')
		cursor=bbdd.cursor()
		cursor.execute("SELECT * FROM marca")
		for tupla in cursor.fetchall():
			self.liststore_marca.append([tupla[1]])
		cursor.close()
		bbdd.close()

	def verificar_marca(self,marca):
		esta=False
		ruta = os.getcwd()
		bbdd=bdapi.connect(ruta+'/Base_Datos/bd_marcas.db')
		cursor=bbdd.cursor()
		cursor.execute("SELECT * FROM marca")
		for tupla in cursor.fetchall():
			if tupla[1] == marca:
				esta=True
				self.ganancia = tupla[4]
		cursor.close()
		bbdd.close()
		return esta

	def aceptar(self,widget,self_padre):
		codigo=self.entry_codigo.get_text()
		descripcion=self.entry_descripcion.get_text()
		marca=self.entry_marca.get_text()
		costo=float (self.entry_costo.get_text() )
		if self.verificar_marca(marca):
			precio= round(costo*( 1+self.ganancia/100),1)
			ruta = os.getcwd()
			bbdd=bdapi.connect(ruta+'/Base_Datos/bd_stock.db')
			cursor=bbdd.cursor()
			cursor.execute(" INSERT INTO bd_stock (codigo,descripcion,marca,costo,precio,stk_disp,pnt_rep,aviso,sw) VALUES(?,?,?,?,?,?,?,?,?)",(codigo,descripcion,marca,costo,precio,0,0,pintar(0,0),True ) )
			bbdd.commit()
			cursor.close()
			bbdd.close()
			self_padre.liststore.append( [int(codigo),descripcion,marca,costo,precio,0,0,pintar(0,0)] )
			question(self,self_padre)
		else:
			nueva_marca(self,self_padre)

	def validar_codigo(self,widget,liststore):
		self.codigo_ok=False
		codigo=self.entry_codigo.get_text()
		if es_int(codigo):
			if not codigo_no_repetido(liststore,codigo):
				self.entry_codigo.set_icon_from_stock(1,gtk.STOCK_APPLY)
				self.entry_codigo.set_property("secondary-icon-tooltip-text","")
				self.codigo_ok=True
			else:
				self.entry_codigo.set_property("secondary-icon-tooltip-text","Codigo Repetido")
				self.entry_codigo.set_icon_from_stock(1,gtk.STOCK_DIALOG_ERROR)
		else:
			self.entry_codigo.set_property("secondary-icon-tooltip-text","Incorrecto")
			self.entry_codigo.set_icon_from_stock(1,gtk.STOCK_DIALOG_ERROR)
		if codigo == "":
			self.entry_codigo.set_property("secondary-icon-stock",None)

	def validar_descripcion(self,widget):
		self.descripcion_ok=False
		descripcion=self.entry_descripcion.get_text()
		if caracteres_validos(descripcion) and descripcion != "":
			self.entry_descripcion.set_icon_from_stock(1,gtk.STOCK_APPLY)
			self.entry_descripcion.set_property("secondary-icon-tooltip-text","")
			self.descripcion_ok=True
		else:
			self.entry_descripcion.set_icon_from_stock(1,gtk.STOCK_DIALOG_ERROR)
			self.entry_descripcion.set_property("secondary-icon-tooltip-text","Incorrecto")

	def validar_marca(self,widget):
		self.marca_ok=False
		marca=self.entry_marca.get_text()
		if caracteres_validos(marca) and marca != "":
			self.entry_marca.set_icon_from_stock(1,gtk.STOCK_APPLY)
			self.entry_marca.set_property("secondary-icon-tooltip-text","")
			self.marca_ok=True
		else:
			self.entry_marca.set_icon_from_stock(1,gtk.STOCK_DIALOG_ERROR)
			self.entry_marca.set_property("secondary-icon-tooltip-text","Incorrecto")

	def validar_costo(self,widget):
		self.costo_ok=False
		costo=self.entry_costo.get_text()
		if es_float(costo):
			self.entry_costo.set_icon_from_stock(1,gtk.STOCK_APPLY)
			self.entry_costo.set_property("secondary-icon-tooltip-text","")
			self.costo_ok=True
		else:
			self.entry_costo.set_icon_from_stock(1,gtk.STOCK_DIALOG_ERROR)
			self.entry_costo.set_property("secondary-icon-tooltip-text","Incorrecto")
		if costo == "":
		 self.entry_costo.set_property("secondary-icon-stock",None)

	def desbloquear_aceptar(self,widget):
		self.btn_ok.set_sensitive(False)
		if self.marca_ok and self.descripcion_ok and self.costo_ok:
			if self.codigo_ok :
				self.btn_ok.set_sensitive(True)

	def aceptar_with_enter(self,widget,event,self_padre):
		if event.keyval ==gtk.keysyms.Return:
			if self.marca_ok and self.descripcion_ok and self.costo_ok:

				if self.codigo_ok:
					self.aceptar(None,self_padre)

	def delete_event(self,widget,event,window):
		window.set_sensitive(True)
		self.window.destroy()

	def cerrar(self,widget,window):
		window.set_sensitive(True)
		self.window.destroy()

	def __init__(self,self_padre):
		self_padre.window.set_sensitive(False)
		self.archivo_glade = "./altas/ventana_altas.glade"
		self.glade = gtk.Builder()
		self.glade.add_from_file(self.archivo_glade)

		self.window = self.glade.get_object("window1")
		self.entry_codigo = self.glade.get_object("entry_codigo")
		self.entry_descripcion = self.glade.get_object("entry_descripcion")
		self.entry_marca = self.glade.get_object("entry_marca")
		self.entry_costo = self.glade.get_object("entry_costo")
		self.liststore_marca = self.glade.get_object("liststore_marca")
		self.table=self.glade.get_object("table1")

		self.completion = gtk.EntryCompletion()
		self.completion.set_model(self.liststore_marca)
		self.entry_marca.set_completion(self.completion)
		self.btn_ok = self.glade.get_object("button_ok")
		self.btn_no = self.glade.get_object("button_no")
		self.completion.set_text_column(0)

		self.codigo_ok,self.marca_ok,self.descripcion_ok,self.costo_ok=False,False,False,False

		self.cargar_lista()
		self.btn_ok.connect("clicked",self.aceptar,self_padre)
		self.window.connect("key-press-event",self.aceptar_with_enter,self_padre)
		self.btn_no.connect("clicked",self.cerrar,self_padre.window)
		self.window.connect("delete-event",self.delete_event,self_padre.window)

		self.entry_codigo.connect("changed",self.validar_codigo,self_padre.liststore)
		self.entry_marca.connect("changed",self.validar_marca)
		self.entry_descripcion.connect("changed",self.validar_descripcion)
		self.entry_costo.connect("changed",self.validar_costo)

		self.entry_codigo.connect("changed",self.desbloquear_aceptar)
		self.entry_marca.connect("changed",self.desbloquear_aceptar)
		self.entry_descripcion.connect("changed",self.desbloquear_aceptar)
		self.entry_costo.connect("changed",self.desbloquear_aceptar)
