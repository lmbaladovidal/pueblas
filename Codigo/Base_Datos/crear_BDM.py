#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3 as bdapi
import random
bbdd=bdapi.connect('bd_marcas.db')
cursor=bbdd.cursor()

cursor.execute("""DROP TABLE IF EXISTS marca""")

cursor.execute("""create table marca (id INTEGER PRIMARY KEY,
				nombre text,
				descripcion text,
				rubro text,
				coeficiente float
				)""")
bbdd.commit()
cursor.close()
bbdd.close()
