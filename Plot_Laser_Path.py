###############################################################################
# Animate path
###############################################################################
# Script for animating the laser/extrusion path for .csv of t,x,y,z
###############################################################################
# Written by:
# William Furr
# wmf54@msstate.edu
# wmf54@cavs.msstate.edu
###############################################################################
# edit history:
##############
# 06/20/2018 original coding
###############################################################################
#
# Import necessary packages.
import numpy as np
import csv
import matplotlib.pyplot as plt
import matplotlib.animation as animation
###############################################################################
#
# Read in the file contents into a NumPy array to easily work with the contents.
##############
# Define the file name. (must be a .csv file format)
laser_location_path=r'RTRC_032_print_path.csv'

with open(laser_location_path, 'r') as f:
        lasertable = list(csv.reader(f,delimiter=','))

# Create numpy array from data
lasertable = np.array(lasertable[1:])
lasertable=lasertable.astype(float)
#dat = dat.astype(float)
# Output path for video file
output_name='O2_Test_Vid'
output_path=r'I:\projects\ColdSpray\Topic6\mr1751\Excel Files'
###############################################################################
# This is stuff I found on stackoverflow to make the updating title for the plot work.
# I don't know what any of this means
####################################

def _blit_draw(self, artists, bg_cache):
    # Handles blitted drawing, which renders only the artists given instead
    # of the entire figure.
    updated_ax = []
    for a in artists:
        # If we haven't cached the background for this axes object, do
        # so now. This might not always be reliable, but it's an attempt
        # to automate the process.
        if a.axes not in bg_cache:
            # bg_cache[a.axes] = a.figure.canvas.copy_from_bbox(a.axes.bbox)
            # change here
            bg_cache[a.axes] = a.figure.canvas.copy_from_bbox(a.axes.figure.bbox)
        a.axes.draw_artist(a)
        updated_ax.append(a.axes)

    # After rendering all the needed artists, blit each axes individually.
    for ax in set(updated_ax):
        # and here
        # ax.figure.canvas.blit(ax.bbox)
        ax.figure.canvas.blit(ax.figure.bbox)

# MONKEY PATCH!!
animation.Animation._blit_draw = _blit_draw


###############################################################################
# Actually do the animation
#############################



# to only use when power is nonzero
index_list=[]
indexes=np.linspace(0,len(lasertable[:,0]),int((len(lasertable[:,0]))/2)).astype(int)
lasertable=lasertable[indexes[:-1]]
for index,value in enumerate(lasertable[:,4]):
    if value>0.001:
        index_list.append(index)
 


lasertable=lasertable[index_list,:]
indices=np.linspace(0,len(lasertable)-1,int((len(lasertable)-1)/8)).astype(int) 
lasertable=lasertable[indices]


x=lasertable[:,1]
y=lasertable[:,2]
t=lasertable[:,0]
p=lasertable[:,4]

fig, ax = plt.subplots()

line, = ax.plot(x, y, 'o')
ttl = ax.set_title('',animated=True)
ttl = ax.text(.5, 1.05, '', transform = ax.transAxes, va='center')

def init():
    ttl.set_text('')
    line.set_data([0],[0])
    return line, ttl


def update(num, x, y, t, line):
    line.set_data(x[:num], y[:num])
    
    ttl.set_text('time:'+str(t[num])+'     '+'x:'+str(x[num])+'     '+'y:'+str(y[num])+'     '+'power:'+str(p[num]))

    return line, ttl

ani = animation.FuncAnimation(fig, update, len(x),init_func=init, fargs=[x, y, t, line],interval=25, blit=True)

# To save the animation
#ani.save(output_path+output_name+'.mp4')

plt.show()