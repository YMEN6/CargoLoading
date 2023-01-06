# -*- coding:utf8 -*-
"""
CargoLoading 2.0
Middle structure:
    Stack:
    Heap:
    Block:
    Brick:


    拼接算法：其实都是二维问题
    判断选位置的时候不依赖坐标轴，那样太麻烦，直接参考OS内存块最佳适配算法，将块大小作为排序标准，每次找最佳的那块来适配
    放进去后，考虑缝隙问题，这个时候再考虑坐标轴。放的时候靠左靠下，将空的位置作为新的块，插回队列里


    不同砖的打包算法：
    Stack：将Cargo放进来的时候，需要考虑3种放法。流程：先判断体积，体积够了，再判断坐标，这个时候发挥作用
    Heap：Stack放进来的时候，2种放法
"""
from color import *


# 注意，Stack和Heap拼接时需要注意方向，Stack注意3个，Heap注意2个，所以他们的对应Brick中都需要注明方向，这个会影响到坐标和摆放（拼接时使用的长和宽）
class Cargo(object):
    UP = 1
    RIGHT = 2

    def __init__(self, cargo_id, length=0, width=0, height=0, dict_input=None):
        """
        接收传入一个dict或者 长、宽、高数据
        :param cargo_id: 货物编号，用于唯一标识货物
        :param length:
        :param width:
        :param height:
        :param dict_input: {"Length": xx, "Width": xx, "Height": xx, "Quantity": xx}
        """
        assert any([all([length, width, height]), dict_input]), "Expect <dict>/<length, width, length> here"
        if isinstance(dict_input, dict):
            temp_list = [dict_input["Length"], dict_input["Width"], dict_input["Height"]]
        else:
            temp_list = [length, width, height]

        temp_list.sort(reverse=True)
        self.length, self.width, self.height = temp_list
        self.vol = self.length * self.width * self.height

        self.id = cargo_id
        self.location = None
        self.parent = None

    def __str__(self):
        return "ID:{}\tLength:{}\tWidth:{}\tHeight:{}\tParent:{}\tLocation: {}".format(
            self.id, self.length, self.width, self.height, self.parent, self.location
        )


class BrickBlock(object):
    def __init__(self, length, width, height, parent):
        """
        在拼接Brick时，用于拼接算法。模拟OS最佳块匹配中的块
        :param length:
        :param width:
        :param height: height=0时，vol退化为area
        :param parent: 代表母块对应的货物编号以及方向  {"id": parent id, "direction": }
        """
        self.vol = length * width * height
        self.length = length
        self.width = width
        self.height = height
        self.parent = parent

    def is_valid(self, target):
        return all([
            target.length <= self.length,
            target.width <= self.width,
            target.height <= self.height,
            target.vol <= self.vol
        ])


