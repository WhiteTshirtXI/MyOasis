from dolfin import Mesh
import os

if not os.path.isfile("mesh/pipe3D.xml"):
    try:
        os.system("gmsh mesh/pipe3D.geo -3 -o mesh/pipe3D.msh")
        os.system("dolfin-convert mesh/pipe3D.msh mesh/pipe3D.xml")
        os.system("rm mesh/pipe3D.msh")
    except RuntimeError:
        raise "Gmsh is required to run this demo"

# Create a mesh
mesh = Mesh("mesh/pipe3D.xml")
