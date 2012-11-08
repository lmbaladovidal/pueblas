#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3 as bdapi
import random
bbdd=bdapi.connect('bd_stock.db')
cursor=bbdd.cursor()

cursor.execute("""DROP TABLE IF EXISTS bd_stock""")

cursor.execute("""create table bd_stock (id INTEGER PRIMARY KEY,
				codigo text,
				descripcion text,
				marca text,
				costo float,
				precio float,
				stk_disp float,
				pnt_rep float,
				aviso bool,
				sw bool
				)""")
#cursor.execute(" INSERT INTO  bd_stock (codigo, descripcion, marca, costo, precio, stk_disp, pnt_rep,aviso, sw) VALUES(?,?,?,?,?,?,?,?,?)",lista3)
	
bbdd.commit()

cursor.close()
bbdd.close()
