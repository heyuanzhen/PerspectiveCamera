import numpy as np

from parameters import *


def norm_vec(vec):
    norm = None
    try:
        norm = vec / np.linalg.norm(vec)
    except Exception:
        print("ERROR: Vector length is 0, it can't be normalized!")
    return norm


def deg_to_rad(deg):
    return np.pi * deg / 180.0


def get_world_to_image_matrix():
    target = np.array(TARGET)
    origin = np.array(ORIGIN)
    vpn = norm_vec(target - origin)
    # print(vpn)
    up = norm_vec(np.array(UP))
    u = norm_vec(np.cross(vpn, up))
    v = np.cross(u, vpn)
    f = F
    fov = deg_to_rad(FOV)
    xres = IMG_W
    yres = IMG_H
    xLength = 2.0 * f * np.tan(fov)
    yox = yres / xres
    yLength = xLength * yox
    # print(xLength, yLength)

    world_to_cam_mat = np.identity(4)
    world_to_cam_mat[0, 0] = u[0]
    world_to_cam_mat[0, 1] = u[1]
    world_to_cam_mat[0, 2] = u[2]
    world_to_cam_mat[0, 3] = np.dot(-origin, u)
    world_to_cam_mat[1, 0] = v[0]
    world_to_cam_mat[1, 1] = v[1]
    world_to_cam_mat[1, 2] = v[2]
    world_to_cam_mat[1, 3] = np.dot(-origin, v)
    world_to_cam_mat[2, 0] = vpn[0]
    world_to_cam_mat[2, 1] = vpn[1]
    world_to_cam_mat[2, 2] = vpn[2]
    world_to_cam_mat[2, 3] = np.dot(-origin, vpn)

    cam_to_img_plane_mat = np.zeros((3, 4))
    cam_to_img_plane_mat[0, 0] = f
    cam_to_img_plane_mat[1, 1] = f
    cam_to_img_plane_mat[2, 2] = 1

    invDx = xres / xLength
    invDy = yres / yLength
    u0 = xres * 0.5
    v0 = yres * 0.5

    img_plane_to_image_mat = np.zeros((2, 3))
    img_plane_to_image_mat[0, 0] = invDx
    img_plane_to_image_mat[0, 2] = u0
    img_plane_to_image_mat[1, 1] = invDy
    img_plane_to_image_mat[1, 2] = v0
    return world_to_cam_mat, cam_to_img_plane_mat, img_plane_to_image_mat


def trans_world_to_img(p, world_to_cam_mat, cam_to_img_plane_mat, img_plane_to_image_mat):
    yres = IMG_H
    homoP = np.array([p[0], p[1], p[2], 1.0])
    posInCam = np.dot(world_to_cam_mat, homoP)
    # print(posInCam)
    posInCam = posInCam / posInCam[2]
    img_plane_pos = np.dot(cam_to_img_plane_mat, posInCam)
    # print(img_plane_pos)
    posInPix = np.dot(img_plane_to_image_mat, img_plane_pos)
    # print(posInPix)
    posInPix[1] = yres - posInPix[1]

    return [posInPix[1], posInPix[0]]
