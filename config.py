# -*- coding:utf8 -*-

from process import *

schema = {
    "test": {
        "path": "data/data.csv",
        "sort": True,
        "leach": False
    },
    "test2": {
        "path": "data/test2.csv",
        "sort": True,
        "leach": True
    },
    # 这个例子里，同一个数据集，sort最高是76 ，不sort是56，差距有点大
    "sorted": {
        "path": "data/test3.csv",
        "sort": True,
        "leach": True
    },
    "random": {
        "path": "data/test3.csv",
        "sort": False,
        "leach": False
    },
    # 放了貌似6万个箱子进去，最高能到八十多，这个改过的版本在笔记本上跑不动，这也是我没往后面继续写的原因
    "big data": {
        "path": "data/test.csv",
        "sort": False,
        "leach": False
    },

    # 以下是课程相关 E1
    # 68.85%
    "E1-1": {
        "path": "data/E1-1.csv",
        "sort": True,
        "leach": True,
        "van": Van(587, 233, 220),
    },
    # 81.74%
    "E1-2": {
        "path": "data/E1-2.csv",
        "sort": True,
        "leach": True,
        "van": Van(587, 233, 220),
    },
    # 85.15%
    "E1-3": {
        "path": "data/E1-3.csv",
        "sort": True,
        "leach": True,
        "van": Van(587, 233, 220),
    },
    # 85.15%
    "E1-4": {
        "path": "data/E1-4.csv",
        "sort": True,
        "leach": True,
        "van": Van(587, 233, 220),
    },
    # 75.35%
    "E1-5": {
        "path": "data/E1-5.csv",
        "sort": True,
        "leach": True,
        "van": Van(587, 233, 220),
    },
    # 我后面看了看。。本质上和我的随机生成没什么区别，所以后面的我就不写入了，直接提供让用户自己输入的方案

    # E2
    # 79.51
    "E2-1": {
        "path": "data/E2-1.csv",
        "sort": True,
        "leach": True,
        "van": Van(587, 233, 220)
    },
    # 75.96
    "E2-2": {
        "path": "data/E2-2.csv",
        "sort": True,
        "leach": True,
        "van": Van(587, 233, 220)
    },
    # 84.77
    "E2-3": {
        "path": "data/E2-3.csv",
        "sort": True,
        "leach": True,
        "van": Van(587, 233, 220)
    },
    # 73.10
    "E2-4": {
        "path": "data/E2-4.csv",
        "sort": True,
        "leach": True,
        "van": Van(587, 233, 220)
    },
    # 74.71
    "E2-5": {
        "path": "data/E2-5.csv",
        "sort": True,
        "leach": True,
        "van": Van(587, 233, 220)
    },

    # E3
    # 81.89
    "E3-1": {
        "path": "data/E3-1.csv",
        "sort": True,
        "leach": True,
        "van": Van(587, 233, 220)
    },
    # 74.67
    "E3-2": {
        "path": "data/E3-2.csv",
        "sort": True,
        "leach": True,
        "van": Van(587, 233, 220)
    },
    # 75.95
    "E3-3": {
        "path": "data/E3-3.csv",
        "sort": True,
        "leach": True,
        "van": Van(587, 233, 220)
    },
    # 67.96
    "E3-4": {
        "path": "data/E3-4.csv",
        "sort": True,
        "leach": True,
        "van": Van(587, 233, 220)
    },
    # 76.35
    "E3-5": {
        "path": "data/E3-5.csv",
        "sort": True,
        "leach": True,
        "van": Van(587, 233, 220)
    },

    # E4
    # 79.45
    "E4-1": {
        "path": "data/E4-1.csv",
        "sort": True,
        "leach": True,
        "van": Van(587, 233, 220)
    },
    # 68.8
    "E4-2": {
        "path": "data/E4-2.csv",
        "sort": True,
        "leach": True,
        "van": Van(587, 233, 220)
    },
    # 73.6
    "E4-3": {
        "path": "data/E4-3.csv",
        "sort": True,
        "leach": True,
        "van": Van(587, 233, 220)
    },
    # 78.06
    "E4-4": {
        "path": "data/E4-4.csv",
        "sort": True,
        "leach": True,
        "van": Van(587, 233, 220)
    },
    # 82.17
    "E4-5": {
        "path": "data/E4-5.csv",
        "sort": True,
        "leach": True,
        "van": Van(587, 233, 220)
    },

    # E5
    # 77.96
    "E5-1": {
        "path": "data/E5-1.csv",
        "sort": True,
        "leach": True,
        "van": Van(587, 233, 220)
    },
    # 77.94
    "E5-2": {
        "path": "data/E5-2.csv",
        "sort": True,
        "leach": True,
        "van": Van(587, 233, 220)
    },
    # 79.36
    "E5-3": {
        "path": "data/E5-3.csv",
        "sort": True,
        "leach": True,
        "van": Van(587, 233, 220)
    },
    # 68.95
    "E5-4": {
        "path": "data/E5-4.csv",
        "sort": True,
        "leach": True,
        "van": Van(587, 233, 220)
    },
    # 76.12
    "E5-5": {
        "path": "data/E5-5.csv",
        "sort": True,
        "leach": True,
        "van": Van(587, 233, 220)
    },

}
