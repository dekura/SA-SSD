'''
@Author: Guojin Chen
@Date: 2020-06-18 17:31:38
@LastEditTime: 2020-06-19 13:41:33
@Contact: cgjhaha@qq.com
@Description: utils
'''
import os
from pathlib import Path


def makedir(path):
    if not Path.exists(path):
        Path.mkdir(path, parents=True, exist_ok=True)

def predir(args):
    args.in_folder = Path(args.in_folder)
    args.log_folder = Path(args.log_folder) / args.name
    makedir(args.log_folder)
    args.res_folder = Path(args.res_folder) / args.name
    makedir(args.res_folder)
    args.res_gds_folder = Path(args.res_folder) / 'hsd_gds'
    makedir(args.res_gds_folder)
    args.res_kitti_folder = Path(args.res_folder) / 'kitti'
    makedir(args.res_kitti_folder)


def logtxt(info,args):
    txt_name = args.name + '_log.txt'
    txt_path = os.path.join(args.log_folder, txt_name)
    with open(txt_path, mode='a+') as f:
        f.write(info)