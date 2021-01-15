'''
@Author: Guojin Chen
@Date: 2020-06-18 17:31:38
LastEditTime: 2021-01-12 10:32:34
@Contact: cgjhaha@qq.com
@Description: utils
'''
import os
from pathlib import Path


def makedir(path):
    if not Path.exists(path):
        Path.mkdir(path, parents=True, exist_ok=True)

def predir(args):
    if 'in_dir' in args:
        args.in_dir = Path(args.in_dir)
    args.log_dir = Path(args.log_dir) / args.name
    makedir(args.log_dir)
    args.res_dir = Path(args.res_dir) / args.name
    makedir(args.res_dir)
    args.res_gds_dir = Path(args.res_dir) / 'hsd_gds'
    makedir(args.res_gds_dir)
    args.win_gds_dir = Path(args.res_dir) / 'win_gds'
    makedir(args.win_gds_dir)
    args.win_clean_gds_dir = Path(args.res_dir) / 'win_clean_gds'
    makedir(args.win_clean_gds_dir)
    args.res_kitti_dir = Path(args.res_dir) / 'kitti'
    makedir(args.res_kitti_dir)
    args.kitti_vel_dir = args.res_kitti_dir / 'velodyne'
    makedir(args.kitti_vel_dir)
    args.kitti_txt_dir = args.res_kitti_dir / 'txt'
    makedir(args.kitti_txt_dir)
    args.kitti_label_dir = args.res_kitti_dir / 'label_2'
    makedir(args.kitti_label_dir)
    args.kitti_imgset_dir = args.res_kitti_dir / 'ImageSets'
    makedir(args.kitti_imgset_dir)


def logtxt(info,args):
    txt_name = args.name + '_log.txt'
    txt_path = os.path.join(args.log_dir, txt_name)
    print(info)
    with open(txt_path, mode='a+') as f:
        f.write(info)

def gen_imgset(args, total_data):
    test_path = args.kitti_imgset_dir / 'test.txt'
    train_path = args.kitti_imgset_dir / 'train.txt'
    val_path = args.kitti_imgset_dir / 'val.txt'
    paths = [test_path, train_path, val_path]
    for path in paths:
        with open(str(path), 'w') as f:
            for i in range(total_data):
                f.writelines('{:06d}\n'.format(i))
    print('generate imageset done')