__author__ = "Andreas Slyngstad"
__runs__   = "Solving NS on a tube with angular velocity, x[2] is along tube"
__mesh__ = "pipe3D.geo located in mesh file"

###############################################
#GMSH WILL RUN EVERY TIME SO USER CAN UPDATE MESH IN pipe3D.geo
#TO REMOVE THIS OPEN tube.py IN PROBLEMS AND CHANGE FIRST
#AND CHANGE 4.LINE WITH
#if not os.path.isfile("mesh/pipe3D1.xml"):
###############################################

from ..NSfracStep import *
from ..tube import *
import numpy as np
import matplotlib.pyplot as plt
from os import path

 #RE = 4*10**4 for r = 2
NS_parameters.update(
	nu = 1,
	dt = 0.0001,
	T = 0.01,
	save_step = 10,
	folder = "vonkarman"
	)


#plot(mesh); interactive()

class Rotating(Expression):

	def eval(self, value, x):
		r = sqrt(x[0]*x[0] + x[1]*x[1])
		theta = 0
		if x[0] > 0 and x[1] >= 0:
			theta = atan(x[1]/x[0])
		elif x[0] > 0 and x[1] < 0:
			theta = atan(x[1]/x[0]) + 2.*pi
		elif x[0] < 0:
			theta = atan(x[1]/x[0]) + pi
		elif x[0] == 0 and x[1] > 0:
			theta = pi/2.
		elif x[0] == 0 and x[1] < 0:
			theta = 3*pi/2.
		elif x[0] == 0 and x[1] == 0: #To much ?
			theta = 0

		#Velocity Component
		value[0] =  r * -sin(theta)
		value[1] = r * cos(theta)

	def value_shape(self):
		return(2,)


#Setting boundary values
subdomain = FacetFunction("size_t", mesh)
subdomain.set_all(0)

## Class definition to mark the subdomains

class boundary(SubDomain):
	def inside(self, x, on_boundary):
		return on_boundary

#class Senter(SubDomain):
#	def insisde(self, x, on_boundary):
#		tol = 1*10**-3
#		return (x[0]  < tol) and (x[1] < tol) and (3 -x[2] < tol)


bd = boundary()

bd.mark(subdomain, 1)

plot(subdomain); interactive()

#Disk
u0x = Rotating()[0]; u0y = Rotating()[1]


def create_bcs(V, Q, **NS_namespace):
	#Sides slip
	slip = DirichletBC(V, 0, subdomain, 1)

	#Test
	#test = DirichletBC(Q, 10, subdomain, 4)
	#Disk
	bc0x = DirichletBC(V, u0x, subdomain, 4)
	bc0y = DirichletBC(V, u0y, subdomain, 4)
	bc0z = DirichletBC(V, 0, subdomain, 4)
	pr1 = DirichletBC(Q, 0, subdomain, 2)

	pr = DirichletBC(Q, 1, subdomain, 3)

	#Top
	top= DirichletBC(V, 0, subdomain, 3)


	return dict(u0 = [slip, bc0x],
				u1 = [slip, bc0y],
				u2 = [slip, bc0z],
				p = [pr])

def initialize(x_1, x_2, bcs, **NS_namespace):
    for ui in x_1:
        [bc.apply(x_1[ui]) for bc in bcs[ui]]
    for ui in x_2:
        [bc.apply(x_2[ui]) for bc in bcs[ui]]

#def pre_solve_hook(u_, **NS_namespace):
	#plot(u_); interactive()

def temporal_hook(tstep, u_, u_1, folder, **NS_namespace):
	if tstep % 10 == 0:

		e = errornorm(u_[0],u_1[0])
		if e < 1E-5: #tol
			f = open(path.join(folder, "killoasis"), "w")
			f.close()


def theend_hook(p_, u_, V, mesh, **NS_namespace):
	x_0 = -3./(2*-0.616)
	a = 0.510
	#sqrt(Assigned Vector Function_X^2+Assigned Vector Function_Y^2)/sqrt(coordsX^2 +coordsY^2)
	F = interpolate( Expression( '(1. - x[2]/x_0)*(1. - x[2]/x_0) * \
		(a*x[2] + ( 2.*a/x_0 - 0.5) * x[2]*x[2])',
					a = a, x_0 = x_0), V)

	G = interpolate(Expression('(1. - x[2]/x_0)*(1. - x[2]/x_0) * \
		(1 + x[2]/(2*x_0) )', x_0 = x_0) , V)


    # Naive implementation
	#from IPython import embed; embed()

	coor = np.zeros((100, 3))
	coor[:,0] = 1
	coor[:,1] = 0
	coor[:,2] = np.linspace(0, 2.5, 100)

	# = u(coor)
	u = []; v = []; w = []
	f = []; g = []
	for c in coor:
		u.append(u_[0](c) )
		v.append(u_[1](c) )
		w.append(u_[2](c) )
		f.append(F(c))
		g.append(G(c))

	mesh = IntervalMesh(99, 0, 2.5)
	V = FunctionSpace(mesh, "Lagrange", 1)
  	u_r = Function(V); u_t = Function(V); u_z = Function(V)
	#u = u[::-1]; v = v[::-1]; w = w[::-1]
	u = np.asarray(u); v = np.asarray(v); w = np.asarray(w)
	u_r.vector()[:] = u[:]
	u_t.vector()[:] = v[:]

	F = Function(V); f = np.asarray(f)
	G = Function(V); g = np.asarray(g)

	plt.figure(1)
	#plt.plot(g, 'green', label='G Function')
	#plt.plot(f, 'r', label= 'F Function')
	#plt.plot(u, 'g--',label='v_r')
	plt.plot(v, 'r--', label='v_theta')
	#plt.show()
	plt.legend()





"""
r_x = 1.; r_y = 0
coor = np.zeros((600, 3))
coor[:,2] = np.linspace(0, 0.05, 600)
coor[:,1] = r_y
coor[:,0] = r_x
# = u(coor)
u = []; v = []; w = []
for c in coor:
	u.append(u_[0](c) )
	v.append(u_[1](c) )
	w.append(u_[2](c) )
"""
