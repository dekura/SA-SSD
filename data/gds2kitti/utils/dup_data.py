'''
Author: Guojin Chen @ CUHK-CSE
Homepage: https://dekura.github.io/
Date: 2020-12-25 10:05:26
LastEditTime: 2021-01-04 19:50:09
Contact: cgjhaha@qq.com
Description: duplicate the dataset

kitti
    training
        calib
            000000.txt
        image_2
            000000.png
        label_2
            000000.txt
        velodyne
            000000.bin

will be duplicated to

kitti
    training
        calib
            000000.txt
            000001.*
            ...
            00000x.*
        image_2
            000000.png
            000001.*
            ...
            00000x.*
        label_2
            000000.txt
            000001.*
            ...
            00000x.*
        velodyne
            000000.bin
            000001.*
            ...
            00000x.*
'''
import os
import shutil
from pathlib import Path

data_path = Path('/Users/dekura/chen/bei/projects/pchsd/SA-SSD/data/gds2kitti/hsd_kitti')
train_path = data_path / 'training'
train_calib = train_path / 'calib'
train_label = train_path / 'label_2'
train_velo = train_path / 'velodyne'
train_img = train_path / 'image_2'

o_calib = train_calib / '000000.txt'
o_img = train_img / '000000.png'
o_label = train_label / '000000.txt'
o_velo = train_velo / '000000.bin'

test_path = data_path / 'testing'

data_obj = {
    'calib': train_calib,
    'o_calib': o_calib,
    'img': train_img,
    'o_img': o_img,
    'label': train_label,
    'o_label': o_label,
    'velo': train_velo,
    'o_velo': o_velo
}


def dup_data():
    MAX_DUP = 3
    for i in range(MAX_DUP):
        for obj in ['calib', 'img', 'label', 'velo']:
            o_obj = 'o_' + obj
            suffix = data_obj[o_obj].suffix # '.txt'
            to_obj_name = ('%06d' % (i + 1)) + suffix
            to_obj = data_obj[obj] / to_obj_name
            shutil.copy(str(data_obj[o_obj]), str(to_obj))



def remove_data(remove_id):
    for obj in ['calib', 'img', 'label', 'velo']:
        o_obj = 'o_' + obj
        suffix = data_obj[o_obj].suffix # '.txt'
        to_obj_name = ('%06d' % (remove_id)) + suffix
        to_obj = data_obj[obj] / to_obj_name
        # shutil.copy(str(data_obj[o_obj]), str(to_obj))
        os.remove(str(to_obj))

def cp_testing():
    if test_path.exists():
        shutil.rmtree(str(test_path))
    shutil.copytree(str(train_path), str(test_path))


if __name__ == '__main__':
    # dup_data()
    # remove_id = 4
    # remove_data(remove_id)
    cp_testing()
