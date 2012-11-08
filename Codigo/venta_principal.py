#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3 as bdapi
import gtk
import gobject
import dbus, dbus.service, dbus.glib

from actualizaciones.actualizar import actualizaciones
from altas.agregar import altas
from bajas.eliminar import bajas
from control.controlar import control
from modificaciones.modificar import modificaciones
from Backup.backup_BBDD import backup
from altas.agregar_marca_en_main import nueva_marca

class principal() :

	def conectar_bd(self):
		bbdd=bdapi.connect('./Base_Datos/bd_stock.db')
		cursor=bbdd.cursor()
		cursor.execute("SELECT * FROM bd_stock")
		self.liststore.clear()
		for tupla in cursor.fetchall():
			if tupla[9]:
				self.liststore.append([int(tupla[1]),tupla[2],tupla[3],tupla[4],tupla[5],tupla[6],tupla[7],tupla[8]])
			else:
				self.liststore.append([int(tupla[1]),tupla[2],tupla[3],tupla[4],tupla[5],tupla[6],tupla[7],False])
		bbdd.commit()
		cursor.close()
		bbdd.close()

	def buscar(self,widget):
		busca=self.entry_buscar.get_text()
		filtrado_por=self.combo_buscar.get_active_text()
		self.liststore.clear()
		bbdd=bdapi.connect('./Base_Datos/bd_stock.db')
		cursor=bbdd.cursor()
		if busca != "":
			cursor.execute("SELECT * FROM bd_stock WHERE "+filtrado_por.lower()+" LIKE '%"+busca+"%'")
			for tupla in cursor.fetchall():
				self.liststore.append([int(tupla[1]),tupla[2],tupla[3],tupla[4],tupla[5],tupla[6],tupla[7],tupla[8]])
		else:
			cursor.execute("SELECT * FROM bd_stock ")
			for tupla in cursor.fetchall():
				self.liststore.append([int(tupla[1]),tupla[2],tupla[3],tupla[4],tupla[5],tupla[6],tupla[7],tupla[8]])
		bbdd.commit()
		cursor.close()
		bbdd.close()

	def bloquear_botones(self):
		self.btn_eliminar.set_sensitive(False)
		self.btn_modificar.set_sensitive(False)

	def need_backup(self,widget):
		backup(self)

	def call_class_actualizaciones(self,widget):
		actualizaciones(self)

	def call_class_altas(self,widget):
		altas(self)

	def call_class_bajas(self,widget):
		bajas(self)
		self.bloquear_botones()

	def call_class_control(self,widget):
		control(self)

	def call_class_modificaciones(self,widget):
		modificaciones(self)
		self.bloquear_botones()

	def new_marca(self,widget):
		nueva_marca(self)

	def desbloquear_botones(self):
		self.btn_modificar.set_sensitive(True)
		self.btn_eliminar.set_sensitive(True)

	def target(self,widget):
		(model, iter) = self.treeselection.get_selected()
		if self.datos_seleccionados != []:
			self.datos_seleccionados=[]
		try:
			for x in range(8):
				self.datos_seleccionados.append(self.liststore.get_value(iter,x))
			self.datos_seleccionados.append(iter)
			self.desbloquear_botones()
		except:
			pass

	def teclas(self,widget,event):
		if event.keyval ==gtk.keysyms.F1:
			self.go_home(None)
		if event.keyval ==gtk.keysyms.F2:
			self.go_stock(None)

	def go_home(self,widget):
		self.notebook.set_current_page(0)
		self.window.set_title("Ventana Principal")

	def go_stock(self,widget):
		self.notebook.set_current_page(1)
		self.window.set_title("Gestion de Productos")

	def cerrar(self,widget):
		gtk.main_quit()

	def delete_event(self,widget,event):
		gtk.main_quit()

	def __init__(self):
		self.datos_seleccionados = []
		self.archivo_glade="./ventana_principal.glade"
		self.glade=gtk.Builder()
		self.glade.add_from_file(self.archivo_glade)
		self.window = self.glade.get_object("window_main")
		self.notebook = self.glade.get_object("notebook_principal")

####################################BOTONES################################
		self.btn_actualizar = self.glade.get_object("actualizar_producto")
		self.btn_agregar = self.glade.get_object("agregar_producto")
		self.btn_eliminar = self.glade.get_object("eliminar_producto")
		self.btn_controlar = self.glade.get_object("controlar_producto")
		self.btn_modificar = self.glade.get_object("modificar_producto")
		self.button_home = self.glade.get_object("button_home")
		self.button_stock = self.glade.get_object("button_stock")
		self.button_backup = self.glade.get_object("button_backup")
		self.button_agregar_marca = self.glade.get_object("agregar_marca")
		self.button_salir = self.glade.get_object("button_salir")
#################################ENTRYS Y COMBO BOX DE BUSQUEDA####################################
		self.entry_buscar = self.glade.get_object("entry_buscar")
		self.hbox_buscar = self.glade.get_object("hbox3")
		filtrado=("Codigo","Descripcion","Marca")
		self.combo_buscar = gtk.combo_box_new_text()
		self.combo_buscar.append_text("Codigo")
		self.combo_buscar.append_text("Descripcion")
		self.combo_buscar.append_text("Marca")
		self.hbox_buscar.pack_start(self.combo_buscar,False,True,0)
###########################LISTSTORES-TREEVIEW#############################
		self.treeview = self.glade.get_object("treeview")
		self.liststore = self.glade.get_object("liststore")
		self.conectar_bd()
############################CONECTANDO SEÑALES#############################
		self.window.connect("key-press-event",self.teclas)
		self.window.connect("delete_event",self.delete_event)
		self.btn_actualizar.connect("clicked",self.call_class_actualizaciones)
		self.btn_agregar.connect("clicked",self.call_class_altas)
		self.btn_eliminar.connect("clicked",self.call_class_bajas)
		self.btn_controlar.connect("clicked",self.call_class_control)
		self.btn_modificar.connect("clicked",self.call_class_modificaciones)
		self.button_agregar_marca.connect("clicked",self.new_marca)
		self.treeview.connect("cursor-changed",self.target)
		self.entry_buscar.connect("changed",self.buscar)
		self.button_home.connect("clicked",self.go_home)
		self.button_stock.connect("clicked",self.go_stock)
		self.button_backup.connect("clicked",self.need_backup)
		self.button_salir.connect("clicked",self.cerrar)
############################TREESELECTIOS##################################
		self.treeselection = self.treeview.get_selection()
###########################################################################
		self.combo_buscar.set_active(0)
		self.combo_buscar.show()

	def main(self):
		gtk.main()


if __name__=="__main__":
	program=principal()
	program.main()
