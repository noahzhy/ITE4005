# Data Science Notes

> Hanyang University, Haoyu Zhang

## Frequent Pattern Analysis  (频繁模式分析)

**Frequent pattern**: a pattern that occurs frequently in a data set.

在数据集中频繁出现的模式。

**Motivation**: Finding inherent regularities in data.

寻找数据固有的规律。

**Applications**: Basket data analysis, cross-marketing, catalog design, sale campaign analysis, etc.

### Frequent Patterns and Association Rules (频繁模式和关联规则)

 <img src="C:\Users\e-it\AppData\Roaming\Typora\typora-user-images\image-20200525171852583.png" alt="image-20200525171852583" style="zoom: 80%;" />
* Itemset X = {$x_1$, ..., $x_k$}
* Find all the association rules X -> Y with **minimum support** and **confidence**
	* **support**, s, *probability* that a transaction contains X ∪ Y 
	* **confidence**, c, *conditional probability* that a transaction having X also contains Y

Let  $sup_{min}$ = 50%,  $conf_{min}$ = 50%
Freq. Pat.: {A:3, B:3, D:4, E:3, AD:3}
Association rules: 
    A -> D  (60%, 100%)
    D -> A  (60%, 75%)

### Closed Patterns and Max-Patterns (闭频繁集 和 极大频繁集)

**Closed Patterns**: 频繁集：大于最小支持率 ($sup_{min}$)

## Algorithms

### Apriori algorithm (先验算法)

Apriori是一种基于交易数据库进行频繁项集挖掘和关联规则学习的算法。算法识别数据库中经常出现的频繁项，并将它们扩展为更大的频繁项集。

<img src="notes\Snipaste_2020-03-29_20-01-27.png" style="zoom:60%;" />



