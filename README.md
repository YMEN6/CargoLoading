# CargoLoading
使用贪心算法完成三维装箱问题

### 

| 时间       | 版本 | 说明                       |
| ---------- | ---- | -------------------------- |
| 2022/11/15 | 0.10 | 项目创建，算法大作业       |
| 2022/12/18 | 0.20 | 项目改进，进行算法层面优化 |

### 作业描述

```bash
算法实践题
物流公司在流通过程中，需要将打包完毕的箱子装入到一个货车的车厢中，为了提高物流效率，需要将车厢尽量填满，显然，车厢如果能被100%填满是最优的，但通常认为，车厢能够填满85%，可认为装箱是比较优化的。
设车厢为长方形，其长宽高分别为L，W，H；共有n个箱子，箱子也为长方形，第i个箱子的长宽高为li，wi，hi（n个箱子的体积总和是要远远大于车厢的体积），做以下假设和要求：
1. 长方形的车厢共有8个角，并设靠近驾驶室并位于下端的一个角的坐标为（0,0,0），车厢共6个面，其中长的4个面，以及靠近驾驶室的面是封闭的，只有一个面是开着的，用于工人搬运箱子；
2. 需要计算出每个箱子在车厢中的坐标，即每个箱子摆放后，其和车厢坐标为（0,0,0）的角相对应的角在车厢中的坐标，并计算车厢的填充率。

问题分解为基础和高级部分，完成基础部分可得78分以上，完成高级部分可得85分以上。
基础部分：
1. 所有的参数为整数；
2. 静态装箱，即从n个箱子中选取m个箱子，并实现m个箱子在车厢中的摆放（无需考虑装箱的顺序，即不需要考虑箱子从内向外，从下向上这种在车厢中的装箱顺序）；
3. 所有的箱子全部平放，即箱子的最大面朝下摆放；
4. 算法时间不做严格要求，只要1天内得出结果都可。

高级部分：
1. 参数考虑小数点后两位；
2. 实现在线算法，也就是箱子是按照随机顺序到达，先到达先摆放；
3. 需要考虑箱子的摆放顺序，即箱子是从内到外，从下向上的摆放顺序；
4. 因箱子共有3个不同的面，所有每个箱子有3种不同的摆放状态；
5. 算法需要实时得出结果，即算法时间小于等于2秒。
```

### 解题思路

##### 思路（基础部分请直接看0.10版本的README）

```bash
在基础版本的基础上，进行以下优化和改进
1）基础版本的每一层只限定使用一个箱子，实际上可以进行拼接。在这个版本里，使用这个结构来代替箱子进行Stack、Heap、Block的拼接，称为Brick
2）基础版本每次排序有点笨，添加索引机制来规避中间不必要地重复排序。
3）在2的基础上，考虑两种算法。基础版本是将所有货物进行排序，后续每添加进一个货物（在线版本），可以直接用索引插入，不排序。 另一个思路就是放弃排序，不贪心，直接按照随机走，就是随机，这个作为第二个版本
4）在1的基础上，Stack添加内部沉降功能，将大面积的下沉到下面，保证物理上的稳定性（贴合实际）
5）另一个核心问题，就是物品放置的问题。没想到最好的模型去解决，如果穷举那时间上、空间上代价也很大。那么，采用这种策略：（基础版本中，将大的那面默认为底面）
  1. 正方形的不需要考虑。非正方形时，单独箱子有6种放置方法，考虑到我是堆叠。其实堆起来只需要考虑3种（在第三维空间），然后在平面上再考虑2种（在二维空间），刚好对上，所以，Stack中需要穷举3种，Heap需要穷举2种
  2. 上述穷举将每次拼装Brick尝试6次，降低到，在Stack拼装brick时尝试3次，在Heap拼接brick时尝试2次。其实这个时候依然代价很爆炸，虽然可能导致局部最优，但依然需要削减这个计算量
  3. Stack不保留所有尝试次数，在每次拼接Stack时，每一层的brick只保留最大的那个结果。Heap同理
  4. 这里就是最大的问题了，我确定这会漏很多解，若不这么做，要么穷举，要么直接随机算法，就是随机选一个放置方法，然后迭代这个过程，去碰最优解。这个可以用遗传算法来做，这一步我就不实现了，因为上述过程已经很复杂了
6)在最后一层组装的时候，其实不一定要贪心，在这里做穷举，前面保持不动，在某些情况下也可能跳出局部最优解
```



##### 问题

```
整体可以抽象为3个问题：
1）大体上的算法，本项目采用的是贪心思维， 采用堆叠拼接实现。
2）物品放置问题，在项目里面，就是打包算法，具体放在Stack和Heap里面去做，将每次要尝试的6次，拆开在2个流程
3）拼接问题，Brick中拼接货物箱子，二维问题，在Brick中实现。
```



##### 算法缺陷

```bash
这种拼接降维的思路，忽略了每一层之间其实有缝隙可以重叠的情况。就是即使穷举了，它还是漏解。
选用这个思路是因为它不需要太高的数学门槛，大家基本都能掌握
```



##### 实际工作

```
1）6个方向没有做，考虑了高级部分要求，如果按照构思的部分穷举，也来不及处理完，而且认为穷举还真的不如随机，干脆换个随机算法，比如用遗传算法来做，而不是用贪心
2）随机到达，本来想做成那种动态的来一个，重算一次。因为作业进度问题，最后还是只是对初版进行了简单优化，没做这部分。对应的，因为没随机到达，而且一开始我就保持了最初有序，所以用来加速的索引也就顺带省掉了
3）如果要将代码从贪心改成其他的方法，只需要改变我中间Stack、Heap的顺序其实就能达到其他组合方式，其他部分代码可以复用
```
