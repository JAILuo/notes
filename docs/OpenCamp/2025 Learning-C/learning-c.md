# Stage 1: Basics

## 题目汇总

1. **01_insert_sort** - 插入排序
2. **02_merge_sort** - 归并排序
3. **03_quick_sort** - 快速排序
4. **04_linear_search** - 线性查找
5. **05_binary_search** - 折半查找
6. **06_stack_maze** - 栈解决迷宫问题
7. **07_queue_maze** - 队列实现广度搜索迷宫问题
8. **08_circular_queue** - 环形队列实现约瑟夫环问题
9. **09_word_counter** - 统计单词个数
10. **10_my_strcpy** - 字符串拷贝
11. **11_command_interpreter** - 字符指针数组 命令解释器
12. **12_student_management** - 结构体指针 学生信息管理
13. **13_universal_sorter** - 函数指针实现通用排序接口
14. **14_calculator** - 函数指针数组实现四则运算
15. **15_url_parser** - http 超链传递参数分析器
16. **16_mysed** - sed 简单流处理器实现
17. **17_myfile** - file命令查看ELF文件头
18. **18_mywc** - MyWC 词频统计器项目
19. **19_mytrans** - MyTrans 查字典翻译项目
20. **20_mybash** - MyBash 命令解释器项目



## 01_insert_sort - 插入排序

### 第一层：建立牢固的直觉认知（像打扑克牌一样）

想象一下你在打扑克牌，你是怎么整理手中的牌的？

1.  你左手一开始是空的（**已排序区**）。
2.  你用右手从牌堆里（**未排序区**）拿起一张新牌。
3.  然后，你用这张新牌，从右往左（或从左往右）跟你左手上**已经排好序**的牌**依次比较**。
4.  找到它应该插入的位置（比如，一张 `7` 应该插在 `6` 和 `8` 之间）。
5.  为了给 `7` 腾出位置，你需要把 `8`、`9`、`10` 这些比它大的牌都**向右移动一个位置**，然后把 `7` 放进去。

**这个全过程，就是插入排序！** 它模拟的是最符合人类直觉的排序方式。

---

### 第二层：图文并茂，一步步“慢放”

我们用一个具体数组来“慢放”这个动画：`[5, 2, 4, 6, 1, 3]`

我们用 `|` 来分隔已排序区和未排序区。

**初始状态：** `5 | 2, 4, 6, 1, 3` （我们认为第一个元素 `5` 自己就是有序的）

**第一轮（处理 2）：**
- 取出 `2`。
- `2` 与 `5` 比较，`2 < 5`，所以 `5` 向右移动一位。
- 找到位置，插入 `2`。
- **结果：** `2, 5 | 4, 6, 1, 3`

**第二轮（处理 4）：**
- 取出 `4`。
- `4` 与 `5` 比较，`4 < 5`，`5` 右移。
- `4` 与 `2` 比较，`4 > 2`，停止比较，插入 `4`。
- **结果：** `2, 4, 5 | 6, 1, 3`

**第三轮（处理 6）：**
- 取出 `6`。
- `6` 与 `5` 比较，`6 > 5`，停止比较，原地插入（不用移动）。
- **结果：** `2, 4, 5, 6 | 1, 3`

**第四轮（处理 1）：**
- 取出 `1`。
- `1` 与 `6` 比较，`1 < 6`，`6` 右移。
- `1` 与 `5` 比较，`1 < 5`，`5` 右移。
- `1` 与 `4` 比较，`1 < 4`，`4` 右移。
- `1` 与 `2` 比较，`1 < 2`，`2` 右移。
- 到达开头，插入 `1`。
- **结果：** `1, 2, 4, 5, 6 | 3`

**第五轮（处理 3）：**
- 取出 `3`。
- `3` 与 `6` 比较，`3 < 6`，`6` 右移。
- `3` 与 `5` 比较，`3 < 5`，`5` 右移。
- `3` 与 `4` 比较，`3 < 4`，`4` 右移。
- `3` 与 `2` 比较，`3 > 2`，停止比较，插入 `3`。
- **结果：** `1, 2, 3, 4, 5, 6 |` （排序完成）

**核心洞察：** 在每一轮中，**已排序区**始终是有序的，我们只是在不断扩大这个有序区的边界。

---

### 第三层：写出带详细追踪的C语言代码

现在，我们把上面的步骤翻译成C语言。关键是要在代码里反映出每一步的思考。

```c
#include <stdio.h>

// 插入排序函数
void insertionSort(int arr[], int n) {
    int i, key, j;
    
    // 从第二个元素开始（索引1），因为第一个元素默认已排序
    for (i = 1; i < n; i++) {
        // ‘key’ 就是我们当前要插入的“新牌”
        key = arr[i];
        
        // j 从 ‘key’ 的前一个位置开始，指向已排序区的“最右端”
        j = i - 1;

        printf("第%d轮：取出 key = %d，与已排序区 [", i, key);
        for (int k = 0; k <= j; k++) {
            printf("%d ", arr[k]);
        }
        printf("] 从右往左比较\n");

        // 将 arr[0..i-1]（已排序区）中所有比 ‘key’ 大的元素
        // 都向右移动一个位置，为 ‘key’ 腾地方
        while (j >= 0 && arr[j] > key) {
            printf("  -> %d > %d，将 %d 向右移动一位\n", arr[j], key, arr[j]);
            arr[j + 1] = arr[j];
            j = j - 1; // 继续向左比较
        }
        
        // 当循环停止时，j+1 就是 ‘key’ 的正确位置
        // 因为此时要么 j=-1（key是最小的），要么 arr[j] <= key（找到了不比key大的元素）
        arr[j + 1] = key;

        printf("  -> 将 key(%d) 插入到位置 %d\n", key, j + 1);
        printf("  -> 当前数组： ");
        for (int k = 0; k < n; k++) {
            printf("%d ", arr[k]);
        }
        printf("\n\n");
    }
}

// 主函数来测试
int main() {
    int arr[] = {5, 2, 4, 6, 1, 3};
    int n = sizeof(arr) / sizeof(arr[0]);

    printf("原始数组： ");
    for (int i = 0; i < n; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n\n开始排序过程：\n");

    insertionSort(arr, n);

    printf("排序后数组： ");
    for (int i = 0; i < n; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");

    return 0;
}
```

**请你一定要运行这段代码！** 看看控制台输出，它会完美重现我们上面“慢放”的每一步。这是理解算法执行流程最有效的方式。

---

### 第四层：专业角度的深度分析（这才是“专业”的体现）

一个专业的程序员不仅要会写，更要会分析。

1.  **时间复杂度**
    - **最坏情况**：数组完全逆序（如 `[5,4,3,2,1]`）。每一个新元素 `key` 都需要和之前所有的元素比较并移动。内层循环会执行 `1 + 2 + ... + (n-1) ≈ n²/2` 次。所以是 **O(n²)**。这是它的主要缺点。
    - **最好情况**：数组已经有序（如 `[1,2,3,4,5]`）。每个 `key` 只需要和它前一个元素比较一次（因为 `arr[j] > key` 条件立刻为假）。所以是 **O(n)**。这是它的一大优点！
    - **平均情况**：也是 **O(n²)**。

2.  **空间复杂度**
    - 我们只用了 `i`, `key`, `j` 等固定数量的额外变量。所以是 **O(1)**，是一种 **原地排序** 算法。

3.  **稳定性**
    - **插入排序是稳定的**。当两个元素相等时（比如两个 `5`），我们只在 `arr[j] > key` 时才移动，对于相等的元素，我们不移动，所以它们原始的相对顺序会被保留。

4.  **适用场景**
    - **小规模数据**：非常高效，常数项因子小。
    - **数据基本有序**：因为最好情况是 O(n)，接近线性时间。
    - **作为高级排序算法的优化子过程**：比如在快速排序或归并排序中，当递归到小数组时，改用插入排序可以提升整体性能。

---

### 总结：如何达到“专业理解”

1.  **生活化类比**：用扑克牌建立牢固的直觉。
2.  **手动模拟**：拿笔在纸上一步步画出来，理解每一步在做什么。
3.  **代码与追踪**：写出带有详细打印信息的代码，让计算机帮你“慢放”整个过程。
4.  **复杂度分析**：从时间（最好、最坏、平均）、空间、稳定性等角度定量分析算法的性能。
5.  **场景思考**：知道它在哪里用得好，在哪里不行。

当你完成以上所有步骤，你就不再是“只知道概念”，而是真正**内化**了插入排序。你可以清晰地在大脑中描绘出它的执行画面，可以准确地分析它的优劣，并能在合适的场景下 confidently（自信地）使用它。

这就是专业的态度和方法。祝你学习愉快，在算法的世界里不断精进！





## 02_merge_sort

### 第一阶段：建立直观理解

#### 1.1 核心思想 - "分而治之"

想象你要整理一副乱序的扑克牌：
- **分**：把整副牌分成两半，再把每一半继续分成两半...直到每堆只有1张牌
- **治**：把只有1张牌的堆（自然有序）两两合并成有序的堆，再合并这些有序堆...

#### 1.2 为什么"合并"是关键？

**关键洞察**：合并两个**已经有序**的数组是非常容易的！而归并排序的智慧就在于，它先把问题分解到最简单的状态（单个元素自然有序），然后通过不断合并来构建更大的有序数组。

---

### 第二阶段：详细分解合并过程

让我们用具体的例子来理解。假设我们要合并两个已经有序的数组：

```
左数组: [2, 5, 8]   右数组: [1, 4, 7, 9]
```

#### 合并的详细步骤：

**步骤1：初始化指针**

```
左数组: [2, 5, 8]    ← i=0 (指向2)
右数组: [1, 4, 7, 9] ← j=0 (指向1)
临时数组: []         ← k=0
```

**步骤2：比较第一个元素**
- 比较 `2` vs `1`
- `1 < 2`，所以把 `1` 放入临时数组
- 移动右指针 j++
```
临时数组: [1]
左数组: [2, 5, 8]    ← i=0
右数组: [1, 4, 7, 9] ← j=1 (指向4)
```

**步骤3：继续比较**
- 比较 `2` vs `4`
- `2 < 4`，所以把 `2` 放入临时数组
- 移动左指针 i++
```
临时数组: [1, 2]
左数组: [2, 5, 8]    ← i=1 (指向5)
右数组: [1, 4, 7, 9] ← j=1
```

**步骤4：继续比较**
- 比较 `5` vs `4`
- `4 < 5`，所以把 `4` 放入临时数组
- 移动右指针 j++
```
临时数组: [1, 2, 4]
左数组: [2, 5, 8]    ← i=1
右数组: [1, 4, 7, 9] ← j=2 (指向7)
```

**步骤5：继续比较**
- 比较 `5` vs `7`
- `5 < 7`，所以把 `5` 放入临时数组
- 移动左指针 i++
```
临时数组: [1, 2, 4, 5]
左数组: [2, 5, 8]    ← i=2 (指向8)
右数组: [1, 4, 7, 9] ← j=2
```

**步骤6：继续比较**
- 比较 `8` vs `7`
- `7 < 8`，所以把 `7` 放入临时数组
- 移动右指针 j++
```
临时数组: [1, 2, 4, 5, 7]
左数组: [2, 5, 8]    ← i=2
右数组: [1, 4, 7, 9] ← j=3 (指向9)
```

**步骤7：继续比较**
- 比较 `8` vs `9`
- `8 < 9`，所以把 `8` 放入临时数组
- 移动左指针 i++
```
临时数组: [1, 2, 4, 5, 7, 8]
左数组: [2, 5, 8]    ← i=3 (超出边界)
右数组: [1, 4, 7, 9] ← j=3
```

**步骤8：处理剩余元素**
- 左数组已经用完，但右数组还有剩余元素 `9`
- 直接把剩余元素全部拷贝到临时数组
```
临时数组: [1, 2, 4, 5, 7, 8, 9]
```

**合并完成！** 我们得到了一个完整的有序数组。

---

### 第三阶段：在归并排序中的完整流程

现在让我们看整个归并排序的过程，用数组 `[5, 2, 4, 6, 1, 3]`：

#### 分解阶段（递归拆分）：
```
原始: [5, 2, 4, 6, 1, 3]
      ↓ 分成 [5,2,4] 和 [6,1,3]
[5,2,4] → 分成 [5] 和 [2,4] → [2,4] 再分成 [2] 和 [4]
[6,1,3] → 分成 [6] 和 [1,3] → [1,3] 再分成 [1] 和 [3]

最终得到： [5] [2] [4] [6] [1] [3]
```

#### 合并阶段（从底部开始）：
```
第一层合并：
合并 [2] 和 [4] → [2,4]
合并 [1] 和 [3] → [1,3]

第二层合并：
合并 [5] 和 [2,4] → [2,4,5]  # 详细过程见下面
合并 [6] 和 [1,3] → [1,3,6]

第三层合并：
合并 [2,4,5] 和 [1,3,6] → [1,2,3,4,5,6]  # 详细过程就是我们上面演示的
```

