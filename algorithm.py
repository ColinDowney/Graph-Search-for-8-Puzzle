# coding: utf-8
import copy
import numpy as np
import random
from collections import deque
import sys
import unittest


class Node(object):
    """ 八数码问题图搜索过程的结点.

        Attributes:
        digits (numpy.array(3*3)): 八数码排列矩阵.
        blank (numpy.array(1*2)): digits里面0（即空格）所处的位置坐标.
        parent (Node): 父节点.
        cost (int): 该节点的耗散值.
        depth (int): 该节点的深度.
    """
    # 移动空格块的坐标变化
    move = {'up': [-1, 0], 'down': [1, 0], 'left': [0, -1], 'right': [0, 1]}

    def __init__(self, digits_square, blank_pos, parent_node=None, cost=sys.maxsize):
        self.digits = digits_square.copy()
        self.parent = parent_node
        self.blank = blank_pos.copy()
        self.cost = cost
        self.depth = 0 if not parent_node else parent_node.depth + 1

    def __eq__(self, other):
        """ Equality between nodes only depends on the digits matrix. """
        return np.array_equal(self.digits, other.digits)

    def __hash__(self):
        """ Hash of node only depends on the digits matrix. """
        return hash(tuple(sorted({k: self.__dict__[k] for k in ['digits']})))

    def __str__(self):
        """ The elements of the digits matrix are concatenated into string. """
        digits = ''
        for i in np.nditer(self.digits):
            digits += i.__str__()
        return digits

    def __repr__(self):
        """ The elements of the digits matrix are concatenated into string. """
        return '<__Node__ {0}>'.format(self.__str__)

    #TODO: check the sort direction
    def __cmp__(self, other):
        """ Compare the nodes based on the cost. """
        return self.cost < other.cost

    def set_cost(self, cost):
        self.cost = cost

    def get_cost(self):
        return self.cost

    def get_neighbor_pos(self, direction):
        """ 获得目前搜索结点的八数码矩阵的空格移动之后的坐标. """
        return self.blank + Node.move[direction.casefold()]

    def get_neighbor(self, pos):
        """ 获得目前搜索结点的八数码矩阵的空格移动到pos坐标之后的新节点. """
        digits = copy.deepcopy(self.digits)
        # 互换空格块和要移动的数码
        digits[self.blank[0], self.blank[1]] = self.digits[pos[0], pos[1]]
        digits[pos[0], pos[1]] = 0

        return Node(digits, pos, self)


class GraphSearch(object):
    """ 图搜索算法.

        Attributes:
        digits (numpy.array(3*3)): 要求解的八数码排列矩阵.
        goal (numpy.array(3*3)): 八数码排列矩阵的目标状态.
        __open (deque): open表（FIFO队列）.
        __close (dict): close表.
    """

    def __init__(self, digits_square):
        self.digits = digits_square
        self.goal = np.array([[1, 2, 3],
                              [8, 0, 4],
                              [7, 6, 5]])
        self._open = deque([])
        self._close = dict([])

    def search(self):
        """ 执行搜索算法

            返回值：list[扩展结点数，生成结点数，最后扩展到的目标结点（用来调用show_path生成解的具体路径）]
            执行失败未找到解或出错则返回空列表.
        """
        # try:
        # 检查初始状态是否是八数码
        if set(self.digits.flatten()) != set(range(9)):
            raise ValueError('传入的矩阵不是0-8数码的矩阵')

        expand_count = 0
        generate_count = 0

        # 将初始节点放入Open表
        blank = self.find_blank(self.digits)  # 查找最初的空格的位置
        root = Node(self.digits, np.array(blank), cost=0)
        root.cost = self.cal_cost(root)
        self.open_put(root)
        generate_count += 1

        while not self.open_empty():
            cur = self.open_pop()  # 从open表中取最前的结点
            if np.array_equal(cur.digits, self.goal):  # Success
                return [expand_count, generate_count, cur]
            self.close_put(cur)
            expand_count += 1

            # 扩展结点
            for direction in ['up', 'down', 'left', 'right']:  # 尝试往四个方向移动空格
                expand = cur.get_neighbor_pos(direction)
                if not (0 <= expand[0] <= 2 and 0 <= expand[1] <= 2):  # 移动超出范围
                    continue
                expand = cur.get_neighbor(expand)  # 获得扩展的结点

                expand.cost = self.cal_cost(expand)  # 计算新扩展的结点的耗散值

                generate_count += self.update_open_close(expand)  # 判断该结点是否已经在close表里面或者是open表里面

            self.open_sort()  # 如果open表的结构不会自动排序的话，要重新对open表按照结点的cost值进行排序
        # except Exception:
        #     print('Oops!')
        return []

    def update_open_close(self, expand):
        """ 判断该结点是否已经在close表里面或者是open表里面（BFS和DFS不需要判断） """
        if expand.__str__() not in self._close and not self.in_open(expand):
            self.open_put(expand)
            return 1
        else:
            return 0

    def open_empty(self):
        """ check if open is empty """
        return not self._open

    def open_pop(self):
        """ get the head of open queue
            从open表取出下一个要扩展的结点
        """
        return self._open.popleft()

    def open_put(self, node):
        """ add element to the open table """
        self._open.append(node)

    def in_open(self, node):
        """ check if node is in open table """
        return node in self._open

    def update_open(self, node):
        """ 如果现在的cost值更小，就将原本就在open表里面的node的cost值更新 """
        index = self._open.index(node)
        if node.cost < self._open[index].cost:
            del(self._open[index])
            self.open_put(node)

    def open_sort(self):
        """ 将open表按照算法要求的顺序排序 """
        pass

    def cal_cost(self, node):
        """ 按照算法的要求计算扩展出的搜索结点的耗散值 """
        return node.depth

    def close_put(self, node):
        """ add element to close table """
        self._close[node.__str__()] = node

    @staticmethod
    def show_path(node):
        """ 按照搜索得到的最终结点，一步一步打印解的步骤（输出从下往上看） """
        print(node.digits)
        cur = node.parent
        step = node.cost
        while cur is not None:
            print('\n第'+step.__str__()+'步==========')
            print(cur.digits)
            step -= 1
            cur = cur.parent

    @staticmethod
    def find_blank(digits):
        """ 查找最初的空格的位置 """
        for i in range(digits.shape[0]):
            for j in range(digits.shape[1]):
                if digits[i][j] == 0:
                    return [i, j]

    def solvable(self):
        """ 判断是否有解 """
        #sequence = []
        pass


