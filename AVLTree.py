############## Preface from instructor #############
# This code is quoted from 7.13 and 7.17 in M&R, but
# with some small changes. I added an AVLTreeNode
# class derived from TreeNode. This was done to include
# the balance_factor attribute, without which the code
# cannot run as listed in the text. I also changed methods
# AVLTree._put and AVLTree.put to use the added
# AVLTreeNode class instead of TreeNode.

# Generally, this is a common use for derived classes
# that an everyday programmer (rather than a library
# developer) would encounter. The off-the-shelf class
# isn't quite what we needed, but we only need to add
# a few things to make it right. A derived class saves
# the effort of doing most of the class again, and
# is generally safer than doing it ourselves anyway.

from BST import TreeNode, BinarySearchTree

class AVLTreeNode(TreeNode):
    def __init__(self, key, value, balance_factor=0, left=None, right=None, parent=None):
        super().__init__(key, value, left=left, right=right, parent=parent)
        self.balance_factor = balance_factor


class AVLTree(BinarySearchTree):
    def __init__(self):
        super().__init__()


    def _put(self, key, value, current_node):
        if key < current_node.key:
            if current_node.left_child:
                self._put(key, value, current_node.left_child)
            else:
                current_node.left_child = AVLTreeNode(
                    key, value, 0, parent=current_node
                )
                self.update_balance(current_node.left_child)
        else:
            if current_node.right_child:
                self._put(key, value, current_node.right_child)
            else:
                current_node.right_child = AVLTreeNode(
                    key, value, 0, parent=current_node
                )
                self.update_balance(current_node.right_child)

    def put(self, key, value):
        if self.root:
            self._put(key, value, self.root)
        else:
            self.root = AVLTreeNode(key, value)
        self.size = self.size + 1

    def update_balance(self, node):
        if node.balance_factor > 1 or node.balance_factor < -1:
            self.rebalance(node)
            return
        if node.parent:
            if node.is_left_child():
                node.parent.balance_factor += 1
            elif node.is_right_child():
                node.parent.balance_factor -= 1

            if node.parent.balance_factor != 0:
                self.update_balance(node.parent)

    def rotate_left(self, rotation_root):
        new_root = rotation_root.right_child
        rotation_root.right_child = new_root.left_child
        if new_root.left_child:
            new_root.left_child.parent = rotation_root
        new_root.parent = rotation_root.parent
        if rotation_root.is_root():
            self.root = new_root
        else:
            if rotation_root.is_left_child():
                rotation_root.parent.left_child = new_root
            else:
                rotation_root.parent.right_child = new_root
        new_root.left_child = rotation_root
        rotation_root.parent = new_root
        rotation_root.balance_factor = (
            rotation_root.balance_factor + 1 - min(new_root.balance_factor, 0)
        )
        new_root.balance_factor = (
            new_root.balance_factor + 1 + max(rotation_root.balance_factor, 0)
        )

    def rotate_right(self, rotation_root):
        """Don't change the definition here. Instead, override it in
        the AVLTreeUnique class (in file HW3WordFrequencies.py).

        This would be a bad decision in production software but since
        this is just a homework assignment we can live with it. (This
        way you are only changing one file.)

        Of course, AVLTreeUnique objects will work fine, but without
        this method, AVLTree objects won't be able to rebalance."""
        raise NotImplementedError

    def rebalance(self, node):
        if node.balance_factor < 0:
            if node.right_child.balance_factor > 0:
                self.rotate_right(node.right_child)
                self.rotate_left(node)
            else:
                self.rotate_left(node)
        elif node.balance_factor > 0:
            if node.left_child.balance_factor < 0:
                self.rotate_left(node.left_child)
                self.rotate_right(node)
            else:
                self.rotate_right(node)

