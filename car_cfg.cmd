#!/bin/bash
#SBATCH --job-name=car
#SBATCH --mail-user=cgjhaha@qq.com
#SBATCH --mail-type=ALL
#SBATCH --output=/research/dept7/glchen/tmp/log/sassd_car.txt
#SBATCH --gres=gpu:1

export LD_LIBRARY_PATH=/research/dept7/glchen/miniconda3/envs/sassd/lib/python3.7/site-packages/spconv:$LD_LIBRARY_PATH
/research/dept7/glchen/miniconda3/envs/sassd/bin/python3  tools/train.py configs/car_cfg.py
