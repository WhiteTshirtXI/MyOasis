__author__ = "Andreas Slyngstad"
__runs__   = "Solving NS on a tube with angular velocity, x[2] is along tube"
__mesh__ = "pipe3D.geo located in mesh file"

###############################################
#GMSH WILL RUN EVERY TIME SO USER CAN UPDATE MESH IN pipe3D.geo
#TO REMOVE THIS OPEN tube.py IN PROBLEMS AND CHANGE FIRST
#AND CHANGE 4.LINE WITH
#if not os.path.isfile("mesh/pipe3D1.xml"):
###############################################

from ..NSCoupled import *
from ..eccentric import *
import numpy as np
import matplotlib.pyplot as plt
from os import path

plot(mesh); interactive()

NS_parameters.update(
	nu = 1,
	max_iter = 10,
	folder = "eccentric"
	)


#plot(mesh); interactive()


#Setting boundary values
subdomain = FacetFunction("size_t", mesh)
subdomain.set_all(0)

## Class definition to mark the subdomains

class Circle(SubDomain):
	def inside(self, x, on_boundary):
		tol = 1E-8
		return on_boundary and (x[0]*x[0] + x[1]*x[1]) > 0.9 - tol

class Mdisk(SubDomain):
	def inside(self, x, on_boundary):
		tol = 1E-8
		a = -0.5; b = 0; r = 0.2
		return on_boundary and ( (x[0] - a)*(x[0] - a) + (x[1] - b)*(x[1] - b) ) < r*r + tol


circle = Circle()
mdisk = Mdisk()
circle.mark(subdomain, 1)
mdisk.mark(subdomain, 2)


#plot(subdomain); interactive()

#Disk
#u0x = Rotating()[0]; u0y = Rotating()[1]

def create_bcs(VQ, **NS_namespace):
    bc0 = DirichletBC(VQ.sub(0), ((0,0)), subdomain, 1)
    bc1 = DirichletBC(VQ.sub(0), ((0,0)), subdomain, 2)
    return dict(up = [bc0, bc1])

#def pre_solve_hook(u_, **NS_namespace):
	#plot(u_); interactive()

def theend_hook(p_, u_, V, mesh, **NS_namespace):
	plot(u_, title='Velocity')
	interactive()
