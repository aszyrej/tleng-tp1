from lxml import etree
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

#ejCatedra
#svg = SVG()
#svg.appendText('(','0','0','1','0', '1.36875', '1', '2.475')
#svg.appendText('A','.69','.53','1')
#svg.appendText('B','1.29','0.08','.7')
#svg.appendText('C','1.71','.53','1')
#svg.appendText('D','2.31','0.08','.7')
#svg.appendLine('0.6','0.72','2.82','.72')
#svg.appendText('E','.6','1.68','1')
#svg.appendText('G','1.2','1.93','.7')
#svg.appendText('F','1.2','1.23','.7')
#svg.appendText('+','1.62','1.68','1')
#svg.appendText('H','2.22','1.68','1')
#svg.appendText(')','0','0','1','2.82', '1.36875', '1', '2.475')
#svg.appendText('-','3.42','1','1')
#svg.appendText('I','4.02','1','1')
#svg.save('test.svg')
		

