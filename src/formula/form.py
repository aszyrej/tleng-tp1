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

if sys.version_info[0] >= 3:
    raw_input = input

import ply.lex as lex
import ply.yacc as yacc
import os

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
        lex.lex(module=self, debug=self.debug)
    #    yacc.yacc(module=self,
    #              debug=self.debug,
    #              debugfile=self.debugfile,
    #              tabmodule=self.tabmodule)

    #def run(self):
    #    while 1:
    #        try:
    #            s = raw_input('form > ')
    #        except EOFError:
    #            break
    #        if not s: continue
    #        yacc.parse(s)

    
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
    t_CHAR  = r'[a-zA-Z+-@#%&$=]'

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

    def p_expr_A(self,p):
        """
        expr_A : DIVIDE expr_T expr_A
            | empty
        """  
    
    def p_expr_T(self,p):
        """
        expr_T : expr_F expr_B
        """    

    def p_expr_B(self,p):
        """
        expr_B : expr_F expr_B
            | empty
        """    

    def p_expr_F(self,p):
        """
        expr_F : expr_I expr_G
        """    

    def p_expr_G(self,p):
        """
        expr_G : POW expr_I expr_H
            | UNDERSCORE expr_I expr_L
            | empty
        """    

    def p_expr_H(self,p):
        """
        expr_H : UNDERSCORE expr_I
            | empty
        """    

    def p_expr_L(self,p):
        """
        expr_L : POW expr_I
            | empty
        """    

    def p_expr_I(self,p):
        """
        expr_I : LPAREN expr_E RPAREN
            | LBRACK expr_E RBRACK
            | CHAR
        """

    def p_empty(p):
        'empty :'
        pass

    def p_error(self, p):
        if p:
            print("Syntax error at '%s'" % p.value)
        else:
            print("Syntax error at EOF")

if __name__ == '__main__':
    form = Form()
    #form.run()

  
