## introduction

这是为了应付手撕算法。

主要看[代码随想录](https://www.bilibili.com/video/BV1fA4y1o715)





## array

### 二分查找

#### 基础

```C
// [a, b)
int binary_search1(int* nums, int numsSize, int target){
    int left = 0, right = numsSize;
    int mid = 0;
    while (left < right) {
       int mid = left + (right - left) / 2;
        if (nums[mid] > target) {
            right = mid;
        } else if (nums[mid] < target){
            left = mid + 1;
        } else {
            return mid;
        }
    }
    return -1;
}

// [a, b]
// [1, 1]
int binary_search2(int* nums, int numsSize, int target){
    int left = 0, right = numsSize - 1; // because the right is close, and invole .
    int mid = 0;
    while (left <= right) {
        int mid = left + (right - left) / 2;
        
        if (nums[mid] > target) {
            right = mid - 1;
        } else if (nums[mid] < target){
            left = mid + 1;
        } else {
            return mid;
        }
    }
    return -1;
}

```

**关键在于考虑使用什么的区间。**

左闭右闭的情况下：获得的size要减一，while 的条件使用 left <= right (要考虑left==right，一个元素的时候也要判断)，进行二分的时候，比如获取到的值大于target，说明要改动右边界，同时，又因为是两边都是闭区间，而这一次判断已经知道这个mid肯定不会是下一次判断区间里的了，所以直接加一即可，小于同理。

左闭右开：size大小即可，while条件又要使用称 left < right ，因为不用判断一个相同的，直接在上一次就可以出结果了。另外，对于nums[mid]大于target，改右边界的时候，因为右边界是开的，那就直接用mid即可，如果是左区间，那就要加一了。



1. **循环条件为什么是 <= ？**
    - 当 `left == right` 时，区间 `[left, right]` 仍有一个元素需要检查
    - 如果写成 `<` 会漏查最后一个元素

2. **mid计算为什么要这样写？**
    - 传统写法 `(left + right)/2` 可能溢出
    - 改进写法 `left + (right - left)/2` 数学等价但更安全

3. **边界更新为什么要 +1/-1？**
    - 因为区间已经明确不包含mid，必须跳过mid位置
    - 不这样做可能导致死循环






#### **变种1：找第一个等于target的元素**

```c
// 示例数组：{1,2,2,2,3} 找第一个2的位置
int find_first(int* nums, int numsSize, int target) {
    int left = 0, right = numsSize - 1;
    while (left <= right) {
        int mid = left + (right - left)/2;
        if (nums[mid] >= target) {
            right = mid - 1; // 向左压缩找更小的
        } else {
            left = mid + 1;
        }
    }
    // 最后检查left是否越界且值匹配
    return (left < numsSize && nums[left] == target) ? left : -1;
}
```

#### **变种2：找最后一个等于target的元素**

```c
int find_last(int* nums, int numsSize, int target) {
    int left = 0, right = numsSize - 1;
    while (left <= right) {
        int mid = left + (right - left)/2;
        if (nums[mid] <= target) {
            left = mid + 1; // 向右压缩找更大的
        } else {
            right = mid - 1;
        }
    }
    // 检查right是否越界且值匹配
    return (right >= 0 && nums[right] == target) ? right : -1;
}
```

#### **变种3：查找插入位置（LeetCode 35）**

```c
int searchInsert(int* nums, int numsSize, int target) {
    int left = 0, right = numsSize; // 注意right初始值
    while (left < right) {          // 不同循环条件
        int mid = left + (right - left)/2;
        if (nums[mid] >= target) {
            right = mid; // 不-1
        } else {
            left = mid + 1;
        }
    }
    return left;
}
```







### 移除元素

> **一、问题描述**
>
> 给定一个数组 `nums` 和一个值 `val`，你需要 **原地** 移除所有等于 `val` 的元素，并返回移除后数组的新长度。
> **要求**：
>
> 1. 不能使用额外的数组空间
> 2. 元素的顺序可以改变
> 3. 不需要考虑数组中超出新长度后面的元素
>
> 示例：
> 输入：`nums = [3,2,2,3], val = 3`
> 输出：`新长度=2`, 数组变为 `[2,2,_,_]`

#### 基础

- **解法1：暴力解法（新手易懂版）**

    ```C
    // 时间复杂度：O(n^2) | 空间复杂度：O(1)
    int removeElement(int* nums, int numsSize, int val) {
        for(int i = 0; i < numsSize; i++) {
            if(nums[i] == val) { // 找到要删除的元素
                // 整体前移一位
                for(int j = i; j < numsSize-1; j++) {
                    nums[j] = nums[j+1];
                }
                numsSize--; // 数组长度减1
                i--;       // 重要！当前位置需要重新检查
            }
        }
        return numsSize;
    }
    ```

    **缺点**：每次删除都要移动大量元素，效率低



- **解法2：双指针法（最优解）**

    **核心逻辑**：

    - 快指针只管往前冲，找到要保留的元素
    - 慢指针负责记录有效元素的位置

    稍微不太 trial。

    具体来说就是，fast一直遍历，一般情况下遇到数组中的值和val不相同的，那就不变，同时slow和fast一起向前推进。

    但是如果遇到和val相同的，那就只有fast继续遍历，但是slow就依然停留在指向这个相同val的数组这里，slow就是这个相同val的index。

    知道下一次遇到正常情况，不是val的时候，那 nums[fast] 就可以直接覆盖nums[slow]的值，就好像做到了向前移动。

    ```C
    int removeElement(int* nums, int numsSize, int val) { 
        int slow = 0; // 初始化慢指针
        for(int fast = 0; fast < numsSize; fast++) { // 快指针遍历
            if(nums[fast] != val) {      // 发现需要保留的元素
                nums[slow] = nums[fast]; // 将元素复制到新位置
                slow++;                  // 移动慢指针
            }
            // 如果等于val，快指针直接跳过
            return slow; // 最终慢指针的位置就是新长度
        }
    }
    
    
    ```
    
    核心：
    
    快指针，获取的新数组所需的元素
    慢指针，新数组的下标。







**总结模板：**

- **核心原理**：通过两个指针的 **相对运动** 实现高效遍历
- **适用场景**：数组操作、字符串处理、链表问题

```C
int function(int* arr, int size) {
    if (size == 0) return 0; // 处理空输入
    
    int slow = 0; // 慢指针初始位置
    
    for (int fast = 0; fast < size; fast++) { // 快指针遍历
        if (满足保留条件) { 
            if (slow != fast) { // 避免不必要的赋值
                arr[slow] = arr[fast]; 
            }
            slow++; // 移动慢指针
        }
    }
    return slow; // 返回新长度
}
```

> 删除有序数组中的重复项
>
> 比较含退格的字符串



#### 变种1：删除有序数组中的重复项 leetcode26

```C
int removeDuplicates(int* nums, int numsSize) {
    if (numsSize == 0) return 0;
    int slow = 0;
    for (int fast = 1; fast < numsSize; fast++) { 
        if (nums[fast] != nums[slow]) { 
            slow++;
            nums[slow] = nums[fast];
        } 
    } 
    return slow + 1;        
}
```



#### 变种2：删除重复项（保留最多2个）

```C
// LeetCode 80. 删除有序数组中的重复项 II
int removeDuplicates(int* nums, int numsSize) {
    if (numsSize <= 2) return numsSize;
    
    int slow = 1; // 允许保留到第二个重复项
    for (int fast = 2; fast < numsSize; fast++) {
        // 比较当前元素与慢指针前一位
        if (nums[fast] != nums[slow-1]) { 
            slow++;
            nums[slow] = nums[fast];
        }
    }
    return slow + 1;
}
```





#### 变种3：移动零到末尾

```C
void moveZeroes(int* nums, int numsSize) { 
    int slow = 0;
    for (int fast = 0; fast < numsSize; fast++) { 
        if (nums[fast] != 0) { 
            nums[slow] = nums[fast];
            slow++;                                                                                                         
        }
    }
    printf("slow:%d\n", slow);
    for (int j = 0; j < numsSize - slow; j++) {
        nums[numsSize - 1 - j] = 0;
        printf("%d  %d\n", numsSize - 1 - j, nums[numsSize - 1 - j]);
    }
    for (int i = 0; i < numsSize; i++) {
        printf("a[%d]: %d\n", i, nums[i]);
    }
}

```

想的是直接快慢指针直接往前覆盖，遇到0记录一下，之后再在后面补零。还有：

```C
// LeetCode 283. 移动零
void moveZeroes(int* nums, int numsSize) {
    int slow = 0;
    // 第一步：移除非零元素
    for (int fast = 0; fast < numsSize; fast++) {
        if (nums[fast] != 0) {
            nums[slow++] = nums[fast];
        }
    }
    // 第二步：填充零
    while (slow < numsSize) {
        nums[slow++] = 0;
    }
}
```



#### **变种4：合并有序数组**

```C
void merge(int* nums1, int nums1Size, int m, int* nums2, int nums2Size, int n) {
    int p = m + n - 1;    // 合并后的末尾
    int p1 = m - 1;       // nums1末尾
    int p2 = n - 1;       // nums2末尾
    
    while (p2 >= 0) {     // 只需处理nums2剩余元素
        if (p1 >= 0 && nums1[p1] > nums2[p2]) {
            nums1[p--] = nums1[p1--];
        } else {
            nums1[p--] = nums2[p2--];
        }
    }
}
```

双指针从后向前合并，避免覆盖未处理元素。





#### 另外：删除排序链表中的重复元素







总结一下特点，好像都用到了数组排好序的特性？





### 有序数组的平方

**问题分析**

给定非递减整数数组，返回各元素平方后的非递减数组。直接平方后排序时间复杂度为O(n log n)，但利用原数组特性可将时间复杂度优化至O(n)。

- **关键思路**

    **双指针法**：利用原数组已排序的特性，平方后的最大值必定出现在数组两端。通过双指针从两端向中间遍历，比较平方值，将较大者逆序填充到结果数组末尾。

1. **初始化指针**：左指针`i`指向数组起始，右指针`j`指向数组末尾，结果数组`ans`从后往前填充。
2. **比较平方值**：每次比较左右指针所指元素的平方值，较大者存入`ans`末尾，移动相应指针。
3. **终止条件**：当左右指针相遇时处理完所有元素。

```C
/**                                                                                                                         
 * Note: The returned array must be malloced, assume caller calls free().                                                   
 */                                                                                                                         
int* sortedSquares(int* nums, int numsSize, int* returnSize) {                                                              
    *returnSize = numsSize;
    int *result = (int *)malloc(sizeof(int) * numsSize);

    int left = 0;                                                                                                           
    int right = numsSize - 1;
    for (int index = numsSize -1 ; index>= 0 ; index--) {
        int left_num = nums[left] * nums[left];
        int right_num = nums[right] * nums[right];
        
        if (left_num > right_num) {
            result[index] = left_num;
            left++;
        } else {
            result[index] = right_num;
            right--;
        }   
    }   

    return result;
}   

```



#### 模板

```C
// 双指针从两端向中间遍历模板
int* solution(int* arr, int n) {
    int left = 0, right = n - 1, pos = n - 1;
    int* result = malloc(n * sizeof(int));
    while (left <= right) {
        // 根据条件选择左或右指针元素处理
        if (condition) {
            result[pos--] = process(arr[left++]);
        } else {
            result[pos--] = process(arr[right--]);
        }
    }
    return result;
}
```

**适用场景**：处理有序数组的合并、查找或转换问题，特别是当极值出现在数组两端时。



#### 变种1：**合并两个有序数组**（LeetCode 88）

```C
void merge(int* nums1, int nums1Size, int m, int* nums2, int nums2Size, int n) {
    int p = m + n - 1;    // 合并后的末尾
    int p1 = m - 1;       // nums1末尾
    int p2 = n - 1;       // nums2末尾
    
    while (p2 >= 0) {     // 只需处理nums2剩余元素
        if (p1 >= 0 && nums1[p1] > nums2[p2]) {
            nums1[p--] = nums1[p1--];
        } else {
            nums1[p--] = nums2[p2--];
        }
    }
}
```

双指针从后向前合并，避免覆盖未处理元素。



#### 变种2：**颜色分类**（LeetCode 75）

```C
void swap(int *a, int *b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}

void sortColors(int* nums, int numsSize) {
    int low = 0, curr = 0;
    int high = numsSize - 1;
    while (curr <= high) {
        if (nums[curr] == 0) {
            swap(&nums[low], &nums[curr]);
            low++;
            curr++;
        } else if (nums[curr] == 1) {
            curr++;
        } else { // nums[curr] == 2
            swap(&nums[curr], &nums[high]);
            high--;
        }
    }
}
```

- **三指针法（荷兰国旗问题）**：将数组划分为三个区域：
    - `[0, low-1]`：存放0
    - `[low, high]`：存放1（动态调整）
    - `[high+1, end]`：存放2
- 通过`low`指针标记0的右边界，`high`指针标记2的左边界，`curr`指针遍历数组，动态交换元素。

> 1. **初始化指针**：
>     - `low = 0`：指向下一个0应插入的位置
>     - `high = numsSize - 1`：指向下一个2应插入的位置
>     - `curr = 0`：当前遍历指针
> 2. **遍历与交换**：
>     - 当`nums[curr] == 0`：与`low`处元素交换，`low`和`curr`右移。
>     - 当`nums[curr] == 1`：跳过，`curr`右移。
>     - 当`nums[curr] == 2`：与`high`处元素交换，`high`左移（此时`curr`不移动，需检查交换后的元素）。
> 3. **终止条件**：`curr > high`时所有元素处理完毕。

除了三指针，当时的问题是被覆盖了元素，所以应该第一时间想到交换的！



#### 变种3：**两数之和 II**（LeetCode 167）













### 长度最小的子数组

#### 基础

给定一个含有 n 个正整数的数组和一个正整数 s ，找出该数组中满足其和 ≥ s 的长度最小的 连续 子数组，并返回其长度。如果不存在符合条件的子数组，返回 0。

示例：

- 输入：s = 7, nums = [2,3,1,2,4,3]
- 输出：2
- 解释：子数组 [4,3] 是该条件下的长度最小的子数组。

提示：

- 1 <= target <= 10^9
- 1 <= nums.length <= 10^5
- 1 <= nums[i] <= 10^5



> 还有一些方法：
> 方法一：暴力法
> 暴力法是最直观的方法。初始化子数组的最小长度为无穷大，枚举数组 nums 中的每个下标作为子数组的开始下标，对于每个开始下标 i，需要找到大于或等于 i 的最小下标 j，使得从 nums[i] 到 nums[j] 的元素和大于或等于 s，并更新子数组的最小长度（此时子数组的长度是 j−i+1）。
>
> 注意：使用 Python 语言实现方法一会超出时间限制。
>
> ```C
> int minSubArrayLen(int s, int* nums, int numsSize) {
>     if (numsSize == 0) {
>         return 0;
>     }
>     int ans = INT_MAX;
>     for (int i = 0; i < numsSize; i++) {
>         int sum = 0;
>         for (int j = i; j < numsSize; j++) {
>             sum += nums[j];
>             if (sum >= s) {
>                 ans = fmin(ans, j - i + 1);
>                 break;
>             }
>         }
>     }
>     return ans == INT_MAX ? 0 : ans;
> }
> ```
>
> 复杂度分析
>
> 时间复杂度：O(n 2)，其中 n 是数组的长度。需要遍历每个下标作为子数组的开始下标，对于每个开始下标，需要遍历其后面的下标得到长度最小的子数组。
>
> 空间复杂度：O(1)。
>
> 方法二：前缀和 + 二分查找
> 方法一的时间复杂度是 O(n 2)，因为在确定每个子数组的开始下标后，找到长度最小的子数组需要 O(n) 的时间。如果使用二分查找，则可以将时间优化到 O(logn)。
>
> 为了使用二分查找，需要额外创建一个数组 sums 用于存储数组 nums 的前缀和，其中 sums[i] 表示从 nums[0] 到 nums[i−1] 的元素和。得到前缀和之后，对于每个开始下标 i，可通过二分查找得到大于或等于 i 的最小下标 bound，使得 sums[bound]−sums[i−1]≥s，并更新子数组的最小长度（此时子数组的长度是 bound−(i−1)）。
>
> 因为这道题保证了数组中每个元素都为正，所以前缀和一定是递增的，这一点保证了二分的正确性。如果题目没有说明数组中每个元素都为正，这里就不能使用二分来查找这个位置了。
>
> 在很多语言中，都有现成的库和函数来为我们实现这里二分查找大于等于某个数的第一个位置的功能，比如 C++ 的 lower_bound，Java 中的 Arrays.binarySearch，C# 中的 Array.BinarySearch，Python 中的 bisect.bisect_left。但是有时面试官可能会让我们自己实现一个这样的二分查找函数
>
> ```C
> int lower_bound(int *a, int l, int r, int q) {
>     if (a[r] < q) return -1;
>     while (l < r) {
>         int mid = (l + r) >> 1;
>         if (a[mid] >= q) {
>             r = mid;
>         } else {
>             l = mid + 1;
>         }
>     }
>     return l;
> }
> int minSubArrayLen(int s, int *nums, int numsSize) {
>     if (numsSize == 0) {
>         return 0;
>     }
>     int ans = INT_MAX;
>     int *sums = (int *)malloc(sizeof(int) * (numsSize + 1));
>     // 为了方便计算，令 size = n + 1
>     // sums[0] = 0 意味着前 0 个元素的前缀和为 0
>     // sums[1] = A[0] 前 1 个元素的前缀和为 A[0]
>     // 以此类推
>     for (int i = 1; i <= numsSize; i++) {
>         sums[i] = sums[i - 1] + nums[i - 1];
>     }
>     for (int i = 1; i <= numsSize; i++) {
>         int target = s + sums[i - 1];
>         int bound = lower_bound(sums, 1, numsSize, target);
>         if (bound != -1) {
>             ans = fmin(ans, bound - (i - 1));
>         }
>     }
>     return ans == INT_MAX ? 0 : ans;
> }
> ```
>
> 复杂度分析
>
> 时间复杂度：O(nlogn)，其中 n 是数组的长度。需要遍历每个下标作为子数组的开始下标，遍历的时间复杂度是 O(n)，对于每个开始下标，需要通过二分查找得到长度最小的子数组，二分查找得时间复杂度是 O(logn)，因此总时间复杂度是 O(nlogn)。
>
> 空间复杂度：O(n)，其中 n 是数组的长度。额外创建数组 sums 存储前缀和。
>



- **滑动窗口法**

    ```C
    #define min(a, b) ((a) < (b) ? (a) : (b))
    
    int minSubArrayLen(int target, int* nums, int numsSize) {
        int left = 0;
        int sum_window = 0;
        int min_len = INT_MAX;
        for (int right = 0; right < numsSize; right++) {
            sum_window += nums[right];
            while (sum_window >= target) {
                int current_len = right - left + 1;
                min_len = min(min_len, current_len);
                sum_window = sum_window - nums[left];
                left++;
            }
        }
        return min_len == INT_MAX ? 0 : min_len;
    }
    
    ```

    定义两个指针 start 和 end 分别表示子数组（滑动窗口窗口）的开始位置和结束位置，维护变量 sum 存储子数组中的元素和（即从 nums[start] 到 nums[end] 的元素和）。

    初始状态下，start 和 end 都指向下标 0，sum 的值为 0。

    每一轮迭代，将 nums[end] 加到 sum，如果 sum≥s，则更新子数组的最小长度（此时子数组的长度是 end−start+1），然后将 nums[start] 从 sum 中减去并将 start 右移，直到 sum<s，在此过程中同样更新子数组的最小长度。在每一轮迭代的最后，将 end 右移。

    这里最好看动画，然后理解。





#### 变种1：**LeetCode 713. 乘积小于K的子数组**

滑动窗口统计乘积小于 `k` 的窗口数目，每次扩展时累加新增子数组数量。

```C
int numSubarrayProductLessThanK(int* nums, int numsSize, int k) {
    if (k <= 1) return 0; // 处理特殊情况：k <= 1时无解
    
    int left = 0;         // 窗口左边界
    int product = 1;      // 当前窗口的乘积
    int count = 0;        // 统计符合条件的子数组数目
    
    for (int right = 0; right < numsSize; right++) {
        product *= nums[right]; // 扩展右边界并更新乘积
        
        // 当乘积超过等于k时，收缩左边界
        while (product >= k) {
            product /= nums[left];
            left++;
        }
        
        // 统计以right结尾的连续子数组数目
        count += (right - left + 1);
    }
    
    return count;
}
```

主要理解这个 count。

记住上面是超过就收缩！！和基础的那个理解类似：获取最小的长度（大于就收缩），这个就获取小于k的，只是要再多定一个变量记录有多少个子数组！







#### 变种2：**LeetCode 3. 无重复字符的最长子串**

**乘积最小的子数组**：需处理负数和零的情况，滑动窗口需调整。

- 滑动窗口维护无重复字符的窗口，记录最大长度。

```C
#define MAX_CHAR 128

int lengthOfLongestSubstring(char* s) {
    int map[MAX_CHAR];
    memset(map, -1, sizeof(map));
    int max_len = 0;

    int left = 0;
    for (int right = 0; s[right] != '\0'; right++) {
        char c = s[right];
        if (map[c] >= left) {
            left = map[c] + 1;
        }
        map[c] = right;
        
        int current_len = right - left + 1;
        if (current_len> max_len) {
            max_len = current_len;
        }
    }
    return max_len;
}
```





#### 变种3：**LeetCode 76. 最小覆盖子串**

如和等于 `k` 的最长子数组，可用哈希表记录前缀和的最早出现位置。

- 滑动窗口扩展至包含所有目标字符后收缩，记录最小窗口。







#### 总结

- **滑动窗口**：适用于连续子数组/子串问题，元素全为正数时最优。
- **前缀和+二分**：适用于元素全为正数且需快速查找的场景。
- **变形问题**：需结合哈希表、单调队列等结构处理复杂条件（如负数、乘积等）。





### 螺旋矩阵Ⅱ

给定一个正整数 n，生成一个包含 1 到 n^2 所有元素，且元素按顺时针顺序螺旋排列的正方形矩阵。

示例:

输入: 3 输出: [ [ 1, 2, 3 ], [ 8, 9, 4 ], [ 7, 6, 5 ] ]



#### 基础

主要是 搞清楚区间的：左闭右开。（循环不变量）

模拟顺时针画矩阵的过程:

- 填充上行从左到右
- 填充右列从上到下
- 填充下行从右到左
- 填充左列从下到上









## 链表

### 移除链表元素 leetcode 203

主要是学会虚拟头节点。

题意：删除链表中等于给定值 val 的所有节点。

示例 1： 输入：head = [1,2,6,3,4,5,6], val = 6 输出：[1,2,3,4,5]

示例 2： 输入：head = [], val = 1 输出：[]

示例 3： 输入：head = [7,7,7,7], val = 7 输出：[]

> ### **解法一：虚拟头节点法（推荐）**
> #### **核心思路**
> 通过引入虚拟头节点（Dummy Node），统一处理头节点和普通节点的删除逻辑，避免复杂的条件判断。
>
> #### **代码实现**
> ```c
> struct ListNode {
>     int val;
>     struct ListNode *next;
> };
> 
> struct ListNode* removeElements(struct ListNode* head, int val) {
>     // 创建虚拟头节点
>     struct ListNode* dummy = (struct ListNode*)malloc(sizeof(struct ListNode));
>     dummy->next = head;
>     struct ListNode* curr = dummy;
> 
>     while (curr->next != NULL) {
>         if (curr->next->val == val) {
>             struct ListNode* temp = curr->next;
>             curr->next = temp->next;
>             free(temp); // 删除节点并释放内存
>         } else {
>             curr = curr->next; // 移动指针
>         }
>     }
> 
>     struct ListNode* new_head = dummy->next;
>     free(dummy); // 释放虚拟头节点
>     return new_head;
> }
> ```
>
> #### **关键点分析**
> 1. **虚拟头节点**：将头节点的删除逻辑与普通节点统一。
> 2. **双指针技巧**：`curr` 指针始终指向待检查节点的前驱节点。
> 3. **内存管理**：及时释放被删除节点和虚拟头节点的内存。
>
> ---
>
> ### **解法二：直接处理头节点**
> #### **核心思路**
> 先处理头节点可能被删除的情况，再处理中间节点。
>
> #### **代码实现**
> ```c
> struct ListNode* removeElements(struct ListNode* head, int val) {
>     // 处理头节点需要删除的情况
>     while (head != NULL && head->val == val) {
>         struct ListNode* temp = head;
>         head = head->next;
>         free(temp);
>     }
> 
>     if (head == NULL) return NULL;
> 
>     // 处理中间节点
>     struct ListNode* curr = head;
>     while (curr->next != NULL) {
>         if (curr->next->val == val) {
>             struct ListNode* temp = curr->next;
>             curr->next = temp->next;
>             free(temp);
>         } else {
>             curr = curr->next;
>         }
>     }
> 
>     return head;
> }
> ```
>
> #### **关键点分析**
> 1. **头节点预处理**：通过循环删除所有值为 `val` 的头节点。
> 2. **边界条件**：处理完头节点后需检查链表是否为空。
>
> ---
>
> ### **模板总结**
> #### **适用场景**
> 链表节点的删除、插入、交换等操作，尤其是需要统一处理头节点的情况。
>
> #### **通用步骤**
> 1. **创建虚拟头节点**：简化头节点处理逻辑。
> 2. **初始化指针**：`curr` 指针遍历链表。
> 3. **循环处理节点**：
>    - 删除：调整指针并释放内存。
>    - 保留：移动指针。
> 4. **返回结果**：释放虚拟头节点，返回新头节点。
>
> ```c
> // 伪代码模板
> struct ListNode* func(struct ListNode* head, ...) {
>     struct ListNode* dummy = create_dummy(head);
>     struct ListNode* curr = dummy;
> 
>     while (curr->next != NULL) {
>         if (需要删除/操作 curr->next) {
>             // 调整指针并释放内存
>         } else {
>             curr = curr->next;
>         }
>     }
> 
>     return extract_new_head(dummy);
> }
> ```
>
> ---
>
> ### **拓展应用**
> 虚拟头节点技巧可扩展至以下问题：
> 1. **删除链表的倒数第 N 个节点（LeetCode 19）**
> 2. **合并两个有序链表（LeetCode 21）**
> 3. **旋转链表（LeetCode 61）**
> 4. **分隔链表（LeetCode 86）**
>
> ---
>
> ### **总结**
> 1. **虚拟头节点法**：简化代码逻辑，避免头节点特判。
> 2. **时间复杂度**：O(n)，空间复杂度 O(1)。
> 3. **内存管理**：C语言需手动释放内存，防止泄漏。
> 4. **代码健壮性**：正确处理连续删除和空链表场景。



### 设计链表 leetcode 707

搞明白删除第n个节点那里，`curr->next` 才是第n 个。



需要注意的是插入的时候：

插入的时候，先更新后面的那个，在更新前面那个（让前面那个指向新的），不然会被覆盖



```C
typedef struct Node {
	int val;
	struct Node* next;
} Node;


typedef struct {
	int size;
	Node* data;
} MyLinkedList;

/** Initialize your data structure here. */

MyLinkedList* myLinkedListCreate() {
	MyLinkedList* obj = (MyLinkedList*)malloc(sizeof(MyLinkedList));
    Node* head = (Node*)malloc(sizeof(Node));
	head->next = (void*)0;
	obj->data = head;
    obj->size = 0;
	return obj;
}

/** Get the value of the index-th node in the linked list. If the index is invalid, return -1. */
int myLinkedListGet(MyLinkedList* obj, int index) {
	if (index < 0 || index >= obj->size) return -1;

	Node* cur = obj->data;
	while (index-- >= 0) {
        cur = cur->next;
    }

	return cur->val;
}

/** Add a node of value val before the first element of the linked list. After the insertion, the new node will be the first node of the linked list. */
void myLinkedListAddAtHead(MyLinkedList* obj, int val) {
	Node* node = (Node*)malloc(sizeof(Node));
	node->val = val;

	node->next = obj->data->next;
	obj->data->next = node;
	obj->size++;
}

/** Append a node of value val to the last element of the linked list. */
void myLinkedListAddAtTail(MyLinkedList* obj, int val) {
	Node* cur = obj->data;
	while (cur->next != ((void*)0)) {
        cur = cur->next;
    }

	Node* tail = (Node*)malloc(sizeof(Node));
	tail->val = val;
	tail->next = (void*)0;
	cur->next = tail;
	obj->size++;
}

/** Add a node of value val before the index-th node in the linked list. If index equals to the length of linked list, the node will be appended to the end of linked list. If index is greater than the length, the node will not be inserted. */
void myLinkedListAddAtIndex(MyLinkedList* obj, int index, int val) {
	if (index > obj->size) return;

	Node* cur = obj->data;
	while (index-- > 0) { 
        cur = cur->next;
    }

	Node* node = (Node*)malloc(sizeof(Node));
	node->val = val;
	node->next = cur->next;
	cur->next = node;
	obj->size++;
}

/** Delete the index-th node in the linked list, if the index is valid. */
void myLinkedListDeleteAtIndex(MyLinkedList* obj, int index) {
	if (index < 0 || index >= obj->size) return;

	Node* cur = obj->data;
	while (index-- > 0) {
        cur = cur->next;
    }

	Node* temp = cur->next;
	cur->next = temp->next;
	free(temp);
	obj->size--;
}

void myLinkedListFree(MyLinkedList* obj) {
	Node* tmp = obj->data;
	while (tmp != NULL) {
		Node* n = tmp;
		tmp = tmp->next;
		free(n);
	}
	free(obj);
}

```





### 反转链表

反转单链表是链表操作的经典问题，要求将链表所有节点的指向反转，例如 `1→2→3→4→5` 变为 `5→4→3→2→1`。核心在于修改每个节点的 `next` 指针，使其指向前一个节点。

#### 基础

- 迭代法

    **核心思路**：使用三个指针 `prev`、`curr`、`next` 逐步反转链表方向。

    - **时间复杂度**：O(n)
    - **空间复杂度**：O(1)

    **C语言实现**：

    ```c
    struct ListNode* reverseList(struct ListNode* head) {
        struct ListNode *prev = NULL, *curr = head, *next = NULL;
        while (curr) {
            next = curr->next; // 保存下一个节点
            curr->next = prev; // 反转当前节点的指针
            prev = curr;       // prev 前移
            curr = next;       // curr 前移
        }
        return prev; // 新头节点
    }
    ```

    **关键点**：

    - 循环中必须先保存 `next`，否则反转后无法继续遍历。
    - 终止条件是 `curr` 为空，此时 `prev` 是原链表尾节点，即新头节点。



- 递归法

    **核心思路**：利用递归栈反向操作指针，先递归到链表末端，再回溯修改指针。

    - **时间复杂度**：O(n)
    - **空间复杂度**：O(n)（递归栈深度）

    **C语言实现**：

    ```c
    struct ListNode* reverseList(struct ListNode* head) {
        if (head == NULL || head->next == NULL) {
            return head; // 终止条件：空或单节点链表
        }
        struct ListNode* newHead = reverseList(head->next);
        head->next->next = head; // 反转指向
        head->next = NULL;       // 防止成环
        return newHead;
    ```

    **关键点**：

    - 递归到最后一个节点开始反转，每次回溯将当前节点 `head` 的下一个节点指向自己。
    - 必须将 `head->next` 置空，否则原头节点会形成环。



#### 变种1：反转链表的一部分（LeetCode 92）

- 定位到需要反转的区间 `[m, n]`，切断子链表，反转后重新连接。
- 使用虚拟头节点简化边界处理。

```C
struct ListNode* reverseBetween(struct ListNode* head, int left, int right) {
    if (left == right) return head;

    struct ListNode dummy;
    dummy.next = head;
    struct ListNode *prev = &dummy;
    for (int i = 0; i < left - 1; i++) prev = prev->next;

    // curr 当前待反转的第一个节点
    struct ListNode *curr = prev->next, *next = NULL;

    // 将后续节点逐个插入到prev之后，共操作left - right次
    for (int i = 0; i < right - left; i++) {
        next = curr->next; 			// 保存待插入节点
        curr->next = next->next;	// 移除待插入节点
        next->next = prev->next;	// 移除待插入节点
        prev->next = next;
    }
    
    return dummy.next;

}
```

1. **虚拟头节点**：避免处理 `left=1` 时头节点变化的特殊情况。
2. **定位前驱节点**：通过 `pre`v 找到区间起始位置的前驱。
3. **头插法反转**：每次将 `curr` 的下一个节点移动到 `prev` 之后，逐步构建反转区间。



解法二：子链表分离反转法

**核心思路**：分离出需要反转的子链表，反转后重新拼接到原链表。此方法逻辑清晰，但需要额外处理子链表的头尾连接。

**时间复杂度**：O(n)
**空间复杂度**：O(1)

```c
// 反转以head为头节点的k个节点，返回新头节点，并通过参数返回尾节点和后继节点
void reverseK(struct ListNode* head, int k, 
              struct ListNode **new_head, 
              struct ListNode **tail, 
              struct ListNode **succ) {
    struct ListNode *prev = NULL, *curr = head, *next = NULL;
    int count = 0;
    while (curr && count < k) {
        next = curr->next;
        curr->next = prev;
        prev = curr;
        curr = next;
        count++;
    }
    *new_head = prev;    // 反转后的头节点
    *tail = head;        // 反转后的尾节点（原头节点）
    *succ = curr;        // 后继节点（第k+1个节点）
}

struct ListNode* reverseBetween(struct ListNode* head, int m, int n) {
    if (m == n) return head;
    struct ListNode dummy;
    dummy.next = head;
    struct ListNode *pre = &dummy;
    
    // 定位到前驱节点
    for (int i = 0; i < m-1; i++) pre = pre->next;
    
    int k = n - m + 1;
    struct ListNode *rev_head, *rev_tail, *succ;
    reverseK(pre->next, k, &rev_head, &rev_tail, &succ);
    
    pre->next = rev_head;    // 前驱节点连接新头
    rev_tail->next = succ;   // 反转后的尾连接后继节点
    
    return dummy.next;
}
```

**关键点**：

- **子链表分离与连接**：需记录反转后的头、尾及后继节点，确保拼接正确。
- **通用反转函数**：可复用此函数解决其他区间反转问题（如每k个一组反转）。



- **模板**

    **链表区间反转问题核心步骤**：

    1. **虚拟头节点**：统一处理所有边界条件。
    2. **定位前驱节点**：移动到 `left-1` 位置。
    3. **反转区间**：
        - **头插法**：逐个移动节点到前驱之后（推荐，代码简洁）。
        - **子链表分离**：反转后重新拼接。
    4. **连接后续节点**：确保反转后的尾部指向剩余链表。

    **代码模板（头插法）**：

    ```c
    struct ListNode* reverseBetween(struct ListNode* head, int m, int n) {
        struct ListNode dummy = {0, head};
        struct ListNode *pre = &dummy;
        for (int i = 0; i < m-1; i++) pre = pre->next;
        struct ListNode *curr = pre->next;
        for (int i = 0; i < n - m; i++) {
            struct ListNode *next = curr->next;
            curr->next = next->next;
            next->next = pre->next;
            pre->next = next;
        }
        return dummy.next;
    }
    ```

    







#### 变种2：**K个一组反转链表（LeetCode 25）**

- 递归或迭代处理每组K个节点，注意剩余节点不足K个时保持原顺序。





#### 变种3：**判断回文链表（LeetCode 234）**

- 反转后半部分链表，与前半部分比较。







### 两两交换





### 链表中的节点







### 删除链表中的倒数第 N 个节点





### 环形链表Ⅱ





## 哈希表









## 字符串



































