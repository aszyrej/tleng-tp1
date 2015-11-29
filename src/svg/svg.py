import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, tostring

class SVG:

    def __init__(self):
        root = Element('svg')
        root.set('xmlns', 'http://www.w3.org/2000/svg')
        root.set('version', '1.1')
        child = SubElement(root, 'g')
        child.set('transform', 'translate(0,200) scale(200)')
        child.set('font-family', 'Courier')
        self.tree = ET.ElementTree(root)
        self.gElement = child

    def appendText(self, char, x, y, fontSize, translateX=0, translateY=0, scaleX=0, scaleY=0):
        text = SubElement(self.gElement, 'text')
        text.text = char
        text.set('x', x)
        text.set('y', y)
        text.set('font-size', fontSize)
        if (translateX != 0 and translateY != 0 and scaleX != 0 and scaleY !=0):
            text.set('transform', 'translate('+translateX+','+translateY+') scale('+scaleX+','+scaleY+')')

    def appendLine(self,x1,y1,x2,y2):
        line = SubElement(self.gElement, 'line')
        line.set('x1',x1)
        line.set('x2',x2)
        line.set('y1',y1)
        line.set('y2',y2)
        line.set('stroke-width','0.03')
        line.set('stroke', 'black')

    def toString(self):
        root = self.tree.getroot()
        return tostring(root)

    def save(self, name):
        self.tree.write(name, xml_declaration=True)

class SVGBuilder:

    def build(self, tree):
        svg = SVG()
        ns = tree.preorder_traversal()
        for node in ns:
            if node.type == 'concat':
                pass
            elif node.type == 'divide':
                pass
            elif node.type == 'p':
                pass
            elif node.type == 'u':
                pass
            elif node.type == 'pu':
                pass
            elif node.type == '<>':
                pass
            elif node.type == '{}':
                pass
            else:
                if (node.type == 'barra'):
                    svg.appendLine(str(node.attrs['x1']), str(node.attrs['y1']), str(node.attrs['x2']), str(node.attrs['y2']))
                elif (node.type == '(' or node.type == ')'):
                    largo_paren = float(node.attrs['y2'])-float(node.attrs['y1'])+float(node.attrs['z'])
                    y = largo_paren-float(node.attrs['z'])
                    
                    if node.type == '(':
                        svg.appendText('(', '0', '0', str(node.attrs['z']), str(node.attrs['x']), str(y), str(node.attrs['z']), str(largo_paren))
                    else:
                        svg.appendText(')', '0', '0', str(node.attrs['z']), str(node.attrs['x']), str(y), str(node.attrs['z']), str(largo_paren))
                elif (node.type != 'brackets' and node.type != 'parens' and node.type != '{' and node.type != '}'):
                    svg.appendText(node.type, str(node.attrs['x']), str(node.attrs['y']), str(node.attrs['z']))

        return svg

        

