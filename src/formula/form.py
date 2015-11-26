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

if sys.version_info[0] >= 3:
    raw_input = input

import ply.lex as lex
import ply.yacc as yacc
import os
import svg
from ete2 import Tree

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
            ast = Tree(str(yacc.parse(s))+";")
            self.process(ast)
            
    def process(self, ast):
        for node in ast.traverse("preorder"):
            if (node.is_root()):
                node.add_features(x=0, y=0, z=1)
            else:
                if len(node.name)==0:
                    try:
                        copy = node.get_sisters()[0]
                        node.add_features(x=copy.x, y=copy.y, z=copy.z)
                    except:
                        print "bla3"
                elif node.name == '\'concat\'' or node.name == '\'divide\'' or node.name == '\'p\'' or node.name == '\'pu\'' or node.name == '\'u\'':
                    up = node.up
                    try:
                        node.add_features(x=up.x, y=up.y, z=up.z)
                    except:
                        print "bla"
                # CONCAT
                elif node.get_sisters()[0].name == '\'concat\'':
                    concatNode = node.get_sisters()[0]
                    try:
                        x = concatNode.x+concatNode.z*0.6
                        y = concatNode.y
                        z = concatNode.z
                        node.add_features(x=x, y=y, z=z)
                        concatNode.add_features(x=x, y=y, z=z)
                    except:
                        print "bla2"
                # SUPERINDICE
                elif node.get_sisters()[0].name == '\'p\'':
                    pNode = node.get_sisters()[0]
                    if pNode.z != 0.7:
                        x = pNode.x+0.6
                        node.add_features(x=x, y=pNode.y, z=pNode.z)
                        pNode.add_features(x=x, z=0.7)
                    else:
                        x = pNode.x+0.6
                        y = pNode.y - 0.45
                        z = 0.7
                        node.add_features(x=x, y=y, z=z)
                        pNode.add_features(x=x, z=z)
                        pNode.up.get_sisters()[0].add_features(x=pNode.x, y=pNode.y, z=pNode.z)
                #SUBINDICE
                elif node.get_sisters()[0].name == '\'u\'':
                    uNode = node.get_sisters()[0]
                    if uNode.z != 0.7:
                        x = uNode.x+0.6
                        uNode.add_features(x=x, z=0.7)
                        node.add_features(x=x, y=uNode.y, z=uNode.z)
                    else:
                        x = uNode.x+0.6
                        y = uNode.y + 0.45
                        z = 0.7
                        node.add_features(x=x, y=y, z=z)
                        uNode.add_features(x=x, z=z)
                        uNode.up.get_sisters()[0].add_features(x=uNode.x, y=uNode.y, z=uNode.z)
        print ast.get_ascii(attributes=["name", "x", "y", "z"])

        
            

    
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

    # Parsing rules

#    precedence = (
#        ('left','PLUS','MINUS'),
#        ('left','TIMES','DIVIDE'),
#        ('left', 'EXP'),
#        ('right','UMINUS'),
#        )


    def p_expr_E(self,p):
        """
        expr_E : expr_T expr_A
        """
        if p[2] != None: p[0] = ('divide', p[1], p[2])
        else: p[0] = p[1]

    def p_expr_A(self,p):
        """
        expr_A : DIVIDE expr_T expr_A
            | empty
        """  
        if p[1] == None: p[0] = None
        elif p[3] == None: p[0] = p[2]
        else: p[0] = ('divide', p[2], p[3])

    def p_expr_T(self,p):
        """
        expr_T : expr_F expr_B
        """    
        if p[2] != None: p[0] = ('concat', p[1], p[2])
        else: p[0] = p[1]

    def p_expr_B(self,p):
        """
        expr_B : expr_F expr_B
            | empty
        """    
        if p[1] == None: p[0] = None
        elif p[2] == None: p[0] = p[1]
        else: p[0] = ('concat', p[1], p[2])

    def p_expr_F(self,p):
        """
        expr_F : expr_I expr_G
        """    
        if p[2] != None:
            if p[2][0] == 'pu':
                p[0] = ('pu', p[1], p[2][1], p[2][2])
            elif p[2][0] == 'p':
                p[0] = ('p', p[1], p[2][1])
            else:
                p[0] = ('u', p[1], p[2][1])
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
            p[0] = ('<', p[2], '>')
        elif p[1] == '{': p[0] = ('{', p[2], '}')
        else: p[0] = p[1]
    

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

  
