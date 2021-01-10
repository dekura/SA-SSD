###
 # @Author: Guojin Chen
 # @Date: 2020-06-19 13:31:33
 # @LastEditTime: 2021-01-08 14:17:16
 # @Contact: cgjhaha@qq.com
 # @Description: 
###

# python=/usr/local/miniconda3/envs/pytorch/bin/python
python=/usr/local/miniconda3/envs/gdspy/bin/python

# case=case1
case=case2


# $python gds2kitti.py \
# --name $case \
# --in_dir '/Users/dekura/chen/bei/projects/pchsd/ICCAD16-N7M2EUV/case1'

$python gds2kitti.py \
--name $case \
--in_dir /Users/dekura/chen/bei/projects/pchsd/ICCAD16-N7M2EUV/$case


# bash create_dataset.sh
cp ./results/$case/kitti/velodyne/test$case.bin ./hsd_kitti/training/velodyne/000000.bin
cp ./results/$case/kitti/label_2/test$case.txt ./hsd_kitti/training/label_2/000000.txt

echo 'dataset created'

$python utils/dup_data.py