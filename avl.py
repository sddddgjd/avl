class Node():
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

class AVL():
    def __init__(self):
        self.node = None
        self.height = -1
        self.balance = 0
    
    def isLeaf(self):
        return self.height == 0

    def insert(self, key):
        tree = self.node
        node = Node(key)

        if tree == None:
            self.node = node
            self.node.left = AVL()
            self.node.right = AVL()
        elif key < tree.key:
            self.node.left.insert(key)
        elif key > tree.key:
            self.node.right.insert(key)

        #rebalansam arborele dupa insertie
        self.rebalance()

    def rebalance(self):
        self.updateHeights(False)
        self.updateBalances(False)
        while self.balance < -1 or self.balance > 1:
            if self.balance > 1:
                if self.node.left.balance < 0:
                    self.node.left.rotateLeft()
                    self.updateHeights()
                    self.updateBalances()
                self.rotateRight()
                self.updateHeights()
                self.updateBalances()

            if self.balance < -1:
                if self.node.right.balance > 0:
                    self.node.right.rotateRight()
                    self.updateHeights()
                    self.updateBalances()
                self.rotateLeft()
                self.updateHeights()
                self.updateBalances()

    def rotateRight(self):
        A = self.node
        B = self.node.left.node
        T = B.right.node

        self.node = B
        B.right.node = A
        A.left.node = T

    def rotateLeft(self):
        A = self.node
        B = self.node.right.node
        T = B.left.node

        self.node = B
        B.left.node = A
        A.right.node = T

    #updatam intaltimea fiecarui subarbore
    def updateHeights(self, deep=True):
        if not self.node == None:
            if deep:
                if self.node.left != None:
                    self.node.left.updateHeights()
                if self.node.right != None:
                    self.node.right.updateHeights()

            self.height = max(self.node.left.height,
                              self.node.right.height) + 1
        else:
            self.height = -1

    #updatam balance-ul fiecarui subarbore
    def updateBalances(self, recurse=True):
        if not self.node == None:
            if recurse:
                if self.node.left != None:
                    self.node.left.updateBalances()
                if self.node.right != None:
                    self.node.right.updateBalances()

            self.balance = self.node.left.height - self.node.right.height
        else:
            self.balance = 0

    def delete(self, key):
        if self.node != None:
            if self.node.key == key:
                if self.node.left.node == None and self.node.right.node == None:
                    self.node = None  # stergem frunza
                # daca mai avem doar un subarbore, alegem acel arbore
                elif self.node.left.node == None:
                    self.node = self.node.right.node
                elif self.node.right.node == None:
                    self.node = self.node.left.node
                # daca avem doi alegem succesorul
                else:
                    replacement = self.successor(self.node)
                    self.node.key = replacement.key

                    # stergem valoarea alesa recursiv
                    self.node.right.delete(replacement.key)

                #rebalansam mereu arborele dupa
                self.rebalance()
                return
            elif key < self.node.key:
                self.node.left.delete(key)
            elif key > self.node.key:
                self.node.right.delete(key)

            self.rebalance()
        else:
            return

    def predecessor(self, node):
        node = node.left.node

        while node.right != None:
            if node.right.node == None:
              return node
            else:
              node = node.right.node
        return node

    def successor(self, node):
        node = node.right.node
        
        while node.left != None:
            if node.left.node == None:
              return node
            else:
              node = node.left.node
        return node

    def inorder(self):
        if self.node == None:
            return []

        result = []

        left = self.node.left.inorder()
        for key in left:
            result.append(key)

        result.append(self.node.key)

        right = self.node.right.inorder()
        for key in right:
            result.append(key)

        return result


tree = AVL()

data = [7, 5, 2, 6, 3, 4, 1, 8, 9, 0]
for i in data:
    tree.insert(i)

tree.delete(3)
tree.delete(8)

print("Sortat", tree.inorder())
