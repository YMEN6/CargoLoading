# -*- coding:utf8 -*-
"""
将算法部分放在这里
"""

from util import *
from structure import *


# 算法开始
class Solution(object):
    def __init__(self, path="data/data.csv", sort=True, leach=False, van=None):
        self.boxes = dict()
        self.sort = sort
        self.leach = leach

        # 从三维降到二维，同一个stack的拥有相同的x, y坐标，对应length、width ，z坐标需要自行计算，对应height
        # stack中的顺序实际对应为从下往上
        self.valid_boxes = list()
        self.stack = dict()
        # 从二维降到一维，同一个heap的拥有相同的y，对应width
        self.valid_stacks = list()
        self.heap = dict()
        # 一维降维到点
        self.valid_heaps = list()
        self.block = dict()
        self.valid_blocks = list()

        self.van = Van() if van is None else van

        self._init(path)

    def _init(self, path):
        """
        初始化函数，这里直接从csv中读取数据
        也可以使用自定义来替代掉这里的数据源
        :param path:
        :return:
        """
        tool = Util(path)
        cargo_id = 0
        for d in tool.get():
            for i in range(d["Quantity"]):
                cargo = Cargo(cargo_id, dict_input=d)
                self.boxes[cargo.id] = cargo
                self.valid_boxes.append(cargo)
                cargo_id += 1

        if self.sort:
            self.valid_boxes.sort(key=lambda x: x.vol, reverse=True)

    def _make_stack(self):
        """
        将cargo堆叠成stack，完成三维降维
        :return:
        """
        stack_id = 0
        valid_boxes_length = len(self.valid_boxes)
        while valid_boxes_length > 0:
            outer_cargo = self.valid_boxes.pop(0)
            stack = MyStack(stack_id, outer_cargo, self.van.height)
            stack.push(self.valid_boxes)
            valid_boxes_length = len(self.valid_boxes)
            self.stack[stack_id] = stack
            self.valid_stacks.append(stack)
            stack_id += 1

        if self.sort:
            self.valid_stacks.sort(key=lambda x: x.vol, reverse=True)

    def _make_heap(self):
        """
        将stack近一步拼接成heap，完成二维降维，将问题简化为一维上的背包问题
        :return:
        """
        heap_id = 0
        valid_stack_length = len(self.valid_stacks)
        while valid_stack_length > 0:
            outer_stack = self.valid_stacks.pop(0)
            heap = MyHeap(heap_id, outer_stack, self.van.width, self.van.height)
            heap.push(self.valid_stacks)
            valid_stack_length = len(self.valid_stacks)
            self.heap[heap_id] = heap
            heap_id += 1

        self.valid_heaps = list(self.heap.keys())
        if self.sort:
            self.valid_heaps.sort(key=lambda x: self.heap[x].vol, reverse=True)

    def _make_block(self):
        """
        背包问题，最后装到包里，这里复用初版的代码
        :return:
        """
        block_id = 0
        valid_heap_length = len(self.valid_heaps)
        while valid_heap_length > 0:
            outer_id = self.valid_heaps[0]
            block = MyBlock(block_id, self.heap[outer_id], self.van.length, self.van.total)
            j = 1
            while valid_heap_length > 0 and valid_heap_length > j:
                inner_id = self.valid_heaps[j]
                if block.push(self.heap[inner_id]) is not None:
                    del self.valid_heaps[j]
                else:
                    j += 1

                valid_heap_length = len(self.valid_heaps)

            del self.valid_heaps[0]
            self.block[block_id] = block
            block.locate()
            block_id += 1
            valid_heap_length = len(self.valid_heaps)

        self.valid_blocks = list(self.block.keys())
        self.valid_blocks.sort(key=lambda x: self.block[x].vol, reverse=True)

    @timer
    def run(self):
        """
        将货物都装上车，每个block实际上就是对应一个车厢。 装箱后按照装箱利用率从高到低排列，并将第一个（最高的）放入车厢van中
        :return:
        """
        self._make_stack()
        self._make_heap()
        self._make_block()
        content = list()
        for bid, block in self.block.items():
            assert isinstance(block, MyBlock)
            # 过滤掉利用率低于60%的情况
            if self.leach and block.percent < 0.6:
                break
            else:
                content.append("Block: {}\n{}".format(bid, block))

        interval = "#" * 100
        word = f"\n{interval}\n".join(content)
        print(word)

        print("\n\n")
        self.van.load(self.block[self.valid_blocks[0]])
        print(yellow(str(self.van)))


if __name__ == '__main__':
    # 写成交互型，提供几个选项：自己测试版本，上面给的几个数据的版本，注意车厢大小
    van = Van(587, 233, 220)
    s = Solution("data/E1-5.csv", leach=True, sort=True, van=van)
    s.run()

