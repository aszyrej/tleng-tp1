#!/usr/bin/env python

import sys
sys.path.insert(0,"../..")
sys.path.insert(0,"../svg")
sys.path.insert(0,"../tree")
sys.path.insert(0,"../ast")


if sys.version_info[0] >= 3:
    raw_input = input

import ply.lex as lex
import ply.yacc as yacc
import os
from svg import SVGBuilder
from tree import Tree
from tree import Node
from ast import ASTProcessor

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
        lex.lex(module=self, debug=0)
        yacc.yacc(module=self,
                  debug=0,
                  debugfile=self.debugfile,
                  tabmodule=self.tabmodule)

    def parse(self, exp):
        ast = Tree(yacc.parse(exp))
        return ast

    def run(self, exp):
        ast = Tree(yacc.parse(exp))
        ast_processor = ASTProcessor()
        ast_processor.process(ast)
        svgB = SVGBuilder()
        svg = svgB.build(ast)
        svg.save('form.svg')
        print "'form.svg' generado exitosamente"

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
        raise Exception("Syntax error at '%s'" % p.value)

if __name__ == '__main__':
    form = Form()
    form.run(sys.argv[1])

  
