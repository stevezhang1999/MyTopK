### Find Top 100 Frequent URLs in 100GB Large File with 1GB Memory



**config.py**: `FILENUMS`：切成的文件数量

**findMostFrequent.py**：主程序，参数是位于同一目录下的大文件名。将会在 `./freq`创建 `res.txt`即为最终结果

**clean.py**：删除`./partition`, `./freq`文件夹的所有内容，为中间文件。结果也存储在`./freq`





由于本题没有给出URL的长度限制，因此有些估算难以进行。

因此分析时尽量避免使用URL长度来作为限制条件。

#### 1. hash partition: 将url分散到小文件当中

- 扫描一遍文件即可，这一步不需要将文件读入内存
- 可能的改进：
  - 改进1：若文件过大，可再哈希分成更小的文件
  - 改进2：参考数据库实现的原理，可以先将文件切成小于500MB的小块（读入内存500MB，输出缓冲区500MB），将小文件块读入内存再进行操作，并批量输出，可以减少IO开销。



####  2. 统计每个文件中的频数，写入新的文件

- 同样，如果逐行seek，不需要将文件读入内存。只需利用一个hash map存储对应的url和出现次数，若扫描到的url已存在于hash map中，将值增加1即可。在python中，利用dict即可。
- 这一步的内存瓶颈：需要空间存储hash map。考虑到key是散列函数返回的结果(MD5: 128bits， 或用简单实现整型即可)，value频数用整数表示，因此都处于<20B的数量级，与一条url几十B至几百B的大小相比，因此不会达到瓶颈。因此，1GB内存的情况下，单个文件约700MB应不会使得内存耗尽

#### 3. 归并排序

- 这里采用最简单的双路归并排序
  - 最终得到一个包含所有url及出现次数、按照出现次数排序的大文件。
  - Pass 0：内部排序
    - 朴素的实现下，并没有输出缓冲区，则内存瓶颈在于读入单个文件并排序输出。若使用快速排序，则额外的空间复杂度是O(logN)，因此空间开销不可忽略。因此文件不能仅仅是略小于内存。在**2**的讨论的基础上，考虑到对数函数的趋势，我们可以认为单个文件300MB~400MB是一个不会使得内存耗尽的值。
  - Pass 0 之后：外部排序
    - 朴素的实现下，没有读入及输出缓冲区，因此没有内容需要预先读入内存。因此空间开销是O(1)，与文件大小无关。
  - **到这里我们终于确定了文件的最大大小，对应的，hash partition当中切分成250~350份都是可以接受的值。**
- 可能的改进：
  - 改进1：题目要求Top100，那么采用完整的排序则是做了额外的工作，可以利用一个最大堆求Top100。
  - 改进2：参考数据库实现的原理，可先写入缓冲区，再批量输出至结果文件，可有效减少IO开销。代价是需要预留缓冲区空间，使得每个文件的最大大小小于朴素的实现。
  - 改进3：若采用改进2中的分块处理，则还可以将双路归并排序扩展为K路归并排序，可以大量减少读写次数，进一步减少IO开销。



##### 其他讨论：

- 我们提到当hash partition得到文件大于我们预设的阈值时，应重新进行partition。如果避免了collision，成功切成小文件，那么大功告成。那么，有没可能里面条目全部相同？那又该如何处理？
  - 是有一定可能的。例如，www.baidu.com的访问可能可以占到一个人一天访问量的千分之一至百分之一，而且这种概率对于大部分人都适用。而如上文切成数百份，那么是可能超出大小的。
  - 如何解决？重新hash partition，若文件大小仍然超出，说明有相当一部分重复。注意到我们在**2**中花费不少篇幅讨论频数统计空间占用，然而**2**中情况是基于极少出现重复的假设，因而统计过程的空间分析很重要。而如果我们已知大量重复，那么频数统计占用的空间可忽略不计，因而也不会耗尽内存。
