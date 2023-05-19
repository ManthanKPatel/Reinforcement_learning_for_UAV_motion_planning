import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib.patches import Circle, PathPatch
import mpl_toolkits.mplot3d.art3d as art3d
import pickle

with open('result_data.pkl', 'rb') as f:
    data = pickle.load(f)
Data = np.array(data['Path'])
Data = Data[:-1]

Y, Z = np.meshgrid(np.arange(-4, 4), np.arange(-4, 4))
# X = 4 #, 8, 12, 16, 20
# circ = [(1, -0.5),(-1.5, 1),(0.5,-1),(-1.5,-1),(0,1),(1.5, 0.5)]
circ = [( -1,-0.5),(1.5,1),(-0.5,-0.5),(1.5,-1),(0,1)]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
for i,X in enumerate(list([0, 4, 8, 12, 16])):
    surf = ax.plot_surface(X, Y, Z, alpha=0.1)  # the vertical plane
    # ax._facecolors2d = ax._facecolor
    surf._facecolors2d=surf._facecolor3d
    surf._edgecolors2d=surf._edgecolor3d
    p = Circle(circ[i], 1.75, alpha=0.2, color = 'b')
    ax.add_patch(p)
    art3d.pathpatch_2d_to_3d(p, z=X, zdir="x")
    #ax.scatter3D(Data[:,0],Data[:,1], Data[:,2], c=Data[:,0], cmap='Greens');
surf = ax.plot(np.flip(Data[:,0]),-Data[:,1],Data[:,2], label='ppo')
surf = ax.plot(Data[:,0],-Data[:,1],Data[:,2], label='po')
ax.legend()
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.show()