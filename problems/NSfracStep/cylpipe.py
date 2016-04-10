__author__ = "Andreas Slyngstad"
__runs__   = "Solving NS on a tube with angular velocity, x[2] is along tube"
__mesh__ = "pipe3D.geo located in mesh file"


from ..NSfracStep import *
from ..cylpipe import *
import numpy as np
import matplotlib.pyplot as plt
from os import path

NS_parameters.update(
	nu = 1,
	dt = 0.01,
	T = 5,
	save_step = 500,
	folder = "Cylpipe"
	)

a = 2

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
#plot(boundaries); interactive()

def create_bcs(V, Q, **NS_namespace):
	#Sides slip
	slip = DirichletBC(V, 0, boundaries, 1)

	#inflow
	u_in = interpolate(Expression('- dpdx/(4*mu) * \
					( r_0*r_0 - (x[0]*x[0] + x[1]*x[1])*\
					(x[0]*x[0] + x[1]*x[1]) )', r_0 = 1, dpdx = -6, mu = 1), V)
	bc0x = DirichletBC(V, 0, boundaries, 2)
	bc0y = DirichletBC(V, 0, boundaries, 2)
	bc0z = DirichletBC(V, 0, boundaries, 2)
	pr_in = DirichletBC(Q, 20, boundaries, 2)

    #outflow
	pr_out = DirichletBC(Q, 14, boundaries, 3)


	return dict(u0 = [slip],
				u1 = [slip],
				u2 = [u_in, slip],
				p = [pr_in, pr_out])

def initialize(x_1, x_2, bcs, **NS_namespace):
    for ui in x_1:
        [bc.apply(x_1[ui]) for bc in bcs[ui]]
    for ui in x_2:
        [bc.apply(x_2[ui]) for bc in bcs[ui]]


def theend_hook(V, Q, u_, mesh, **NS_namespace):
    #plot(u_, title='Velocity', interactive=True)
    u_e = interpolate(Expression('- dpdx/(4*mu) * \
					( r_0*r_0 - (x[0]*x[0] + x[1]*x[1])*\
					(x[0]*x[0] + x[1]*x[1]) )', r_0 = 1, dpdx = -6, mu = 1), V)

    coor = np.zeros((200, 3))
    coor[:,0] = np.linspace(-1, 1, 200); coor[:,1] = 0; coor[:,2] = 1

    coor1 = np.zeros((200, 3))
    coor1[:,0] = np.linspace(-1, 1, 200) #;coor[:,1] = 0

    u_a = []; u_0 = []; u_1 = []; u_3 = []; u_5=[]
    u_val = [0, 1, 3, 5]; u_list = [u_0, u_1, u_3, u_5]

    #GENERATE VALUES OF VELOCITY AT CHOSEN Z
    for i in range(len(u_val)):
        coor[:,2] = u_val[i]
        for c in coor:
        	u_list[i].append(u_[2](c) )
    for d in coor1:
        u_a.append(u_e(d)) #Different values if z removed from coor

    u_a = np.asarray(u_a)
    u_0 = np.asarray(u_0); u_1 = np.asarray(u_1); u_3 = np.asarray(u_3); u_5 = np.asarray(u_5);

    plot(u_e, interactive=True)
    fig = plt.figure(1)
    ax = fig.add_subplot(111)
    ax.plot(coor[:,0], u_a, label="Analytical Solution")
    for i in range(len(u_val)):
        string = "u_z for z = %d" % u_val[i]
        ax.plot(coor[:,0], u_list[i], label = string)

    ax.set_xlabel("radius in the X-Direction, Y=0")
    ax.set_ylabel("Velocity u_z")

    plt.legend()
    plt.show()

    # Save solution to file
    #Ve = VectorFunctionSpace(mesh, 'CG', 1)
    #e = project(u_, Ve)
    #File('cylpipe_velocity.pvd') << e