class Brick(object):
    CARGO = 1
    STACK = 2

    def __init__(self, length, width, height, tp=CARGO):
        # 期望的上限长、宽、高，影响可用块
        self.length = length
        self.width = width
        self.height = height
        self.type = tp

        # queue: {"vol": []}
        self._queue = dict()
        # 初始化可用块，并插入队列
        block = BrickBlock(length, width, height, None)
        self._queue[block.vol] = [block]
        self._vol_list = [block.vol]
        self.store = dict()
        self.orders = list()

        # 真实体积
        self.vol = 0
        self.remain_max_vol = block.vol
        # 实际长、宽、高（货物用掉的）
        self.real_height = 0

    def add(self, target):
        """
        将箱子/堆叠拼接成块，如果返回False，代表放不进了
        :param target:
        :return:
        """
        # 剩余空间不够，没法加了
        assert hasattr(target, "vol")
        if target.vol > self.remain_max_vol:
            return False

        for vol in self._vol_list:
            if vol >= target.vol and len(self._queue[vol]):
                for bk in self._queue[vol]:
                    if bk.is_valid(target):
                        # 流程：块选择 -> 箱子/Stack定位 -> 块移除 -> 块分裂 -> 刷新缓存
                        target.parent = bk.parent
                        self._queue[vol].remove(bk)
                        self._split(bk, target)
                        self._queue_flush()
                        # 处理箱子/Stack
                        self.store[target.id] = target
                        self.orders.append(target.id)
                        self.vol += target.vol
                        # 其实都是同一层（偷个懒，只记录height，用于heap合并）
                        self.real_height = max(target.height, self.real_height)
                        return True
        return False

    def locate(self, *args, **kwargs):
        """
        为Brick内的对象赋予坐标
        :param args:
        :param kwargs:
        :return:
        """
        if self.type == Brick.CARGO:
            x, y, z = args
            for tid in self.orders:
                target = self.store[tid]
                # 初始快，直接赋予x, y, z
                if target.parent is None:
                    target.location = [x, y, z]
                else:
                    parent = self.store[target.parent["id"]]
                    px, py, pz = parent.location
                    # XOY平面，UP就是同X，在Y上面； RIGHT就是同Y，在X右面。 同一层，所以Z和parent都等
                    if target.parent["direction"] == Cargo.UP:
                        location = [px, py + parent.width, z]
                    else:
                        location = [px + parent.length, py, z]
                    target.location = location

        elif self.type == Brick.STACK:
            x, y = args
            for tid in self.orders:
                target = self.store[tid]
                assert isinstance(target, MyStack)
                if target.parent is None:
                    target.location = [x, y]
                else:
                    parent = self.store[target.parent["id"]]
                    px, py = parent.location
                    if target.parent["direction"] == Cargo.UP:
                        location = [px, py + parent.width]
                    else:
                        location = [px + parent.length, py]
                    target.location = location
                target.locate()
        else:
            raise Exception("Invalid brick element type, expect <Cargo, MyStack>, receive {}".format(self.type))

    def quantity(self):
        if self.type == Brick.CARGO:
            return len(self.store)
        else:
            return sum(map(lambda x: x[1].quantity(), self.store.items()))

    def _queue_flush(self):
        self._vol_list = list()
        tmp_list = list(self._queue.keys())
        for key in tmp_list:
            if len(self._queue[key]) == 0:
                self._queue.pop(key)
            else:
                self._vol_list.append(key)
        self._vol_list.sort()
        self.remain_max_vol = self._vol_list[-1] if len(self._vol_list) else 0

    def _queue_push(self, bb):
        """
        向块缓存中插入块
        :param bb:
        :return:
        """
        assert isinstance(bb, BrickBlock)
        if bb.vol not in self._queue.keys():
            self._queue[bb.vol] = list()
        self._queue[bb.vol].append(bb)

    def _split(self, block, target):
        """
        完成block的划分，并插入到queue
        贪心切分，一个矩形会被另一个矩形切割成一个正方形和2个矩形，将大的矩形和正方形进行拼接，最后得到2块
        这里做穷举代价有点高，漏解就漏解吧
        :param block:
        :param target:
        :return:
        """
        block_up = target.length * (block.width - target.width)
        block_right = target.width * (block.length - target.length)
        up = {
            "id": target.id,
            "direction": Cargo.UP
        }
        right = {
            "id": target.id,
            "direction": Cargo.RIGHT
        }
        if block_up > block_right:
            bk_up = BrickBlock(block.length, (block.width - target.width), block.height, up)
            bk_right = BrickBlock((block.length - target.length), target.width, block.height, right)
        else:
            bk_up = BrickBlock(target.length, (block.width - target.width), block.height, up)
            bk_right = BrickBlock((block.length - target.length), block.width, block.height, right)
        self._queue_push(bk_up)
        self._queue_push(bk_right)

    def __str__(self):
        usage = self.vol / (self.length * self.width * self.height) * 100
        if self.type == Brick.CARGO:
            word = green("Cargo Brick: Length({})\tWidth({})\tHeight({})\tVol({})\tUsage({:.2f}%)".format(
                self.length, self.width, self.height, self.vol, usage
            ))
        else:
            word = blue("Stack Brick: Length({})\tWidth({})\tArea({})\tUsage({:.2f}%)".format(
                self.length, self.width, self.vol, usage
            ))
        words = list()
        for _, cargo in self.store.items():
            words.append(str(cargo))
        content = "{}\n{}".format(word, "\t\t".join(words))
        return content


