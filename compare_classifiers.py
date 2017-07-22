"""
PURPOSE:
Given a set of _scores.txt results files, output a list of which instances were classified 
correctly and which incorrectly and summarize with a table of overlaps

Must set path to Miniconda in HPC:  export PATH=/mnt/home/azodichr/miniconda3/bin:$PATH


INPUT:
  -scores      Comma separated list of scores files
  -ids         Comma separated list of what to call each file (same order as scores)
  -save        Save name

OPTIONAL INPUT:
  -pos          String of positive class (Default = 1)
  -neg          String of negative class (Default = 0)
  -plot         T/F Make venn diagram in python (Default = T)

OUTPUT:
  -save_instances.txt       Lists of instances correctly vs. incorrectly classified
  -save_ovlp_matrix.txt  Matrix with counts for overlaps between _scores files


AUTHOR: Christina Azodi

REVISIONS:   Submitted 7/12/2017

python ~/GitHub/ML-Pipeline/compare_classifiers.py -scores NNU_Ras_FET01_df_p0.01.txt_onlyARs_sup0.2_conf0.2_lift_RF_scores.txt,NNU_Ras_FET01_df_p0.01.txt_plusARs_sup0.2_conf0.2_lift_RF_scores.txt -ids aRules,Both

"""
import pandas as pd
import numpy as np
from collections import defaultdict
import sys, os
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import venn

pos, neg, save, plot = '1', '0', 'compare_clf', 'T'

for i in range (1,len(sys.argv),2):
  if sys.argv[i] == "-scores":
    SCORES = sys.argv[i+1]
  if sys.argv[i] == "-ids":
    IDS = sys.argv[i+1]
  if sys.argv[i] == '-save':
    save = sys.argv[i+1]
  if sys.argv[i] == '-p':
    pos = sys.argv[i+1]
  if sys.argv[i] == '-n':
    neg = sys.argv[i+1]
if len(sys.argv) <= 1:
  print(__doc__)
  exit()

scores_files = SCORES.strip().split(',')
n_comparing = len(scores_files)
ids = IDS.strip().split(',')

tp = defaultdict(list)
fn = defaultdict(list)

count = 0
tp_total = 0
for scores_file in scores_files:
  with open(scores_file) as f:
      name = ids[count]
      for l in f:
          line = l.strip().split('\t')
          gene, true, pred = line[0], line[1], line[5]
          if true == pos:
            if count == 0:
              tp_total += 1     # Add to the count of total number of true positives in the dataframe
            if pred == pos:
              tp[name].append(gene)
            else:
              fn[name].append(gene)
      count += 1


out1 = open(save+'_pred_compared.txt', 'w')
out1.write('%s\n## True positives and true negatives predicted by each model:\n' % (save))
for i in tp:
  out1.write('%s\tTP\t%s\n' % (i, ','.join(str(x) for x in tp[i])))
  out1.write('%s\tFN\t%s\n' % (i, ','.join(str(x) for x in fn[i])))

out1.write('\n\n## Overlap matrix. Positives in dataset = %i\n\n' % (tp_total))

df = pd.DataFrame(0, index=ids, columns=ids)

# Make a table of overlaps
ids2 = ids[:]
for A in ids:
  for B in ids2:
    if A == B:
      df[A][B] = len(tp[A])
    else:
      df[A][B] = len(list(set(tp[A]).intersection(tp[B])))
  ids2.remove(A)
print(df)

df.to_csv(out1)


### Output a list of overlaps for making a venn diagram in R "VennDiagram"
def intersection(*listas):
  return set(listas[0]).intersection(*listas[1:])

if n_comparing == 2:
  n12 = len(intersection(tp[ids[0]], tp[ids[1]])) 
  area2 = len(tp[ids[1]]) 
  area1 = len(tp[ids[0]])  
  venn_diag_list = [area1, area2, n12]

if n_comparing == 3:
  n123 = len(intersection(tp[ids[0]], tp[ids[1]], tp[ids[2]]))
  n12 = len(intersection(tp[ids[0]], tp[ids[1]]))
  n13 = len(intersection(tp[ids[0]], tp[ids[2]])) 
  n23 = len(intersection(tp[ids[1]], tp[ids[2]]))  
  area3 = len(tp[ids[2]]) 
  area2 = len(tp[ids[1]]) 
  area1 = len(tp[ids[0]])  
  venn_diag_list = [area1, area2, area3, n12, n13, n23, n123]


