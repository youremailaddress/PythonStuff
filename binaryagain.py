import os
import sys
import numpy as np
import math
import gc
now = os.path.dirname(os.path.realpath(__file__))+'/'

def read_bits_from_file(filename, bigendian=True):
    """
    :param filename: 文件名
    :param bigendian: True表示高位在前（即顺序输出），False表示高位在后（即逆序）
    例如：将字符a变成二进制列表
    高位在前：[0, 1, 1, 0, 0, 0, 0, 1]
    低位在前：[1, 0, 0, 0, 0, 1, 1, 0]
    :return:  将一个文件变成二进制列表
    """
    # 检查文件是否为空
    count = os.path.getsize(filename)
    if count == 0:
        raise Exception("⚠警告：文件内容为空，请检查！")

    bitlist = list()
    if filename == None:
        f = sys.stdin
        raise Exception("⚠警告：文件不存在，请检查！")
    else:
        # 以二进制读取文件
        f = open(filename, "rb")
    while True:
        # 每次读取16384比特
        bytes = f.read(16384)
        if bytes:  # 如果读取不为空
            # 将读取的二进制变成二进制列表，此时列表中的每一项以字符串形式存在
            temp = list(bin(int(bytes.hex(), 16))[2:])
            # 检查列表是否省略高位的0，如果省略在前面加入0
            t = len(bytes)*8 - len(temp)
            while t>0:
                t-=1
                temp.insert(0, 0)
            # 将列表中的字符串变成int
            bitlist.extend([int(x) for x in temp])
            gc.collect()
        else:
            break
    # 关闭流
    f.close()
    del temp
    # 判断用户是否需要逆序返回列表，默认正序返回
    if bigendian:
        return bitlist
    else:
        return bitlist[-1::-1]

def encrypt(filename):   
    q = read_bits_from_file(now + filename)
    de = int(math.sqrt(len(q)/3))
    los = len(q)-de**2*3
    part_1 = q[:los]
    part_2 = q[los:los+de**2]
    part_3 = q[los+de**2:los+2*de**2]
    part_4 = q[los+2*de**2:los+3*de**2]
    part_2 = np.reshape(part_2,(de,de))
    part_3 = np.reshape(part_3,(de,de))
    part_4 = np.reshape(part_4,(de,de))
    part_2 = part_2.T
    I = np.ones((de,de))
    part_3 = I - part_3
    del I
    part_4 = part_4.T
    part_2 = np.reshape(part_2,(1,de**2))[0].tolist()
    part_3 = np.reshape(part_3,(1,de**2))[0].tolist()
    part_4 = np.reshape(part_4,(1,de**2))[0].tolist()
    ency = part_1+part_2+part_3+part_4
    del part_1,part_2,part_3,part_4
    return ency

def readit(thelist,i,nums):
    if (i+1)*nums < len(thelist):
        cut = thelist[i*nums:(i+1)*nums]
        return cut
    else:
        cut = thelist[i*nums:]
        return cut

def write_bits_to_file(filename,alist):
    newlist = []
    newlist.extend([str(int(y)) for y in alist])
    binary = "0b"+"".join(newlist)
    del newlist
    num = int(binary,0)
    del binary
    sixt = hex(num)[2:]
    del num
    #i = 0
    #strr = ""
    #while True:
        # 每次读取16384比特
        #inside = readit(newlist,i,16384)
        #i = i + 1
        #if inside:  # 如果读取不为空
            #binary = "0b"+"".join(inside)
            #num = int(binary,0)
            #sixt = hex(num)[2:]
            #strr = strr + sixt
            #an = bytes.fromhex(sixt)
        #else:
            #break
    # 关闭流
    an = bytes.fromhex(sixt)
    f = open(now+filename,"ab+")
    f.write(an)
    gc.collect()
    f.close()

def allfiles():
    avalist = []
    fileList = os.listdir(now) 
    for fn in fileList:
        dec = now +fn 
        if os.path.isfile(dec) and os.path.getsize(dec) < 2097152:
            avalist.append(fn)
        gc.collect()
    del fileList
    return avalist


def main(m,filename):
    if m == 1:
        if filename == "*all":
            for url in allfiles():
                if url is not now + "binaryagain.py":
                    main(m,url)
        else:
            flow = encrypt(filename)
            write_bits_to_file("en"+filename,flow)
            del flow
            return None
    elif m == 2:
        if filename == "*all":
            if filename == "*all":
                for url in allfiles():
                    if url is not now + "binaryagain.py":
                        main(m,url)
        else:
            flow = encrypt(filename)
            write_bits_to_file("de"+filename,flow)
            del flow
            return None


if __name__ == "__main__":
    m = input("加密输入1，解密输入2：")
    m = int(m)
    if m == 1:
        n = input("输入加密文件名：")
        main(m,n)
    elif m == 2:
        n = input("输入解密文件名：")
        main(m,n)
