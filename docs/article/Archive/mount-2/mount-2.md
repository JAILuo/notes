## introdcution

之前写过一部分，但是感觉对这部分的理解其实一般，这里再看看别人的文章理解：

- [挂载（mount）深入理解 - 江召伟 - 博客园](https://www.cnblogs.com/jiangzhaowei/p/11843026.html)
- [Mounting definition by The Linux Information Project](https://www.linfo.org/mounting.html)



几个比较重要的理解：

The [*mount point*](https://www.linfo.org/mount_point.html) is the directory (usually an empty one) in the currently accessible filesystem to which a additional filesystem is mounted. It becomes the root directory of the added directory tree, and that tree becomes accessible from the directory to which it is mounted (i.e., its mount point). Any original contents of a directory that is used as a mount point become invisible and inaccessible while the filesystem is still mounted.