#!/bin/bash
function wait_n_proc {
    n_proc="$(nproc --all)"
   while [ `jobs | wc -l` -ge $n_proc ]
   do
      sleep 3
   done
}
rm -r data
mkdir -p data
for i in `seq 5 2 99`;do 
	  wait_n_proc; python project.py -b $i -c  > data/data_blockSize_$i.csv &  
done
