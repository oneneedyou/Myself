#!/bin/bash
#占用cpu
for i in `seq $(cat /proc/cpuinfo |grep "processor" |wc -l)`; do sha512sum /dev/zero & done
#查看cpu使用情况
top
#释放刚占用的cpu
kill -9 `ps -ef |grep sha512sum |awk '{print $2}'`


#占用内存，size大小自己按需调整
mkdir -p /tmp/memory && mount -t tmpfs -o size=13000M tmpfs /tmp/memory && dd if=/dev/zero of=/tmp/memory/block
#查看内存使用情况（该命令可以在占用前、占用后、释放后使用，作个对比）
free -m
#释放内存
rm -rf /tmp/memory/block && umount /tmp/memory && rmdir /tmp/memory



#快速占用磁盘空间
#fallocate 命令可以为文件预分配物理空间，du命令也可以看到文件的大小，如果空间不足会提示，且创建文件失败，速度很快*
fallocate -l 40G test3



