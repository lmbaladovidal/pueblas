#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3 as bdapi
import gtk,os

from validaciones.validacion import caracteres_validos
from validaciones.validacion import codigo_no_repetido_modificado
from validaciones.validacion import articulo_no_repetido_modificado
from validaciones.validacion import es_int
from validaciones.validacion import es_float

class modificaciones():

	def press_btn_ok(self,widget,self_padre):
		contenido_entrys = []
		contenido_entrys.append(self.entry_codigo.get_text())
		contenido_entrys.append(self.entry_descripcion.get_text())
		contenido_entrys.append(self.entry_marca.get_text())
		contenido_entrys.append(self.entry_costo.get_text())
		contenido_entrys.append(self_padre.datos_seleccionados[0])
		ruta = os.getcwd()
		bbdd = bdapi.connect(ruta+'/Base_Datos/bd_stock.db')
		cursor=bbdd.cursor()
		cursor.execute("UPDATE bd_stock SET codigo = ?, descripcion = ?, marca = ? ,costo =? WHERE codigo = ?",contenido_entrys)
		self_padre.window.set_sensitive(True)
		self.tupla = []
		bbdd.commit()
		cursor.close()
		bbdd.close()
		iter=self_padre.datos_seleccionados[8]
		marca = self.entry_marca.get_text()
		self_padre.liststore.set_value(iter,0,int(self.entry_codigo.get_text()) )
		self_padre.liststore.set_value(iter,1,self.entry_descripcion.get_text() )
		self_padre.liststore.set_value(iter,2,marca )
		self_padre.liststore.set_value(iter,3,float(self.entry_costo.get_text()) )
		if self.ganancia == 0:
			self.validar_marca(marca)
		print float(self.entry_costo.get_text())*float(1+self.ganancia/100)
		print float(self.entry_costo.get_text())
		print (1+float(self.ganancia)/100)
		print self.ganancia
		self_padre.liststore.set_value(iter,4,float(self.entry_costo.get_text())*float(1+self.ganancia/100) )
		self.window.destroy()

	def validar_codigo(self,widget):
		self.codigo_ok=False
		codigo=self.entry_codigo.get_text()
		if es_int(codigo) and not codigo_no_repetido_modificado(self.liststore_elejido,self.entry_codigo,self.id_codigo):
			self.entry_codigo.set_icon_from_stock(1,gtk.STOCK_APPLY)
			self.codigo_ok=True
		else:
			self.entry_codigo.set_icon_from_stock(1,gtk.STOCK_DIALOG_ERROR)
		if codigo == "":
			self.codigo_ok=False

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
		esta=False
		if caracteres_validos(marca) and marca != "":
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
		if esta:
			self.entry_marca.set_icon_from_stock(1,gtk.STOCK_APPLY)
			self.marca_ok=True
		else:
			self.entry_marca.set_icon_from_stock(1,gtk.STOCK_DIALOG_ERROR)

	def validar_costo(self,widget):
		self.costo_ok=False
		costo=self.entry_costo.get_text()
		if es_float(costo):
			self.entry_costo.set_icon_from_stock(1,gtk.STOCK_APPLY)
			self.costo_ok=True
		else:
			self.entry_costo.set_icon_from_stock(1,gtk.STOCK_DIALOG_ERROR)
		if costo == "":
		 self.entry_costo.set_property("secondary-icon-stock",None)

	def desbloquear_aceptar(self,widget):
		self.btn_ok.set_sensitive(False)
		if self.marca_ok and self.descripcion_ok and self.costo_ok:
			#1 bien y la otra vacia o las 2 bien
			if self.codigo_ok:
				self.btn_ok.set_sensitive(True)

	def press_btn_no(self,widget,window):
		window.set_sensitive(True)
		self.window.destroy()
		
	def delete_event(self,widget,event,window):
		window.set_sensitive(True)
		self.window.destroy()

	def cargar_lista(self,self_padre):
		ruta = os.getcwd()
		bbdd=bdapi.connect(ruta+'/Base_Datos/bd_marcas.db')
		cursor=bbdd.cursor()
		cursor.execute("SELECT * FROM marca")
		for tupla in cursor.fetchall():
			self.liststore_marca.append([tupla[1] ])
		cursor.close()
		bbdd.close()

	def __init__(self,self_padre):
		self.ganancia = 0
		self_padre.window.set_sensitive(False)
		self.archivo_glade = "./modificaciones/ventana_modificaciones.glade"
		self.glade = gtk.Builder()
		self.glade.add_from_file(self.archivo_glade)
		self.window = self.glade.get_object("window")
		self.entry_codigo = self.glade.get_object("entry_codigo")
		self.entry_descripcion = self.glade.get_object("entry_descripcion")
		self.entry_marca = self.glade.get_object("entry_marca")
		self.entry_costo = self.glade.get_object("entry_costo")
		self.btn_ok = self.glade.get_object("button_ok")
		self.btn_no = self.glade.get_object("button_no")
		self.liststore_marca = self.glade.get_object("liststore_marca")
		self.btn_ok.connect("clicked",self.press_btn_ok,self_padre)
		self.btn_no.connect("clicked",self.press_btn_no,self_padre.window)
		self.window.connect("delete-event",self.delete_event,self_padre.window)
		self.completion = gtk.EntryCompletion()
		self.cargar_lista(self_padre)
		self.completion.set_model(self.liststore_marca)
		self.entry_marca.set_completion(self.completion)
		self.completion.set_text_column(0)

		self.id_codigo=int(self_padre.datos_seleccionados[0])
		self.entry_codigo.set_text(str(self.id_codigo))
		self.entry_descripcion.set_text(self_padre.datos_seleccionados[1])
		self.entry_marca.set_text(self_padre.datos_seleccionados[2])
		self.entry_costo.set_text(str(self_padre.datos_seleccionados[3]))

		self.liststore_elejido=self_padre.liststore
		self.codigo_ok,self.nro_art_ok,self.marca_ok,self.descripcion_ok,self.costo_ok=True,True,True,True,True

		self.entry_codigo.connect("changed",self.validar_codigo)
		self.entry_marca.connect("changed",self.validar_marca)
		self.entry_descripcion.connect("changed",self.validar_descripcion)
		self.entry_costo.connect("changed",self.validar_costo)

		self.entry_codigo.connect("changed",self.desbloquear_aceptar)
		self.entry_marca.connect("changed",self.desbloquear_aceptar)
		self.entry_descripcion.connect("changed",self.desbloquear_aceptar)
		self.entry_costo.connect("changed",self.desbloquear_aceptar)
