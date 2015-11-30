#!/usr/bin/env python

import sys
sys.path.insert(0,"../tree")

from tree import Tree
from tree import Node

class ASTProcessor:

    """
    Clase encargada de procesar el AST generado por el Parser, cargandolo de informacion
    que luego sera utilizada por el SVGBuilder.
    """

    def process(self, ast):

        # variables nodo root
        ast.root.attrs['x'] = 0
        ast.root.attrs['y'] = 0
        ast.root.attrs['z'] = 1
        ns = ast.preorder_traversal()
        index = 0
        for node in ns:

            ## NO TERMINALES
            if node.type == 'concat' \
            or node.type == 'p' \
            or node.type == 'u' \
            or node.type == 'pu':
                node.first_child().copy_node_attrs(node)

            ## caso DIVIDE: copiamos las variables del nodo al primer operador (numerador)
            ## modificando la variable 'y' de manera que quede por encima de la barra
            ## de division.
            elif node.type == 'divide':
                node.first_child().copy_node_attrs(node)
                node.first_child().attrs['y'] = node.attrs['y'] - 0.19
                numerador = ns.index(node.children[1]) - 1
                if ns[numerador].parent.type == 'u' or ns[numerador].parent.type =='pu':
                    node.last_child().attrs['y1'] = node.attrs['y'] - 0.28*node.attrs['y'] + 0.1
                else:
                    node.last_child().attrs['y1'] = node.attrs['y'] - 0.28*node.attrs['y']
                node.last_child().attrs['y2'] = node.last_child().attrs['y1']
            elif node.type == 'parens':
                node.first_child().copy_node_attrs(node)
            elif node.type == 'brackets':
                node.first_child().copy_node_attrs(node)

            ## NODOS TERMINALES ##
            else:
                ## caso CONCAT: copiamos la informacion del nodo actual al siguiente
                ## nodo en el PREORDER, modificando la variable 'x', de manera que
                ## escriba a continuacion del nodo actual.
                if node.parent.type == 'concat':
                    if (index+1<len(ns)):
                        ns[index+1].attrs['x'] = node.attrs['x']+0.6*node.attrs['z']
                        ns[index+1].attrs['y'] = node.attrs['y']
                        ns[index+1].attrs['z'] = node.attrs['z']

                ## caso P (superindice)
                elif node.parent.type == 'p':
                    ## caso Nodo izquierdo de P: seteamos las variables del nodo derecho
                    ## (superindice) de manera que quede mas arriba y con un size mas
                    ## pequenio. Tambien nos aseguramos de avanzar la variable 'x'.
                    if (node.left_sibling == None):
                        node.right_sibling.attrs['x'] = node.attrs['x']+0.6*node.attrs['z']
                        node.right_sibling.attrs['y'] = node.attrs['y']-0.45
                        node.right_sibling.attrs['z'] = node.attrs['z']*0.7
                    ## caso Nodo derecho de P: reestablecemos los valores de 'y' y 'z'
                    ## para que el siguiente nodo del PREORDER escriba como inidicaba 
                    ## la configuracion antes de poner el superindice.
                    else:
                        if (index+1<len(ns)):
                            ns[index+1].attrs['x'] = node.attrs['x']+0.6*node.attrs['z']
                            ns[index+1].attrs['y'] = node.parent.attrs['y']
                            ns[index+1].attrs['z'] = node.parent.attrs['z']


                ## caso U (subindice): parecido al caso P con la diferencia de que debe escribirse
                ## el subindice por debajo. (variable 'y')
                elif node.parent.type == 'u':
                    ## caso nodo izquierdo de U.
                    if (node.left_sibling == None):
                        node.right_sibling.attrs['x'] = node.attrs['x']+0.6*node.attrs['z']
                        node.right_sibling.attrs['y'] = node.attrs['y']+0.25
                        node.right_sibling.attrs['z'] = 0.7*node.attrs['z']
                    ## caso nodo derecho de U.
                    else:
                        if (index+1<len(ns)):
                            ns[index+1].attrs['x'] = node.attrs['x']+0.6*node.attrs['z']
                            ns[index+1].attrs['y'] = node.parent.attrs['y']
                            ns[index+1].attrs['z'] = node.parent.attrs['z']

                ## caso PU (superindice y subindice)
                elif node.parent.type == 'pu':
                    ## caso nodo izquierdo de PU. Seteamos las varibles del nodo superindice
                    ## y subindice
                    if (node.left_sibling == None):
                        ns[index+1].attrs['x'] = node.attrs['x']+0.6*node.attrs['z']
                        ns[index+1].attrs['y'] = node.attrs['y']-0.45
                        ns[index+1].attrs['z'] = 0.7*node.attrs['z']
                        ns[index+2].attrs['x'] = node.attrs['x']+0.6*node.attrs['z']
                        ns[index+2].attrs['y'] = node.attrs['y']+0.25
                        ns[index+2].attrs['z'] = 0.7*node.attrs['z']
                    ## caso nodo derecho de PU: restablecemos los valores de 'y' y 'z'
                    ## y avanzamos la variable 'x'
                    elif (node.right_sibling == None):
                        if (index+1<len(ns)):
                            ns[index+1].attrs['x'] = node.attrs['x']+0.6*node.attrs['z']
                            ns[index+1].attrs['y'] = node.parent.attrs['y']
                            ns[index+1].attrs['z'] = node.parent.attrs['z']

                ## caso DIVIDE.
                elif node.parent.type == 'divide':
                    if (node.left_sibling == None):
                        node.right_sibling.attrs['x'] = node.attrs['x']+0.6*node.attrs['z']
                        node.right_sibling.attrs['y'] = node.attrs['y']
                        node.right_sibling.attrs['z'] = node.attrs['z']

                    elif (node.right_sibling != None):
                        node.right_sibling.attrs['x'] = node.attrs['x']+0.6*node.attrs['z']
                        node.right_sibling.attrs['y'] = node.attrs['y']
                        node.right_sibling.attrs['z'] = node.attrs['z']

                    ## caso nodo BARRA: encargado de posicionar correctamente el dividiendo,
                    ## divisor y la barra de division.
                    else:
                        long_a = node.left_sibling.attrs['x'] - node.first_sibling().attrs['x']
                        long_b = node.attrs['x'] - node.left_sibling.attrs['x']

                        inicio_a = node.first_sibling().attrs['x']
                        fin_a = node.left_sibling.attrs['x']

                        # movemos el denominador en el eje x e y segun las expresiones
                        # que haya

                        if node.parent.branch_has_type(['p', 'pu', 'divide']):
                            node.left_sibling.move(-long_a,1.25)
                        else:
                            node.left_sibling.move(-long_a,1.05)
                                                    
                        inicio_b = node.left_sibling.attrs['x']
                        fin_b = node.attrs['x']-long_a
        
                        node.attrs['x1'] = node.first_sibling().attrs['x']

                        # centrar B
                        if (long_a > long_b):
                            node.attrs['x2'] = fin_a
                            node.left_sibling.move(((long_a-long_b)/2.0),0)
                        # centrar A
                        elif (long_a < long_b):
                            node.attrs['x2'] = fin_b
                            node.first_sibling().move(((long_b-long_a)/2.0),0)
                        else:
                            node.attrs['x2'] = fin_b
                        
                        if (index+1<len(ns)):    
                            ns[index+1].attrs['x'] = node.attrs['x2']
                            ns[index+1].attrs['y'] = node.first_sibling().attrs['y']
                            ns[index+1].attrs['z'] = node.attrs['z'] 

                ## caso LLAVES.
                elif node.parent.type == 'brackets':
                    ## caso '{': copia la informacion al nodo derecho.
                    if (node.left_sibling == None):
                        node.right_sibling.copy_node_attrs(node)
                    ## caso E:  avanza la variable 'x'
                    elif (node.right_sibling != None):
                        node.right_sibling.attrs['x'] = node.attrs['x'] +0.6*node.attrs['z']
                        node.right_sibling.attrs['y'] = node.attrs['y']
                        node.right_sibling.attrs['z'] = node.attrs['z']
                    ## caso '}': reestablece la configuracion de '{' para
                    ## el siguiente nodo en el PREORDER.
                    else:
                        if (index+1<len(ns)):
                            ns[index+1].attrs['x'] = node.attrs['x']
                            if ((node.parent.parent == None or node.parent.parent.type == 'p' or node.parent.parent.type == 'u') and node.parent.left_sibling!=None):
                                ns[index+1].attrs['y'] = node.parent.left_sibling.attrs['y']
                                ns[index+1].attrs['z'] = node.parent.left_sibling.attrs['z']
                            else:
                                ns[index+1].attrs['y'] = node.attrs['y']
                                ns[index+1].attrs['z'] = node.attrs['z']

                ## caso PARENTESIS
                elif node.parent.type == 'parens':
                    ## caso '(': copia la informacion al nodo derecho avanzando 'x'
                    if (node.left_sibling == None):
                        node.right_sibling.attrs['x'] = node.attrs['x'] +0.6*node.attrs['z']
                        node.right_sibling.attrs['y'] = node.attrs['y']
                        node.right_sibling.attrs['z'] = node.attrs['z']
                    ## caso E:  avanza la variable 'x'
                    elif (node.right_sibling != None):
                        node.right_sibling.attrs['x'] = node.attrs['x'] +0.6*node.attrs['z']
                        node.right_sibling.attrs['y'] = node.attrs['y']
                        node.right_sibling.attrs['z'] = node.attrs['z']
                    ## caso ')': estira el '(' y reestablece la configuracion de ')' para
                    ## el siguiente nodo en el PREORDER.
                    else:
                        h_l_attrs = node.left_sibling.find_higher_and_lower_attrs()
                        node.first_sibling().attrs['y1'] = h_l_attrs['y'][0]
                        node.first_sibling().attrs['y2'] = h_l_attrs['y'][1]
                        node.attrs['y1'] = h_l_attrs['y'][0]
                        node.attrs['y2'] = h_l_attrs['y'][1]
                        node.attrs['y'] = node.first_sibling().attrs['y']
                        y_paren = (float(node.attrs['y2'])-float(node.attrs['y1']))*0.3
                        if (index+1<len(ns)):
                            ns[index+1].attrs['x'] = node.attrs['x'] +0.6*node.attrs['z']
                            if ((node.parent.parent == None or node.parent.parent.type == 'p' or node.parent.parent.type == 'u') and node.parent.left_sibling!=None):
                                ns[index+1].attrs['y'] = y_paren
                                ns[index+1].attrs['z'] = node.parent.left_sibling.attrs['z']
                            else:
                                ns[index+1].attrs['y'] = y_paren
                                ns[index+1].attrs['z'] = node.attrs['z']
            index += 1