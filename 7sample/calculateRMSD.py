import MDAnalysis as mda
import numpy as np
import MDAnalysis.analysis.rms
import optparse

if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("--ref", dest = "ref")
    parser.add_option("--trajectory", dest = "trajectory")
    parser.add_option("--output", dest = "output")

    (options, args) = parser.parse_args()

    ref = options.ref
    trajectory = options.trajectory
    output = options.output

    u_ref = mda.Universe(ref)
    u_trajectory = mda.Universe(trajectory)

    hl_length = len(u_ref.residues)

    atomGrpRef = u_ref.select_atoms("backbone and not name O")
    atomGrpTrj = u_trajectory.select_atoms("backbone and not name O and resid 1:%d" % hl_length)

    rmsd_value = MDAnalysis.analysis.rms.RMSD(atomGrpTrj, atomGrpRef).run().rmsd[:,2]

    with open(output, "w+") as fo:
        fo.write("%.3f\n%.3f" % (np.average(rmsd_value), np.std(rmsd_value)))
