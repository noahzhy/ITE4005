# Data Science Notes

> Hanyang University, Haoyu Zhang

## Frequent Pattern Analysis  (频繁模式分析)

**Frequent pattern**: a pattern that occurs frequently in a data set.

在数据集中频繁出现的模式。

**Motivation**: Finding inherent regularities in data.

寻找数据固有的规律。

**Applications**: Basket data analysis, cross-marketing, catalog design, sale campaign analysis, etc.

### Frequent Patterns and Association Rules (频繁模式和关联规则)

 <div align=center><img src="C:\Users\e-it\AppData\Roaming\Typora\typora-user-images\image-20200526011133256.png" alt="image-20200526011133256" style="zoom:50%;" />

* Itemset X = {$x_1$, ..., $x_k$}
* Find all the association rules X -> Y with **minimum support** and **confidence**
	* **support**, s, *probability* that a transaction contains X ∪ Y 
	* **confidence**, c, *conditional probability* that a transaction having X also contains Y

<img src="C:\Users\e-it\AppData\Roaming\Typora\typora-user-images\image-20200526005818744.png" alt="image-20200526005818744" style="zoom: 67%;" />

<img src="C:\Users\e-it\AppData\Roaming\Typora\typora-user-images\image-20200526005851655.png" alt="image-20200526005851655" style="zoom:67%;" />

**A -> B**: support 就是 A 和 B 同时在 itemset 中存在的概率，confidence 是 $\frac{support(A∪B)}{support(A)}$，即$\frac{A 和 B 同时在 itemset 中存在的概率}{A 在 itemset 中存在的概率}$

Let  $sup_{min}=50\%$,  $conf_{min}=50\%$
Freq. Pat.: $\{A:3, B:3, D:4, E:3, AD:3\}$ 
Association rules: 
    **A -> D**  $(60\%, 100\%)$
    **D -> A**  $(60\%, 75\%)$

### Closed Patterns and Max-Patterns (闭频繁集 和 极大频繁集)

#### References:

* [数据挖掘中的模式发现（一）频繁项集、频繁闭项集、最大频繁项集](https://blog.csdn.net/u013007900/article/details/54743395)

**Closed Patterns**: 频繁集：大于最小支持率 ($sup_{min}$)



## Algorithms

### Apriori algorithm (先验算法)

Apriori是一种基于交易数据库进行频繁项集挖掘和关联规则学习的算法。算法识别数据库中经常出现的频繁项，并将它们扩展为更大的频繁项集。

<img src="C:\Users\e-it\AppData\Roaming\Typora\typora-user-images\image-20200526012243527.png" alt="image-20200526012243527" style="zoom: 50%;" />

<img src="notes\Snipaste_2020-03-29_20-01-27.png" style="zoom: 50%;" />



