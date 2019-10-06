#------------------------------
# Import Libraries          
import numpy as np
import trimesh
import sys
import argparse
#------------------------------

# 3D object model class
class converter_obj:
        def __init__(self, input_path, output_path):                            # Constructor Definition
            self.input_path  = input_path
            self.output_path = output_path
            self.mesh        = trimesh.load(self.input_path)

        def print_surfaceArea(self):                                            # Total Surface Area
            area = self.mesh.area
            print("     Surface area of the model    : ",area)
        
        def print_volume(self):                                                 # Volume
            volume = self.mesh.volume
            print("     Volume of the model          : ",volume)

        def apply_scale(self, scale_rate):                                      # Scale rate
            self.mesh = self.mesh.apply_scale(scale_rate)

        def apply_transformation(self, transformation_matrix):                  # Size of transformation matrix must be 4x4
            self.mesh = self.mesh.apply_transform(transformation_matrix)

        def apply_translation(self, translation_matrix):                        # Size of translation matrix must be (3,)
            self.mesh = self.mesh.apply_translation(translation_matrix)

        def check_position(self, point_coordinates):                            # Check the 3D point if it is inside the model
            try:
                ret = self.mesh.contains(np.array([point_coordinates]))
                if ret[0]:
                    print("3D point is inside the model")
                else:
                    print("3D point is outside the model")
            except:
                print("3D point is inside the model")

        def plot_Model(self):                                                   # 3D plotting
            self.mesh.show()

        def create_binaryStl(self):                                             # Convert file from .obj to binary .stl file
            self.mesh.export(self.output_path)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-i","--inputPath", required=True, help="Input file path")
    ap.add_argument("-o","--outputPath", required=True, help="Output file path" )
    ap.add_argument("-s","--scaleRate", required=False, help="Scale rate description", type=float)
    ap.add_argument("-tf","--transformationMatrix", required=False, help="Transformation matrix (it must be 4x4 matrix)", type=str)
    ap.add_argument("-tl","--translationMatrix", required=False, help="Translation matrix", type=str)
    ap.add_argument("-p","--pointCoordinates", required=False, help="X,Y,Z coordinates of 3D point, eg 1,2,3", type=str)

    args = vars(ap.parse_args())

    print("------------------------------------------------------------------------------------------------")
    print("3D_Model working...")
    obj = converter_obj(args["inputPath"],args["outputPath"])
    obj.print_surfaceArea()
    obj.print_volume()

    if(args["transformationMatrix"] is not None):
        arrTF = np.array(args["transformationMatrix"].split(","), dtype=float)
        arrTF = arrTF.reshape(4,4)
        obj.apply_transformation(arrTF)
    if(args["translationMatrix"] is not None):
        arrTL = np.array(args["translationMatrix"].split(","), dtype=float)
        obj.apply_translation(arrTL)
    if(args["pointCoordinates"] is not None):
        arrP = np.array(args["pointCoordinates"].split(","), dtype=float)
        obj.check_position(arrP)
    if(args["scaleRate"] is not None):
        obj.apply_scale(args["scaleRate"])

    obj.create_binaryStl()