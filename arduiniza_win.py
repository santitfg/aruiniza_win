#!/usr/bin/env python
  
# Generación de archivo keywords.txt para Arduino IDE
# por RafaG, 2017
#
# GPL 3.0
  
import argparse
import re
  
# Gestión de argumentos
parser = argparse.ArgumentParser()
parser.add_argument('file', type=argparse.FileType('r'))
args = parser.parse_args()
  
# Aquí procesamos lo que se tiene que hacer con el argumento
if args.file:
    k1 = "KEYWORD1"
    k2 = "KEYWORD2"
    l1 = "LITERAL1"
    cad_clase = re.compile('(class)\s\w+')
    cad_metodo = re.compile('^\s*\w+(\s+\w+)+\(')
    cad_constructor = re.compile('^\s*\w+\(')
    cad_variable = re.compile('^\s*\w.*=')
    cad_public = "public:"
    cad_private = "private:"
    lista_k1 = []
    lista_k2 = []
    lista_l1 = []
    add_k2 = False
  
    # Recorremos el archivo de la clase
    codigo = args.file.readlines()
    for linea in codigo:
        # Buscamos "public:"
        if (linea.find(cad_public) != -1):
            add_k2 = True
        # Buscamos "private:"
        if (linea.find(cad_private) != -1):
            add_k2 = False
        # Buscamos "class" (K1)
        if (re.search(cad_clase, linea)):
            elementos = linea.split()
            lista_k1.append(elementos[1])
        # Buscamos métodos (K2)
        if (re.search(cad_metodo, linea) and add_k2):
            elementos = linea.split('(')
            lista_k2.append(elementos[0].split()[-1])
            continue
        # Buscamos constructores
        if (re.search(cad_constructor, linea) and add_k2):
            continue
        # Buscamos variables (L1)
        if (re.search(cad_variable, linea) and add_k2):
            elementos = linea.split('=')
            lista_l1.append(elementos[0].split()[-1])
  
    args.file.close()

    with open("keywords.txt", "w") as keywords:
        # Generamos la salida
        for el_k1 in lista_k1:
            keywords.write(el_k1 + "\t" + k1)
            keywords.write("\n")
    
        for el_k2 in lista_k2:
            keywords.write(el_k2 + "\t" + k2)
            keywords.write("\n")

        for el_l1 in lista_l1:
            keywords.write(el_l1 + "\t" + l1)
            keywords.write("\n")
