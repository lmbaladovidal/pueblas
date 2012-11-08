#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gtk,os,time,shutil,sys

class backup:

	def dividir_hora(self):
		hora_actual=str(time.ctime())
		hora_actual=hora_actual.replace(" ","-")
		hora_actual=hora_actual.replace(":","-") #windows y la re concha de tu madre!!!!!!
		return str(hora_actual)

	def __init__(self,self_ventana_principal):
		self.ruta_archivo_db=""
		self_ventana_principal.window.set_sensitive(False)

		self.dialog = gtk.FileChooserDialog("Realizando Backup",
											None,
											gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
											(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
											gtk.STOCK_SAVE, gtk.RESPONSE_OK))
		self.dialog.set_default_response(gtk.RESPONSE_OK)
		self.filter2 = gtk.FileFilter()
		self.filter2.set_name("Base de Datos")
		self.filter2.add_mime_type("archi/db")
		self.filter2.add_pattern("*.db")
		self.dialog.add_filter(self.filter2)
		response = self.dialog.run()
		if response == gtk.RESPONSE_OK:
			ruta=str(self.dialog.get_current_folder() )

			if sys.platform == "linux2":
				carpeta=ruta+"/BACKUP-"+self.dividir_hora()
				os.mkdir(carpeta)
				ruta[0:-6]+'/Base_Datos/marcas_rosarinas.db'
				shutil.copyfile('../Base_Datos/stock_rosarino.db',carpeta+"/stock_rosarino.db")
				shutil.copyfile('../Base_Datos/marcas_rosarinas.db',carpeta+"/marcas_rosarinas.db")

			elif sys.platform == "win32":
				carpeta=ruta+"\\BACKUP_"+self.dividir_hora()
				os.mkdir(carpeta)
				shutil.copyfile('../Base_Datos/stock_rosarino.db',carpeta+"\\stock_rosarino.db")
				shutil.copyfile('../Base_Datos/marcas_rosarinas.db',carpeta+"\\marcas_rosarinas.db")

		self_ventana_principal.window.set_sensitive(True)
		self.dialog.destroy()
