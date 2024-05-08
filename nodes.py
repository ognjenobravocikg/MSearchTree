class MNode:
    def __init__(self,m):
        self.keys=[]
        self.children=[]
        self.m=m                

    def isLeaf(self):
        if len(self.children) == 0:
            return 0
        return 1

    def insertKey(self, key):
        if (len(self.keys)>self.m):
            self.keys.append(key)
            self.redistribute()
        else:
            self.keys.append(key)
            self.keys.sort()

    def isFull(self, key):
        return (len(self.keys)==self.m)
    
    def isEmpty(self, key):
        return (len(self.keys)==0)

    def redistribute(self):
        middle_index = len(self.keys) // 2 
        left_keys = self.keys[:middle_index]
        right_keys = self.keys[middle_index+1:]

        left = MNode(self.m)
        left.keys = left_keys
        left.children = self.children[:middle_index+1]

        right = MNode(self.m)
        right.keys = right_keys
        right.children = self.children[middle_index+1:]

        middle_key = self.keys[middle_index]  
        self.keys = [middle_key] 
        self.children = [left, right]

    def print_tree(self, depth=0, position=None):
        tree_str = ""
        indent = "  " * depth
        if position is None:
            tree_str += f"{indent}Root: Keys: {self.keys}\n"
        else:
            tree_str += f"{indent}{position.capitalize()} Child: Keys: {self.keys}\n"
        for i, child in enumerate(self.children):
            if child:
                tree_str += child.print_tree(depth + 1, "left" if i == 0 else "right")
        return tree_str

    def __repr__(self):
        return f"Keys: {self.keys}, Children: {len(self.children)}"

class MSearchTree:
    def __init__(self, m):
        self.root = MNode(m)

    def get_root(self):
        return self.root


