#!/usr/bin/env python3
txt = '''
3N	3p	2l	36	1b	3v	26	33
1W	49	2a	3g	47	04	33	3W
21	3M	0F	0X	1g	2H	0x	1R
1n	3I	2r	0P	2U	16	2L	2D
1t	1s	3H	0d	0s	1K	2D	05
1K	1O	0S	1D	3o	1L	3J	1G
4D	0G	0L	0x	1Q	2p	2a	1K
4E	1w	2Q	19	1k	3G	24	0p
22	4F	0P	3C	3J	1D	2n	1m
2i	1J	3P	2v	1s	2O	0k	1M

2M	0w	3L	3D	2r	0S	1p	15
3V	3e	3I	0n	3u	1O	0u	0Z
3g	2U	1C	0Y	1N	3n	0W	3Q
22	13	0V	3c	0E	34	0W	1t
1D	2N	3H	47	0s	2p	0Z	34
0g	3v	1Q	0s	0D	0K	2h	3D
3L	2x	1Q	20	2n	2L	1C	2p
0A	29	3r	0D	45	0k	2e	2W
25	3U	1W	2r	46	2s	2X	39
3p	0X	0E	1q	0q	4B	49	48
3r	3b	3C	1M	1j	0l	4A	48
40	3m	4E	0s	2s	1v	3T	0I
3t	2B	2k	2t	2O	0e	2l	1L

28	2a	0J	1L	0c	3C	2o	0X
00	2Z	2d	1T	2u	1t	1j	0l
1o	1E	3T	18	3E	1G	27	0L
0v	2t	06	11	1A	2U	4B	1O
2M	3d	2S	0x	0w	0q	0p	2V
18	0q	1D	49	2O	00	1v	2t
1k	3s	3G	21	3w	0W	29	2r
2O	2L	0g	3Y	0M	0u	3i	3C
1r	2c	2q	3o	30	0a	39	1K
'''

rr = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwx'
# rr = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwx1234567890'

for base in range(58, 64):
    t = ''
    tt = ''
    print()
    print(f'Base{base}')
    for x in txt.split():
        n = rr.index(x[0]) * base + rr.index(x[1])
        # n = rr.index(x[0]) * len(rr) + rr.index(x[1])
        # n = int(x, 36)
        # t += '{},'.format(n)
        # tt += chr(n)
        tt += '{}{}'.format(rr[n // 16], rr[n % 16])
    print(t)
    print(tt)
