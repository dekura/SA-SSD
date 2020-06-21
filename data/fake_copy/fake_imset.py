'''
@Author: Guojin Chen
@Date: 2020-06-20 18:26:23
@LastEditTime: 2020-06-20 18:31:41
@Contact: cgjhaha@qq.com
@Description: 
'''



names = [
    'test',
    'train',
    'trainval',
    'val'
]

for name in names:
    txt_path = '/Users/dekura/Downloads/case1_fakekitti/ImageSet/'+name + '.txt'
    for i in range(1,201):
        i_str = str(i).zfill(6)
        with open(txt_path, 'a+') as f:
            f.write(i_str+'\n')



