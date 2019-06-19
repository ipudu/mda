import yaml


# VMD supported file formats
# http://www.ks.uiuc.edu/Research/vmd/plugins/molfile/

vmd_topo = ['parm', 'prmtop', 'parm7', 'rst7',
            'bgf', 'car', 'crd', 'psf', 'log', 
            'gro', 'g96', 'h5', 'namdbin', 'mdf',
            'nc', 'molden', 'pdb', 'pqr', 'mol2',
            'arc', 'POSCAR', 'CONTCAR', 'xbgf', 'vsf',
            'vcf', 'axsf', 'xsf', 'xyz']

vmd_traj = ['binpos', 'crd', 'crdbox', 'nc', 'dcd',
            'cpmd', 'dlpolyhist', 'trr', 'xtc', 'tng',
            'h5', 'lammpstrj', 'nc', 'xml', 'OUTCAR',
            'XCATCAR', 'vtf', 'axsf', 'xsf', 'xyz']

class Parser:

    def __init__(self, infile):
        """read input file and do some checks
        
        Arguments:
            infile {yaml} -- [input file of mda]
        """
        stream = open(infile, 'r')
        self.data = yaml.load(stream, Loader=yaml.FullLoader)
        self.check()
    
    def check(self):
        """check the input file
        """
        if 'topo' not in self.data:
            raise Exception("No topology file specified!")
        if 'traj' not in self.data:
            raise Exception("No trajectory file specified!")

        # TODO: fully check the input file

if __name__ == '__main__':
    Parser('input.yaml')