#### 详细演示合并 `[5]` 和 `[2,4]`：
```
步骤1: [5] vs [2,4] → 2<5 → 取2 → 结果: [2]
步骤2: [5] vs [4]   → 4<5 → 取4 → 结果: [2,4]  
步骤3: 左数组还有 [5]，直接加入 → 结果: [2,4,5]
```

---

### 第四阶段：代码的逐行解释

让我们再看一遍合并函数的代码，这次我加上极其详细的注释：

```c
void merge(int start, int mid, int end)
{
    int i = start;      // 左半部分的起始指针
    int j = mid + 1;    // 右半部分的起始指针  
    int k = start;      // 临时数组的指针

    // 核心循环：比较左右两部分的元素，取较小的放入临时数组
    while (i <= mid && j <= end) {
        if (students[i].score >= students[j].score) {
            // 左半部分的分数 >= 右半部分，取左半部分的元素
            // 使用 >= 保证稳定性（相等时保持原顺序）
            temp[k++] = students[i++];
        } else {
            // 右半部分的分数更大，取右半部分的元素
            temp[k++] = students[j++];
        }
    }

    // 处理左半部分剩余的元素（如果有）
    // 这些元素都比已经放入的所有元素大，直接拷贝
    while (i <= mid) {
        temp[k++] = students[i++];
    }

    // 处理右半部分剩余的元素（如果有）
    // 这些元素都比已经放入的所有元素大，直接拷贝
    while (j <= end) {
        temp[k++] = students[j++];
    }

    // 把排好序的临时数组内容复制回原数组
    for (k = start; k <= end; k++) {
        students[k] = temp[k];
    }
}
```

#### 关键理解点：

1. **三个指针的作用**：
   - `i`：遍历左半部分
   - `j`：遍历右半部分  
   - `k`：指向临时数组中要放入下一个元素的位置

2. **核心循环的条件**：`i <= mid && j <= end`
   - 这个条件确保只要左右两部分都还有元素，就继续比较
   - 一旦某一部分用完，循环就结束

3. **两个"清理"循环**：
   - 第一个 `while (i <= mid)`：处理左半部分剩余元素
   - 第二个 `while (j <= end)`：处理右半部分剩余元素
   - 这两个循环只会执行其中一个（因为核心循环结束时，至少有一个部分已用完）

4. **稳定性**：
   - `>=` 保证了当分数相等时，我们先取左边的元素
   - 这保持了原始输入的顺序，所以是稳定排序

---


### 第五阶段：可视化类比

想象你有两叠已经按分数排好序的学生卡片：
- 左手拿一叠（左半部分）
- 右手拿一叠（右半部分）
- 面前有一个空桌子（临时数组）

你的操作：
1. 比较左右手最上面的卡片分数
2. 把分数更高的那张卡片放到桌子上
3. 重复直到某一叠卡片用完
4. 把剩下那叠卡片全部放到桌子上
5. 把桌子上的卡片按顺序放回原处

**这就是合并过程的本质！**

---

### 总结：理解合并过程的要点

1. **前提条件**：要合并的两个部分必须各自已经有序
2. **核心操作**：比较两个部分的当前元素，取合适的放入结果
3. **指针移动**：每次放入一个元素后，移动对应部分的指针
4. **剩余处理**：当一个部分用完时，另一个部分的剩余元素直接全部拷贝
5. **稳定性**：通过比较时的等号处理来保持原始相对顺序

现在你应该能够：
- 在纸上手动模拟任何数组的合并过程
- 理解代码中每个变量和每个循环的作用
- 解释为什么归并排序是稳定的
- 理解"分而治之"策略的巧妙之处

这个理解是内化的、专业的，而不只是知道概念！



### 时间/空间

归并排序并不总是优于插入排序。**在以下几种情况更适合使用插入排序而不是归并排序**：

- **输入规模很小**：当 (n) 很小时，插入排序的常数因子小、实现简单，实际运行往往比归并排序快。许多实际排序库在递归/分治排序（如归并或快速排序）到达小数组时会切换到插入排序（常见阈值例如 10–20）。
- **数据接近有序**：如果序列已经部分或几乎有序，插入排序接近线性时间 ( \Theta(n + d) )（d 表示逆序对数或需要移动的程度），表现优异，而归并排序仍为 ( \Theta(n\log n) )。
- **内存或空间受限**：标准自顶向下归并排序需要额外的 (O(n)) 辅助空间（用于合并）；即使有原地归并的变体，常数和实现复杂度也很高。插入排序只需要 (O(1)) 额外空间，适合对内存、堆栈或分配有严格限制的环境（嵌入式、实时系统、某些安全/内存受限场景）。
- **实现和维护成本**：插入排序实现非常简单且少出错，适用于对代码体积、易审计性或确定性要求高的场合。
- **稳定性与低开销的场景**：插入排序天然稳定、数据移动成本低（比如元素很小或移动很便宜），在这种情况下优先考虑。



关于“递归影响空间”的澄清

- 标准归并排序一般用递归实现，它带来两个方面的额外空间开销：
    - 递归调用栈：深度为 (O(nlog n))，栈空间通常不是主要问题，但在极端受限的系统上可能重要。
    - 合并时的辅助数组：标准做法需要 (O(n)) 额外内存来暂存元素，这是最主要的空间开销来源。
- 因此，**空间受限**确实是一个重要原因，使得归并排序不适合某些环境；插入排序由于仅需要常数额外空间，更适合这些场景。



什么时候在工程实现里常见的折中做法

- 使用分治排序（归并或快速排序）对大块数据排序，但当子数组长度小于某个阈值（如 10–50）时，改用插入排序来完成最终阶段。这结合了两者优点：大规模时保持 (O(nlog n)) 性能，小规模时利用插入排序常数低的优势。
- 对内存敏感时，考虑使用**原地排序算法（如堆排序）**或对归并算法做原地/迭代优化，但通常代价是实现复杂度和常数因子增加。



总结（要点）

- 插入排序在小规模或几乎有序数据、内存受限或要求实现简单的场合更合适。
- 归并排序在大规模数据和对时间复杂度有严格要求时更优，但需要额外的空间（通常 (O(n))）。
- 实际工程中常用“先分治后小数组切换为插入排序”的混合策略以兼顾性能与空间、实现复杂度。





## 03_quick_sort

### 第一层：建立牢固的直觉认知（像整理书架一样）

想象你要整理一个杂乱的书架，快速排序的思路是：

1. **选择"基准"**：从书架上随便挑一本书作为参考点（比如中间的一本）。
2. **分区**：把其他书分成两堆：
   - 比基准书"小"的放左边（比如按书名顺序，书名在基准书之前的）
   - 比基准书"大"的放右边（书名在基准书之后的）
3. **基准归位**：**把基准书放在左右两堆中间的正确位置。**
4. **递归处理**：对左边和右边的两堆书，分别重复上述过程。

**关键洞察**：快速排序的核心是 **"分治+分区"**——每次分区都能让基准元素到达其最终正确位置！

---

### 第二层：图文并茂，一步步"慢放"

让我们用同样的数组来演示：`[5, 2, 4, 6, 1, 3]`

我们选择第一个元素 `5` 作为基准（pivot）。

#### 第一次分区过程：

**初始状态：** `[5, 2, 4, 6, 1, 3]` （pivot = 5）

**步骤1：** 从右向左找第一个小于5的元素
- 找到 `3 < 5`，位置5 → `[5, 2, 4, 6, 1, 3]`

**步骤2：** 从左向右找第一个大于5的元素  
- 找到 `6 > 5`，位置3 → `[5, 2, 4, 6, 1, 3]`

**步骤3：** 交换这两个元素
- 交换6和3 → `[5, 2, 4, 3, 1, 6]`

**步骤4：** 继续从右向左找小于5的元素
- 找到 `1 < 5`，位置4 → `[5, 2, 4, 3, 1, 6]`

**步骤5：** 继续从左向右找大于5的元素
- 指针相遇，停止查找

**步骤6：** 将基准5与相遇位置的元素交换
- 交换5和1 → `[1, 2, 4, 3, 5, 6]`

**分区完成！** 现在：
- 基准 `5` 已经在最终正确位置
- 左边 `[1, 2, 4, 3]` 都 ≤ 5
- 右边 `[6]` 都 ≥ 5

#### 递归处理左右分区：

**处理左边 `[1, 2, 4, 3]`（pivot = 1）：**
- 分区后：`[1, 2, 4, 3]`（1已经在正确位置）
- 左边：`[]`（空）
- 右边：`[2, 4, 3]`

**处理 `[2, 4, 3]`（pivot = 2）：**

- 分区后：`[2, 4, 3]` → 交换后 `[2, 3, 4]`
- 左边：`[]`
- 右边：`[3, 4]`

**处理 `[3, 4]`（pivot = 3）：**

- 分区后：`[3, 4]`
- 左边：`[]`
- 右边：`[4]`

**处理右边 `[6]`：**
- 单个元素，自然有序

**最终结果：** `[1, 2, 3, 4, 5, 6]`

---

### 第三层：写出带详细追踪的C语言代码

```c
#include <stdio.h>

// 交换两个元素
void swap(int* a, int* b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}

// 分区函数 - 快速排序的核心
int partition(int arr[], int low, int high, int depth) {
    int pivot = arr[low];  // 选择第一个元素作为基准
    int left = low + 1;
    int right = high;
    
    // 打印当前分区信息
    for (int i = 0; i < depth; i++) printf("  ");
    printf("分区: [");
    for (int i = low; i <= high; i++) {
        if (i == low) printf("(%d)", arr[i]);  // 标记基准
        else printf("%d", arr[i]);
        if (i < high) printf(" ");
    }
    printf("]\n");
    
    while (left <= right) {
        // 从左向右找第一个大于pivot的元素
        while (left <= right && arr[left] <= pivot) {
            left++;
        }
        // 从右向左找第一个小于pivot的元素  
        while (left <= right && arr[right] >= pivot) {
            right--;
        }
        
        if (left < right) {
            for (int i = 0; i < depth; i++) printf("  ");
            printf("  交换: %d <-> %d\n", arr[left], arr[right]);
            swap(&arr[left], &arr[right]);
            left++;
            right--;
        }
    }
    
    // 将基准放到正确位置
    for (int i = 0; i < depth; i++) printf("  ");
    printf("  基准归位: (%d) 放到位置 %d\n", pivot, right);
    swap(&arr[low], &arr[right]);
    
    // 打印分区结果
    for (int i = 0; i < depth; i++) printf("  ");
    printf("  结果: [");
    for (int i = low; i <= high; i++) {
        if (i == right) printf("[%d]", arr[i]);  // 标记基准最终位置
        else printf("%d", arr[i]);
        if (i < high) printf(" ");
    }
    printf("]\n");
    
    return right;  // 返回基准的最终位置
}

// 快速排序主函数
void quickSort(int arr[], int low, int high, int depth) {
    if (low < high) {
        // pi是分区后基准的索引
        int pi = partition(arr, low, high, depth);
        
        // 递归排序左半部分
        if (low < pi - 1) {
            for (int i = 0; i < depth; i++) printf("  ");
            printf("递归左: [");
            for (int i = low; i <= pi - 1; i++) printf("%d ", arr[i]);
            printf("]\n");
            quickSort(arr, low, pi - 1, depth + 1);
        }
        
        // 递归排序右半部分  
        if (pi + 1 < high) {
            for (int i = 0; i < depth; i++) printf("  ");
            printf("递归右: [");
            for (int i = pi + 1; i <= high; i++) printf("%d ", arr[i]);
            printf("]\n");
            quickSort(arr, pi + 1, high, depth + 1);
        }
    }
}

// 包装函数
void quickSortWrapper(int arr[], int n) {
    printf("原始数组: [");
    for (int i = 0; i < n; i++) printf("%d ", arr[i]);
    printf("]\n\n开始快速排序过程:\n");
    
    quickSort(arr, 0, n - 1, 0);
    
    printf("\n排序后数组: [");
    for (int i = 0; i < n; i++) printf("%d ", arr[i]);
    printf("]\n");
}

int main() {
    int arr[] = {5, 2, 4, 6, 1, 3};
    int n = sizeof(arr) / sizeof(arr[0]);
    
    quickSortWrapper(arr, n);
    return 0;
}
```

**请运行这段代码！** 观察输出，你会看到：
- 每次分区的详细过程
- 元素的交换和基准的归位
- 递归的深度和范围

---

### 第四层：专业角度的深度分析

#### 4.1 时间复杂度分析

- **最好情况**：每次分区都很平衡（基准选中位数）
  - 递归深度：O(log n)
  - 每层工作量：O(n)
  - **时间复杂度：O(n log n)**

