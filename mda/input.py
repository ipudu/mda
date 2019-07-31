import yaml
import json

from pathlib import Path

# VMD supported file formats
# http://www.ks.uiuc.edu/Research/vmd/plugins/molfile/

vmd_topo = [
    "parm",
    "prmtop",
    "parm7",
    "rst7",
    "bgf",
    "car",
    "crd",
    "psf",
    "log",
    "gro",
    "g96",
    "h5",
    "namdbin",
    "mdf",
    "nc",
    "molden",
    "pdb",
    "pqr",
    "mol2",
    "arc",
    "POSCAR",
    "CONTCAR",
    "xbgf",
    "vsf",
    "vcf",
    "axsf",
    "xsf",
    "xyz",
]

vmd_traj = [
    "binpos",
    "crd",
    "crdbox",
    "nc",
    "dcd",
    "cpmd",
    "dlpolyhist",
    "trr",
    "xtc",
    "tng",
    "h5",
    "lammpstrj",
    "nc",
    "xml",
    "OUTCAR",
    "XCATCAR",
    "vtf",
    "axsf",
    "xsf",
    "xyz",
    "netcdf",
]

single = ["xyz", "pdb", "mol2"]

# VMD analysis
# http://www-s.ks.uiuc.edu/Research/vmd/vmd-1.9.1/ug/node136.html
# the last one, tcl is magic

vmd_measure = [
    "avpos",
    "center",
    "cluster",
    "contacts",
    "dc",
    "dipole",
    "fit",
    "gofr",
    "hbonds",
    "inverse",
    "minmax",
    "rg",
    "rmsd",
    "rmsf",
    "sasa",
    "sumweights",
    "bond",
    "angle",
    "dihed",
    "imprp",
    "energy",
    "surface",
    "pbc2onc",
    "pbcneighbors",
    "inertia",
    "symmetry",
    "tcl",
]

cpptraj = ["dc"]

other = ["gt", "order"]


class Parser:
    def __init__(self, infile):
        """Read input file and do some checks
        
        Arguments:
            infile {string} -- input file of mda
        """
        self.outfile = Path(infile).stem
        stream = open(infile, "r")
        self.data = yaml.load(stream, Loader=yaml.FullLoader)
        self.check()
        self.output()

    def check(self):
        """check the input file
        """

        self.single = None
        self.vmd = {}
        self.cpptraj = {}
        self.other = {}

        # check if it's only single traj without topo
        for i in self.data:
            if i in single:
                self.single = self.data[i]

        if "measure" not in self.data:
            raise Exception("No calculation specified!")

        # check if using vmd as backend
        for m in self.data["measure"]:
            for j in vmd_measure:
                if m.startswith(j):
                    if j in self.vmd:
                        self.vmd[j].append(m)
                    else:
                        self.vmd[j] = [m]

        # check if using CPPTRAJ as backend
        for m in self.data["measure"]:
            for j in cpptraj:
                if m.startswith(j):
                    if j in self.cpptraj:
                        self.cpptraj[j].append(m)
                    else:
                        self.cpptraj[j] = [m]

        # check if using MDAnalysis as backend
        for m in self.data["measure"]:
            for j in other:
                if m.startswith(j):
                    if j in self.other:
                        self.other[j].append(m)
                    else:
                        self.other[j] = [m]

        if self.single is None:
            if "topo" not in self.data:
                raise Exception("No topology file specified!")
            if "traj" not in self.data:
                raise Exception("No trajectory file specified!")

        # TODO: fully check the input file

    def output(self):
        """Print out the structure of input file
        """
        print(json.dumps(self.data, indent=4))