class MyStack(object):
    def __init__(self, stack_id: int, cargo: Cargo, limit: int):
        """
        用于初试货物组装成stack使用， height代表这个堆的高度， limit代表最高的高度，这里应该传入车厢高度
        最底层是一个Cargo，所以初始化还是要传入Cargo
        :param stack_id:
        :param cargo:
        :param limit: van.height
        """
        assert isinstance(cargo, Cargo)
        self.id = stack_id
        bottom = Brick(cargo.length, cargo.width, cargo.height, tp=Brick.CARGO)
        bottom.add(cargo)
        self.stack = [bottom]
        self.limit = limit

        self.height = cargo.height
        self.length = cargo.length
        self.width = cargo.width
        self.vol = cargo.vol
        self.brick = None

        self.parent = None
        # [x, y]
        self.location = None
        self.number = None

    def is_valid(self, cargo: Cargo):
        assert isinstance(cargo, Cargo)
        standard = self.stack[-1]
        return all([standard.length >= cargo.length,
                    standard.width >= cargo.width]) and self.height + cargo.height <= self.limit

    # ToDo 其实应该写成生成器
    def push(self, cargoes: list):
        min_height = self.limit
        while True:
            valid_cargo = list()
            for cargo in cargoes:
                if self.is_valid(cargo):
                    if self.brick is None:
                        standard = self.stack[-1]
                        self.brick = Brick(standard.length, standard.width, cargo.height, tp=Brick.CARGO)
                    if self.brick.add(cargo):
                        valid_cargo.append(cargo)
                min_height = min(min_height, cargo.height)

            # 走了一轮，连brick都加不进来，那显然后面也是白跑，可以break了
            if self.brick is None:
                break
            # 走完一轮，全都加不进了（这个版本要求cargo降序），那就将brick插入stack
            self.stack.append(self.brick)
            self.height += self.brick.height
            self.vol += self.brick.vol
            self.brick = None
            # 移除有效货物
            for cargo in valid_cargo:
                cargoes.remove(cargo)
            # 货物没了，或者最矮的货物都比剩余空间高，那就可以中断这个stack的堆叠了
            if len(cargoes) == 0 or min_height + self.height > self.limit:
                break

    def locate(self):
        x, y = self.location
        z = 0
        for brick in self.stack:
            brick.locate(x, y, z)
            z += brick.height

    def quantity(self):
        if self.number is None:
            self.number = sum(map(lambda x: x.quantity(), self.stack))
        return self.number

    def __str__(self):
        return "堆({})共{}个CargoBrick({}件货物)\t长({})宽({})高({})体积({}):\n{}".format(
            self.id, len(self.stack), self.quantity(), self.length, self.width, self.height, self.vol,
            "\n\n".join([str(brick) for brick in self.stack])
        )