if n_comparing == 4:
  n1234 = len(intersection(tp[ids[0]], tp[ids[1]], tp[ids[2]], tp[ids[3]]))
  n234 = len(intersection(tp[ids[1]], tp[ids[2]], tp[ids[3]]))
  n134 = len(intersection(tp[ids[0]], tp[ids[2]], tp[ids[3]]))
  n124 = len(intersection(tp[ids[0]], tp[ids[1]], tp[ids[3]]))
  n123 = len(intersection(tp[ids[0]], tp[ids[1]], tp[ids[2]]))
  n12 = len(intersection(tp[ids[0]], tp[ids[1]]))
  n13 = len(intersection(tp[ids[0]], tp[ids[2]])) 
  n14 = len(intersection(tp[ids[0]], tp[ids[3]])) 
  n23 = len(intersection(tp[ids[1]], tp[ids[2]])) 
  n24 = len(intersection(tp[ids[1]], tp[ids[3]])) 
  n34 = len(intersection(tp[ids[2]], tp[ids[3]])) 
  area4 = len(tp[ids[3]])
  area3 = len(tp[ids[2]]) 
  area2 = len(tp[ids[1]]) 
  area1 = len(tp[ids[0]])  
  venn_diag_list = [area1, area2, area3, area4, n12, n13, n14, n23, n24, n34, n123, n124, n134, n234, n1234]

if n_comparing == 5:
  n12345 = len(intersection(tp[ids[0]], tp[ids[1]], tp[ids[2]], tp[ids[3]], tp[ids[4]]))
  n2345 = len(intersection(tp[ids[1]], tp[ids[2]], tp[ids[3]], tp[ids[4]]))
  n1345 = len(intersection(tp[ids[0]], tp[ids[2]], tp[ids[3]], tp[ids[4]]))
  n1245 = len(intersection(tp[ids[0]], tp[ids[1]], tp[ids[3]], tp[ids[4]]))
  n1235 = len(intersection(tp[ids[0]], tp[ids[1]], tp[ids[2]], tp[ids[4]]))
  n1234 = len(intersection(tp[ids[0]], tp[ids[1]], tp[ids[2]], tp[ids[3]]))
  n345 = len(intersection(tp[ids[2]], tp[ids[3]], tp[ids[4]]))
  n245 = len(intersection(tp[ids[1]], tp[ids[3]], tp[ids[4]]))
  n235 = len(intersection(tp[ids[1]], tp[ids[2]], tp[ids[4]]))
  n234 = len(intersection(tp[ids[1]], tp[ids[2]], tp[ids[3]]))
  n145 = len(intersection(tp[ids[0]], tp[ids[3]], tp[ids[4]]))
  n135 = len(intersection(tp[ids[0]], tp[ids[2]], tp[ids[4]]))
  n134 = len(intersection(tp[ids[0]], tp[ids[2]], tp[ids[3]]))
  n125 = len(intersection(tp[ids[0]], tp[ids[1]], tp[ids[4]]))
  n124 = len(intersection(tp[ids[0]], tp[ids[1]], tp[ids[3]]))
  n123 = len(intersection(tp[ids[0]], tp[ids[1]], tp[ids[2]]))
  n12 = len(intersection(tp[ids[0]], tp[ids[1]]))
  n13 = len(intersection(tp[ids[0]], tp[ids[2]])) 
  n14 = len(intersection(tp[ids[0]], tp[ids[3]])) 
  n15 = len(intersection(tp[ids[0]], tp[ids[4]])) 
  n23 = len(intersection(tp[ids[1]], tp[ids[2]])) 
  n24 = len(intersection(tp[ids[1]], tp[ids[3]])) 
  n25 = len(intersection(tp[ids[1]], tp[ids[4]])) 
  n34 = len(intersection(tp[ids[2]], tp[ids[3]])) 
  n35 = len(intersection(tp[ids[2]], tp[ids[4]]))
  n45 = len(intersection(tp[ids[3]], tp[ids[4]])) 
  area5 = len(tp[ids[4]]) 
  area4 = len(tp[ids[3]])
  area3 = len(tp[ids[2]]) 
  area2 = len(tp[ids[1]]) 
  area1 = len(tp[ids[0]])  
  venn_diag_list = [area1, area2, area3, area4, area5, n12, n13, n14, n15,n23, n24, n25,
   n34, n35, n45, n123, n124, n125, n134, n135, n145, n234, n235, n245, n345, n1234, 
   n1235, n1245, n1345, n2345, n12345]

print('Overlap list needed for VennDiagram in R')
print(venn_diag_list)
out1.write('\n\n## Overlap list needed for VennDiagram in R:\n\n%s' % venn_diag_list)

if plot.lower() == 't' or plot.lower() == 'true':
  if n_comparing == 5:
    labels = venn.get_labels([tp[ids[0]], tp[ids[1]], tp[ids[2]], tp[ids[3]], tp[ids[4]]], fill = ['number'])
    fig, ax = venn.venn5(labels, names = ids)
  elif n_comparing == 4:
    labels = venn.get_labels([tp[ids[0]], tp[ids[1]], tp[ids[2]], tp[ids[3]]], fill = ['number'])
    fig, ax = venn.venn4(labels, names = ids)
  elif n_comparing == 3:
    labels = venn.get_labels([tp[ids[0]], tp[ids[1]], tp[ids[2]]], fill = ['number'])
    fig, ax = venn.venn3(labels, names = ids)
  elif n_comparing == 2:
    labels = venn.get_labels([tp[ids[0]], tp[ids[1]]], fill = ['number'])
    fig, ax = venn.venn2(labels, names = ids)
  filename = save+'_pred_compared.png'
  fig.savefig(filename)