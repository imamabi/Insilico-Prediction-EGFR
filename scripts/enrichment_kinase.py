#call from directory containing sorted_results
#creates text document of enrichment chart
#USAGE: python enrichment_kinase.py

import sys
import glob

#loop through files in the directory
files_names = glob.glob('*_sorted_results*')

for filename in files_names:
  prefix = filename[:-15]
  f=open(filename, 'r')

  elist=[]
  lcount=0
  tcount=0

  first=1

  for line in f:
    if first == 0:
      linesplit=line.split()
      lig_name=linesplit[2]
      if 'DB' in lig_name[-14:]:
        lcount=lcount+1
        elist.append(1)
        tcount=tcount+1
      else:
        elist.append(0)
        tcount=tcount+1

    else:
      first = 0

  f.close()

  current_lcount=0
  current_tcount=0

  f2=open(f'{prefix}_enrichment.txt', 'w')

  for e in elist:
    current_lcount = current_lcount + e
    current_tcount = current_tcount + 1

    percentl = float(current_lcount) / lcount * 100
    percentt = float(current_tcount) / tcount * 100

    f2.write(str(percentt)+'\t'+str(percentl)+'\n')

  f2.close()
