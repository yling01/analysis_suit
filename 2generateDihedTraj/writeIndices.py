import optparse
def getPhiPsi(pdb_file):
    fi = open(pdb_file)
    index = [] #index will be C, N, CA, C, N
    for line in fi:
        if len(line) < 20:
            continue
        line = line.split()
        if line[1] in ["C", "N", "CA"]:
            index.append(line[2])
    fi.close()
    index.insert(0, index[-1])
    index.append(index[1])
    with open("PhiPsi.ndx", "w+") as fo:
        fo.write("[ PhiPsi ]\n")
        counter = 0
        for i in range(len(index) - 3):
            counter += 1
            if not counter % 3:
                continue
            fo.write(" ".join(index[i:i + 4]))
            fo.write("\n")

def getOmega(pdb_file):
    fi = open(pdb_file)
    index = [] #index will be CA, C, N, CA
    for line in fi:
        if len(line) < 20:
            continue
        line = line.split()
        if line[1] in ["C", "N", "CA"]:
            index.append(line[2])
    fi.close()
    i = index.pop(0)
    index.append(i)
    index.append(index[0])
    with open("Omega.ndx", "w+") as fo:
        fo.write("[ Omega ]\n")
        for i in range(0, len(index), 3):
            if i + 4 > len(index):
                break
            fo.write(" ".join(index[i:i+4]))
            fo.write("\n")

def getArgument(arg):
    if arg[0].upper() == "T":
        return True
    return False

if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option('--PhiPsi', dest = 'PhiPsi',
                      default = "False")
    parser.add_option('--Omega', dest = 'Omega',
                      default = "False")
    parser.add_option('--gro', dest = 'gro',
                      default = '')
    (options, args) = parser.parse_args()
    gro = options.gro
    PhiPsi = getArgument(options.PhiPsi)
    Omega = getArgument(options.Omega)

    while not(gro):
        gro = input("Enter the name of the gro file:\n")
    if PhiPsi:
        getPhiPsi(gro)
    if Omega:
        getOmega(gro)
