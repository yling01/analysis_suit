'''
Tim Ling

Last update: 2020.07.03
'''
import matplotlib
matplotlib.use('AGG')

import optparse
import os
import sys
import time

sys.path.insert(1, 'source/')

from MakeFigure import *
from CalcNIP import *
from Cluster import *
from MakeDensityMtx import *
import shutil
def getInput(input):
    if input[0].upper() == "T":
        return True
    return False

parser = optparse.OptionParser()
parser.add_option('--projection', dest = 'projection',
                  default = 'all.txt',
                  help = 'Projection')
parser.add_option('--interactive', dest = 'interactive',
                  default = "False",
                  help = 'True to select cluster centers')
parser.add_option('--timer', dest = 'time_procedure',
                  default = 'False',
                  help = 'True to time to analysis procedure')
parser.add_option('--debug', dest = 'debug',
                  default = 'False',
                  help = 'True to print out useful information')
parser.add_option('--seq', dest = 'seq',
                  default = 'Result',
                  help = 'Name of sequence')
parser.add_option('--s1OmegaAngle', dest = "s1OmegaAngle",
                  default = "../1trimTrajectory/s1/struct_omega.xvg")

(options,args) = parser.parse_args()

time_procedure = getInput(options.time_procedure)
interactive = getInput(options.interactive)
debug = getInput(options.debug)
dir_name = options.seq
projectionFile = options.projection

s1OmegaAngle = options.s1OmegaAngle

trajectory_len = len(np.loadtxt(s1OmegaAngle, comments=["#", "@"]))

if not os.path.exists(projectionFile):
    sys.exit("\nNo projection input!!!\nExiting\n")

if os.path.exists(dir_name):
    dir = os.listdir(dir_name)

    # Checking if the list is empty or not
    if len(dir) != 0:
        signal = input("\nThe analysis has been performed.\n" \
                        + "Enter 1 to cotinue and other keys to exit.\n" \
                        + "(!!!Note: Files Might Be Overwritten!!!)\n")
        if int(signal) != 1:
            sys.exit("\nConflict of directory name!!!\nExiting...\n")
    shutil.rmtree(dir_name)

os.makedirs(dir_name)

s1_dir = dir_name + "/s1"
s2_dir = dir_name + "/s2"

os.makedirs(s1_dir)
os.makedirs(s2_dir)

if time_procedure:
    start = time.perf_counter()

projection = np.loadtxt(projectionFile)

h1, h2 = create_histogram(projection[:trajectory_len], projection[trajectory_len:])
s1_density, s1_density_clean = combine_density_coor(h1, 0.1000)
s2_density, s2_density_clean = combine_density_coor(h2, 0.1000)

np.savetxt(s1_dir + "density.txt", s1_density, fmt = "%10.5f")
os.system("gnuplot -e \"TITLE=\'%s\'; INPUT=\'%s/density.txt\'\" plot.gplt" % (s1_dir, file_prefix))
os.system("convert -density 300 %s/tmp.eps %s/density.png" % (s1_dir, s1_dir))
np.savetxt(s2_dir + "density.txt", s2_density, fmt = "%10.5f")
os.system("gnuplot -e \"TITLE=\'%s\'; INPUT=\'%s/density.txt\'\" plot.gplt" % (s2_dir, file_prefix))
os.system("convert -density 300 %s/tmp.eps %s/density.png" % (s2_dir, s2_dir))

print("Performing cluster analysis...")
projection_cluster_assignment1 = get_cluster_assignment(s1_density_clean, projection[:trajectory_len], "s1_decision_graph.png", interactive, s1_dir)
projection_cluster_assignment2 = get_cluster_assignment(s2_density_clean, projection[trajectory_len:], "s2_decision_graph.png", interactive, s2_dir)

print("Writing cluster assignment...")
np.savetxt(s1_dir + "/s1_assignment.txt", projection_cluster_assignment1, fmt = "%d")
np.savetxt(s2_dir + "/s2_assignment.txt", projection_cluster_assignment2, fmt = "%d")

write_cluster_ndx(s1_dir + "/s1_cluster.ndx", projection_cluster_assignment1)
write_cluster_ndx(s2_dir + "/s2_cluster.ndx", projection_cluster_assignment2)

projection1_clean = projection[:trajectory_len][np.argwhere(projection_cluster_assignment1 != 0).flatten()]
projection2_clean = projection[trajectory_len:][np.argwhere(projection_cluster_assignment2 != 0).flatten()]

print("Calculating NIP scores...")
h1_clean, h2_clean = create_histogram(projection1_clean, projection2_clean)
NIP_clean = calc_NIP(h1_clean, h2_clean)
NIP_ttl = calc_NIP(h1, h2)

with open("%s/NIP.txt" % s1_dir, "w+") as fi:
    fi.write(str(NIP_ttl[0]))
    fi.write("\n")
    fi.write(str(NIP_clean[0]))

with open("%s/NIP.txt" % s2_dir, "w+") as fi:
    fi.write(str(NIP_ttl[1]))
    fi.write("\n")
    fi.write(str(NIP_clean[1]))

print("Calculating population...")
s1_population = calculate_population(projection_cluster_assignment1)
s2_population = calculate_population(projection_cluster_assignment2)

for i in range(5):
    with open("%s/cluster%d.txt" % (s1_dir, (i + 1)), "w+") as fi:
        fi.write(str(s1_population[i]))
        fi.write("\n")

for pop in s1_population:
    with open("%s/population_total.txt" % (s1_dir), "w+") as fi:
        fi.write("%.5f\n" % pop)

for i in range(5):
    with open("%s/cluster%d.txt" % (s2_dir, (i + 1)), "w+") as fi:
        fi.write(str(s2_population[i]))
        fi.write("\n")

for pop in s2_population:
    with open("%s/population_total.txt" % (s2_dir), "w+") as fi:
        fi.write("%.5f\n" % pop)

if time_procedure:
    end = time.perf_counter()
    print("=" * 80)
    print(f"This analysis procedure finishes in {end - start:0.4f} seconds")

if debug:
    np.savetxt("s1_density.txt", s1_density, fmt="%10.5f")
    np.savetxt("s2_density.txt", s2_density, fmt="%10.5f")
    np.savetxt("s1_density_kept.txt", s1_density_clean, fmt="%10.5f")
    np.savetxt("s2_density_kept.txt", s2_density_clean, fmt="%10.5f")

    s1_distance_mtx = calculate_distance_matrix(s1_density_clean)
    s2_distance_mtx = calculate_distance_matrix(s2_density_clean)
    np.savetxt("s1_distance.dmtx", s1_distance_mtx, fmt="%5d%5d%10.5f%10.5f%10.5f")
    np.savetxt("s2_distance.dmtx", s2_distance_mtx, fmt="%10.5f")
print("\nDone...")
