import os
import textwrap
import MDAnalysis
import numpy as np

from numpy import linalg as LA
from mda.input import Parser
from datetime import datetime


class Measure:

    def __init__(self, parser):

        self.inp = parser.data
        self.vmd = parser.vmd
        self.other = parser.other
        self.single = parser.single
        self.outfile = parser.outfile

        self.run()

    def load(self, topo, traj):
        self.u = MDAnalysis.Universe(topo, traj)
    
    def load_single(self, single):
        self.u = MDAnalysis.Universe(single)

    def vmd_load(self, topo, topo_t, traj, traj_t):
        """Load topology and trajectory
        
        Arguments:
            topo {string} -- topology file
            topo_t {string} -- topology file type
            traj {string} -- trajectory file
            traj_t {string} -- trajectory file type
        
        Returns:
            string -- tcl code to load topo and traj
        """

        if topo_t.lower() == 'lammpsdata':
            # note: using the default sytle (full)
            tcl = textwrap.dedent(
                    """
                    # load topology and trajectory
                    topo readlammpsdata {0}
                    mol addfile {1} type {2} waitfor all
                    """).format(topo, traj, traj_t)
        else:
            tcl = textwrap.dedent(
                    """
                    # load topology and trajectory
                    mol new {0} type {1} waitfor all
                    mol addfile {2} type {3} waitfor all
                    """).format(topo, topo_t, traj, traj_t)
        
        return tcl

    def vmd_load_single(self, single):
        """Load single file
        
        Arguments:
            single {string} -- single file
        
        Returns:
            string -- tcl code to load single file
        """

        tcl = textwrap.dedent(
                """
                # load single
                mol new {0} waitfor all
                """).format(single)

        return tcl
 
    def rg(self, sel, weight='mass'):
        """Radius of Gyration

        rg = sqrt(sum (mass(n) ( r(n) - r(com) )^2)/sum(mass(n)))
        
        Arguments:
            sel {string} -- atom selection
        
        Keyword Arguments:
            weight {string} -- weighting factor (default: {'mass'})
        
        Returns:
            string -- tcl code to measure Rg
        """

        outfile, time = self.outfile_and_time(self.rg, sel)
        
        tcl = textwrap.dedent(
            """
            #..........................................................
            # Raidus of Gyration script generated by mda
            #..........................................................
        
            # set output file
            set outfile [open {0} w]
            puts $outfile "{3}"
        
            # select molecules
            set sel [atomselect top "{1}"]

            # loop over frames
            set nf [molinfo top get numframes]

            for {{set i 0}} {{$i < $nf}} {{incr i}} {{
                puts "frame $i of $nf"
                $sel frame $i
                
                set rg [measure rgyr $sel weight {2}]
                puts $outfile "$rg"
                
            }}

            close $outfile
            """
        ).format(outfile, sel, weight, time)

        return tcl
    

    def gofr(self, sel1, sel2, delta=0.1, rmax=10.0,
             usepbc=True, selupdate=False, first=0, last=-1, step=1):
        """Radius distribution function
        
        Arguments:
            sel1 {string} -- center
            sel2 {string} -- surrounding
        
        Keyword Arguments:
            delta {float} --  bin size (default: {0.1})
            rmax {float} -- maximum r  (default: {10.0})
            usepbc {bool} -- periodic boundary condition (default: {True})
            selupdate {bool} -- update selections (default: {False})
            first {int} -- first frame (default: {0})
            last {int} -- last frame (default: {-1})
            step {int} -- step (default: {1})
        
        Returns:
            string -- tcl code to measure gofr
        """

        outfile, time = self.outfile_and_time(self.gofr, sel1+' '+sel2)
        
        tcl = textwrap.dedent(
            """
            #..........................................................
            # gofr script generated by mda
            #..........................................................

            # set output file
            set outfile [open {0} w]
            puts $outfile "{10}"
            
            # select center and surrounding
            set sel1 [atomselect top {1}]
            set sel2 [atomselect top {2}]

            set gr [measure gofr $sel1 $sel2 delta {3} rmax {4} \\
                    usepbc {5} selupdate {6} first {7} last {8} step {9}]
            
            set r [lindex $gr 0]
            set gr2 [lindex $gr 1]
            set igr [lindex $gr 2]
            foreach j $r k $gr2 l $igr {{
                puts $outfile "$j $k $l"
            }}
            close $outfile         
            """
        ).format(outfile, sel1, sel2, delta, rmax,
                 usepbc, selupdate, first, last, step, time)
        
        return tcl

    def sasa(self, sel, srad=1.4):
        """Solvent accessible surface area
        
        Arguments:
            sel {string} -- atom selection
        
        Keyword Arguments:
            srad {float} -- probing solvent (default: {1.4})
        
        Returns:
            string -- tcl code to measure sasa
        """

        outfile, time = self.outfile_and_time(self.sasa, sel)                                 

        tcl = textwrap.dedent(
            """
            #..........................................................
            # sasa script generated by mda
            #..........................................................
            
            # set output file
            set outfile [open {0} w]
            puts $outfile "{3}"
            
            # select molecules
            set sel [atomselect top {1}]

            # loop over frames
            set nf [molinfo top get numframes]

            for {{set i 0}} {{$i < $nf}} {{incr i}} {{
                puts "frame $i of $nf"
                $sel frame $i
                
                set sasa [measure sasa {2} $sel]
                puts $outfile "$sasa"
                
            }}

            close $outfile     
            """
        ).format(outfile, sel, srad, time)
        
        return tcl
    
    def inertia(self, sel):
        """Inertia Tensor
        
        Arguments:
            sel {string} -- atom selection
        
        Returns:
            string -- tcl code to measure eigen values of IT
        """
        
        outfile, time = self.outfile_and_time(self.inertia, sel)

        tcl = textwrap.dedent(
            """
            #..........................................................
            # inertia script generated by mda
            #..........................................................
            
            # set output file
            set outfile [open {0} w]
            puts $outfile "# lambda1 lambda2 lambda3\\
                           acylindricity asphericity"
            puts $outfile "# acyindricity = (l2 - l3)/(l1 + l2 + l3)"
            puts $outfile "# asphericity = (l1 - 0.5(l2 + l3))/(l1 + l2 + l3)"

            puts $outfile "{2}"
            
            # select molecules
            set sel [atomselect top {1}]

            # loop over frames
            set nf [molinfo top get numframes]

            for {{set i 0}} {{$i < $nf}} {{incr i}} {{
                puts "frame $i of $nf"
                $sel frame $i
                
                set inertia [measure inertia $sel eigenvals]
                #set com [lindex $inertia 0]
                #set moment [lindex $inertia 1]
                set eigen [lindex $inertia 2]
                
                set l1 [lindex $eigen 0]
                set l2 [lindex $eigen 1]
                set l3 [lindex $eigen 2]

                set cs [expr ($l2-$l3)/($l1+$l2+$l3)]
                set s [expr ($l1-($l2+$l3)/2)/($l1+$l2+$l3)]
                puts $outfile "$eigen $cs $s"
                
            }}

            close $outfile     
            """
        ).format(outfile, sel, time)

        return tcl

    def tcl(self, cmd):
        """tcl commands
        
        Arguments:
            cmd {string} -- commands
        
        Returns:
            tcl -- tcl codes
        """
        outfile, time = self.outfile_and_time(self.tcl, 'vmd')

        tcl = textwrap.dedent(
            """
            #..........................................................
            # vmd script generated by mda
            #..........................................................

            """
        )

        tcl += cmd

        return tcl

    def gt(self, sel):
        """Gyration Tensor
        
        Arguments:
            sel {string} -- atom selection
        """

        outfile, time = self.outfile_and_time(self.gt, sel) 
        
        sel = self.u.select_atoms(sel)

        W = []

        for ts in self.u.trajectory:
            diff = sel.positions - sel.center_of_mass()

            tmp1 = np.sum(diff ** 2, axis=0)
            tmp2 = np.sum(diff[:,0] * diff[:,1], axis=0)
            tmp3 = np.sum(diff[:,0] * diff[:,2], axis=0)
            tmp4 = np.sum(diff[:,1] * diff[:,2], axis=0)

            S = 1 / sel.n_atoms * np.array([[tmp1[0], tmp2,    tmp3],
                                            [tmp2,    tmp1[1], tmp4],
                                            [tmp3,    tmp4,    tmp1[2]]])
            
            w, _ = LA.eig(S)
            W.append(np.sort(w)[::-1])

        with open(outfile, 'w') as f:
            f.write('# lambda1 lambda2 lambda3 Rg kappa^2 b\n')
            f.write('# diag(lambda1, lambda2, lambda3) = eigenvalue(S)\n')
            f.write('# lambda1 + lambda2 + lambda3 = Rg^2\n')
            f.write('# kappa^2 = 1 - 3(l1l2 + l2l3 + l3l1)/(l1 + l2 + l3)^2\n')
            f.write('# b = lmabda1 - 0.5(lambda2 + lambda3)\n')
            f.write(time + '\n')
        
            W = np.array(W)

            for w in W:
                Rg = np.sqrt(np.sum(w))
                kappa2 = 1 - 3 *(w[0] * w[1] + w[1] * w[2] + w[2] * w[0]) / \
                         (np.sum(w)) ** 2
                b = b = w[0] - 0.5 * (w[1]+w[2])

                f.write('{} {} {} {} {} {}\n'.format(w[0], w[1], w[2], 
                                                   Rg, kappa2, b))

    def vmd_make_input(self):

        with open('mda.tcl', 'w') as f:
            if self.single is None:

                topo, topo_t, traj, traj_t = \
                self.inp['topo']['path'], self.inp['topo']['type'], \
                self.inp['traj']['path'], self.inp['traj']['type']

                f.write(self.vmd_load(topo, topo_t, traj, traj_t))
            
            else:
                f.write(self.vmd_load_single(self.single))

            
            for k, v in self.vmd.items():
                calculation = getattr(self, k)
                for j in v:
                    f.write(calculation(**self.inp['measure'][j]))

    def outfile_and_time(self, func, sel):
        """Get output file name and time
        
        Arguments:
            func {method} -- method called
        
        Returns:
            string -- outfile and time
        """

        outfile = self.outfile + '_' + func.__name__ + '_' + \
                    '-'.join(sel.split()) + '.dat'
        time = datetime.now().strftime("# %m/%d/%Y, %H:%M:%S")
        
        return outfile, time

    def run(self):

        if self.vmd:
            self.vmd_make_input()
            os.system('vmd -dispdev text < mda.tcl > vmd.log')
        if self.other:
            if self.single:
                self.load_single(self.single)
            else:
                self.load(self.inp['topo']['path'], 
                          self.inp['traj']['path'])

            # run calculations
            for k, v in self.other.items():
                calculation = getattr(self, k)
                for j in v:
                    calculation(**self.inp['measure'][j])


if __name__ == '__main__':
    p = Parser('input.yaml')
    Measure(p)