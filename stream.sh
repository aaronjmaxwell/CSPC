#!/bin/bash
file=tweet_activity_metrics_sciencepolicy_20190215_20190301_en.csv

echo "hashtag"
python3 code/hashtag.py
awk '{a[i++]=$0} END {for (j=i-1; j>=0;) print a[j--] }' stream.out | sed 's/\//,/g' | sed 's/:/,/g' | sed 's/ /,/g' >> data/hashtag.csv

#echo "promotion"
#python3 code/promotion.py
#awk '{a[i++]=$0} END {for (j=i-1; j>=0;) print a[j--] }' panelstream.out | sed 's/\//,/g' | sed     's/:/,/g' | sed 's/ /,/g' | sed "s/(/'(/g" | sed "s/,)/)/g" | sed "s/)/)'/g" >> data/promotion.csv

#echo "SciParl"
#python3 code/sciparl.py
#awk '{a[i++]=$0} END {for (j=i-1; j>=0;) print a[j--] }' smpstream.out | sed 's/\//,/g' | sed     's/:/,/g' | sed 's/ /,/g' | sed "s/(/'(/g" | sed "s/,)/)/g" | sed "s/)/)'/g" >> data/sciparl.csv

python3 code/cleaner.py $file
awk '{a[i++]=$0} END {for (j=i-1; j>=0;) print a[j--] }' activity.out >> data/activity.csv

rm -fv *.out $file
python3 code/plot_hashtag.py
#python3 code/plot_activity.py
#python3 code/mentions.py
#python3 code/communicators.py