class MyHeap(object):
    def __init__(self, heap_id: int, stack: MyStack, limit: int, ceiling: int):
        """
        将stack组装成heap，从二维降到一维， limit代表最大宽度
        :param heap_id:
        :param stack:
        :param limit: van.width
        :param ceiling: van.height
        """
        assert isinstance(stack, MyStack)
        self.id = heap_id
        # height = 0,让brick此时只关注面积，忽略高度
        bottom = Brick(stack.length, stack.width, ceiling, tp=Brick.STACK)
        bottom.add(stack)
        self.heap = [bottom]
        self.limit = limit
        self.ceiling = ceiling

        self.width = stack.width
        self.length = stack.length
        self.height = stack.height
        self.vol = stack.vol
        self.brick = None
        self.number = None

    def is_valid(self, stack):
        assert isinstance(stack, MyStack)
        standard = self.heap[-1]
        # return standard.length >= stack.length and self.width + stack.width <= self.limit
        return all([
            standard.length >= stack.length,
            self.width + stack.width <= self.limit,
            stack.height <= self.ceiling
        ])

    def push(self, stacks: list):
        min_width = self.limit
        while True:
            valid_stack = list()
            for stack in stacks:
                if self.is_valid(stack):
                    if self.brick is None:
                        standard = self.heap[-1]
                        self.brick = Brick(standard.length, stack.width, self.ceiling, tp=Brick.STACK)
                    if self.brick.add(stack):
                        valid_stack.append(stack)
                min_width = min(min_width, stack.width)

            if self.brick is None:
                break
            self.heap.append(self.brick)
            self.width += self.brick.width
            self.height = max(self.height, self.brick.real_height)
            self.vol += self.brick.vol
            self.brick = None
            for stack in valid_stack:
                stacks.remove(stack)
            if len(stacks) == 0 or min_width + self.width > self.limit:
                break

    def locate(self, x):
        y = 0
        for brick in self.heap:
            brick.locate(x, y)
            y += brick.width

    def quantity(self):
        if self.number is None:
            self.number = sum(map(lambda x: x.quantity(), self.heap))
        return self.number

    def __str__(self):
        return "heap({})共{}个StackBrick({}件货物)\t长({})宽({})高({})体积({}):\n{}".format(
            self.id, len(self.heap), self.quantity(), self.length, self.width, self.height, self.vol,
            "\n\n\n".join([str(brick) for brick in self.heap])
        )


class MyBlock(object):
    def __init__(self, block_id: int, heap: MyHeap, limit_length: int, limit_vol: int):
        """
        将heap组成block，将一维进行合并
        :param block_id:
        :param heap:
        :param limit_length: van.length
        :param limit_vol: van.total
        """
        assert isinstance(heap, MyHeap)
        self.id = block_id
        self.block = [heap]
        self.limit_length = limit_length
        self.limit_vol = limit_vol

        self.block_length = heap.length
        self.width = heap.width
        self.height = heap.height
        self.vol = heap.vol
        self.percent = 0
        self.number = None

    def _update_percent(self):
        self.percent = 1.0 * self.vol / self.limit_vol

    def is_valid(self, heap):
        assert isinstance(heap, MyHeap)
        return self.block_length + heap.length <= self.limit_length and self.vol + heap.vol <= self.limit_vol

    def push(self, heap):
        if self.is_valid(heap):
            self.block.append(heap)
            self.block_length += heap.length
            self.width = max(self.width, heap.width)
            self.height = max(self.height, heap.height)
            self.vol += heap.vol
            self._update_percent()
            return heap
        else:
            return None

    def locate(self):
        x = 0
        for heap in self.block:
            heap.locate(x)
            x += heap.length

    def quantity(self):
        if self.number is None:
            self.number = sum(map(lambda x: x.quantity(), self.block))
        return self.number

    def __str__(self):
        front = "Block({})共{}个heap({}件货物)\t长({}) 宽({}) 高({})\t体积({})\t利用率({:.2f}%)".format(
            self.id, len(self.block), self.quantity(), self.block_length, self.width, self.height, self.vol,
            self.percent * 100,
        )
        return "{}:\n{}".format(
            cyan(front), "\n\n\n\n".join([str(heap) for heap in self.block])
        )


class Van(object):
    def __init__(self, length=7600, width=2400, height=2400):
        """
        车厢主体，在这里其实没什么用。。。
        :param length:
        :param width:
        :param height:
        """
        self.length = length
        self.width = width
        self.height = height

        self.total = self.length * self.width * self.height
        self.used = 0
        self.vol = self.total

    def load(self, block: MyBlock):
        assert block.vol <= self.total and all([
            block.block_length <= self.length, block.width <= self.width, block.height <= self.height
        ])
        self.used = block.vol

    def usage(self):
        return 1.0 * self.used / self.total

    def __str__(self):
        return "Van: Length({}) Width({}) Height({}) Volume({}) Usage:{}({:.2f}%)".format(
            self.length, self.width, self.height,
            self.total,
            self.used,
            self.usage() * 100
        )


if __name__ == '__main__':
    c = Cargo(1, 100, 200, 300)
    s = Brick(100, 200, 300)
    s.add(c)
    print(s)
