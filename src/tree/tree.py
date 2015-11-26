class Node:
    def __init__(self,type,children=None):
         self.type = type
         self.x = 0
         self.y = 0
         self.z = 0
         self.parent = None
         self.rightSibling = None
         self.leftSibling = None

         if children:
            self.children = children
            index = 0
            for n in self.children:
                n.parent = self
                if (index-1>=0): n.leftSibling = self.children[index-1]
                if (index+1<=len(self.children)-1): n.rightSibling = self.children[index+1]
                index += 1
         else:
              self.children = [ ]

    def __str__(self):
        if (self.parent == None): par = ""
        else: par = self.parent.type
        if (self.leftSibling == None): lSib = ""
        else: lSib = self.leftSibling.type
        if (self.rightSibling == None): rSib = ""
        else: rSib = self.rightSibling.type 
        return "(type: " + self.type \
            + ", par: " + par \
            + ", lSib: " + lSib \
            + ", rSib: " + rSib \
            + ", x: " + str(self.x) \
            + ", y: " + str(self.y) \
            + ", z: " + str(self.z) \
            + ", children: " + str(self.children) \
            + ")"

    def __repr__(self):
        return self.__str__()  

    def preorder(self):
        res = [self]
        for n in self.children:
            res = res + n.preorder()
        return res     

    def has_children(self):
        return len(self.children)>0 

    def copy_node_attrs(self,node):
        self.x = node.x
        self.y = node.y
        self.z = node.z

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


        


