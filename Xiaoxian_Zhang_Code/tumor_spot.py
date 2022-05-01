import os
import sys
import json
import logging
import argparse
import openslide
import numpy as np
from os import makedirs
from os.path import join
from skimage import img_as_ubyte, io
from skimage.color import rgb2hsv

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../')

parser = argparse.ArgumentParser(description='Get tumor mask of tumor-WSI and '
                                             'save it in npy format')
# parser.add_argument('wsi_path', default=None, metavar='WSI_PATH', type=str,
#                     help='Path to the WSI file')
# parser.add_argument('json_path', default=None, metavar='JSON_PATH', type=str,
#                     help='Path to the JSON file')
# parser.add_argument('npy_path', default=None, metavar='NPY_PATH', type=str,
#                     help='Path to the output npy mask file')
parser.add_argument('--level', default=1, type=int, help='at which WSI level'
                    ' to obtain the mask, default 6')
parser.add_argument('--step_size', default=256, type=int, help='non-overlapping')
parser.add_argument('--patch_size', default=256, type=int, help='non-overlapping')

def get_patch_point(json_path):
    with open(json_path) as f:
        dicts = json.load(f)
    tumor_polygons = dicts['positive']
    spot_list = []
    for tumor_polygon in tumor_polygons:
        vertices = np.array(tumor_polygon["vertices"])  # 20x
        x_min = vertices.min(0)[0]
        y_min = vertices.min(0)[1]
        x_max = vertices.max(0)[0]
        y_max = vertices.max(0)[1]
        spot_list.append(np.array([x_min, y_min, x_max, y_max]))

    return spot_list

def thres_saturation(img, t=30):
    # typical t = 15
    img = rgb2hsv(img)
    h, w, c = img.shape
    sat_img = img[:, :, 1]
    sat_img = img_as_ubyte(sat_img)
    ave_sat = np.sum(sat_img) / (h * w)
    return ave_sat >= t

"""
level=1->20x
"""
def run(args, wsi_wholepath, json_path, out_tumor_path):

    slide = openslide.OpenSlide(wsi_wholepath)
    spot_list = get_patch_point(json_path)
    for _, spot in enumerate(spot_list):
        x_min = spot[0]
        y_min = spot[1]
        x_max = spot[2]
        y_max = spot[3]
        step_y_max = int(np.floor((y_max - y_min) / args.step_size))  # rows
        step_x_max = int(np.floor((x_max - x_min) / args.step_size))  # columns
        for y in range(step_y_max):
            for x in range(step_x_max):
                img = slide.read_region((x_min + x * args.step_size, y_min + y * args.step_size), 1,
                                        (args.patch_size, args.patch_size))
                img = np.array(img)[..., :3]
                if thres_saturation(img, t=30):
                    io.imsave(join(out_tumor_path, str(x) + '_' + str(y) + '.png'), img_as_ubyte(img))
                    # img.save(os.path.join(out_tumor_path, str(x) + '_' + str(y) + '.png'))


# def main():
#     logging.basicConfig(level=logging.INFO)
#     args = parser.parse_args()
#     wsi_path = '/nas/tangwenhao/data/camelyon16/train/tumor'
#     for wsi in os.listdir(wsi_path):
#         wsi_wholepath = os.path.join(wsi_path, wsi)
#         (wsi_path, wsi_extname) = os.path.split(wsi_wholepath)  # 分离文件路径和文件名
#         (wsi_name, extension) = os.path.splitext(wsi_extname)  # 分离文件名和后缀
#         json_path = '/nas/tangwenhao/data/camelyon16/train/json/%s.json' % wsi_name
#         out_tumor_path = '/nas/tangwenhao/data/camelyon16/pre_test/patch_tumor/%s' % wsi_name
#         makedirs(out_tumor_path, exist_ok=True)
#         run(args, wsi_wholepath, json_path, out_tumor_path)
#         print("finish,{}\n".format(wsi_name))
def main():
    logging.basicConfig(level=logging.INFO)
    args = parser.parse_args()
    json_path = '/nas/tangwenhao/data/camelyon16/pre_test/json'
    for json in os.listdir(json_path):
        json_wholepath = os.path.join(json_path, json)
        (json_path, json_extname) = os.path.split(json_wholepath)  # 分离文件路径和文件名
        (json_name, extension) = os.path.splitext(json_extname)  # 分离文件名和后缀
        wsi_path = '/nas/tangwenhao/data/camelyon16/test/%s.tif'%json_name
        out_tumor_path = '/nas/tangwenhao/data/camelyon16/pre_test/patch_tumor/%s' % json_name
        makedirs(out_tumor_path, exist_ok=True)
        run(args, wsi_path, json_wholepath, out_tumor_path)
        print("finish,{}\n".format(json_name))


if __name__ == "__main__":
    main()