- **最坏情况**：每次分区都极度不平衡（数组已有序或逆序）
  - 递归深度：O(n) 
  - 每层工作量：O(n)
  - **时间复杂度：O(n²)**

- **平均情况**：**O(n log n)**
  - 数学期望证明平均性能很好

#### 4.2 空间复杂度

- **最好情况**：O(log n) - 递归栈深度
- **最坏情况**：O(n) - 递归栈深度
- **是原地排序算法**（除了递归栈，不需要额外空间）

#### 4.3 稳定性

- **快速排序是不稳定的**
- 原因：分区过程中的长距离交换可能改变相等元素的相对顺序

#### 4.4 基准选择策略

基准选择严重影响性能：

1. **第一个/最后一个元素**：简单但可能导致最坏情况
2. **随机选择**：避免最坏情况的简单方法
3. **三数取中**：选择首、中、尾三个元素的中位数
4. **随机化快速排序**：实际应用中常用

#### 4.5 优化技巧

1. **小数组使用插入排序**：当子数组很小时（如<10个元素），插入排序更高效
2. **尾递归优化**：减少递归栈深度
3. **三路快排**：处理有大量重复元素的情况

#### 4.6 与归并排序的比较

| 特性           | 快速排序           | 归并排序           |
| -------------- | ------------------ | ------------------ |
| 平均时间复杂度 | O(n log n)         | O(n log n)         |
| 最坏时间复杂度 | O(n²)              | O(n log n)         |
| 空间复杂度     | O(log n)           | O(n)               |
| 稳定性         | 不稳定             | 稳定               |
| 数据访问模式   | 局部性好，缓存友好 | 顺序访问           |
| 适用场景       | 通用内部排序       | 外部排序、链表排序 |

---

### 第五层：关键洞察与记忆技巧

#### 5.1 核心思想总结

1. **"分区+递归"思维**：选择基准 → 分区 → 基准归位 → 递归处理
2. **原地操作**：通过交换在原始数组上操作，空间效率高
3. **平均性能优秀**：实际应用中通常是最快的通用排序算法

#### 5.2 分区过程的关键点

- **双指针技巧**：左右指针向中间扫描
- **交换策略**：找到违规元素就交换
- **基准归位**：最终将基准放到正确位置

#### 5.3 实际应用建议

- **随机化基准**：避免最坏情况
- **结合插入排序**：小数组优化
- **注意稳定性需求**：如果需要稳定排序，选择其他算法

---

### 总结：快速排序的专业理解路径

1. **生活化类比**：整理书架的分区过程
2. **手动模拟**：在纸上演练分区和递归的完整流程
3. **代码追踪**：通过详细打印理解每一步的执行
4. **复杂度分析**：理解为什么平均O(n log n)、最坏O(n²)
5. **对比思考**：与归并排序、堆排序等其他O(n log n)算法比较



### 深入理解 partition 函数中的循环条件

#### 循环条件的意义

```c
while (i <= j) {
    // ...
}
```

**这个条件的核心目的是：确保两个指针 `i` 和 `j` 在相遇或交叉时停止循环。**

让我们通过一个具体的例子来理解：

假设数组为：`[5, 2, 4, 6, 1, 3]`，pivot = 5

##### 执行过程：

**初始状态：**

```
i → 2 (索引1)
j → 3 (索引5)
数组: [5, 2, 4, 6, 1, 3]
```

**步骤1：** i 向右移动，找到第一个 >5 的元素

- i 停在 6 (索引3)

**步骤2：** j 向左移动，找到第一个 <5 的元素  
- j 停在 1 (索引4)

**步骤3：** 交换 6 和 1
```
数组变为: [5, 2, 4, 1, 6, 3]
i → 6 (索引4)
j → 1 (索引3)
```

**此时 i > j，循环应该停止！**

如果条件是 `i < j`，循环会继续，但这是错误的，因为指针已经交叉，继续操作会导致逻辑错误。

#### 为什么需要 `i <= j` 而不是 `i < j`

1. **处理相遇情况**：
   - 当 `i == j` 时，当前元素还没有被检查
   - 我们需要确保这个元素也被正确处理

2. **防止指针越界**：
   - 如果只用 `i < j`，在某些情况下指针可能会超出数组边界

3. **确保分区完整性**：
   - 只有当 `i > j` 时，才说明所有元素都已经检查完毕

#### 内层循环中的 `i <= j` 条件

```c
while (i <= j && a[i] <= pivot) {
    i++;
}
while (i <= j && a[j] >= pivot) {
    j--;
}
```

**这里的 `i <= j` 同样重要：**

1. **防止指针越界**：
   - 确保在移动指针时不会超出当前分区的范围

2. **提前终止**：
   - 当指针相遇或交叉时，立即停止内层循环

3. **保持逻辑一致性**：
   - 外层循环检查 `i <= j`，内层循环也要相应检查

#### 完整的执行流程示例

让我们再看一次完整的执行过程：

```
初始: [5, 2, 4, 6, 1, 3], pivot=5, i=1, j=5

循环1:
  i 移动: 2≤5 → 4≤5 → 6>5 (停在索引3)
  j 移动: 3≥5? 否 → 停在索引5
  交换 6↔3: [5, 2, 4, 3, 1, 6], i=4, j=4

循环2:
  i 移动: 1≤5? 是 → i=5
  j 移动: 1≥5? 否 → 停在索引4
  现在 i=5, j=4 → i>j → 循环结束

最终交换: a[0]↔a[4]: [1, 2, 4, 3, 5, 6]
```

#### 如果改为 `i < j` 会发生什么？

如果我们将条件改为 `while (i < j)`：

```
在最后一次循环时：
i=4, j=4 → i==j → 循环不执行
但此时元素 1 还没有被正确处理！
```

这样会导致分区不完整，排序结果错误。

#### 总结

**`i <= j` 条件的重要性：**

1. **完整性**：确保所有元素都被检查
2. **安全性**：防止指针越界
3. **正确性**：保证分区逻辑的正确执行
4. **终止性**：在合适的时机终止循环

这个条件是快速排序分区算法的核心，它确保了：
- 左指针 `i` 找到所有应该放在右边的元素
- 右指针 `j` 找到所有应该放在左边的元素
- 最终 `pivot` 被放置到正确的位置

理解了这一点，你就掌握了快速排序分区算法的精髓！





### 代码

```C
#include <stdio.h>

// 基础版本的partition函数
int partition(int a[], int start, int end)
{
    int pivot = a[start];
    int i = start + 1;
    int j = end;
    
    while (i <= j) {
        while (i <= j && a[i] <= pivot) i++;
        while (i <= j && a[j] >= pivot) j--;
        
        if (i < j) {
            int temp = a[i];
            a[i] = a[j];
            a[j] = temp;
            i++;
            j--;
        }
    }
    
    a[start] = a[j];
    a[j] = pivot;
    
    return j;
}

void quicksort(int a[], int start, int end)
{
    int mid;
    if (end > start) {
        mid = partition(a, start, end);
        quicksort(a, start, mid-1);
        quicksort(a, mid+1, end);
    }
}

// 测试函数
int main()
{
    int arr[] = {5, 2, 4, 6, 1, 3};
    int n = sizeof(arr) / sizeof(arr[0]);
    
    printf("原始数组: ");
    for (int i = 0; i < n; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
    
    quicksort(arr, 0, n-1);
    
    printf("排序后数组: ");
    for (int i = 0; i < n; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
    
    return 0;
}
```

```C
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_STUDENTS 100
#define NAME_LEN     50

typedef struct {
    char name[NAME_LEN];
    int score;
} Student;

Student students[MAX_STUDENTS];

void swap(int i, int j) {
    Student temp = students[i];
    students[i] = students[j];
    students[j] = temp;
}

int partition(int left, int right) {
    // 选择第一个元素作为pivot
    Student pivot = students[left];
    int i = left + 1;
    int j = right;

    while (i <= j) {
        // 从左边找第一个小于pivot的元素（因为我们是从高到低排序）
        while (i <= j && students[i].score >= pivot.score) {
            i++;
        }
        // 从右边找第一个大于pivot的元素
        while (i <= j && students[j].score <= pivot.score) {
            j--;
        }

        if (i < j) {
            swap(i, j);
            i++;
            j--;  // 修正：j--- 改为 j--
        }
    }
    
    // 将pivot放到正确位置
    swap(left, j);
    return j;
}

void quick_sort(int left, int right) {
    int mid;  // 修正：改为int类型
    if (left < right) {
        mid = partition(left, right);
        quick_sort(left, mid - 1);
        quick_sort(mid + 1, right);
    }
}

int main(void) {
    FILE *file = fopen("03_students.txt", "r");
    if (!file) {
        printf("错误：无法打开文件 03_students.txt\n");
        return 1;
    }

    int n;
    fscanf(file, "%d", &n);

    if (n <= 0 || n > MAX_STUDENTS) {
        printf("学生人数无效：%d（应为 1-%d）\n", n, MAX_STUDENTS);
        fclose(file);
        return 1;
    }

    for (int i = 0; i < n; i++) {
        fscanf(file, "%s %d", students[i].name, &students[i].score);
    }
    fclose(file);

    quick_sort(0, n - 1);

    // 输出结果
    printf("\n快速排序后按成绩从高到低排序的学生名单：\n");
    for (int i = 0; i < n; i++) {
        printf("%s %d\n", students[i].name, students[i].score);
    }

    return 0;
}
```









## 04_linear_search

省略。主要看快速选择：

现在重点实现找出第k小元素的算法。基于快速排序的partition思想，我们可以在平均情况 Θ(n) 时间内解决这个问题。

#### 基于快速选择的第k小元素查找算法

这个算法（称为快速选择）是快速排序的变种：

1. 使用partition函数将数组分成两部分
2. 根据pivot的位置决定继续在哪个部分搜索
3. 只递归处理包含第k小元素的那一半，而不是完全排序

```C
#include <stdio.h>
#include <stdlib.h>

// 交换函数
void swap(int *a, int *b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}

// 分区函数 - 选择第一个元素作为pivot
int partition(int a[], int start, int end) {
    int pivot = a[start];
    int i = start + 1;
    int j = end;
    
    while (i <= j) {
        while (i <= j && a[i] <= pivot) i++;
        while (i <= j && a[j] >= pivot) j--;
        
        if (i < j) {
            swap(&a[i], &a[j]);
            i++;
            j--;
        }
    }
    
    // 将pivot放到正确位置
    swap(&a[start], &a[j]);
    return j;
}

// 随机选择pivot的分区函数 - 避免最坏情况
int randomized_partition(int a[], int start, int end) {
    // 随机选择pivot
    int random_index = start + rand() % (end - start + 1);
    swap(&a[start], &a[random_index]);
    
    return partition(a, start, end);
}

// 查找第k小元素的主要函数
int order_statistic(int a[], int start, int end, int k) {
    if (start == end) {
        return a[start];
    }
    
    // 使用随机化partition避免最坏情况
    int pivot_index = randomized_partition(a, start, end);
    int i = pivot_index - start + 1;  // pivot是当前范围内的第i小元素
    
    if (k == i) {
        // 找到了第k小的元素
        return a[pivot_index];
    } else if (k < i) {
        // 在第k小的元素在前半部分
        return order_statistic(a, start, pivot_index - 1, k);
    } else {
        // 在第k小的元素在后半部分
        return order_statistic(a, pivot_index + 1, end, k - i);
    }
}

// 包装函数，简化调用
int find_kth_smallest(int a[], int n, int k) {
    if (k < 1 || k > n) {
        printf("错误：k 必须在 1 到 %d 之间\n", n);
        return -1;
    }
    return order_statistic(a, 0, n - 1, k);
}

// 测试函数
int main() {
    int arr[] = {5, 2, 4, 6, 1, 3};
    int n = sizeof(arr) / sizeof(arr[0]);
    
    printf("原始数组: ");
    for (int i = 0; i < n; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n\n");
    
    // 测试查找各种顺序统计量
    for (int k = 1; k <= n; k++) {
        int result = find_kth_smallest(arr, n, k);
        printf("第 %d 小的元素是: %d\n", k, result);
        
        // 重新复制数组，因为order_statistic会修改原数组
        int temp_arr[] = {5, 2, 4, 6, 1, 3};
        for (int i = 0; i < n; i++) {
            arr[i] = temp_arr[i];
        }
    }
    
    // 单独测试一些边界情况
    printf("\n--- 边界情况测试 ---\n");
    int test_arr[] = {5, 2, 4, 6, 1, 3};
    
    printf("最小值 (k=1): %d\n", find_kth_smallest(test_arr, n, 1));
    
    for (int i = 0; i < n; i++) {
        test_arr[i] = 5;  // 所有元素相同
    }
    printf("所有元素相同时的第3小元素: %d\n", find_kth_smallest(test_arr, n, 3));
    
    return 0;
}
```





