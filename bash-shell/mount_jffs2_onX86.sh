#!/bin/sh
#我们在调试硬件板时，经常需要做多个jffs2的根文件系统映像，有时也要对比其他途径得到的可用的jffs2根文件系统映像。但jffs2的文件系统映像不象光盘的映像文件一样可以通过loop设备来挂载，总不可能一个个烧录到硬件板去看吧。
#后来到网上google了一把，左翻右翻之后总算找到了一个方法。因为jffs2是构建于MTD设备上的文件系统，所以无法通过loop设备来挂载，但是可以通过mtdram设备来挂载。mtdram是在用RAM实现的MTD设备，可以通过mtdblock设备来访问。使用mtdram设备很简单，只要加载mtdram和mtdblock两个内核模块即可。这两个内核模块一般的linux内核发行版都有编译好的，直接用modprobe命令加载。
#　　下面是在Fedora core 6环境下使用mtdram设备挂载jffs2根文件系统映像的具体步骤：
#　　1.加载mtdblock内核模块
#　　[root@localhost ~]# modprobe mtdblock
#　　2.加载mtdram内核模块，将该设备的大小指定为jffs2根文件系统映像的大小，块擦除大小(即flash的块大小)指定为制作该jffs2根文件系统时“-e”参数指定的大小，缺省为64KB。下面两个参数的单位都是KB。
#　　[root@localhost ~]# modprobe mtdram total_size=49152 erase_size=128
#　　3.这时将出现MTD设备/dev/mtdblock0，使用dd命令将jffs2根文件系统拷贝到/dev/mtdblock0设备中。
#　　[root@localhost prebuilt_bin]# dd if=rootfs.jffs2_zylonite_qvga of=/dev/mtdblock0
#　　98304+0 records in
#　　98304+0 records out
#　　50331648 bytes (50 MB) copied, 1.98391 seconds, 25.4 MB/s
#　　4.将保存了jffs2根文件系统的MTD设备挂载到指定的目录上。
#　　[root@localhost prebuilt_bin]# mount -t jffs2 /dev/mtdblock0 /mnt/mtd
#　　这之后就可以到/mnt/mtd目录查看、修改挂载的jffs2根文件系统了，修改后的jffs2根文件系统可以通过dd命令拷贝为一个jffs2的映像文件。
modprobe mtdblock
modprobe mtdram total_size=16384 erase_size=256
dd if=/root/work/rootbox_IVA.jffs2 of=/dev/mtdblock0
mount -t jffs2 /dev/mtdblock0 /mnt/
