import os
import sys
import logging
import argparse
import openslide
import numpy as np
from os import makedirs
from os.path import join
from skimage import img_as_ubyte, io
from skimage.color import rgb2hsv
from tqdm import tqdm

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

def thres_saturation(img, t=15):
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
def run(args, wsi_wholepath, out_tumor_path):
    image=[]
    slide = openslide.OpenSlide(wsi_wholepath)
    dimension = slide.level_dimensions[1]
    step_y_max = int(np.floor(dimension[1]/args.step_size)) # rows
    step_x_max = int(np.floor(dimension[0]/args.step_size)) # columns
    for y in range(step_y_max):
        for x in range(step_x_max):
            img = slide.read_region((x * args.step_size * 2, y * args.step_size * 2), 1,
                                    (args.patch_size, args.patch_size))
            img = np.array(img)[..., :3]
            if thres_saturation(img, t=15):
                image.append(img)
            #     print("start to save")
                io.imsave(join(out_tumor_path, str(x) + '_' + str(y) + '.png'), img_as_ubyte(img))
    # return np.array(image)



def main():
    logging.basicConfig(level=logging.INFO)
    args = parser.parse_args()
    wsi_path = '/nas/tangwenhao/data/camelyon16/train/normal'
    with tqdm(total=len(os.listdir(wsi_path))) as pbar:
        for wsi in os.listdir(wsi_path):
            wsi_wholepath = os.path.join(wsi_path, wsi)
            (wsi_path, wsi_extname) = os.path.split(wsi_wholepath)  # 分离文件路径和文件名
            (wsi_name, extension) = os.path.splitext(wsi_extname)  # 分离文件名和后缀
            # json_path = '/nas/tangwenhao/data/camelyon16/train/json/%s.json' % wsi_name
            out_tumor_path = '/nas/tangwenhao/data/camelyon16/TransMIL/train/%s' % wsi_name
            if os.path.exists(out_tumor_path):
                    pass
            else:
                makedirs(out_tumor_path, exist_ok=True)
                run(args, wsi_wholepath, out_tumor_path)
                # print(image.shape)
                pbar.update(1)
            # print("finish,{}\n".format(wsi_name))

if __name__ == "__main__":
    main()
