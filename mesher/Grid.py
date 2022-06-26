import math
from mesher.Pose import Pose
import numpy as np
from scipy.spatial.transform import Rotation as R
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class Grid:
    def __init__(self,radius:float ,v_steps: int,v_size: float,h_steps: int,h_size: float,up_only: bool=True):
        """
        Creates a grid of poses around a central point.

        Parameters
        ----------
        radius : float
                 The radius of the sphere where the poses are generated.

        v_steps : int
                  The number of steps (in each direction) in the vertical plane

        v_size : float
                  The size of the steps in the vertical plane (in radians).

        h_steps : int
                  The number of steps (in each direction) in the horizontal plane

        h_size : float
                  The size of the steps in the horizontal plane (in radians).

        up_only : bool
                  A boolean that controls whether there are points above and below the horizon in the vertical plane.

        """
        self._circle_radius = radius
        self._v_steps = v_steps
        self._h_steps = h_steps
        self._v_size = v_size
        self._h_size = h_size
        self._up_only = up_only
        self._poses = []
        self.generate_mesh()
        self._base_position = np.array([0,0,0])
        self._base_rotation = R.from_euler('xyz',[0,0,0],degrees=False)

    @property
    def base_position(self):
        """
        Getter setter for the base_position (or centre of sphere).
        """
        return self._base_position

    @base_position.setter
    def base_position(self,value: np.array):
        self._base_position = value
        for p in self._poses:
            p.translate(self._base_position)

    @property
    def base_rotation(self):
        """
        Getter setter for the rotation of the base_position (or centre of the sphere).
        """
        return self._base_rotation

    @base_rotation.setter
    def base_rotation(self,value: R):
        self._base_rotation = value
        for p in self._poses:
            p.rotate(self._base_position,self._base_rotation)

    def generate_mesh(self):
        v_base = 0
        if not self._up_only:
            v_base = -self._v_steps
        for i in range(v_base,self._v_steps+1):
            for j in range(-self._h_steps,self._h_steps+1):
                pose = self._point_on_sphere(self._circle_radius,self._v_size*i,self._h_size*j)
                self._poses.append(pose)
    
    def draw(self, show_lines: bool = False):
        """
        Plot the points using matplotlib.

        Parameters
        ----------
        show_lines : bool
                     A boolean that controls whether the direction vectors are visualised.
        """
        fig = plt.figure(figsize=(10,10))
        ax = fig.add_subplot(111,projection='3d')
        ax.scatter(self._base_point[0],self._base_point[1],self._base_point[2])
        for pose in self._poses:
            ax.scatter(pose.x_position,pose.y_position,pose.z_position)
            if show_lines:
                t = pose.line_endpoint()
                ax.plot([pose.x_position,t[0]],[pose.y_position,t[1]],[pose.z_position,t[2]])
        plt.show()

    def _point_on_sphere(radius:float , rotation_y: float, rotation_x: float):
        """
        Generates a point on the surface of a sphere.

        Parameters
        ----------
        radius : float
                 Radius of the sphere

        rotation_y : float
                     Rotation in the vertical plane in radians.


        rotation_x : float
                     Rotation the horizontal plane in radians.

        Returns 
        -------
        Pose : The pose on the sphere.
        """
        rotation_y = math.pi/2 - rotation_y
        x = radius * math.cos(rotation_x) * math.sin(rotation_y)
        y = radius * math.sin(rotation_x) * math.sin(rotation_y)
        z = radius * math.cos(rotation_y)
        rot = R.from_euler('xyz',[0,-(math.pi/2-rotation_y),rotation_x],degrees=False)
        position = np.array([x,y,z])
        pos = Pose(position,rot)
        return pos