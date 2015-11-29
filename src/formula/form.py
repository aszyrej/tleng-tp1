#!/usr/bin/env python

import sys
sys.path.insert(0,"../..")
sys.path.insert(0,"../svg")
sys.path.insert(0,"../tree")


if sys.version_info[0] >= 3:
    raw_input = input

import ply.lex as lex
import ply.yacc as yacc
import os
from svg import SVGBuilder
from tree import Tree
from tree import Node

class Parser:
    """
    Base class for a lexer/parser that has the rules defined as methods
    """
    tokens = ()
    precedence = ()

    def __init__(self, **kw):
        self.debug = kw.get('debug', 0)
        self.names = { }
        try:
            modname = os.path.split(os.path.splitext(__file__)[0])[1] + "_" + self.__class__.__name__
        except:
            modname = "parser"+"_"+self.__class__.__name__
        self.debugfile = modname + ".dbg"
        self.tabmodule = modname + "_" + "parsetab"
        #print self.debugfile, self.tabmodule

        # Build the lexer and parser
        lex.lex(module=self, debug=1)
        yacc.yacc(module=self,
                  debug=1,
                  debugfile=self.debugfile,
                  tabmodule=self.tabmodule)

    def run(self):
        while 1:
            try:
                s = raw_input('form > ')
            except EOFError:
                break
            if not s: continue
            ast = Tree(yacc.parse(s))
            print self.process(ast)
            svgB = SVGBuilder()
            svg = svgB.build(ast)
            svg.save('test.svg')

    def process(self, ast):
        ast.root.attrs['x'] = 0
        ast.root.attrs['y'] = 0
        ast.root.attrs['z'] = 1
        ns = ast.preorder_traversal()       
        index = 0
        for node in ns:
            if node.type == 'concat' \
            or node.type == 'p' \
            or node.type == 'u' \
            or node.type == 'pu':
                node.first_child().copy_node_attrs(node)
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
                pass
            elif node.type == 'brackets':
                node.first_child().copy_node_attrs(node)
            else:
                if node.parent.type == 'concat':
                    if (index+1<len(ns)):
                        ns[index+1].attrs['x'] = node.attrs['x']+0.6*node.attrs['z']
                        ns[index+1].attrs['y'] = node.attrs['y']
                        ns[index+1].attrs['z'] = node.attrs['z']

                elif node.parent.type == 'p':
                    if (node.left_sibling == None):
                        node.right_sibling.attrs['x'] = node.attrs['x']+0.6*node.attrs['z']
                        node.right_sibling.attrs['y'] = node.attrs['y']-0.45
                        node.right_sibling.attrs['z'] = node.attrs['z']*0.7
                    else:
                        if (index+1<len(ns)):
                            ns[index+1].attrs['x'] = node.attrs['x']+0.6*node.attrs['z']
                            ns[index+1].attrs['y'] = node.parent.attrs['y']
                            ns[index+1].attrs['z'] = node.parent.attrs['z']

                elif node.parent.type == 'u':
                    if (node.left_sibling == None):
                        node.right_sibling.attrs['x'] = node.attrs['x']+0.6*node.attrs['z']
                        node.right_sibling.attrs['y'] = node.attrs['y']+0.25
                        node.right_sibling.attrs['z'] = 0.7*node.attrs['z']
                    else:
                        if (index+1<len(ns)):
                            ns[index+1].attrs['x'] = node.attrs['x']+0.6*node.attrs['z']
                            ns[index+1].attrs['y'] = node.parent.attrs['y']
                            ns[index+1].attrs['z'] = node.parent.attrs['z']

                elif node.parent.type == 'pu':
                    if (node.left_sibling == None):
                        ns[index+1].attrs['x'] = node.attrs['x']+0.6*node.attrs['z']
                        ns[index+1].attrs['y'] = node.attrs['y']-0.45
                        ns[index+1].attrs['z'] = 0.7*node.attrs['z']
                        ns[index+2].attrs['x'] = node.attrs['x']+0.6*node.attrs['z']
                        ns[index+2].attrs['y'] = node.attrs['y']+0.25
                        ns[index+2].attrs['z'] = 0.7*node.attrs['z']
                    elif (node.right_sibling == None):
                        if (index+1<len(ns)):
                            ns[index+1].attrs['x'] = node.attrs['x']+0.6*node.attrs['z']
                            ns[index+1].attrs['y'] = node.attrs['y']
                            ns[index+1].attrs['z'] = node.attrs['z']

                elif node.parent.type == 'divide':
                    
                    if (node.left_sibling == None):
                        node.right_sibling.attrs['x'] = node.attrs['x']
                        node.right_sibling.attrs['y'] = node.attrs['y']
                        node.right_sibling.attrs['z'] = node.attrs['z']

                    elif (node.right_sibling != None):
                        node.right_sibling.attrs['x'] = node.attrs['x'] +0.6*node.attrs['z']
                        node.right_sibling.attrs['y'] = node.attrs['y']
                        node.right_sibling.attrs['z'] = node.attrs['z']

                    else:
                        long_a = node.left_sibling.attrs['x'] - node.first_sibling().attrs['x']
                        long_b = node.attrs['x'] - node.left_sibling.attrs['x']

                        inicio_a = node.first_sibling().attrs['x']
                        fin_a = node.left_sibling.attrs['x']

                        #node.left_sibling.move(0,node.left_sibling.attrs['y'] - node.parent.attrs['y'] + 0.95)

                        if node.left_sibling.type == 'p' or node.left_sibling.type == 'pu':
                            node.left_sibling.move(-long_a,1.05)
                        else:
                            node.left_sibling.move(-long_a,0.95)

                        inicio_b = node.left_sibling.attrs['x']
                        fin_b = node.attrs['x']-long_a
        
                        node.attrs['x1'] = node.first_sibling().attrs['x']
                        if (long_a > long_b):
                            
                            node.attrs['x2'] = fin_a
                            
                            # centrar B
                            node.left_sibling.move(((long_a-long_b)/2.0),0)

                        else:

                            node.attrs['x2'] = fin_b
                            
                            # centrar A
                            node.first_sibling().move(((long_b-long_a)/2.0),0)
                        
                        if (index+1<len(ns)):    
                            ns[index+1].attrs['x'] = node.attrs['x2']
                            ns[index+1].attrs['y'] = node.attrs['y2']        
                elif node.parent.type == 'brackets':
                    if (node.left_sibling == None):
                        node.right_sibling.copy_node_attrs(node)
                    elif (node.right_sibling != None):
                        node.right_sibling.attrs['x'] = node.attrs['x'] +0.6*node.attrs['z']
                        node.right_sibling.attrs['y'] = node.attrs['y']
                        node.right_sibling.attrs['z'] = node.attrs['z']
                    else:
                        if (index+1<len(ns)):
                            ns[index+1].attrs['x'] = node.attrs['x']
                            if ((node.parent.parent == None or node.parent.parent.type == 'p' or node.parent.parent.type == 'u') and node.parent.left_sibling!=None):
                                ns[index+1].attrs['y'] = node.parent.left_sibling.attrs['y']
                                ns[index+1].attrs['z'] = node.parent.left_sibling.attrs['z']
                            else:
                                ns[index+1].attrs['y'] = node.attrs['y']
                                ns[index+1].attrs['z'] = node.attrs['z']


            index += 1
        return ns[0]
    
