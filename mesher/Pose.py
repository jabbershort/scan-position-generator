import numpy as np
from scipy.spatial.transform import Rotation as R

class Pose():
    def __init__(self, position: np.array, rotM: R):
        """
        Creates a pose with position and rotation

        Parameters
        ----------
        position : numpy.array
                   3D location of pose

        rotation : scipy.spatial.transform.Rotation
                   Rotation of pose

        """
        self.position = position
        self.rotation = rotM

    @property
    def x_position(self):
        """
        Getter setter for the x_position
        """
        return self.position[0]
    
    @x_position.setter
    def x_position(self,value: float):
        self.position[0] = value

    @property
    def y_position(self):
        """
        Getter setter for the y_position
        """
        return self.position[1]

    @y_position.setter
    def y_position(self,value: float):
        self.position[1] = value

    @property
    def z_position(self):
        """
        Getter setter for the z_position
        """
        return self.position[2]

    @z_position.setter
    def z_position(self,value: float):
        self.position[2] = value

    def line_endpoint(self):
        """
        Returns the endpoint of a line 0.1 units long. Primarily used for display of direction vectors.
        """
        end_position = np.array([self.x_position-0.1,self.y_position,self.z_position])
        line_vector = np.array([-0.1,0,0])
        
        # rotated_end_point = np.linalg.inv(self.rot)@end_position
        rotated_vector = self.rotation.apply(line_vector)
        end_point = np.array([
            self.x_position+rotated_vector[0],
            self.y_position+rotated_vector[1],
            self.z_position+rotated_vector[2]
            ])
        return end_point

    def translate(self, translation: np.array):
        """
        Translate the pose to a different base position.

        Parameters
        ----------
        translation : numpy.array
                      The 3D translation of the pose.
        """
        self.x_position += translation[0]
        self.y_position += translation[1]
        self.z_position += translation[2]


    # TODO rotate pose around base point
    def rotate(self, base_position: np.array, rotation: R):
        print("Function not yet implemented.")

    # TODO: string override

    # TODO: Inverse Kinematics for robot arms


