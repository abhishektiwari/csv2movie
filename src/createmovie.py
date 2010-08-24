'''
Created on 18/02/2010

@author: Abhishek Tiwari
'''
import os
import matplotlib.pyplot as plt
import numpy as np

def createmovie(xtit, ytit, list1, list2,foutput, fdir, fps):
    "Creates array of temp images and then stitch them together to create the movie"
    y = np.zeros((len(list1),len(list2)), list2.dtype)
    for i in range(len(list2)):
        y[i][i]= list2[i]
    print len(y), len(list1)
    j=1;
    for step in range(len(list1)):
        if j<len(list1):
            plt.plot(list1,y[j],'b.')
            plt.xlabel(xtit)
            plt.ylabel(ytit)
            plt.title(xtit+" vs "+ytit)
            plt.grid(True)
            filename = str('%05d' % step) + '_tmp.png'
            print filename
            plt.savefig(filename)      
        j=j+1
    output_avi=fdir+os.path.sep+xtit+"_"+ytit+".avi"
    output_mp4=fdir+os.path.sep+"movie.mp4"
    
    command = ('mencoder',
           'mf://*.png',
           '-mf',
           'type=png:w=800:h=600:fps=10',
           '-ovc',
           'lavc',
           '-lavcopts',
           'vcodec=mpeg4',
           '-oac',
           'copy',
           '-o',
           output_avi)
    
    if foutput is "mencoder":
        try:
            print "using mencoder to create movie"
            os.spawnvp(os.P_WAIT, 'mencoder', command)
        except OSError:
            print "could not find the mencoder or there is problem with command"
    if foutput is "ffmpeg":
        try:
            print "using ffmpeg to create movie"
            os.system("ffmpeg -r "+str(fps)+" -b 1800 -i %05d_tmp.png "+output_mp4)
        except OSError:
            print "could not find the ffmpeg or there is problem with command"