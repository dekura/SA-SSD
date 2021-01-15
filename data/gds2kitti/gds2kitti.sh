###
 # @Author: Guojin Chen
 # @Date: 2020-06-19 13:31:33
 # @LastEditTime: 2021-01-13 17:03:50
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

# $python gds2win.py \
# --name $case \
# --in_dir /Users/dekura/chen/bei/projects/pchsd/ICCAD16-N7M2EUV/$case

# $python win2kitti.py \
# --name $case \
# --in_dir ./results/$case/win_gds

# bash create_dataset.sh
# cp ./results/$case/kitti/velodyne/test$case.bin ./hsd_kitti/training/velodyne/000000.bin
# cp ./results/$case/kitti/label_2/test$case.txt ./hsd_kitti/training/label_2/000000.txt
bash win2kitti.sh
echo 'win2kitti done'

rm -rf ./hsd_kitti/training/velodyne
rm -rf ./hsd_kitti/training/label_2
rm -rf ./hsd_kitti/ImageSets
cp -r ./results/$case/kitti/velodyne ./hsd_kitti/training/velodyne
cp -r ./results/$case/kitti/label_2 ./hsd_kitti/training/label_2
cp -r ./results/$case/kitti/ImageSets ./hsd_kitti/ImageSets
rm -rf ./hsd_kitti/testing/
cp -r ./hsd_kitti/training/ ./hsd_kitti/testing/
echo 'dataset created'
echo 'copy training to testing done'


# $python utils/dup_data.py