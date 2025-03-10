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





#### 另外：删除排序链表中的重复元素





总结一下特点，好像都用到了数组排好序的特性？







26. 移除链表元素









