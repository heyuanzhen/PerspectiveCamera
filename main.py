import scipy.io as si
import os
import numpy as np

from parameters import *
from libs.projection import trans_world_to_img, get_world_to_image_matrix

RAW_DIR = "./resources/raw"
PROCESSED_DIR = "./resources/processed"


def load_mat(mat_name):
    mat_path = os.path.join(RAW_DIR, mat_name)
    data = si.loadmat(mat_path)
    return data


def transform_one_file(data, fn):
    world_to_cam_mat, cam_to_img_plane_mat, img_plane_to_image_mat = get_world_to_image_matrix()
    num_p = data.shape[1]
    num_frames = int(data.shape[0] / 3)
    img_p = np.zeros((num_frames * 2, num_p))
    for pi in range(num_p):
        for fi in range(num_frames):
            p = data[fi * 3: (fi + 1) * 3, pi]
            p_img = trans_world_to_img(p, world_to_cam_mat, cam_to_img_plane_mat, img_plane_to_image_mat)
            img_p[fi * 2, pi] = p_img[0]
            img_p[fi * 2 + 1, pi] = p_img[1]
            print(p_img)
    save_path = os.path.join(PROCESSED_DIR, fn)
    si.savemat(save_path, {'img_p': img_p}, appendmat=False)


def transform_all_files():
    raw_fn_list = os.listdir(RAW_DIR)
    for raw_fn in raw_fn_list:
        data = load_mat(raw_fn)
        data = data['BM'] * CORD_SCALE_FACTOR
        transform_one_file(data, raw_fn)


if __name__ == "__main__":
    transform_all_files()