class BFSSearch(GraphSearch):
    """ 宽度优先搜索 """
    pass


class DFSSearch(GraphSearch):
    """ 深度优先搜索 """
    def __init__(self, digits_square):
        super().__init__(digits_square)
        self._open = []

    def open_pop(self):
        temp = self._open[0]
        del self._open[0]
        return temp

    def open_sort(self):
        # 升序排序
        sorted(self._open, key=Node.get_cost, reverse=True)


class AStarSearch(GraphSearch):
    """ A*搜索基类 """

    def __init__(self, digits_square):
        super().__init__(digits_square)
        self._open = []

    def open_pop(self):
        temp = self._open[0]
        del self._open[0]
        return temp

    def open_sort(self):
        # 升序排序
        sorted(self._open, key=Node.get_cost)

    def update_open_close(self, expand):
        if expand.__str__() in self._close:
            if expand.cost < self._close[expand.__str__()].cost:
                del self._close[expand.__str__()]  # 将这个结点从close表中删除，重新放回open表里面
                self.open_put(expand)
        elif self.in_open(expand):
            self.update_open(expand)  # 如果现在的cost值更小，就将原本就在open表里面的node的cost值更新
        else:
            self.open_put(expand)
            return 1
        return 0


class AStarSearchW(AStarSearch):
    pass


class AStarSearchP(AStarSearch):
    pass


class AStarSearchS(AStarSearch):
    pass


def random_digits_array():
    """ 生成随机的八数码矩阵 """
    r = np.array(random.sample(range(9), 9))
    return r.reshape(3, 3)


if __name__ == '__main__':
    d = np.array([[8, 1, 3],
                  [7, 0, 4],
                  [6, 2, 5]], dtype=int)
    g = DFSSearch(d)
    result = g.search()  # expand, generate, final
    if not result:
        print('fail')
    else:
        GraphSearch.show_path(result[2])
        print('扩展结点数：'+result[0].__str__())
        print('生成结点数：'+result[1].__str__())

    # class A(object):
    #     def __init__(self, a, b, c):
    #         self.a = a
    #         self.b = b
    #         self.c = c
    #
    #     def __eq__(self, other):
    #         return self.a == other.a and self.b == other.b
    #
    #     def __hash__(self):
    #         return hash(tuple(sorted({k: self.__dict__[k] for k in ['a', 'b']})))
    #
    #     def __repr__(self):
    #         return self.a.__str__()+self.b.__str__()+self.c.__str__()
    #
    #     def C(self):
    #         return self.c
    #
    #     def __cmp__(self, other):
    #         return self.c < other.c