class Form(Parser):

    tokens = (
        'UNDERSCORE','POW','DIVIDE', 'CHAR',
        'LBRACK','RBRACK','LPAREN','RPAREN',
        )

    # Tokens

    t_UNDERSCORE  = r'_'
    t_POW  = r'\^'
    t_DIVIDE  = r'/'
    t_LBRACK  = r'\{'
    t_RBRACK  = r'\}'
    t_LPAREN  = r'\('
    t_RPAREN  = r'\)'
    t_CHAR  = r'[a-zA-Z+-]'

    t_ignore = " \t"

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")
    
    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    def p_expr_E(self,p):
        """
        expr_E : expr_T expr_A
        """
        if p[2] != None:
            p[0] = Node('divide', [p[1], p[2], Node('barra')])
        else: p[0] = p[1]

    def p_expr_A(self,p):
        """
        expr_A : DIVIDE expr_T expr_A
            | empty
        """  
        if p[1] == None: p[0] = None
        elif p[3] == None: p[0] = p[2]
        else: 
            p[0] = Node('divide', [p[2], p[3], Node('barra')])

    def p_expr_T(self,p):
        """
        expr_T : expr_F expr_B
        """    
        if p[2] != None:
            p[0] = Node('concat', [p[1], p[2]])
        else: p[0] = p[1]

    def p_expr_B(self,p):
        """
        expr_B : expr_F expr_B
            | empty
        """    
        if p[1] == None: p[0] = None
        elif p[2] == None: p[0] = p[1]
        else:
            p[0] = Node('concat', [p[1], p[2]])

    def p_expr_F(self,p):
        """
        expr_F : expr_I expr_G
        """    
        if p[2] != None:
            if p[2][0] == 'pu':
                p[0] = Node('pu', [p[1], p[2][1], p[2][2]])
            elif p[2][0] == 'p':
                p[0] = Node('p', [p[1], p[2][1]])
            else:
                p[0] = Node('u', [p[1], p[2][1]])
        else:
            p[0] = p[1]

    def p_expr_G(self,p):
        """
        expr_G : POW expr_I expr_H
            | UNDERSCORE expr_I expr_L
            | empty
        """    
        if p[1] == None:
            p[0] = None
        elif p[1] == '^':
            if p[3] == None:
                p[0] = ('p', p[2])
            else:
                p[0] = ('pu', p[2], p[3])
        elif p[1] == '_':
            if p[3] == None:
                p[0] = ('u', p[2])
            else:
                p[0] = ('pu', p[3], p[2])
       
    def p_expr_H(self,p):
        """
        expr_H : UNDERSCORE expr_I
            | empty
        """    
        if p[1] != None: p[0] = p[2]
        else: p[0] = None

    def p_expr_L(self,p):
        """
        expr_L : POW expr_I
            | empty
        """    
        if p[1] != None: p[0] = p[2]
        else: p[0] = None

    def p_expr_I(self,p):
        """
        expr_I : LPAREN expr_E RPAREN
            | LBRACK expr_E RBRACK
            | CHAR
        """
        if p[1] == '(': 
            p[0] = Node('parens', [Node('('), p[2], Node(')')])
        elif p[1] == '{':
            p[0] = Node('brackets', [Node('{'), p[2], Node('}')])
        else: p[0] = Node(p[1])
    
    def p_empty(self,p):
        'empty :'
        pass

    def p_error(self,p):
        if p:
            print("Syntax error at '%s'" % p.value)
        else:
            print("Syntax error at EOF")

if __name__ == '__main__':
    form = Form()
    form.run()

  
