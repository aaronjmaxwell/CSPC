#!/bin/bash
file=tweet_activity_metrics_sciencepolicy_20180418_20180425_en.csv

python3 hashtag.py
awk '{a[i++]=$0} END {for (j=i-1; j>=0;) print a[j--] }' stream.out | sed 's/\//,/g' | sed 's/:/,/g' | sed 's/ /,/g' >> hashtag.csv

#python3 promotion.py
#awk '{a[i++]=$0} END {for (j=i-1; j>=0;) print a[j--] }' panelstream.out | sed 's/\//,/g' | sed     's/:/,/g' | sed 's/ /,/g' | sed "s/(/'(/g" | sed "s/,)/)/g" | sed "s/)/)'/g" >> promotion.csv

python3 cleaner.py $file
awk '{a[i++]=$0} END {for (j=i-1; j>=0;) print a[j--] }' activity.out >> activity.csv

rm -fv *.out $file
python3 plot_hashtag.py
python3 plot_activity.py
#python3 mentions.py
