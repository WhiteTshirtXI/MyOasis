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
from ..cylpipe import *
import numpy as np
import matplotlib.pyplot as plt
from os import path

NS_parameters.update(
	nu = .1,
	omega = 0.95,
	max_iter = 250,
	folder = "eccentric"
	)

#plot(mesh, interactive=True)
#Setting boundary values
boundaries = FacetFunction("size_t", mesh)

top = AutoSubDomain(lambda x: near(x[2], 6))
bottom = AutoSubDomain(lambda x: near(x[2], 0))
nos = DomainBoundary() #AutoSubDomain(lambda x: not near(x[2], 2) and not near(x[2], 0))

boundaries.set_all(0)
nos.mark(boundaries,1)
top.mark(boundaries, 2)
bottom.mark(boundaries, 3)
plot(boundaries); interactive()

def create_bcs(VQ, **NS_namespace):
	u_in = Expression(("0", "0",'- dpdx/(4*mu) * \
					(r_0*r_0 - (x[0]*x[0] + x[1]*x[1])*\
					(x[0]*x[0] + x[1]*x[1]))'), r_0 = 1, dpdx =-2.5, mu = 1)

	u_in = Expression(("0", "0", "8"))
	#CIRCUMFERENCE PROPERTIES
	noslip = DirichletBC(VQ.sub(0), ((0, 0, 0)), boundaries, 1)

	#INFLOW PROPERTIES
	#inflow = DirichletBC(VQ.sub(0), ((0, 0, 1)), boundaries, 3)
	inflow = DirichletBC(VQ.sub(0), u_in, boundaries, 3)
	p_in = DirichletBC(VQ.sub(1), 6, boundaries, 3)

	#OUTFLOW PROPERTIES
	p_out = DirichletBC(VQ.sub(1), 0, boundaries, 2)

	outflow = DirichletBC(VQ.sub(0), u_in, boundaries, 2)
	return dict(up = [p_in, p_out, noslip])

#def pre_solve_hook(u_, **NS_namespace):
#	print u_[2](np.array([0,0,0]))

	#print u_[2].vector().array().max()
#	plot(u_, interactive=True)

def theend_hook(VQ, u_, mesh, **NS_namespace):
	#plot(u_e, interactive=True)
	plot(u_, title='Velocity', interactive=True)

	V = FunctionSpace(mesh, 'CG', 2)
	u_e = interpolate(Expression('- dpdx/(4*mu) * \
					( r_0*r_0 - (x[0]*x[0] + x[1]*x[1])*\
					(x[0]*x[0] + x[1]*x[1]) )', r_0 = 1, dpdx = -2.5, mu = 1), V)

	coor = np.zeros((200, 3))
	coor[:,0] = np.linspace(-1, 1, 200) ;coor[:,1] = 0; coor[:,2] = 1

	coor1 = np.zeros((200, 3))
	coor1[:,0] = np.linspace(-1, 1, 200) #;coor[:,1] = 0

	print mesh.num_cells()
	#Velocity Coordinates
	u = []; u_a = []
	for c in coor:
		u.append(u_[2](c) )
	for d in coor1:
		u_a.append(u_e(d)) #Different values if z removed from coor

	u = np.asarray(u); u_a = np.asarray(u_a)

	plt.figure(1)
	plt.plot(coor[:,0], u, label='Numerical')
	plt.plot(coor[:,0], u_a, label='Exact')
	plt.legend()
	plt.show()

	# Save solution to file
	Ve = VectorFunctionSpace(mesh, 'CG', 1)
	e = project(u_, Ve)
	File('cylpipe_velocity.pvd') << e
