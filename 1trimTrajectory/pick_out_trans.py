import numpy as np

outfile = open("frame.ndx", "w")
outfile.write("[ frame ]\n")

dihedral = np.loadtxt("out.xvg", comments = ["#", "@"], usecols = range(2,10))
counter = 0
for frame_index in range(0,len(dihedral)):
	counter += 1
	has_cis = False
	for dihedral_index in range(0, 8):
		if abs(float(dihedral[frame_index][dihedral_index])) < 90:
			has_cis = True
	if has_cis:
		pass
	else:
		outfile.write(str(counter) + "\n")

outfile.close()