## 05_binary_search

```C
int binarysearch(int number)
{
	int mid, start = 0, end = LEN - 1;

	/* 假定a是排好序的 */
    // 左开右开：a[0...LEN-1]
    // 左开右闭：a[0...LEN]
	/* mustbe(start, end, number)，因为a[start..end]就是整个数组a[0..LEN-1] */
	while (start <= end) {
	/* mustbe(start, end, number)，因为一开始进入循环时是正确的，每次循环也都维护了这个条件 */
		mid = (start + end) / 2;
		if (a[mid] < number)
			/* 既然a是排好序的，a[start..mid]应该都比number小，所以mustbe(mid+1, end, number) */
			start = mid + 1;
			/* 维护了mustbe(start, end, number) */
		else if (a[mid] > number)
			/* 既然a是排好序的，a[mid..end]应该都比number大，所以mustbe(start, mid-1, number) */
			end = mid - 1;
			/* 维护了mustbe(start, end, number) */
		else
			/* a[mid] == number，说明找到了 */
			return mid;
	}
	/* 
	 * mustbe(start, end, number)一直被循环维护着，到这里应该仍然成立，在a[start..end]范围之外一定不存在number，
	 * 但现在a[start..end]是空序列，在这个范围之外的正是整个数组a，因此整个数组a中都不存在number
	 */
	return -1;
}
```

见algorithm目录的题目。这里关注一些里面的拓展。

