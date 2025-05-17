import cv2
import trimesh
import math
import numpy as np

class GeometryUtils:
    @staticmethod
    def intersection_ray_plain(ray_pt0, ray_pt1, plane_point, plane_normal, epsilon=1e-6):
        """
        Compute the intersection of a ray (through two points) and a plane.

        Parameters:
        -----------
        ray_pt0 : array-like of shape (3,)
            First point on the ray (ray origin).
        ray_pt1 : array-like of shape (3,)
            Second point on the ray (defines its direction).
        plane_point : array-like of shape (3,)
            Any point on the plane.
        plane_normal : array-like of shape (3,)
            Normal vector of the plane.
        epsilon : float
            Tolerance for detecting parallelism (default: 1e-6).

        Returns:
        --------
        numpy.ndarray or None
            Intersection point as a length-3 array, or None if the ray is
            parallel to the plane or the intersection lies behind the origin.
        """
        # Convert inputs
        p0 = np.asarray(ray_pt0, dtype=float) if not isinstance(ray_pt0, np.ndarray) else ray_pt0
        p1 = np.asarray(ray_pt1, dtype=float) if not isinstance(ray_pt1, np.ndarray) else ray_pt1
        p_plane = np.asarray(plane_point, dtype=float) if not isinstance(plane_point, np.ndarray) else plane_point
        n = np.asarray(plane_normal, dtype=float) if not isinstance(plane_normal, np.ndarray) else plane_normal

        # Direction vector of the ray
        d = p1 - p0

        # Check for parallelism: dot(n, d) == 0 → no intersection or infinite
        denom = np.dot(n, d)
        if abs(denom) < epsilon:
            return None

        # Compute ray parameter t
        t = np.dot(n, (p_plane - p0)) / denom

        # If t < 0, intersection is behind the ray origin
        if t < 0:
            return None

        # Return the intersection point
        return p0 + t * d

    def rvec_to_euler(rvec, degrees=True):
        """
        Convert a Rodrigues rotation vector to Euler angles (roll, pitch, yaw),
        using the Z–Y–X (yaw–pitch–roll) convention.

        Parameters
        ----------
        rvec : array-like, shape (3,)
            Rodrigues rotation vector.
        degrees : bool
            If True, return angles in degrees; otherwise in radians.

        Returns
        -------
        tuple of floats
            (roll, pitch, yaw) in specified units.
        """
        # 1) Rodrigues → rotation matrix
        R, _ = cv2.Rodrigues(np.asarray(rvec, dtype=float))

        # 2) Extract angles
        # sy = sqrt(R00² + R10²)
        sy = math.hypot(R[0, 0], R[1, 0])

        singular = sy < 1e-6
        if not singular:
            # Standard case
            roll = math.atan2(R[2, 1], R[2, 2])  # rotation about X
            pitch = math.atan2(-R[2, 0], sy)  # rotation about Y
            yaw = math.atan2(R[1, 0], R[0, 0])  # rotation about Z
        else:
            # Gimbal lock: pitch ≈ ±90°
            roll = math.atan2(-R[1, 2], R[1, 1])
            pitch = math.atan2(-R[2, 0], sy)
            yaw = 0.0

        if degrees:
            roll, pitch, yaw = map(math.degrees, (roll, pitch, yaw))

        return roll, pitch, yaw

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
        cam_R, _ = cv2.Rodrigues(self.cam_rvec)
        x0y0z1 = cam_R.dot(np.array([0, 0, 1]))  # frame plain normal vector from (0, 0)
        W, H = self.im_size

        p_cv_cam_x0y0z0 = self.cam_tvec
        p_cv_cam_x0y0z1 = p_cv_cam_x0y0z0 + x0y0z1

        cam_cv_intersection = GeometryUtils.intersection_ray_plain(
            p_cv_cam_x0y0z0,
            p_cv_cam_x0y0z1,
            (0, 0, 0)
            (0, 1, 0)
        )

        fx, fy, cx, cy = self.cam_intrinsics[[(0, 0), (1, 1), (0, 2), (1, 2)]].tolist()


mesh = ZeroMesh()
mesh.project()
trimesh_cam = mesh.convert_to_trimesh_cam()
