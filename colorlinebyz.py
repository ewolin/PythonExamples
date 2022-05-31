#!/usr/bin/env python


import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm, Normalize


def plotcoloredline(x, y, z):
    fig = plt.figure()
#    ax = fig.gca(projection='3d')
    ax = fig.gca()
    N = len(x)
#1 colored by value of `z`
#ax.scatter(x, y, z, c = plt.cm.jet(z/max(z))) 
#    ax.scatter(x, y, z, c = plt.cm.jet(np.linspace(0,1,N)))
#2 colored by index (same in this example since z is a linspace too)
    for i in range(N-1):
        #ax.plot(x[i:i+2], y[i:i+2], z[i:i+2], color=plt.cm.jet(i/N))
        ax.plot(x[i:i+2], y[i:i+2], color=plt.cm.jet(i/N))
    return fig

def plotcoloredline2(tr, fig, plottype='line'):

    y = tr.data
    x = tr.times()
    z = y

# Create a colormap for red, green and blue and a norm to color
# f' < -0.5 red, f' > 0.5 blue, and the rest green
#cmap = ListedColormap(['r', 'g', 'b'])
    N = len(x)
#cmap = cmap=plt.get_cmap('seismic')(200) #ListedColormap(['r', 'g', 'b'])
#cmap = cmap=plt.get_cmap('RdBu')(200) 
#cmap = cmap=plt.get_cmap('RdYlBu')(N) 
    cmap = plt.cm.RdYlBu
    norm = Normalize(vmin=-1.,vmax=1.)
    bounds = np.linspace(-1, 1, 100)
    norm = BoundaryNorm(boundaries=bounds, ncolors=256)

    if plottype == 'line':

    
    # Create a set of line segments so that we can color them individually
    # This creates the points as a N x 1 x 2 array so that we can stack points
    # together easily to get the segments. The segments array for line collection
    # needs to be numlines x points per line x 2 (x and y)
        points = np.array([x, y]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
    
    # Create the line collection object, setting the colormapping parameters.
    # Have to set the actual values used for colormapping separately.
    #lc = LineCollection(segments, cmap=cmap, norm=norm)
        lc = LineCollection(segments, cmap=cmap, zorder=1)
        lc.set_array(z)
        lc.set_linewidth(3)
        fig.gca().add_collection(lc)
    
        fig.gca().set_xlim(x.min(), x.max())
        fig.gca().set_ylim(-1.1, 1.1)


    elif plottype == 'scatter':
    #ax.scatter(x, y, c=y, cmap=cmap(np.linspace(0,1,N)), s=20, zorder=2)
#    ax.scatter(x, y, c=y, cmap=cmap, s=50, zorder=2)
        fig.gca().scatter(x, y, c=y, cmap=cmap, s=50, zorder=2)


def main():
    theta = np.linspace(-4 * np.pi, 4 * np.pi, 100)
    z = np.linspace(-2, 2, 100)
    r = z**2 + 1
    x = r * np.sin(theta)
    y = r * np.cos(theta)


    #cols = 'rgbcmy'

    #for i in range(len(x)-1):
    #    ax.plot(x[i:i+2], y[i:i+2]+0.1, z[i:i+2], color=cols[i%6])
    plotcoloredline(x,y,z)
    plt.show()


if __name__ == "__main__":
    main()


