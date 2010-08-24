"""
CSV2Movie takes a csv file as input and creates movies by stitching the plotted images 
frame by frame. Each image plot will become a single frame in the movie. CSV2Movie 
requires mencoder (http://www.mplayerhq.hu/) or ffmpeg (http://www.ffmpeg.org/) to 
create the light weight movies for the csv file data. User needs to provide the 
command-line arguments and either short- or long-style flags to specify various options.

On Ubuntu you can install mencoder and ffmpeg using synaptic package manager. For Windows
you have to download the executable files for mencoder and ffmpeg and set the environment
variables. For Mac OS installation details are here
here http://www.macosxhints.com/article.php?story=20061220082125312

usage: python CSV2Movie.py [ -h | -f | -t | -c | -d | -m | -e] [arg] ...
Options and arguments (and corresponding environment variables):
-h    : print this help message (also --help)
-f    : input CSV file location (also --file)
-t    : tab-delimited csv files
-c    : comma-separated values (CSV) file (default)
-s    : semi colon delimited file
-o    : colon delimited file
-m    : use  ffmpeg to create movie (default)
-e    : use  mencoder to create movie
-p    : frames per second for the movie (also --fps) (defult fps=10)
arg   : reference columns for plotting. CSVPlot plots all other columns against
        the reference column. By default it uses column 1.

Example use:
1. For help information,
python CSV2Movie.py --help 
OR
python CSV2Movie.py --h 
2. For plotting column x and y of file data.csv,
python CSV2Movie.py -c -m -f data.csv x y
python CSV2Movie.py -t -e --file=data.csv x y


"""
'''
Created on 18/02/2010

@author: Abhishek Tiwari
http://www.abhishek-tiwari.com

Permission is hereby granted to use and abuse this document
so long as proper attribution is given.

'''
import os
import sys
import getopt
import numpy as np
import csv
import createmovie as mov

class Usage(Exception):
    "Usage() exception class, which we catch in an except clause at the end of main()"
    def __init__(self,msg):
        "A description of the Usage constructor"
        self.msg=msg

def main(argv=None):
    "main() function to analyse the command line flags and arguments, and activate further anlysis"
    fdelimiter=","
    foutput="mencoder"
    fargument="0"
    fps=10
    if argv is None:
        argv=sys.argv
    try:
        if len(argv) <=2:
            raise Usage(__doc__)
        try:
            opts,args= getopt.getopt(sys.argv[1:],"ctsomehp:f:",["help","file=","fps="])
        except getopt.error,msg:
            raise Usage(msg)
        #Option processing
        for option, value in opts:
            if option in ("-h","--help"):
                raise Usage(__doc__)
                sys.exit(0)
            else:
                if option in ("-f","--file"):
                    fname=value
                    print "Input CSV File:", fname
                    fdir=os.path.realpath(os.path.dirname(fname))
                    #fdir=os.path.dirname(os.path.realpath(fname))
            if option in("-t"):
                fdelimiter="\t"
            elif option in("-c"):
                fdelimiter=","
            elif option in("-s"):
                fdelimiter=";"
            elif option in("-o"):
                fdelimiter=":"
            if option in("-m"):
                foutput="ffmpeg"
            elif option in ("-e"):
                foutput="mencoder"
            if option in ("-p","--fps"):
                fps=value
        #Argument processing
        if len(args) !=0:
            for argument in args:
                argument.strip()
                try:
                    cargument = int(argument)
                except:
                    print 'cannot cast column argument to int'
                if isinstance(cargument, int) and cargument>=1:
                    print "For column-",cargument
                    fargument=cargument-1
                    plotter(fname, fdelimiter, foutput, fargument, fdir, fps)
        else:
            plotter(fname, fdelimiter, foutput, fargument, fdir, fps)
    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2

def plotter(fname, fdelimiter, foutput, fargument, fdir,fps):
    "This function parse the data in csv file and then calls different plotting functions"
    try:
        fopen=open(fname,'r')
        csvreader = csv.reader(fopen, delimiter=",")
        fields = csvreader.next()
    except:
        print "Can not open input csv file",fname
    fopen.close
    data=np.loadtxt(fname, delimiter=fdelimiter, unpack=True, skiprows=1)
    i=0;
    while i<len(fields):
        if  fargument != i:
            xtit=fields[fargument]
            ytit=fields[i] 
            print xtit, ytit
            mov.createmovie(xtit, ytit, data[fargument], data[i],foutput, fdir, fps)
            os.system("rm *_tmp.png")
            i=len(fields);
        i=i+1
        
if __name__ == "__main__":
    "The main program collected into function main()"
    sys.exit(main())