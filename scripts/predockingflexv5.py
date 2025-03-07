#current file input is first line of new file = @<TRIPOS>MOLECULE and out file name is second line
#python predockingflexv5.py  
# call in directory with many concatenated .mol2 files for processing


import os
import sys, glob
import shlex, subprocess

##############path to programs and project directory
pythonsh = '/home/sel228/shared/docking/scripts/mgltools_x86_64Linux2_1.5.6/bin/pythonsh'
prepLigand = '/home/sel228/shared/docking/scripts/mgltools_x86_64Linux2_1.5.6/MGLToolsPckgs/AutoDockTools/Utilities24/prepare_ligand5.py'

l=glob.glob('*.mol2')
os.system('mkdir splits')


molfile_list={}

for f in l:

  #split files
  file1=open(f, 'r')
  file2=open('splits/test.txt', 'w')
  file2.close()
  i=0
  for line in file1:
    if(i==1):
      if '*' in line:
        out_file='star.mol2'
      else:
        out_file=line.strip() + '.mol2'
      if(out_file not in molfile_list):
        molfile_list[out_file]=1
        ofile=out_file
      else:
        molfile_list[out_file]=molfile_list[out_file]+1
        ofile=out_file[0:-5]+'_'+str(molfile_list[out_file])+'.mol2'
        molfile_list[ofile]=1
      file2=open('splits/'+ofile, 'w')
      file2.write('@<TRIPOS>MOLECULE\n')
    if(line.strip()=='@<TRIPOS>MOLECULE'):
      i=0
      file2.close()
    if(i > 0):
      file2.write(line)   
    i=i+1
  file1.close()
  file2.close()

print(molfile_list)
os.system('mkdir pdbqt')

#create pdbqt files
for molfile in molfile_list:
  pdbqtfile=molfile[:-4]+'pdbqt'
  file3=open('ligands.txt', 'a')
  file3.write(molfile[0:-5]+'\t')
  file3.close()
  #print pdbqtfile
  p=subprocess.Popen(pythonsh + ' ' + prepLigand + ' -l splits/' + molfile + ' -o pdbqt/' +pdbqtfile, shell=True)
  sts=os.waitpid(p.pid, 0)[1]
  #remove mol2 file
  os.system('rm splits/' +molfile)

os.system('rm splits/test.txt')

# Create ligand_sort.txt
f4=open('ligands.txt', 'r')
tdof={}
for line in f4:
        linesplit = line.split()
        dof_i = int(linesplit[2])
        if dof_i in tdof:
                tdof[dof_i].append([int(linesplit[1]),linesplit[0]])
        else:
                tdof[dof_i] = []
                tdof[dof_i].append([int(linesplit[1]),linesplit[0]])
f4.close()
tdof_list = list(tdof.keys())
tdof_list.sort()
tdof_list.reverse()

f5=open('ligands_sort.txt', 'w')
for this_dof in tdof_list:
        #print this_dof
        #print tdof[this_dof]
        tdof[this_dof].sort()
        tdof[this_dof].reverse()
        for lig in tdof[this_dof]:
                #print lig
                f5.write(lig[1]+' '+str(this_dof)+'\n')
