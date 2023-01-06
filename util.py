# -*- coding:utf8 -*-
"""
将和作业算法无关的部分抽离放在这里
"""
import os
import sys
import pandas as pd

from random import randint
from datetime import datetime, timedelta
from color import *


def create_usage(x=7600, y=2400, z=2400, path="data/test.csv"):
    data = list()
    columns = ['Length', 'Width', 'Height', 'Quantity']
    limit = x * y * z
    limit *= 10
    vol = 0
    while vol < limit:
        ix = randint(1, round(x / 5))
        iy = randint(1, round(y / 10))
        iz = randint(1, round(z / 10))
        i_vol = ix * iy * iz
        quantity = randint(0, 4)
        data.append([ix, iy, iz, quantity])
        vol += (i_vol * quantity)
    df = pd.DataFrame(data=data, columns=columns)
    df.to_csv(path, index=False)


class Util(object):
    def __init__(self, path):
        if os.path.exists(path):
            self.df = pd.read_csv(path)
        else:
            print("File <{}> not exist".format(path))
            sys.exit(1)

    def get(self):
        assert isinstance(self.df, pd.DataFrame)
        return self.df.to_dict("records")


def timer(func):
    """
    装饰器，用于计时，输出时间
    :param func:
    :return:
    """
    def wrapper(self, *args, **kwargs):
        start = datetime.now()
        ret = func(self, *args, **kwargs)
        end = datetime.now()
        print(green("function {} cost {} s".format(func.__name__, (end - start).total_seconds())))
        return ret
    return wrapper


if __name__ == '__main__':
    create_usage(path="data/test2.csv")