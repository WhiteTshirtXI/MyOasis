from dolfin import Mesh
import os

if not os.path.isfile("mesh/eccentric1.xml"):
    try:
        os.system("gmsh mesh/eccentric.geo -2 -o mesh/eccentric.msh")
        os.system("dolfin-convert mesh/eccentric.msh mesh/eccentric.xml")
        os.system("rm mesh/eccentric.msh")
    except RuntimeError:
        raise "Gmsh is required to run this demo"

# Create a mesh
mesh = Mesh("mesh/eccentric.xml")
