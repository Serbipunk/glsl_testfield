import cv2
import trimesh
import numpy as np

class ZeroMesh:
    def __init__(self):
        self.model = trimesh.load("../data/smpl000.obj", process=False)
        self.vertices = np.array(self.model.vertices)
        self.vertices = self.vertices[:, [0, 2, 1]] + [0, 0.225, 0.918]
        self.cam_intrinsics = np.array([[806.4, 0, 337.9],
                                        [0, 806.4, 503.9],
                                        [0, 0, 1]], np.float32)
        self.cam_tvec = np.array([-0.128, 1.097, 1.794], np.float32)
        self.cam_rvec = np.array([1.445, -0.051, 0.138], np.float32)
        self.im_size = (768, 1024)

    def project(self):
        points_2d, jaccobian = cv2.projectPoints(
            self.vertices,
            self.cam_rvec,
            self.cam_tvec,
            self.cam_intrinsics,
            None
        )
        points_2d = np.round(points_2d.reshape(-1, 2)).astype(np.int32)
        im = np.ones(shape=self.im_size[::-1], dtype=np.uint8) * 255
        for x, y in points_2d:
            cv2.circle(im, (x, y), 1, 0, -1)
        cv2.imwrite("out.png", im)

    def convert_to_trimesh_cam(self):
        pass

mesh = ZeroMesh()
mesh.project()