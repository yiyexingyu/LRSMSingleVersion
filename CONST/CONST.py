
"""
小工具停靠窗口
每个button或action对应的CONST
"""
NONE_RES = -1
MOVE_TOOL = 1
QUICK_SELECT_TOOL = 2
RECT_QUICK_SELECT_TOOL = 3
ELLIPSE_QUICK_SELECT_TOOL = 4
GRIP_TOOL = 5
GRIP_TONGS = 6
GRIP_ROTATE = 7
ZOOM_TOOL = 8

RECTANGLE = 3
ELLIPSE = 4

import struct


def t():
    f = open("D:/其他/t1.txt")
    text = f.read()
    print(type(text))
    print(len(text))
    bin_text = encode(text, '')
    # for i in range(len(bin_text)):
    #     print(bin_text[i], end=" ")
    #     if i % 5 == 0 and i >= 3:
    #         print("")
    print(bin_text)
    print(len(bin_text))
    # for i in range(len(text)):
    #     print(encode())
    f.close()

    b0 = 0
    b1 = 0
    for bt in bin_text:
        if bt == '0':
            b0 += 1
        else:
            b1 += 1
    print("b0: ", b0)
    print("b1: ", b1)

    test1(bin_text)


def t2():
    a = 12
    ba = struct.pack('i', a)
    print(ba)


def encode(s, join_text=' '):
    return join_text.join([bin(ord(c)).replace('0b', '') for c in s])


def decode(s):
    return ''.join([chr(i) for i in [int(b, 2) for b in s.split(' ')]])


def test1(bin_text):
    current_bin = bin_text[0]
    new_bin_text = bin_text[0]
    _len, m = 1, []
    for bt in bin_text[1:]:
        if bt != current_bin:
            new_bin_text += bt
            current_bin = bt

            if _len > 1:
                m.append(_len)
            _len = 1
        else:
            _len += 1

    print(len(new_bin_text))
    print(new_bin_text)

    print("len: ", len(m))
    print("m: ", m)


# t()



