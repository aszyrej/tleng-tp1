#!/usr/bin/env python

# -----------------------------------------------------------------------------
# calc.py
#
# A simple calculator with variables.   This is from O'Reilly's
# "Lex and Yacc", p. 63.
#
# Class-based example contributed to PLY by David McNab
# -----------------------------------------------------------------------------

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
        ast.root.z = 1
        ns = ast.preorder_traversal()
        index = 0
        for node in ns:
            if node.type == 'concat':
                try:
                    ns[index+1].copy_node_attrs(node)
                except:
                    pass
            elif node.type == 'divide':
                try:
                    ns[index+1].copy_node_attrs(node)
                    ns[index+1].y -= 0.19
                    node.children[-1].y1 = node.y - 0.28*node.y
                    node.children[-1].y2 = node.y - 0.28*node.y
                except:
                    pass
            elif node.type == 'p':
                try:
                    ns[index+1].copy_node_attrs(node)
                except:
                    pass
            elif node.type == 'u':
                try:
                    ns[index+1].copy_node_attrs(node)
                except:
                    pass
            elif node.type == 'pu':
                try:
                    ns[index+1].copy_node_attrs(node)
                except:
                    pass
            elif node.type == 'parens':
                pass
            elif node.type == 'brackets':
                pass
            else:
                if node.parent.type == 'concat':
                    try:
                        ns[index+1].x = node.x+0.6*node.z
                        ns[index+1].y = node.y
                        ns[index+1].z = node.z
                    except:
                        pass
                elif node.parent.type == 'p':
                    try:
                        if (node.leftSibling == None):
                            ns[index+1].x = node.x+0.6*node.z
                            ns[index+1].y = node.y-0.45
                            ns[index+1].z = 0.7*node.z
                        else:
                            ns[index+1].copy_node_attrs(node.parent)
                            ns[index+1].x = node.x+0.6*node.z
                    except:
                        pass
                elif node.parent.type == 'u':
                    try:
                        if (node.leftSibling == None):
                            ns[index+1].x = node.x+0.6*node.z
                            ns[index+1].y = node.y+0.25
                            ns[index+1].z = 0.7*node.z
                        else:
                            ns[index+1].copy_node_attrs(node.parent)
                            ns[index+1].x = node.x+0.6*node.z
                    except:
                        pass
                elif node.parent.type == 'pu':
                    try:
                        if (node.leftSibling == None):
                            ns[index+1].x = node.x+0.6*node.z
                            ns[index+1].y = node.y-0.45
                            ns[index+1].z = 0.7*node.z
                            ns[index+2].x = node.x+0.6*node.z
                            ns[index+2].y = node.y+0.25
                            ns[index+2].z = 0.7*node.z
                        elif (node.rightSibling == None):
                            ns[index+1].copy_node_attrs(node.parent)
                            ns[index+1].x = node.x+0.6*node.z
                    except:
                        pass
                elif node.parent.type == 'divide':
                    try:
                        if (node.leftSibling == None):
                            ns[index+1].x = node.x
                            ns[index+1].z = node.z
                            ns[index+1].y = node.y + 0.95
                        elif (node.rightSibling != None):
                            ns[index+1].x = node.x+0.6*node.z
                            ns[index+1].z = node.z
                        else:
                            node.leftSibling.y = node.parent.y + 0.95
                            long_a = node.leftSibling.x - node.parent.children[0].x
                            long_b = node.x - node.leftSibling.x
                            if (long_a >= long_b):
                                # inicial A - final A
                                node.x1 = node.parent.children[0].x
                                node.x2 = node.leftSibling.x
                                ns[index+1].x = node.x2
                                # centrar B
                                node.leftSibling.x = node.parent.children[0].x + ((long_a-long_b)/2.0)
                            else:
                                # inicial B - final B
                                node.x1 = node.leftSibling.x
                                node.x2 = node.x
                                ns[index+1].x = node.x2
                                # centrar A
                                node.parent.children[0].x = node.leftSibling.x + ((long_b-long_a)/2.0)
                    except Exception as e:
                        print e

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

  
