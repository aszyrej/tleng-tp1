import unittest
import os

class TestSVG(unittest.TestCase):
    
    def test_case1(self):
        os.system('python ../formula/form.py "AVIONES/BARCOS"')
        res_actual = os.system("diff form.svg imgs/caso1.svg")
        self.assertEqual(res_actual, 0)
        os.system('rm form.svg')

    def test_case2(self):
        os.system('python ../formula/form.py "MAR/AGUA+SAL"')
        res_actual = os.system("diff form.svg imgs/caso2.svg")
        self.assertEqual(res_actual, 0)
        os.system('rm form.svg')

    def test_case3(self):
        os.system('python ../formula/form.py "VIENTO^{FUERTE}/VELERO_{EN+PROBLEMAS}"')
        res_actual = os.system('diff form.svg imgs/caso3.svg')
        self.assertEqual(res_actual, 0)
        os.system('rm form.svg')

    def test_case4(self):
        os.system('python ../formula/form.py "SUPER^{HEROE}_{VILLANO}"')
        res_actual = os.system('diff form.svg imgs/caso4.svg')
        self.assertEqual(res_actual, 0)
        os.system('rm form.svg')

    def test_case5(self):
        os.system('python ../formula/form.py "(A^BC^D/E^F_G+H)-I"')
        res_actual = os.system('diff form.svg imgs/caso5.svg')
        self.assertEqual(res_actual, 0)
        os.system('rm form.svg')

    def test_case6(self):
        os.system('python ../formula/form.py "(A^BC^D/E^F_G+{H/J})-I"')
        res_actual = os.system('diff form.svg imgs/caso6.svg')
        self.assertEqual(res_actual, 0)
        os.system('rm form.svg')

    
if __name__ == '__main__':
    unittest.main()