import unittest
import sys
sys.path.insert(0,"../tree")
sys.path.insert(0,"../formula")

from tree import Tree
from tree import Node
from form import Form

class TestParser(unittest.TestCase):
    '''
    Testeando que los arboles AST sean generados correctamente a partir de varias expresiones.
    '''

    @classmethod
    def setUpClass(self):
        self.form = Form()

    def test_concat(self):
        exp = "ABCD"
        ast = self.form.parse(exp)
        ns = ast.root.preorder()
        res_actual = [n.type for n in ns]
        res_expected = ["concat", "A", "concat", "B", "concat", "C", "D"]
        self.assertEqual(res_actual, res_expected)

    def test_divide(self):
        exp = "A/B"
        ast = self.form.parse(exp)
        ns = ast.root.preorder()
        res_actual = [n.type for n in ns]
        res_expected = ["divide", "A", "B", "barra"]
        self.assertEqual(res_actual, res_expected)

    def test_superindice(self):
        exp = "A^B"
        ast = self.form.parse(exp)
        ns = ast.root.preorder()
        res_actual = [n.type for n in ns]
        res_expected = ["p", "A", "B"]
        self.assertEqual(res_actual, res_expected)

    def test_subindice(self):
        exp = "A_B"
        ast = self.form.parse(exp)
        ns = ast.root.preorder()
        res_actual = [n.type for n in ns]
        res_expected = ["u", "A", "B"]
        self.assertEqual(res_actual, res_expected)

    def test_parentesis(self):
        exp = "(A)"
        ast = self.form.parse(exp)
        ns = ast.root.preorder()
        res_actual = [n.type for n in ns]
        res_expected = ["parens", "(", "A", ")"]
        self.assertEqual(res_actual, res_expected)

    def test_llaves(self):
        exp = "{A/B}C"
        ast = self.form.parse(exp)
        ns = ast.root.preorder()
        res_actual = [n.type for n in ns]
        res_expected = ['concat', 'brackets', '{', 'divide', 'A', 'B', 'barra', '}', 'C']
        self.assertEqual(res_actual, res_expected)

    def test_llaves(self):
        exp = "(A/B)C"
        ast = self.form.parse(exp)
        ns = ast.root.preorder()
        res_actual = [n.type for n in ns]
        res_expected = ['concat', 'parens', '(', 'divide', 'A', 'B', 'barra', ')', 'C']
        self.assertEqual(res_actual, res_expected)

    def test_super_sub_indice(self):
        exp = "A^B_C"
        ast = self.form.parse(exp)
        ns = ast.root.preorder()
        res_actual = [n.type for n in ns]
        res_expected = ["pu", "A", "B", "C"]
        self.assertEqual(res_actual, res_expected)

    def test_combinado1(self):
        exp = "(A^BC^D/E^F_G+H)I"
        ast = self.form.parse(exp)
        ns = ast.root.preorder()
        res_actual = [n.type for n in ns]
        res_expected = ["concat", "parens", "(", "divide", "concat", "p", "A", "B", "p", "C", "D", "concat", "pu", "E", "F", "G", "concat", "+", "H", "barra", ")", "concat", "", "I"]
        self.assertEqual(res_actual, res_expected)

    def test_combinado1(self):
        exp = "(A^BC^D/E^F_G+H)-I"
        ast = self.form.parse(exp)
        ns = ast.root.preorder()
        res_actual = [n.type for n in ns]
        res_expected = ["concat", "parens", "(", "divide", "concat", "p", "A", "B", "p", "C", "D", "concat", "pu", "E", "F", "G", "concat", "+", "H", "barra", ")", "concat", "-", "I"]
        self.assertEqual(res_actual, res_expected)

    def test_combinado2(self):
        exp = "(A^{BC})"
        ast = self.form.parse(exp)
        ns = ast.root.preorder()
        res_actual = [n.type for n in ns]
        res_expected = ['parens', '(', 'p', 'A', 'brackets', '{', 'concat', 'B', 'C', '}', ')']
        self.assertEqual(res_actual, res_expected)

    def test_combinado3(self):
        exp = "({A/B/C}{D/E})^{J+K}"
        ast = self.form.parse(exp)
        ns = ast.root.preorder()
        res_actual = [n.type for n in ns]
        res_expected = ['p', 'parens','(', 'concat', 'brackets', '{', 'divide', 'A', 'divide', 'B', 'C', 'barra', 'barra', '}', 'brackets', '{', 'divide', 'D', 'E', 'barra', '}', ')', 'brackets', '{', 'concat', 'J', 'concat', '+', 'K', '}']
        self.assertEqual(res_actual, res_expected)

    def test_expresion_invalida1(self):
        exp = "^B"
        self.assertRaises(Exception, lambda: self.form.parse(exp)) 

    def test_expresion_invalida2(self):
        exp = "A^B^C"
        self.assertRaises(Exception, lambda: self.form.parse(exp)) 

    def test_expresion_invalida3(self):
        exp = "A_B_C"
        self.assertRaises(Exception, lambda: self.form.parse(exp))

if __name__ == '__main__':
    unittest.main()