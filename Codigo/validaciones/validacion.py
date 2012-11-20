#!/usr/bin/env python
# -*- coding: utf-8 -*-

def caracteres_validos(palabra):
	correcto=True
	try:
		for letra in range(len(palabra)):
			#si no es mayuscula y no es miniscula y no es espacio
			if not ( 65 <=ord(palabra[letra]) <=90 )and not (97<=ord(palabra[letra])<= 122) and not ord(palabra[letra]) == 32:
				#si no es numero,si no es   , - . /  y no es ( )
				if not ( 48 <=ord(palabra[letra]) <=57 ) and not ( 44 <=ord(palabra[letra]) <=47 ) and not ( 40 <=ord(palabra[letra]) <=41 ):
					correcto=False
					break
		return correcto
	except:
		return False

def codigo_no_repetido(liststore,codigo):
	repetido=False
	for fila in range(len(liststore) ):
		if liststore[fila][0] == int(codigo):
			repetido=True
			break
	if repetido:
		return True
	else:
		return False

def articulo_no_repetido(liststore_elejido,entry):
	repetido=False
	for fila in range(len(liststore_elejido) ):
		if liststore_elejido[fila][1] == int(entry.get_text()):
			repetido=True
			break
	if repetido:
		return True
	else:
		return False

def es_int(valor):
	try:
		int(valor)
		return True
	except:
		return False

def es_float(valor):
	try:
		float(valor)
		return True
	except:
		return False


def codigo_no_repetido_modificado(liststore_elejido,entry,id_codigo):
	repetido=False
	for fila in range(len(liststore_elejido) ):
		if liststore_elejido[fila][0] == int(entry.get_text()) and int(entry.get_text()) != id_codigo :
			repetido=True
			break
	if repetido:
		return True
	else:
		return False

def articulo_no_repetido_modificado(liststore_elejido,entry,id_nro_art):
	repetido=False
	for fila in range(len(liststore_elejido) ):
		if liststore_elejido[fila][1] == int(entry.get_text()) and int(entry.get_text()) != id_nro_art:
			repetido=True
			break
	if repetido:
		return True
	else:
		return False

def pintar(cantidad,cantidad_minima):
	if cantidad <= cantidad_minima:
		return True
	else:
		return False
