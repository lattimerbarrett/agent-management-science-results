"""Check coordinate-flat certificates for RM(7,14).
A mask specifies the FREE coordinates of a 7-dimensional linear flat.
An integer point x is on it iff x & ~mask == 0.
Its indicator has degree 7, so any XOR of these indicators is RM(7,14).
Projection pi(x)=x>>7 partitions F2^14 into 128 affine 7-flats.
The witness support projects to <=64 values; hence at least64 fibres
are disjoint and their indicators may independently be added, each
increasing weight by128. Thus seed w produces w+128k for 0<=k<=64.
"""
SEEDS = {312: [4600, 11411, 13843], 314: [13617, 6888, 9495], 316: [10301, 5955, 5003], 318: [4947, 11372, 5011, 9532], 320: [2521, 3611, 6535], 324: [6458, 3251, 9893], 328: [3793, 11363, 12649], 332: [13144, 7273, 11027], 336: [3868, 13894, 5737], 338: [10066, 6317, 12515], 340: [3538, 10891, 5938, 3568], 342: [7338, 9045, 12956, 7211], 344: [1465, 2546, 12997], 346: [10065, 9585, 5969, 13168, 3215], 348: [3227, 9452, 12597], 350: [4339, 5361, 10851, 5532], 352: [4476, 13100, 1961, 701], 354: [3373, 13010, 13665, 9585, 7213], 356: [14617, 5864, 11303], 358: [5574, 6377, 5326, 5678, 6761, 11057, 5678], 360: [5872, 6388, 10838, 11852], 364: [12886, 7736, 9543, 8527], 366: [11602, 3506, 4781, 2727], 368: [9817, 7324, 13900, 4893], 370: [6311, 8437, 2741, 12455, 3928], 372: [11620, 6769, 1468, 3532], 374: [7754, 956, 3406, 8629], 376: [6266, 3788, 6884, 4765], 378: [10902, 6798, 9585, 1507], 380: [923, 9464, 8826, 5517], 382: [6415, 14634, 6415, 9944, 6947, 9436, 13609, 7465], 384: [12406, 3866, 10837, 12839], 386: [10650, 1878, 1946, 14437], 388: [7699, 6755, 5929, 10598], 390: [13617, 2986, 1957, 2766], 392: [14382, 9303, 10581, 12506], 394: [9020, 9938, 10034, 4413, 6445, 6457, 8510], 396: [11496, 14874, 9573, 10010], 398: [9014, 12649, 13137, 3246], 400: [5484, 747, 9813, 5703], 402: [14642, 7284, 7346, 9037], 404: [12649, 8903, 13894, 2965], 406: [9773, 1389, 8813, 7724, 6610], 408: [1389, 3623, 2936, 8847], 410: [11468, 2930, 13606, 4915], 412: [1483, 2963, 13413, 2639], 414: [14690, 15412, 1693, 11036], 416: [8886, 9307, 5692, 13665], 418: [14540, 1845, 5647, 13417, 1843], 420: [10791, 13339, 4563, 5976], 422: [11541, 9712, 1630, 4842], 424: [5662, 3257, 13414, 10609], 426: [6539, 9844, 4699, 13451], 428: [12518, 5042, 13339, 2801], 430: [8315, 3913, 13898, 3529, 12470], 432: [13582, 5059, 3623, 4922], 434: [11307, 11548, 5076, 7369], 436: [9066, 12597, 5323, 6716], 438: [5042, 3785, 7693, 12598, 5213]}

def certificate():
    generated=set()
    stats={}
    for w,masks in SEEDS.items():
        support=set()
        for mask in masks:
            assert mask.bit_count()==7
            s=mask
            while True:
                if s in support:support.remove(s)
                else:support.add(s)
                if s==0:break
                s=(s-1)&mask
        assert len(support)==w
        # Using actual support, not union of constituent projections, is stronger.
        projected={x>>7 for x in support}
        free=128-len(projected)
        assert free>=64,(w,free)
        generated.update(w+128*k for k in range(free+1))
        stats[w]=free
    generated |= {16384-x for x in generated}
    return generated,stats

if __name__=='__main__':
    generated,stats=certificate()
    expected=set(range(312,16384-312+1,2))
    print('Verified seed count:',len(SEEDS))
    print('Uncovered residue representatives:',sorted(set(range(312,440,2))-SEEDS.keys()))
    print('Missing central weights:', sorted(expected-generated))
    print('Disjoint parallel-flat counts:',stats)
