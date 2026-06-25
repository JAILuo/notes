`qemu` 使用主机的共享文件夹：

- 挂载：`mount -t 9p -o trans=virtio share /mnt/host`

    在**虚拟机内部**，将宿主机暴露的名为 `share` 的 9P 共享目录，通过 `virtio` 传输协议，挂载到虚拟机内的 `/mnt/host` 路径下，从而实现宿主机与虚拟机之间的文件共享

    - `-t` 是 `mount` 命令用来指定**文件系统类型**的选项，这里 `9p` 表示 **Plan 9 文件系统协议**（9P）。
        9P 是一种网络文件系统协议，常用于虚拟机与宿主机之间、容器与宿主机之间共享文件。
    - `-o` 用于指定**挂载选项**（options），多个选项用逗号分隔。
        `trans=virtio` 表示传输层使用 **virtio** 协议。
        - virtio 是半虚拟化 I/O 标准，性能接近物理硬件。
        - 在 KVM/QEMU 虚拟机中，9p 文件系统通常会配合 virtio 传输来实现高效的共享目录访问。
    - 

- 卸载：`umount /mnt/host`