> 1、本节的折半查找算法有一个特点：如果待查找的元素在数组中有多个则返回其中任意一个，以本节定义的数组`int a[8] = { 1, 2, 2, 2, 5, 6, 8, 9 };`为例，如果调用`binarysearch(2)`则返回3，即`a[3]`，而有些场合下要求这样的查找返回`a[1]`，也就是说，如果待查找的元素在数组中有多个则返回第一个。请修改折半查找算法实现这一特性。
>
> 2、编写一个函数`double mysqrt(double y);`求`y`的正平方根，参数`y`是正实数。我们用折半查找来找这个平方根，在从0到`y`之间必定有一个取值是`y`的平方根，如果我们查找的数`x`比`y`的平方根小，则x2<y，如果我们查找的数`x`比`y`的平方根大，则x2>y，我们可以据此缩小查找范围，当我们查找的数足够准确时（比如满足|x2-y|<0.001），就可以认为找到了`y`的平方根。思考一下这个算法需要迭代多少次？迭代次数的多少由什么因素决定？
>
> 3、编写一个函数`double mypow(double x, int n);`求`x`的`n`次方，参数`n`是正整数。最简单的算法是：
>
> ```
> double product = 1;
> for (i = 0; i < n; i++)
> 	product *= x;
> ```
>
> 这个算法的时间复杂度是Θ(n)。其实有更好的办法，比如`mypow(x, 8)`，第一次循环算出x·x=x2，第二次循环算出x2·x2=x4，第三次循环算出4·x4=x8。这样只需要三次循环，时间复杂度是Θ(lgn)。思考一下如果`n`不是2的整数次幂应该怎么处理。请分别用递归和循环实现这个算法。
>
> 从以上几题可以看出，折半查找的思想有非常广泛的应用，不仅限于从一组排好序的元素中找出某个元素的位置，还可以解决很多类似的问题。[[编程珠玑\]](https://akaedu.github.io/book/bi01.html#bibli.pearls)对于折半查找的各种应用和优化技巧有非常详细的介绍。

### 问题一：返回第一个匹配元素的二分查找

#### 算法思路

要返回第一个匹配元素，我们需要在找到目标值时继续向左搜索，直到找到第一个出现的位置。

#### 代码实现

```c
#include <stdio.h>

// 返回第一个匹配元素的二分查找
int binarysearch_first(int a[], int n, int target) {
    int start = 0;
    int end = n - 1;
    int result = -1;  // 记录找到的位置
    
    while (start <= end) {
        int mid = start + (end - start) / 2;  // 防止溢出
        
        if (a[mid] == target) {
            result = mid;      // 记录当前位置
            end = mid - 1;     // 继续在左半部分查找
        } else if (a[mid] < target) {
            start = mid + 1;   // 目标在右半部分
        } else {
            end = mid - 1;     // 目标在左半部分
        }
    }
    
    return result;
}

// 测试函数
int main() {
    int a[8] = {1, 2, 2, 2, 5, 6, 8, 9};
    int n = 8;
    int target = 2;
    
    int index = binarysearch_first(a, n, target);
    
    printf("数组: ");
    for (int i = 0; i < n; i++) {
        printf("%d ", a[i]);
    }
    printf("\n");
    
    if (index != -1) {
        printf("元素 %d 第一次出现的位置: a[%d] = %d\n", target, index, a[index]);
    } else {
        printf("元素 %d 未找到\n", target);
    }
    
    return 0;
}
```

#### 算法分析

**时间复杂度**：O(log n)
- 每次迭代将搜索范围减半
- 即使需要继续搜索，总体时间复杂度仍为对数级

**关键改进**：
- 找到目标时不立即返回，而是记录位置并继续向左搜索
- 最终返回第一个匹配的位置

---

### 问题二：用二分查找求平方根

#### 算法思路

利用二分查找在区间 [0, y] 中寻找平方根：
- 如果 mid² < y，说明平方根在右半部分
- 如果 mid² > y，说明平方根在左半部分
- 当 |mid² - y| < 精度要求时停止

#### 代码实现

```c
#include <stdio.h>
#include <math.h>

#define EPSILON 0.001  // 精度要求

double mysqrt(double y) {
    if (y < 0) {
        printf("错误：y 必须是非负数\n");
        return -1;
    }
    
    // 处理特殊情况
    if (y == 0 || y == 1) {
        return y;
    }
    
    double low, high;
    
    // 确定搜索区间
    if (y < 1) {
        low = y;
        high = 1;
    } else {
        low = 0;
        high = y;
    }
    
    double mid;
    int iterations = 0;
    
    while (high - low > EPSILON) {
        mid = (low + high) / 2;
        double square = mid * mid;
        
        if (square < y) {
            low = mid;
        } else {
            high = mid;
        }
        
        iterations++;
        printf("迭代 %d: mid = %.6f, mid² = %.6f, 误差 = %.6f\n", 
               iterations, mid, square, fabs(square - y));
    }
    
    printf("总共迭代次数: %d\n", iterations);
    return (low + high) / 2;
}

// 测试函数
int main() {
    double test_cases[] = {2.0, 4.0, 10.0, 0.25, 100.0};
    int n = sizeof(test_cases) / sizeof(test_cases[0]);
    
    for (int i = 0; i < n; i++) {
        double y = test_cases[i];
        printf("\n计算 sqrt(%.2f):\n", y);
        double result = mysqrt(y);
        double actual = sqrt(y);
        printf("计算结果: %.6f\n", result);
        printf("标准库结果: %.6f\n", actual);
        printf("绝对误差: %.6f\n", fabs(result - actual));
    }
    
    return 0;
}
```

#### 迭代次数分析

**迭代次数由以下因素决定**：
1. **初始区间大小**：区间越大，需要更多迭代
2. **精度要求**：精度越高（EPSILON越小），需要更多迭代
3. **目标值的大小**：值越大，需要的迭代次数可能越多

**数学推导**：
- 每次迭代区间减半
- 初始区间大小：max(1, y)
- 需要的迭代次数：log₂(初始区间大小 / EPSILON)

**示例计算**：
对于 y = 100, EPSILON = 0.001：
- 初始区间大小 = 100
- 迭代次数 ≈ log₂(100 / 0.001) ≈ log₂(100000) ≈ 17次

---

### 问题三：快速幂算法

#### 算法原理

利用分治思想：
- xⁿ = (x^(n/2))² （当n为偶数）
- xⁿ = x · (x^((n-1)/2))² （当n为奇数）

#### 递归实现

```c
#include <stdio.h>

// 递归实现的快速幂
double mypow_recursive(double x, int n) {
    // 基本情况
    if (n == 0) return 1.0;
    if (n == 1) return x;
    
    // 递归计算一半的幂
    double half = mypow_recursive(x, n / 2);
    
    if (n % 2 == 0) {
        // n为偶数：xⁿ = (x^(n/2))²
        return half * half;
    } else {
        // n为奇数：xⁿ = x · (x^((n-1)/2))²
        return x * half * half;
    }
}
```

#### 循环实现

```c
// 循环实现的快速幂
double mypow_iterative(double x, int n) {
    double result = 1.0;
    double base = x;
    
    while (n > 0) {
        if (n % 2 == 1) {
            // 如果当前位为1，乘到结果中
            result *= base;
        }
        // 基数平方
        base *= base;
        // 指数右移一位
        n /= 2;
    }
    
    return result;
}
```

#### 完整测试代码

```c
#include <stdio.h>
#include <math.h>

// 朴素实现 - 时间复杂度 O(n)
double mypow_naive(double x, int n) {
    double result = 1.0;
    for (int i = 0; i < n; i++) {
        result *= x;
    }
    return result;
}

// 递归实现的快速幂
double mypow_recursive(double x, int n) {
    if (n == 0) return 1.0;
    if (n == 1) return x;
    
    double half = mypow_recursive(x, n / 2);
    
    if (n % 2 == 0) {
        return half * half;
    } else {
        return x * half * half;
    }
}

// 循环实现的快速幂
double mypow_iterative(double x, int n) {
    double result = 1.0;
    double base = x;
    int exponent = n;
    
    while (exponent > 0) {
        if (exponent % 2 == 1) {
            result *= base;
        }
        base *= base;
        exponent /= 2;
    }
    
    return result;
}

// 性能测试
void performance_test(double x, int n) {
    printf("\n测试: %.2f^%d\n", x, n);
    
    // 朴素方法
    printf("朴素方法: ");
    double result1 = mypow_naive(x, n);
    printf("%.6f\n", result1);
    
    // 递归快速幂
    printf("递归快速幂: ");
    double result2 = mypow_recursive(x, n);
    printf("%.6f\n", result2);
    
    // 循环快速幂
    printf("循环快速幂: ");
    double result3 = mypow_iterative(x, n);
    printf("%.6f\n", result3);
    
    // 标准库（参考）
    printf("标准库pow: ");
    double result4 = pow(x, n);
    printf("%.6f\n", result4);
}

int main() {
    // 测试各种情况
    double bases[] = {2.0, 3.0, 1.5};
    int exponents[] = {10, 15, 20, 0, 1, 7}; // 包括非2的幂次
    
    for (int i = 0; i < sizeof(bases) / sizeof(bases[0]); i++) {
        for (int j = 0; j < sizeof(exponents) / sizeof(exponents[0]); j++) {
            performance_test(bases[i], exponents[j]);
        }
    }
    
    // 大数测试
    printf("\n=== 大数性能测试 ===\n");
    performance_test(1.0001, 10000);
    
    return 0;
}
```

#### 处理非2的整数次幂

**关键洞察**：任何正整数都可以表示为2的幂次之和

**处理方法**：
- 将指数n用二进制表示
- xⁿ = x^(二进制表示的加权和) = ∏ x^(2^i) （对于所有二进制位为1的i）

**示例**：计算 x¹³
- 13的二进制：1101 = 8 + 4 + 1
- x¹³ = x⁸ · x⁴ · x¹

#### 时间复杂度分析

- **朴素算法**：O(n) - 需要n次乘法
- **快速幂算法**：O(log n) - 只需要log₂n次乘法

**优势对比**：
```
指数大小   朴素算法乘法次数   快速幂乘法次数
   16          16                4
  1024        1024              10
 10000       10000              14
```

---

### 二分查找思想的广泛应用

从以上问题可以看出，二分查找的核心思想——**通过比较不断将问题规模减半**——具有广泛的应用：

1. **搜索问题**：在有序集合中查找元素
2. **数值计算**：求平方根、立方根等
3. **优化问题**：寻找函数的最优解
4. **分治算法**：快速幂、归并排序等

#### 二分查找的应用模式

```c
// 二分查找的通用模式
type binary_search(type lower, type upper) {
    while (满足精度要求) {
        type mid = (lower + upper) / 2;
        
        if (满足条件(mid)) {
            // 根据问题调整搜索方向
            lower = mid;  // 或 upper = mid
        } else {
            // 调整另一个边界
            upper = mid;  // 或 lower = mid
        }
    }
    
    return 最终结果;
}
```

这种"减半治理"的思想是计算机科学中最重要的算法范式之一，体现了分而治之的智慧。









## 06_stack_maze

### 代码

```C
#include <stdio.h>

#define MAX_ROW 5
#define MAX_COL 5

// 坐标结构体
struct point { 
    int row, col; 
} stack[512];
int top = 0;

// 栈操作函数
void push(struct point p) {
    stack[top] = p;
    top++;
}

struct point pop(void) {
    top--;
    return stack[top];
}

int is_empty(void) {
    return top == 0;
}

// 迷宫定义：0=通路，1=墙
int maze[MAX_ROW][MAX_COL] = {
    {0, 1, 0, 0, 0},
    {0, 1, 0, 1, 0},
    {0, 0, 0, 0, 0},
    {0, 1, 1, 1, 0},
    {0, 0, 0, 1, 0}
};

// 前驱记录数组
struct point predecessor[MAX_ROW][MAX_COL];

// 初始化前驱数组
void init_predecessor() {
    for (int i = 0; i < MAX_ROW; i++) {
        for (int j = 0; j < MAX_COL; j++) {
            predecessor[i][j].row = -1;
            predecessor[i][j].col = -1;
        }
    }
}

// 可视化打印迷宫
void print_maze(void) {
    for (int i = 0; i < MAX_ROW; i++) {
        for (int j = 0; j < MAX_COL; j++) {
            if (maze[i][j] == 0)
                printf(". ");  // 未访问的通路
            else if (maze[i][j] == 1)
                printf("█ ");  // 墙
            else if (maze[i][j] == 2)
                printf("* ");  // 已访问的路径
        }
        putchar('\n');
    }
    printf("*********\n");
}

// 访问函数：标记访问、记录前驱、压入栈
void visit(int row, int col, struct point pre) {
    struct point visit_point = { row, col };
    maze[row][col] = 2;                    // 标记为已访问
    predecessor[row][col] = pre;           // 记录从哪里来的
    push(visit_point);                     // 加入路径栈
    
    printf("访问(%d,%d)，前驱是(%d,%d)\n", 
           row, col, pre.row, pre.col);
}

int main(void) {
    struct point p = { 0, 0 };  // 起点
    
    // 初始化前驱数组
    init_predecessor();
    
    printf("开始DFS迷宫求解...\n");
    printf("初始迷宫:\n");
    print_maze();
    
    maze[p.row][p.col] = 2;     // 标记起点为已访问
    predecessor[p.row][p.col].row = -1;  // 起点没有前驱
    predecessor[p.row][p.col].col = -1;
    push(p);                    // 起点入栈
    
    int step = 1;
    
    while (!is_empty()) {
        p = pop();  // 弹出栈顶（最近访问的点）
        printf("\n步骤%d: 从栈中弹出(%d,%d)\n", step, p.row, p.col);
        
        // 检查是否到达终点
        if (p.row == MAX_ROW - 1 && p.col == MAX_COL - 1) {
            printf("找到终点！\n");
            break;
        }
        
        // 尝试四个方向：右、下、左、上
        // 注意：由于栈是LIFO，实际搜索顺序是上、左、下、右
        
        // 右
        if (p.col + 1 < MAX_COL && maze[p.row][p.col + 1] == 0) {
            printf("  向右探索到(%d,%d)\n", p.row, p.col + 1);
            visit(p.row, p.col + 1, p);
        }
        
        // 下
        if (p.row + 1 < MAX_ROW && maze[p.row + 1][p.col] == 0) {
            printf("  向下探索到(%d,%d)\n", p.row + 1, p.col);
            visit(p.row + 1, p.col, p);
        }
        
        // 左
        if (p.col - 1 >= 0 && maze[p.row][p.col - 1] == 0) {
            printf("  向左探索到(%d,%d)\n", p.row, p.col - 1);
            visit(p.row, p.col - 1, p);
        }
        
        // 上
        if (p.row - 1 >= 0 && maze[p.row - 1][p.col] == 0) {
            printf("  向上探索到(%d,%d)\n", p.row - 1, p.col);
            visit(p.row - 1, p.col, p);
        }
        
        printf("当前迷宫状态:\n");
        print_maze();
        step++;
        
        // 防止无限循环
        if (step > 50) {
            printf("步数过多，可能陷入循环，退出\n");
            break;
        }
    }
    
    // 输出最终路径
    if (p.row == MAX_ROW - 1 && p.col == MAX_COL - 1) {
        printf("\n=== 找到路径 ===\n");
        printf("路径(从终点到起点):\n");
        
        // 使用前驱数组回溯路径
        while (p.row != -1 && p.col != -1) {
            printf("(%d, %d)\n", p.row, p.col);
            struct point prev = predecessor[p.row][p.col];
            p = prev;
        }
    } else {
        printf("\n没有找到路径！\n");
        
        // 打印当前栈状态用于调试
        printf("栈中剩余点: ");
        for (int i = 0; i < top; i++) {
            printf("(%d,%d) ", stack[i].row, stack[i].col);
        }
        printf("\n");
    }

    return 0;
}
```



### 深入理解访问点、前驱点和DFS搜索过程

#### 1. 访问点 vs 前驱点

- **访问点**：当前正在探索的位置
- **前驱点**：当前点是从哪个点**走过来**的

**生活化比喻**：
想象你在迷宫中走，每走一步就在地上：
- 放一个标记（**访问点**：表示你来过这里）
- 画一个箭头指向你来的方向（**前驱点**：记录你从哪里来）

#### 2. 为什么一个点可以探索多个地方？

这是**深度优先搜索的核心特性**！

```c
// 在(2,0)这个位置，可以往多个方向走
if (可以向右走) visit(2,1);
if (可以向下走) visit(3,0);
if (可以向左走) visit(...);
if (可以向上走) visit(...);
```

**关键理解**：DFS不是一次只走一条路，而是**把所有的可能性都先记录下来**，然后一条条尝试。

### 详细分解步骤3的执行过程

让我们一步步分析你说的这个场景：

#### 步骤3开始前的状态
```
栈: [(0,0), (1,0), (2,0)]  ← 即将弹出(2,0)
迷宫:
* █ . . .    * = 已访问
* █ . █ .    
* . . . .    . = 未访问  
. █ █ █ .    █ = 墙
. . . █ .
```

#### 步骤3执行过程

```c
p = pop();  // 弹出(2,0)，现在p=(2,0)
```

**(2,0)这个位置可以往哪些方向走？**

1. **向右检查 (2,1)**：
   - `(2,1)` 是 `.`（通路，未访问）
   - ✅ 可以走！调用 `visit(2,1, (2,0))`
   - 含义：从(2,0)走到(2,1)，记录(2,0)是(2,1)的前驱

2. **向下检查 (3,0)**：
   - `(3,0)` 是 `.`（通路，未访问）  
   - ✅ 可以走！调用 `visit(3,0, (2,0))`
   - 含义：从(2,0)走到(3,0)，记录(2,0)是(3,0)的前驱

3. **向左检查 (2,-1)**：越界 ❌
4. **向上检查 (1,0)**：已访问 ❌

#### 步骤3结束后的状态
```
栈: [(0,0), (1,0), (2,1), (3,0)]  ← 新加入两个点
迷宫:
* █ . . .    
* █ . █ .    
* * . . .    // (2,1)变成*
* █ █ █ .    // (3,0)变成*  
. . . █ .
```

### 为什么这样设计？DFS的"探索-回溯"机制

#### DFS的核心思想：一条路走到黑，不行就回头

```c
// 伪代码说明DFS策略
while (栈不为空) {
    当前位置 = 弹出栈顶();
    
    if (到达终点) break;
    
    // 记录所有可能的下一步
    for (每个方向) {
        if (可以走) {
            标记为已访问;
            记录前驱(从哪来的);
            入栈;  // 先记录，稍后探索
        }
    }
    // 注意：由于栈是LIFO，最后入栈的会先被探索
}
```

#### 搜索路径的可视化

让我们跟踪实际的搜索顺序：

```
开始: (0,0)
↓
(0,0) → 只能向下 → (1,0)
↓  
(1,0) → 只能向下 → (2,0)
↓
(2,0) → 可以向右和向下
        ↓
        先探索最后入栈的: (3,0) ← 栈顶
        ↓
        (3,0) → 只能向下 → (4,0)
        ↓
        (4,0) → 可以向右 → (4,1)
        ↓
        (4,1) → 可以向右 → (4,2)
        ↓
        (4,2) → 遇到墙，死路！回溯到(2,1)
        ↓
        (2,1) → 继续探索...
```

### 前驱点的关键作用：重建路径

前驱点就像"面包屑"，让我们能找到回家的路：

```c
// 找到终点后，通过前驱链回溯
终点(4,4) ← 前驱是(3,4)
        (3,4) ← 前驱是(2,4)  
        (2,4) ← 前驱是(2,3)
        ... ← 一直回溯到起点(0,0)
```

### 从思维转换到代码的关键突破

#### 1. 理解"探索"与"访问"的区别

- **探索**：检查一个位置能不能走
- **访问**：实际走到那个位置并做记录

#### 2. 栈的作用：待探索的候选列表

把栈想象成你的"待办事项清单"：
```c
栈 = [要探索的位置1, 位置2, 位置3, ...]
```

#### 3. 前驱的作用：路径记忆

前驱数组就像你的"足迹记录"：
```c
前驱[当前位置] = 从哪个位置来的
```

### 完整的思维转换示例

**人类思维**："我从A点走到B点，再走到C点..."

**代码思维**：
```c
// 1. 把起点加入待探索列表
栈 = [起点]

// 2. 循环处理待探索列表
while (栈不为空) {
    // 3. 取出一个位置探索
    当前位置 = 弹出栈顶()
    
    // 4. 如果是终点，结束
    if (当前位置 == 终点) break;
    
    // 5. 检查所有邻居
    for (每个邻居) {
        if (邻居可走且未访问) {
            // 6. 标记访问，记录从哪里来的，加入待探索列表
            标记邻居为已访问
            记录[邻居]的前驱 = 当前位置
            栈.push(邻居)
        }
    }
}

// 7. 通过前驱链重建路径
```

### 总结

理解这个算法的关键是：

1. **栈管理探索顺序**：决定下一步探索哪里
2. **前驱记录来源**：知道每个点是从哪里来的  
3. **DFS策略**：深度优先，一条路走到底再回溯
4. **多方向记录**：一个点可以同时记录多个可行的下一步

现在你应该能理解为什么(2,0)可以探索两个地方了：它不是在同时走两条路，而是**把两条路都记录下来**，然后按照栈的顺序（后进先出）一条条尝试。

这种"记录所有可能性，然后系统性地尝试"正是DFS的精髓！



## 06_stack 问题解答与代码改进

> 1、修改本节的程序，要求从起点到终点正向打印路线。你能想到几种办法？
>
> 2、本节程序中`predecessor`这个数据结构占用的存储空间太多了，改变它的存储方式可以节省空间，想想该怎么改。
>
> 3、上一节我们实现了一个基于堆栈的程序，然后改写成递归程序，用函数调用的栈帧替代自己实现的堆栈。本节的DFS算法也是基于堆栈的，请把它改写成递归程序，这样改写可以避免使用`predecessor`数据结构，想想该怎么做。

### 问题一：从起点到终点正向打印路线

有几种方法可以实现正向打印路线：

#### 方法1：使用临时数组存储路径
```c
// 正向打印路径
void print_path_forward(struct point end_point) {
    struct point path[512];
    int path_len = 0;
    struct point p = end_point;
    
    // 收集路径（从终点到起点）
    while (p.row != -1 && p.col != -1) {
        path[path_len++] = p;
        p = predecessor[p.row][p.col];
    }
    
    // 正向打印（从起点到终点）
    printf("路径(从起点到终点):\n");
    for (int i = path_len - 1; i >= 0; i--) {
        printf("(%d, %d)", path[i].row, path[i].col);
        if (i > 0) printf(" -> ");
    }
    printf("\n");
}
```

#### 方法2：递归打印
```c
// 递归正向打印
void print_path_recursive(struct point p) {
    if (p.row == -1 && p.col == -1) return;
    
    struct point prev = predecessor[p.row][p.col];
    print_path_recursive(prev);
    
    printf("(%d, %d)", p.row, p.col);
    if (p.row != MAX_ROW - 1 || p.col != MAX_COL - 1) {
        printf(" -> ");
    }
}
```

#### 方法3：使用双向链表
```c
struct path_node {
    struct point p;
    struct path_node *next;
};

void print_path_linked_list(struct point end_point) {
    struct path_node *head = NULL;
    struct point p = end_point;
    
    // 构建链表（从终点到起点）
    while (p.row != -1 && p.col != -1) {
        struct path_node *new_node = malloc(sizeof(struct path_node));
        new_node->p = p;
        new_node->next = head;
        head = new_node;
        p = predecessor[p.row][p.col];
    }
    
    // 正向打印
    printf("路径(从起点到终点):\n");
    struct path_node *current = head;
    while (current != NULL) {
        printf("(%d, %d)", current->p.row, current->p.col);
        if (current->next != NULL) printf(" -> ");
        current = current->next;
    }
    printf("\n");
    
    // 释放内存
    while (head != NULL) {
        struct path_node *temp = head;
        head = head->next;
        free(temp);
    }
}
```

### 问题二：优化predecessor的存储空间

#### 优化方案1：使用方向编码
```c
// 方向编码：0=右, 1=下, 2=左, 3=上, -1=无前驱
char predecessor_dir[MAX_ROW][MAX_COL];

void init_predecessor_dir() {
    for (int i = 0; i < MAX_ROW; i++) {
        for (int j = 0; j < MAX_COL; j++) {
            predecessor_dir[i][j] = -1;
        }
    }
}

// 修改visit函数
void visit_dir(int row, int col, int from_dir) {
    struct point visit_point = { row, col };
    maze[row][col] = 2;
    predecessor_dir[row][col] = from_dir;  // 只存储方向
    push(visit_point);
}

// 根据方向编码重建路径
void print_path_from_dir(struct point end_point) {
    struct point path[512];
    int path_len = 0;
    struct point p = end_point;
    
    // 收集路径
    while (predecessor_dir[p.row][p.col] != -1) {
        path[path_len++] = p;
        
        // 根据方向找到前驱点
        int dir = predecessor_dir[p.row][p.col];
        if (dir == 0) p.col--;      // 来自左边
        else if (dir == 1) p.row--; // 来自上面
        else if (dir == 2) p.col++; // 来自右边
        else if (dir == 3) p.row++; // 来自下面
    }
    path[path_len++] = p;  // 起点
    
    // 正向打印
    printf("路径(从起点到终点):\n");
    for (int i = path_len - 1; i >= 0; i--) {
        printf("(%d, %d)", path[i].row, path[i].col);
        if (i > 0) printf(" -> ");
    }
    printf("\n");
}
```

#### 优化方案2：使用单字节存储坐标
```c
// 将(row,col)编码为一个字节：高4位存row，低4位存col
unsigned char predecessor_byte[MAX_ROW][MAX_COL];

void init_predecessor_byte() {
    for (int i = 0; i < MAX_ROW; i++) {
        for (int j = 0; j < MAX_COL; j++) {
            predecessor_byte[i][j] = 0xFF;  // 0xFF表示无前驱
        }
    }
}

// 编码坐标
unsigned char encode_point(struct point p) {
    return (p.row << 4) | p.col;
}

// 解码坐标
struct point decode_point(unsigned char code) {
    struct point p;
    p.row = (code >> 4) & 0x0F;
    p.col = code & 0x0F;
    return p;
}

void visit_byte(int row, int col, struct point pre) {
    struct point visit_point = { row, col };
    maze[row][col] = 2;
    predecessor_byte[row][col] = encode_point(pre);
    push(visit_point);
}
```

### 问题三：改写为递归DFS程序

#### 递归DFS实现（避免使用predecessor）
```c
#include <stdio.h>

#define MAX_ROW 5
#define MAX_COL 5

// 迷宫定义
int maze[MAX_ROW][MAX_COL] = {
    {0, 1, 0, 0, 0},
    {0, 1, 0, 1, 0},
    {0, 0, 0, 0, 0},
    {0, 1, 1, 1, 0},
    {0, 0, 0, 1, 0}
};

// 路径栈（用于存储找到的路径）
struct point {
    int row, col;
};
struct point path_stack[512];
int path_top = 0;

void path_push(struct point p) {
    path_stack[path_top++] = p;
}

void path_pop() {
    path_top--;
}

// 递归DFS函数
int dfs_recursive(int row, int col, int target_row, int target_col) {
    // 越界检查
    if (row < 0 || row >= MAX_ROW || col < 0 || col >= MAX_COL) {
        return 0;
    }
    
    // 墙或已访问检查
    if (maze[row][col] == 1 || maze[row][col] == 2) {
        return 0;
    }
    
    // 标记为已访问并加入路径
    maze[row][col] = 2;
    struct point current = {row, col};
    path_push(current);
    
    // 检查是否到达终点
    if (row == target_row && col == target_col) {
        return 1;  // 找到路径
    }
    
    // 递归探索四个方向
    if (dfs_recursive(row, col + 1, target_row, target_col) ||  // 右
        dfs_recursive(row + 1, col, target_row, target_col) ||  // 下
        dfs_recursive(row, col - 1, target_row, target_col) ||  // 左
        dfs_recursive(row - 1, col, target_row, target_col)) {  // 上
        return 1;  // 某个方向找到了路径
    }
    
    // 如果所有方向都没找到路径，回溯
    path_pop();
    return 0;
}

// 打印路径
void print_recursive_path() {
    printf("递归DFS找到的路径(从起点到终点):\n");
    for (int i = 0; i < path_top; i++) {
        printf("(%d, %d)", path_stack[i].row, path_stack[i].col);
        if (i < path_top - 1) printf(" -> ");
    }
    printf("\n");
}

int main(void) {
    printf("递归DFS迷宫求解...\n");
    
    // 保存原始迷宫状态（用于重置）
    int original_maze[MAX_ROW][MAX_COL];
    for (int i = 0; i < MAX_ROW; i++) {
        for (int j = 0; j < MAX_COL; j++) {
            original_maze[i][j] = maze[i][j];
        }
    }
    
    // 执行递归DFS
    if (dfs_recursive(0, 0, MAX_ROW - 1, MAX_COL - 1)) {
        print_recursive_path();
    } else {
        printf("没有找到路径！\n");
    }
    
    // 恢复迷宫状态
    for (int i = 0; i < MAX_ROW; i++) {
        for (int j = 0; j < MAX_COL; j++) {
            maze[i][j] = original_maze[i][j];
        }
    }
    
    return 0;
}
```

#### 递归DFS的优势

1. **代码更简洁**：不需要显式管理栈
2. **自动路径记录**：函数调用栈自动记录路径
3. **无需predecessor**：通过递归调用自动维护路径信息
4. **更符合思维模式**：深度优先的自然表达

#### 递归DFS的注意事项

1. **栈溢出风险**：对于大型迷宫可能导致栈溢出
2. **性能考虑**：函数调用有一定开销
3. **状态管理**：需要小心管理全局状态

### 完整整合版本

```c
#include <stdio.h>

#define MAX_ROW 5
#define MAX_COL 5

// 迷宫定义
int maze[MAX_ROW][MAX_COL] = {
    {0, 1, 0, 0, 0},
    {0, 1, 0, 1, 0},
    {0, 0, 0, 0, 0},
    {0, 1, 1, 1, 0},
    {0, 0, 0, 1, 0}
};

// 优化后的前驱存储（方向编码）
char predecessor_dir[MAX_ROW][MAX_COL];

void init_predecessor_dir() {
    for (int i = 0; i < MAX_ROW; i++) {
        for (int j = 0; j < MAX_COL; j++) {
            predecessor_dir[i][j] = -1;
        }
    }
}

// 栈实现
struct point { int row, col; } stack[512];
int top = 0;

void push(struct point p) { stack[top++] = p; }
struct point pop(void) { return stack[--top]; }
int is_empty(void) { return top == 0; }

void visit(int row, int col, int from_dir) {
    struct point visit_point = { row, col };
    maze[row][col] = 2;
    predecessor_dir[row][col] = from_dir;
    push(visit_point);
}

// 从方向编码重建并正向打印路径
void print_path_forward(struct point end_point) {
    struct point path[512];
    int path_len = 0;
    struct point p = end_point;
    
    // 收集路径（从终点到起点）
    while (predecessor_dir[p.row][p.col] != -1) {
        path[path_len++] = p;
        int dir = predecessor_dir[p.row][p.col];
        if (dir == 0) p.col--;      // 来自左边
        else if (dir == 1) p.row--; // 来自上面
        else if (dir == 2) p.col++; // 来自右边
        else if (dir == 3) p.row++; // 来自下面
    }
    path[path_len++] = p;  // 起点
    
    // 正向打印
    printf("路径(从起点到终点):\n");
    for (int i = path_len - 1; i >= 0; i--) {
        printf("(%d, %d)", path[i].row, path[i].col);
        if (i > 0) printf(" -> ");
    }
    printf("\n");
}

// 迭代DFS主函数
void dfs_iterative() {
    struct point p = {0, 0};
    init_predecessor_dir();
    
    maze[p.row][p.col] = 2;
    predecessor_dir[p.row][p.col] = -1;  // 起点无前驱
    push(p);
    
    while (!is_empty()) {
        p = pop();
        
        if (p.row == MAX_ROW - 1 && p.col == MAX_COL - 1) {
            printf("找到路径！\n");
            print_path_forward(p);
            return;
        }
        
        // 探索四个方向
        if (p.col + 1 < MAX_COL && maze[p.row][p.col + 1] == 0) {
            visit(p.row, p.col + 1, 2);  // 2表示来自左边
        }
        if (p.row + 1 < MAX_ROW && maze[p.row + 1][p.col] == 0) {
            visit(p.row + 1, p.col, 3);  // 3表示来自上面
        }
        if (p.col - 1 >= 0 && maze[p.row][p.col - 1] == 0) {
            visit(p.row, p.col - 1, 0);  // 0表示来自右边
        }
        if (p.row - 1 >= 0 && maze[p.row - 1][p.col] == 0) {
            visit(p.row - 1, p.col, 1);  // 1表示来自下面
        }
    }
    
    printf("没有找到路径！\n");
}

int main(void) {
    printf("=== 优化后的DFS迷宫求解 ===\n");
    dfs_iterative();
    return 0;
}
```

### 总结

通过这三种改进，我们实现了：

1. **正向打印路径**：更直观的路径显示
2. **空间优化**：将predecessor从8字节/点优化到1字节/点
3. **递归实现**：更简洁的代码，自动路径管理

这些改进展示了算法优化的重要思路：在保持正确性的前提下，不断追求更好的用户体验、更高的空间效率和更简洁的代码结构。



## 07_queue_maze

```c
#include <stdio.h>

#define MAX_ROW 5
#define MAX_COL 5

struct point { int row, col, predecessor; } queue[512];
int head = 0, tail = 0;

void enqueue(struct point p)
{
	queue[tail++] = p;
}

struct point dequeue(void)
{
	return queue[head++];
}

int is_empty(void)
{
	return head == tail;
}

int maze[MAX_ROW][MAX_COL] = {
	0, 1, 0, 0, 0,
	0, 1, 0, 1, 0,
	0, 0, 0, 0, 0,
	0, 1, 1, 1, 0,
	0, 0, 0, 1, 0,
};

void print_maze(void)
{
	int i, j;
	for (i = 0; i < MAX_ROW; i++) {
		for (j = 0; j < MAX_COL; j++)
			printf("%d ", maze[i][j]);
		putchar('\n');
	}
	printf("*********\n");
}

void visit(int row, int col)
{
	struct point visit_point = { row, col, head-1 };
	maze[row][col] = 2;
	enqueue(visit_point);
}

int main(void)
{
	struct point p = { 0, 0, -1 };

	maze[p.row][p.col] = 2;
	enqueue(p);
	
	while (!is_empty()) {
		p = dequeue();
		if (p.row == MAX_ROW - 1  /* goal */
		    && p.col == MAX_COL - 1)
			break;
		if (p.col+1 < MAX_COL     /* right */
		    && maze[p.row][p.col+1] == 0)
			visit(p.row, p.col+1);
		if (p.row+1 < MAX_ROW     /* down */
		    && maze[p.row+1][p.col] == 0)
			visit(p.row+1, p.col);
		if (p.col-1 >= 0          /* left */
		    && maze[p.row][p.col-1] == 0)
			visit(p.row, p.col-1);
		if (p.row-1 >= 0          /* up */
		    && maze[p.row-1][p.col] == 0)
			visit(p.row-1, p.col);
		print_maze();
	}
	if (p.row == MAX_ROW - 1 && p.col == MAX_COL - 1) {
		printf("(%d, %d)\n", p.row, p.col);
		while (p.predecessor != -1) {
			p = queue[p.predecessor];
			printf("(%d, %d)\n", p.row, p.col);
		}
	} else
		printf("No path!\n");

	return 0;
}
```

可以直接改06的stack为queue，然后还用前驱，再切换到这个版本



> 1、本节的例子直接在队列元素中加一个指针成员表示前趋，想一想为什么上一节的[例 12.3 “用深度优先搜索解迷宫问题”](https://akaedu.github.io/book/ch12s03.html#stackqueue.dfs)不能采用这种方法表示前趋？
>
> 2、本节例子中给队列分配的存储空间是512个元素，其实没必要这么多，那么解决这个问题至少要分配多少个元素的队列空间呢？跟什么因素有关？
>
> 是因为stack的top只能一直指向栈顶，同时，这个queue的大小也是够支持最大的探索范围是吗？但是具体来说怎么确定最大的大小呢？和什么有关？迷宫大小？

### 问题一：为什么DFS不能采用队列的这种前驱表示方法？

#### 关键差异：栈 vs 队列的访问特性

**队列（BFS）的特性：**
```c
struct point { int row, col, predecessor; } queue[512];
// predecessor 存储的是前驱点在队列中的索引
```

**为什么这在BFS中可行：**
1. **顺序访问**：BFS按层次顺序访问节点，队列中的节点索引是稳定的
2. **前驱保持**：前驱节点在出队后，其索引在队列数组中仍然有效
3. **线性增长**：队列索引单调递增，不会重复使用

**DFS（栈）的问题：**
```c
// 如果尝试在DFS中使用类似方法：
struct point { int row, col, predecessor; } stack[512];
```

**为什么这在DFS中不可行：**
1. **回溯破坏**：当DFS回溯时，栈顶元素被弹出，其索引可能被后续节点重用
2. **前驱失效**：前驱节点弹出后，其栈索引可能指向完全不同的节点
3. **索引混乱**：栈索引会不断被重用，无法稳定指向正确的前驱

#### 具体例子说明

**BFS工作方式：**
```
队列索引: 0   1   2   3   4   5
节点:     A   B   C   D   E   F
前驱:    -1  0   0   1   1   2

A(0) → B(1), C(2)   [前驱=0]
B(1) → D(3), E(4)   [前驱=1]  
C(2) → F(5)         [前驱=2]
```
即使B、C出队，它们的索引1、2在队列数组中仍然指向正确的节点。

**DFS工作方式：**
```
栈状态1: [A(0), B(1), C(2)]   // A→B→C
弹出C:   [A(0), B(1)]
新入栈: [A(0), B(1), D(2)]   // 索引2被重用！
```
现在如果D的前驱指向索引1(B)，这是正确的。但如果继续回溯：
```
弹出D,B: [A(0)]
新入栈: [A(0), E(1)]         // 索引1被重用！
```
如果E的前驱指向索引0(A)，这是正确的。但如果有节点前驱指向索引1，现在指向的是E而不是原来的B！

### 问题二：队列空间分配与迷宫大小的关系

#### 队列最小空间计算

**理论分析：**
- 最坏情况下，队列需要存储所有可达的迷宫位置
- 对于 `MAX_ROW × MAX_COL` 的迷宫，最大队列大小为迷宫中的通路数量

**具体计算：**
```c
// 我们的迷宫：5×5，但包含墙
int maze[MAX_ROW][MAX_COL] = {
    {0, 1, 0, 0, 0},  // 3个通路
    {0, 1, 0, 1, 0},  // 2个通路  
    {0, 0, 0, 0, 0},  // 5个通路
    {0, 1, 1, 1, 0},  // 2个通路
    {0, 0, 0, 1, 0}   // 3个通路
};
// 总通路数 = 3+2+5+2+3 = 15
```

**但是！BFS的特性决定了实际需要的空间更少：**

#### BFS的层次扩展特性

BFS按层次扩展，队列中同时存在的最大节点数由**迷宫宽度**决定：

```
层次0: [ (0,0) ]                     → 队列大小: 1
层次1: [ (1,0) ]                     → 队列大小: 1  
层次2: [ (2,0) ]                     → 队列大小: 1
层次3: [ (2,1), (3,0) ]              → 队列大小: 2
层次4: [ (2,2), (3,1), (4,0) ]       → 队列大小: 3
层次5: [ (2,3), (3,2), (4,1) ]       → 队列大小: 3
层次6: [ (2,4), (3,3), (4,2) ]       → 队列大小: 3
层次7: [ (3,4), (4,3) ]              → 队列大小: 2
层次8: [ (4,4) ]                     → 队列大小: 1
```

**关键发现**：队列最大大小为3，远小于总通路数15！

#### 通用公式

对于 `m × n` 的迷宫，BFS队列的最大大小为：
```c
min(m, n)  // 大致关系，实际取决于迷宫结构
```

更精确地说，最大队列大小由**迷宫的最宽层次**决定。

### 改进的BFS实现（优化空间）

基于以上分析，我们可以大幅减少队列空间：

```c
#include <stdio.h>

#define MAX_ROW 5
#define MAX_COL 5

// 计算最小队列大小：迷宫最宽层次 + 安全边界
// 对于5x5迷宫，最宽层次通常不超过min(5,5)=5，加安全边界
#define QUEUE_SIZE 10  // 原512 → 10，节省98%空间！

struct point { 
    int row, col; 
    int predecessor;  // 前驱在队列中的索引
} queue[QUEUE_SIZE];

int head = 0, tail = 0;

// 循环队列实现
void enqueue(struct point p) {
    queue[tail] = p;
    tail = (tail + 1) % QUEUE_SIZE;
}

struct point dequeue(void) {
    struct point p = queue[head];
    head = (head + 1) % QUEUE_SIZE;
    return p;
}

int is_empty(void) {
    return head == tail;
}

int is_full(void) {
    return (tail + 1) % QUEUE_SIZE == head;
}

int maze[MAX_ROW][MAX_COL] = {
    {0, 1, 0, 0, 0},
    {0, 1, 0, 1, 0},
    {0, 0, 0, 0, 0},
    {0, 1, 1, 1, 0},
    {0, 0, 0, 1, 0}
};

void print_maze(void) {
    for (int i = 0; i < MAX_ROW; i++) {
        for (int j = 0; j < MAX_COL; j++) {
            printf("%d ", maze[i][j]);
        }
        putchar('\n');
    }
    printf("*********\n");
}

void visit(int row, int col) {
    if (is_full()) {
        printf("错误：队列已满！可能需要增大QUEUE_SIZE\n");
        return;
    }
    
    struct point visit_point = { row, col, head }; // 前驱是当前队首
    maze[row][col] = 2;
    enqueue(visit_point);
}

int main(void) {
    struct point p = { 0, 0, -1 };

    maze[p.row][p.col] = 2;
    enqueue(p);
    
    while (!is_empty()) {
        p = dequeue();
        
        if (p.row == MAX_ROW - 1 && p.col == MAX_COL - 1) {
            break;
        }
        
        // 探索四个方向
        if (p.col + 1 < MAX_COL && maze[p.row][p.col + 1] == 0) {
            visit(p.row, p.col + 1);
        }
        if (p.row + 1 < MAX_ROW && maze[p.row + 1][p.col] == 0) {
            visit(p.row + 1, p.col);
        }
        if (p.col - 1 >= 0 && maze[p.row][p.col - 1] == 0) {
            visit(p.row, p.col - 1);
        }
        if (p.row - 1 >= 0 && maze[p.row - 1][p.col] == 0) {
            visit(p.row - 1, p.col);
        }
        
        print_maze();
    }
    
    if (p.row == MAX_ROW - 1 && p.col == MAX_COL - 1) {
        // 重建路径
        int path[512];
        int path_len = 0;
        
        // 从终点回溯到起点
        int current_index = head - 1;
        if (current_index < 0) current_index = QUEUE_SIZE - 1;
        
        while (current_index != -1) {
            path[path_len++] = current_index;
            current_index = queue[current_index].predecessor;
        }
        
        // 正向打印路径
        printf("路径(从起点到终点):\n");
        for (int i = path_len - 1; i >= 0; i--) {
            int idx = path[i];
            printf("(%d, %d)", queue[idx].row, queue[idx].col);
            if (i > 0) printf(" -> ");
        }
        printf("\n");
    } else {
        printf("No path!\n");
    }

    return 0;
}
```

### 关键洞察总结

#### 1. 前驱表示方法的差异

**BFS能用队列索引表示前驱的原因：**
- 队列顺序访问，索引稳定
- 前驱节点在队列数组中永久存在
- 索引单调递增（或循环），不会混淆

**DFS不能用栈索引表示前驱的原因：**
- 栈回溯时索引被重用
- 前驱节点弹出后索引失效
- 索引指向的内容会变化

#### 2. 队列空间与迷宫大小的关系

**队列最小空间由以下因素决定：**
- **迷宫宽度**：决定BFS每层最大节点数
- **迷宫结构**：墙的分布影响实际扩展
- **安全边界**：防止边界情况下的队列溢出

**经验公式：**
```c
// 保守估计
QUEUE_SIZE = min(MAX_ROW, MAX_COL) × 2 + 4;

// 我们的5x5迷宫
QUEUE_SIZE = min(5,5) × 2 + 4 = 14
// 实际测试中8-10就足够了
```

#### 3. 你的思考是正确的！

你观察到的关键点：
- ✅ **栈的top只能指向栈顶**：确实，这限制了索引的稳定性
- ✅ **队列大小与迷宫大小相关**：正确，但不是简单的乘法关系
- ✅ **BFS的空间效率比想象中高**：因为按层次扩展，同时存在的节点数有限

### 实际应用建议

1. **对于BFS**：使用 `QUEUE_SIZE = min(m, n) * 2 + 4` 作为安全大小
2. **对于DFS**：必须使用独立的前驱数组，不能依赖栈索引
3. **通用规则**：BFS空间复杂度 O(宽度)，DFS空间复杂度 O(深度)

这种理解对于优化算法和避免内存浪费非常重要！





## 11_command_interpreter

### 代码

```C
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MAX_ARGS 10
#define MAX_INPUT_LENGTH 256

int shell_parse(char *buf, char *argv[]);
void execute_command(int argc, char *argv[]);

// in:  format -> hello world "hello world" 1234567
// Multiple command parameters entered from the command line (number of parameters does not exceed 10)
// out:  format -> Parameter X: Content, Length: X
// Parse the command parameters through a character pointer array, and sequentially display the content and length of each parameter on the screen
//
int main(void)
{
    FILE *file;
    char input[MAX_INPUT_LENGTH];
    char *argv[MAX_ARGS + 1] = {NULL};
    int argc = 0;

    file = fopen("command_file.txt", "r");
    if (!file) {
        fprintf(stderr, "❌ Error: Cannot open input file '%s'\n", "command_file.txt");
        return 1;
    }

    printf("✅ Reading commands from '%s':\n\n", "command_file.txt");

    while (fgets(input, MAX_INPUT_LENGTH, file) != NULL) {
        input[strcspn(input, "\n")] = '\0';

        if (strlen(input) == 0 || strspn(input, " \t") == strlen(input)) {
            continue;
        }

        printf("➡️  Input: %s\n", input);

        argc = shell_parse(input, argv);

        if (argc == 0) {
            printf("⚠️  No valid command parsed.\n\n");
            continue;
        }

        execute_command(argc, argv);
        printf("\n");
    }

    fclose(file);
    return 0;
}

enum {
    STATE_INIT,
    STATE_IN_WORD
};

// shell_parse 和 execute_command 保持不变
int shell_parse(char *buf, char *argv[])
{
    int argc = 0;
    int state = 0;
    char *current = buf;
    char *start = buf;

    if (buf == NULL || argv == NULL) {
        return 0;
    }

    while (*current != '\0' && argc < MAX_ARGS) {
        switch (state) {
        case STATE_INIT:
            // 刚开始，遇到正常字符（非空白），存好开始位置，进入下一个状态处理
            // 如果时空格，换行，回车，则跳过，不做处理，跳过即可
            if (*current == '\0' || *current == '\t') {
                current++;
            } else {
                start = current;
                state = STATE_IN_WORD;
                current++;
            }
            break;
        case STATE_IN_WORD:
            if (*current == ' ' || *current == '\t' || *(current + 1) == '\0') {
                if (*(current + 1) == '\0' && *current != ' ' && *current != '\t') {
                    // 如果最后一个字符不是空白，需要包含它
                    current++;
                }
                // 结束当前参数
                if (*current == ' ' || *current == '\t' || *current == '\0') {
                    if (*current == ' ' || *current == '\t') {
                        *current = '\0';
                    }
                    // 指针存的是地址，而不是字符串
                    // 指针指向的地址存的是字符串的地址，而不是字符串本身
                    // 自己一开始的想法是一个个字符的复制，
                    // 这种方式低效还需要分配内存
                    argv[argc++] = start;
                    state = STATE_INIT;
                }
                current++;                
            } else {
                current++;
            }
            break;
        default:
            break;
        }
    }
    // 处理字符串结束时仍在单词状态的情况
    if (state == STATE_IN_WORD && start != NULL) {
        argv[argc++] = start;
    }

    return argc;
}

void execute_command(int argc, char *argv[])
{
    printf("Parsing result: Total %d parameters\n", argc);

    for (int i = 0; i < argc; i++) {
        printf("Parameter %d: Content: %s, Length: %zu\n",
               i + 1, argv[i], strlen(argv[i]));
    }

    if (strcmp(argv[0], "help") == 0) {
        printf("This is help command\n");
    } else if (strcmp(argv[0], "echo") == 0) {
        printf("Echo: ");
        for (int i = 1; i < argc; i++) {
            printf("%s ", argv[i]);
        }
        printf("\n");
    } else if (strcmp(argv[0], "add") == 0 && argc == 3) {
        int a = atoi(argv[1]);
        int b = atoi(argv[2]);
        printf("%d + %d = %d\n", a, b, a + b);
    } else {
        printf("Unknown command: %s\n", argv[0]);
    }
}

```



### 指针梳理

你的问题很好！让我用`"abc defg"`这个例子一步步解析，解释指针操作的原理：

#### 初始状态
```c
buf = "abc defg"
argv = [NULL, NULL, NULL, ...]  // 初始为空
argc = 0
state = STATE_NORMAL
current = ↑ (指向'a')
start = NULL
```

##### 第一步：遇到字符'a'
```c
// 状态：STATE_NORMAL, *current = 'a'
if (*current != ' ' && *current != '\t') {
    start = current;  // start现在指向'a'
}
// 此时：start = ↑ (指向'a')
```

##### 第二步：继续扫描到空格
```c
// 扫描过程：a→b→c→空格
// 当current指向空格时：
if (state == STATE_NORMAL && start && (*current == ' ')) {
    *current = '\0';        // 把空格变成字符串结束符
    argv[argc++] = start;   // argv[0] = 指向"abc"的指针
    start = NULL;           // 重置start
}
```

##### 关键理解：为什么`argv[argc++] = start`可行？

#### 内存布局变化：
```
处理前： ['a','b','c',' ','d','e','f','g','\0']
         ↑
        start指向这里

处理后： ['a','b','c','\0','d','e','f','g','\0']
         ↑
        argv[0]指向这里
```

##### 指针赋值原理：
- `start`保存的是内存地址，不是字符串内容
- `argv[0] = start`只是复制了这个地址值
- 现在`argv[0]`指向以`\0`结尾的"abc"字符串

#### 第三步：处理"defg"
```c
// current继续移动到'd'
if (*current != ' ' && *current != '\t') {
    start = current;  // start现在指向'd'
}

// 扫描到字符串结尾时：
if (state == STATE_NORMAL && start && *(current + 1) == '\0') {
    // 注意：此时current指向'g'，下一个字符是'\0'
    argv[argc++] = start;  // argv[1] = 指向"defg"的指针
}
```

#### 最终结果
```
内存: ['a','b','c','\0','d','e','f','g','\0']
              ↑             ↑
         argv[0]       argv[1]

argv = [指向"abc"的指针, 指向"defg"的指针, NULL, ...]
argc = 2
```

#### 与你想法"一个个字符赋值"的对比

**你的想法（需要复制）：**
```c
// 低效方式
char temp[100];
int j = 0;
for (int i = 0; buf[i] != ' '; i++) {
    temp[j++] = buf[i];
}
temp[j] = '\0';
argv[0] = strdup(temp);  // 还要分配新内存！
```

**指针方式（原地操作）：**
```c
// 高效方式：只是记录位置，不复制内容
start = current;  // 记录开始位置
// ... 扫描到空格
*current = '\0';  // 插入结束符
argv[argc++] = start;  // 记录指针
```

##### 优势
1. **零拷贝**：不复制字符串内容
2. **高效**：O(n)时间复杂度
3. **省内存**：只在原字符串上操作

这就是C语言字符串处理的精髓：通过指针和`\0`来"虚拟"分割字符串，而不是物理复制！



### bug

> 很好的问题！让我详细解释为什么要这样修改，以及原代码的问题所在：
>
> ## 原代码的核心问题
>
> ### 1. STATE_INIT 状态的逻辑错误
> ```c
> // 原代码（错误）
> if (*current == '\0' && *current == '\n' && *current == '\r')
> ```
> **问题分析：**
> - 这个条件永远为假，因为一个字符不可能同时等于`\0`、`\n`和`\r`
> - 实际上应该检查的是**空白字符**，而不是结束符
> - 这导致STATE_INIT状态无法正确跳过空白字符
>
> ### 2. 缺少字符串结束处理
> **问题表现：**
> - `"help"` 被解析为0个参数
> - `"add 5 3"` 只解析出2个参数而不是3个
>
> **原因：**
> 当扫描到字符串结尾时，循环条件 `*current != '\0'` 为假，循环退出。但如果此时还在 `STATE_IN_WORD` 状态，最后一个参数没有被添加到 `argv` 中。
>
> ## 修改原理详解
>
> ### 1. 正确的空白字符处理
> ```c
> // 修改后
> if (*current == ' ' || *current == '\t') {
>     current++;  // 跳过空白字符
> }
> ```
> **为什么这样改：**
> - 在 `STATE_INIT` 状态，我们的任务是**寻找参数的开始**
> - 遇到空格或制表符时，应该跳过，继续寻找
> - 遇到非空白字符时，标记为参数开始，进入 `STATE_IN_WORD`
>
> ### 2. 字符串结束的特殊处理
> ```c
> // 处理字符串结束的情况
> if (*(current + 1) == '\0' && *current != ' ' && *current != '\t') {
>     current++;  // 包含最后一个字符
> }
> ```
> **为什么需要这个：**
> 考虑字符串 `"help"` 的解析过程：
> ```
> 初始: h e l p \0
>           ↑
>        current指向'p'时，下一个字符是'\0'
> ```
> 如果不特殊处理，`current` 指向 'p' 时循环继续，但 'p' 不是空白字符，不会结束参数。然后循环检查 `*(current+1) == '\0'`，循环退出，参数丢失。
>
> ### 3. 循环外的参数处理
> ```c
> // 处理字符串结束时仍在单词状态的情况
> if (state == STATE_IN_WORD && start != NULL) {
>     argv[argc++] = start;
> }
> ```
> **为什么需要这个：**
> 这是对上述情况的补充保障。即使前面的特殊处理没覆盖到，这里也能确保最后一个参数被添加。
>
> ## 状态机工作流程示例
>
> 以 `"add 5 3"` 为例：
>
> ```
> 初始: a d d   5   3 \0
> 状态: STATE_INIT
> ```
>
> 1. **STATE_INIT** → 遇到'a'，`start`指向'a'，进入`STATE_IN_WORD`
> 2. **STATE_IN_WORD** → 扫描到空格，结束"add"参数
> 3. **STATE_INIT** → 跳过空格，遇到'5'，`start`指向'5'，进入`STATE_IN_WORD`
> 4. **STATE_IN_WORD** → 扫描到空格，结束"5"参数
> 5. **STATE_INIT** → 跳过空格，遇到'3'，`start`指向'3'，进入`STATE_IN_WORD`
> 6. **STATE_IN_WORD** → 发现`*(current+1) == '\0'`，包含'3'，结束参数
> 7. **循环外检查** → 确保"3"被添加
>
> ## 总结
>
> 这些修改确保了：
> 1. **完整性**：所有参数都被正确解析
> 2. **正确性**：空白字符被正确处理
> 3. **边界安全**：字符串开始和结束的情况都被覆盖
> 4. **状态一致**：状态机在各种情况下都能正确转换
>
> 这就是为什么需要这样修改的原因！



## 15_url_parser

### 代码

```C
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>

/**
 * URL参数解析器
 * 输入：包含http/https超链接的字符串
 * 输出：解析出所有的key-value键值对，每行显示一个
 */
// 该版本安全通过
// 完全避免动态内存分配
//  int parse_url(const char* url) {
//     int err = 0;
    
//     const char* query_start = strchr(url, '?');
//     if (query_start == NULL) {
//         printf("没有查询参数\n");
//         err = -1;
//         goto exit;
//     }
    
//     query_start++;
    
//     const char* current = query_start;
//     while (*current != '\0') {
//         // 找到当前参数的开始和结束
//         const char* param_start = current;
//         const char* param_end = strchr(param_start, '&');
        
//         if (param_end == NULL) {
//             param_end = param_start + strlen(param_start);
//         }
        
//         // 在当前参数中查找 =
//         const char* equal_sign = strchr(param_start, '=');
//         if (equal_sign != NULL && equal_sign < param_end) {
//             printf("key = %.*s, value = %.*s\n", 
//                 (int)(equal_sign - param_start), param_start,
//                 (int)(param_end - equal_sign - 1), equal_sign + 1);
//         } else {
//             // 只有 key，没有 value
//             printf("%.*s\n", (int)(param_end - param_start), param_start);
//         }
        
//         // 移动到下一个参数
//         if (*param_end == '&') {
//             current = param_end + 1;
//         } else {
//             break;
//         }
//     }

// exit:
//     return err;
// }


// 有问题，为什么这份代码在我对Ubuntu虚拟机上不会出问题？
// 但是在这里会崩溃？
// strtok的问题吗？strtok 函数会修改原始字符串，它用 \0 替换分隔符
// 但是操作的是复制过后的值了呀？
// 是因为编译器的问题？
// int parse_url(const char* url) {
//     int err = 0;
    
//     char *query_start  = strchr(url, '?');
//     if (query_start == NULL) {
//         printf("没有查询参数\n");
//         err = -1;
//         goto exit;
//     }
    
//     query_start++;
//     // 复制参数字符串到可修改的缓冲区
//     char* query_str = strdup(query_start);
//     if (query_str == NULL) {
//         err = -1;
//         goto exit;
//     }
    
//     // printf("...test\n");
//     // 一开始怀疑是这里的问题，需要进一步证明
//     char* token = strtok(query_str, "&");
//     // printf("test...\n");
//     while (token != NULL) {
//         char *equal_sign = strchr(token, '=');
//         if (equal_sign == NULL) {
//             printf("only key\n");
//         } else {
//             *equal_sign = '\0';
//             printf("key = %s, value = %s\n", token, equal_sign + 1);
//         }
//         token = strtok(NULL, "&");
//     }

//     free(query_str);
// exit:
//     return err;
// }


// 这个版本也会出问题?
// 同样也是在这台机器上会有问题，但是在我的电脑上没有问题，在onlinegdb上跑也没问题
// 看看编译器版本？
// int parse_url(const char* url) {
//     int err = 0;
    
//     const char* query_start = strchr(url, '?');
//     if (query_start == NULL) {
//         printf("没有查询参数\n");
//         err = -1;
//         goto exit;
//     }
    
//     query_start++;
    
//     // 复制参数字符串
//     char* query_str = strdup(query_start);
//     if (query_str == NULL) {
//         err = -1;
//         goto exit;
//     }

//     // 手动分割参数，避免使用 strtok
//     char* current = query_str;
//     while (*current != '\0') {
//         // 找到当前参数的结尾（& 或字符串结尾）
//         char* param_end = strchr(current, '&');
//         if (param_end != NULL) {
//             *param_end = '\0';  // 临时截断
//         }
        
//         // 在当前参数中查找 =
//         char* equal_sign = strchr(current, '=');
//         if (equal_sign != NULL) {
//             *equal_sign = '\0';  // 分割 key 和 value
//             printf("key = %s, value = %s\n", current, equal_sign + 1);
//         } else {
//             printf("%s\n", current);
//         }
        
//         // 移动到下一个参数
//         if (param_end != NULL) {
//             current = param_end + 1;
//         } else {
//             break;  // 没有更多参数
//         }
//     }

//     free(query_str);

// exit:
//     return err;
// }


// 这一版使用malloc就行？
// 看来是这个云环境的libc库的strdup 有问题？
int parse_url(const char* url) {
    int err = 0;
    
    const char* query_start = strchr(url, '?');
    if (query_start == NULL) {
        printf("没有查询参数\n");
        err = -1;
        goto exit;
    }
    
    query_start++;
    
    // 使用 malloc + strcpy 替代 strdup
    size_t len = strlen(query_start);
    char* query_str = (char*)malloc(len + 1);
    if (query_str == NULL) {
        printf("内存分配失败\n");
        err = -1;
        goto exit;
    }
    strcpy(query_str, query_start);

    // 手动分割参数
    char* current = query_str;
    while (*current != '\0') {
        char* param_end = strchr(current, '&');
        if (param_end != NULL) {
            *param_end = '\0';
        }
        
        char* equal_sign = strchr(current, '=');
        if (equal_sign != NULL) {
            *equal_sign = '\0';
            printf("key = %s, value = %s\n", current, equal_sign + 1);
        } else {
            printf("%s\n", current);
        }
        
        if (param_end != NULL) {
            current = param_end + 1;
        } else {
            break;
        }
    }

    free(query_str);

exit:
    return err;
}

int main() {
    const char* test_url = "https://cn.bing.com/search?name=John&age=30&city=New+York";

    printf("Parsing URL: %s\n", test_url);
    printf("Parameters:\n");

    parse_url(test_url);

    return 0;
}
```







## 16_mysed



## 17_myfile



## 18_mywc



## 19_mytrans



## 20_mybash






## TODO



## TODO





