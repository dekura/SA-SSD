'''
@Author: Guojin Chen
@Date: 2020-06-18 17:53:11
LastEditTime: 2021-01-08 16:40:36
@Contact: cgjhaha@qq.com
@Description: transfer the gds to polygon arrays.
'''
import csv
import gdspy
import numpy as np
from pathlib import Path
from .consts import LAYERS, HSD_WH

'''
@description: transfer the gds to polygon arrays.
@param {type}
    args argparse.args
@return: polys {
    'rect': [],
    'wire': [],
}
'''
def _get_offset(infile, args):
    dtype = 0
    gdsii = gdspy.GdsLibrary(unit=1e-9)
    gdsii.read_gds(infile,units='convert')
    cell = gdsii.top_level()[0]
    bbox = cell.get_bounding_box()
    width = int((bbox[1,0]-bbox[0,0]))
    height= int((bbox[1,1]-bbox[0,1]))
    w_offset = int(bbox[0,0] + (width)/2)
    # h_offset = int(bbox[0,1] + (height)/2)
    # h_offset = int(bbox[0,1] - height)
    h_offset = int(bbox[0,1])
    return [w_offset, h_offset]



def _gds2poly(infile, offsets, args):
    dtype = 0
    gdspy.current_library = gdspy.GdsLibrary()
    gdsii = gdspy.GdsLibrary(unit=1e-9)
    gdsii.read_gds(infile,units='convert')
    cell = gdsii.top_level()[0]
    bbox = cell.get_bounding_box()
    # width = int((bbox[1,0]-bbox[0,0]))
    # height= int((bbox[1,1]-bbox[0,1]))
    # w_offset = int(bbox[0,0] + (width)/2)
    # h_offset = int(bbox[0,1] + (height)/2)
    w_offset = offsets[0]
    h_offset = offsets[1]
    polys = {}
    for name, num in LAYERS.items():
        try:
            polyset = cell.get_polygons(by_spec=True)[(num,dtype)]
            for poly in range(0, len(polyset)):
                for points in range(0, len(polyset[poly])):
                    polyset[poly][points][0]=int(polyset[poly][points][0]-w_offset)
                    polyset[poly][points][1]=int(polyset[poly][points][1]-h_offset)
            polys[name] = polyset
        except:
            print('layer {}:{} not found, skipping...'.format(name, num))
    return polys


def _center2poly(x, y, offsets):
    x = x - offsets[0]
    y = y - offsets[1]
    p0 = [x - HSD_WH, y - HSD_WH]
    p1 = [x - HSD_WH, y + HSD_WH]
    p2 = [x + HSD_WH, y + HSD_WH]
    p3 = [x + HSD_WH, y - HSD_WH]
    poly = [p0, p1, p2, p3]
    return poly


def check_in_flag(hsd_flag, sum_xy):
    flag = False
    for i in hsd_flag:
        if np.abs(sum_xy - i) < 10:
            flag = True
            return flag
    return flag

'''
visualize the hotspot in gds

and now we also need to save the center
to get the velodyne

hsd_polys: {
    'dup_removed': is the removed duplicated polys
}
'''
def _csv2poly(csv_path, offsets, args):
    csv_file = open(csv_path, 'r')
    reader = csv.DictReader(csv_file)
    hsd_polys = {}
    hsd_sets = set()
    hsd_flag = []
    for row in reader:
        if int(row['category']) >= 1000:
            raise 'hsd out of range, please check'
        x = float(row['x'])
        y = float(row['y'])
        # simple checks, remove duplicated hotspots
        if check_in_flag(hsd_flag, x+y):
            pass
        else:
            hsd_sets.add((x, y))
            hsd_flag.append(x+y)
            # if x+y == -187565.7:
                # print(x, y)
        if not row['category'] in hsd_polys:
            hsd_polys[row['category']] = []
        hsd_polys[row['category']].append(_center2poly(x,y, offsets))
    hsd_polys['dup_removed'] = []
    # print(hsd_flag[30])
    # print(hsd_sets)
    for center in hsd_sets:
        x, y = center
        hsd_polys['dup_removed'].append(_center2poly(x, y, offsets))
    # print(hsd_polys['dup_removed'][30])
    return hsd_polys


# def gds2poly(args):
#     gds_paths = Path(args.in_dir).glob('*.gds')
#     for gds_path in gds_paths:
#         gds_name = gds_path.stem
#         # print(type(gds_name))
#         csv_path = gds_name + '.csv'
#         csv_path = args.in_dir / csv_path
#         offsets = _get_offset(str(gds_path), args)
#         # print(offsets)
#         _gds2poly(str(gds_path), offsets, args)
#         _csv2poly(csv_path, offsets, args)
