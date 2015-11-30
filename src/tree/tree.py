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
        return "(type: " + self.type \
            + ", attrs: " + str(self.attrs) \
            + ", children" + str(self.children) \
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
        for n in self.preorder():
            n.attrs['x'] += x
            n.attrs['y'] += y
            if 'x1' in n.attrs:
                n.attrs['x1'] += x
            if 'x2' in n.attrs:
                n.attrs['x2'] += x
            if 'y1' in n.attrs:
                n.attrs['y1'] += y
            if 'y2' in n.attrs:
                n.attrs['y2'] += y

    def find_higher_and_lower_attrs(self):
        res = {}
        for n in self.preorder():
            for a in n.attrs.keys():
                if not(a in res):
                    res[a] = [None]*2
                if res[a][0]==None or res[a][0]>n.attrs[a]:                   
                    res[a][0] = n.attrs[a]
                if res[a][1]==None or res[a][1]<n.attrs[a]:
                    res[a][1] = n.attrs[a]
        return res 

    def branch_has_type(self, types):
        index = 0
        for n in self.preorder():
            if index!=0:
                for t in types:
                    if n.type == t:
                        return True
            index+=1
        return False


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


        


