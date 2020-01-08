#!/usr/bin/env python
# coding: utf-8
import math
import getopt
import sys
import os
import re
from fractions import Fraction
from itertools import product, permutations


## TODO: add pass im option  
test = '/home/shera/P3DFFT++/p3dfft.3/sample/C/test3D_r2c_c'
output_dir = '/home/shera/benchresult_r2c_c'
job_output = '/home/shera/job_p3dfft++'

dimensions_256 = [(16,16),(32,8),(64,4)]
dimensions_512 = [(32,16),(64,8),(128,4)]
dimensions_1024 = [(32,32),(64,16),(128,8)]
dimensions_2048 = [(32,64)]
dimensions = {256:dimensions_256, 512:dimensions_512, 1024:dimensions_1024, 2048:dimensions_2048}

grid_nums = ['256 256 256 2 10', '512 512 512 2 10', '1024 1024 1024 2 10','2048 2048 2048 2 10']


def runline(output_dir, test, dimension,grid):
    coreNum = dimension[0] * dimension[1]
    r = "ibrun -n " + str(coreNum) + " " + test
    record = "echo " + "\'" + str(dimension[0]) + " " + str(dimension[1]) + "\'"
    outFname = os.path.join(output_dir, "output_" + str(coreNum) + "_" + str(dimension[0]) + "_" + str(dimension[1]))+"_"+grid[0:4] 
    time = "grep 'Time' " + outFname
    catch = "grep 'time' " + outFname
    return r + " >> " + outFname  + '\n' + record + "\n" +time + '\n'+ catch + '\n'

def script_header(batchf, output_dir, sd,core):
    node_num = int(core/24)+1
    batchf.write('#!/bin/bash\n')
    batchf.write('#SBATCH --job-name="' + "p3dfft++_Benchmarks" + '"\n')
    batchf.write('#SBATCH --output="' + output_dir + "/p3dfft_Benchmarks" + str(core) + '"\n')
    batchf.write('#SBATCH --partition=compute \n')
    batchf.write('#SBATCH --nodes=' + str(node_num) + '\n')
    batchf.write('#SBATCH --ntasks-per-node=24'+'\n')
    batchf.write('#SBATCH -t 00:20:00\n')
  
def buildall(test, grid_nums,core,dimensions_coreNum, output_dir):
    fname = job_output +  "/p3dfft++_Benchmarks" +str(core) + ".sh"
    batchf = open(fname, 'w')
    script_header(batchf, output_dir,job_output, core)
    for grid in grid_nums:
        batchf.write("echo '" + grid + "' > stdin\n")
        batchf.write("echo '" + grid + "\'" + "\n")
        for dimension in dimensions_coreNum:
            batchf.write("echo " + "\'" + str(dimension[0]) + " " + str(dimension[1]) + "\'" + " > dims\n")
            batchf.write(runline(output_dir,test,dimension,grid))
        batchf.write("\n")    
    batchf.close()


def main():
    for i in dimensions:
        buildall(test, grid_nums,i,dimensions[i], output_dir)


if __name__ == '__main__':
    main()
