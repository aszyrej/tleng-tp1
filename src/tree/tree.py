class Node:
    def __init__(self,type,children=None):
         self.type = type
         self.attrs = {}
         self.parent = None
         self.right_sibling = None
         self.left_sibling = None

         if children:
            self.children = children
            index = 0
            for n in self.children:
                n.parent = self
                if (index-1>=0): n.left_sibling = self.children[index-1]
                if (index+1<=len(self.children)-1): n.right_sibling = self.children[index+1]
                index += 1
         else:
              self.children = [ ]

    def __str__(self):
        if (self.parent == None): par = ""
        else: par = self.parent.type
        if (self.left_sibling == None): lSib = ""
        else: lSib = self.left_sibling.type
        if (self.right_sibling == None): rSib = ""
        else: rSib = self.right_sibling.type 
        return "(type: " + self.type \
            + ", par: " + par \
            + ", lSib: " + lSib \
            + ", rSib: " + rSib \
            + ", children: " + str(self.children) \
            + ")"

    def __repr__(self):
        return self.__str__()  

    def first_child(self):
        return self.children[0]

    def last_child(self):
        return self.children[-1]

    def first_sibling(self):
        return self.parent.children[0]

    def last_sibling(self):
        return self.parent.children[-1]

    def move(self,x,y):
        self.attrs['x'] += x
        self.attrs['y'] += y
        if 'x1' in self.attrs:
            self.attrs['x1'] += x
        if 'x2' in self.attrs:
            self.attrs['x2'] += x
        if 'y1' in self.attrs:
            self.attrs['y1'] += y
        if 'y2' in self.attrs:
            self.attrs['y2'] += y
        for n in self.children:
            n.move(x,y)

    def preorder(self):
        res = [self]
        for n in self.children:
            res = res + n.preorder()
        return res     

    def has_children(self):
        return len(self.children)>0 

    def copy_node_attrs(self,node):
        for k in node.attrs.keys():
            self.attrs[k] = node.attrs[k]

    def check_type_in_children(self,type):
        for n in self.children:
            if n.type == type: return True
        return False

class Tree:
    def __init__(self, root):
        self.root = root

    def get_root(self):
        return self.root

    def __str__(self):
        return str(self.root)

    def __repr__(self):
        return self.__str__()

    def preorder_traversal(self):
        return self.root.preorder()


        


