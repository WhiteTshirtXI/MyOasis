__author__ = "Andreas Slyngstad"
__dsic__   = "Solving NS on a tube with angular velocity, x[2] is along tube"
###############################################
#GMSH WILL RUN EVERY TIME SO USER CAN UPDATE MESH IN pipe3D.geo
#TO REMOVE THIS OPEN tube.py IN PROBLEMS AND CHANGE FIRST
#AND CHANGE 4.LINE WITH
#if not os.path.isfile("mesh/pipe3D.xml"):
###############################################

from ..NSCoupled import *
from ..tube import *
import numpy as np

#plot(mesh);interactive()

NS_parameters.update(
	nu = 1,
	omega = 1,
	max_iter = 1,
	folder = "CoupledPipe"
	)

#Setting boundary values
boundaries = FacetFunction("size_t", mesh)

top = AutoSubDomain(lambda x: near(x[2], 3))
bottom = AutoSubDomain(lambda x: near(x[2], 0.0))
nos = DomainBoundary()

boundaries.set_all(0)
nos.mark(boundaries,1)
top.mark(boundaries, 2)
bottom.mark(boundaries, 3)
plot(boundaries); interactive()

class Rotating(Expression):

	def eval(self, value, x):
		r = sqrt(x[0]*x[0] + x[1]*x[1])
		if x[0] > 0 and x[1] >= 0:
			theta = atan(x[1]/x[0])
		elif x[0] > 0 and x[1] < 0:
			theta = atan(x[1]/x[0]) + 2*pi
		elif x[0] < 0:
			theta = atan(x[1]/x[0]) + pi
		elif x[0] == 0 and x[1] > 0:
			theta = pi/2.
		elif x[0] == 0 and x[1] < 0:
			theta = 3*pi/2.
		elif x[0] == 0 and x[1] == 0: #To much ?
			theta = 0

		#Velocity Component
		value[0] = r * -sin(theta)
		value[1] = r * cos(theta)
		value[2] = 0

	def value_shape(self):
		return(3,)

spin = Rotating( degree = 3)

def create_bcs(VQ, **NS_namespace):

	#SIDES
	nos = DirichletBC(VQ.sub(0), ((0, 0, 0)) , boundaries, 1)

	#TOP SIDE
	press = DirichletBC(VQ.sub(1), 0 , boundaries, 2)
	#top = DirichletBC(VQ.sub(0), ((1, 0, 0)) , boundaries, 2)

	#DISK
	bottom = DirichletBC(VQ.sub(0), spin , boundaries, 3)

	return dict(up = [bottom, press] )

def theend_hook(u_, p_, mesh, **NS_namespace):
	plot(mesh); interactive()
	plot(u_, title='Velocity', interactive = True)
	#interactive()
	r_x = 1.; r_y = 0
	coor = np.zeros((100, 3))
	#coor[:,2] = np.linspace(0, 0.1, 600)
	coor[:,2] = 0
	#coor[:,1] = r_y; coor[:,0] = r_x
	coor[:,1] = 0; coor[:,0] = np.linspace(0, 2, 100)
	# = u(coor)
	u = []; v = []; w = []
	for c in coor:
		u.append(u_[0](c) )
		v.append(u_[1](c) )
		w.append(u_[2](c) )


	mesh = IntervalMesh(99, 0, 0.05)
	V = FunctionSpace(mesh, "Lagrange", 1)
  	u_r = Function(V)
	u = np.asarray(u); v = np.asarray(v)
  	u_r.vector()[:] = (u[:] + v[:])/np.sqrt(r_x*r_x + r_y*r_y)
	file = File("newton.vtk")
	file  << u_
	#u_theta.vector()[:] =

	#plot(u_r); interactive()
