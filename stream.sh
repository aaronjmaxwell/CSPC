#!/bin/bash
file=daily_tweet_activity_metrics_sciencepolicy_20201121_20201127_en.csv 

echo "hashtag"
python3 code/hashtag.py
awk '{a[i++]=$0} END {for (j=i-1; j>=0;) print a[j--] }' stream.out | sed 's/\//,/g' | sed 's/:/,/g' | sed 's/ /,/g' > streamed.out
python3 code/cleaner.py hashtag streamed.out

echo "activity"
python3 code/cleaner.py activity $file

#echo "promotion"
#python3 code/promotion.py
#awk '{a[i++]=$0} END {for (j=i-1; j>=0;) print a[j--] }' panelstream.out | sed 's/\//,/g' | sed     's/:/,/g' | sed 's/ /,/g' | sed "s/(/'(/g" | sed "s/,)/)/g" | sed "s/)/)'/g" >> data/promotion.csv

#echo "SciParl"
#python3 code/sciparl.py
#awk '{a[i++]=$0} END {for (j=i-1; j>=0;) print a[j--] }' smpstream.out | sed 's/\//,/g' | sed     's/:/,/g' | sed 's/ /,/g' | sed "s/(/'(/g" | sed "s/,)/)/g" | sed "s/)/)'/g" >> data/sciparl.csv

#echo "covid"
#python3 code/covid.py
#awk '{a[i++]=$0} END {for (j=i-1; j>=0;) print a[j--] }' covidstream.out | sed 's/\//,/g' | sed 's/:/,/g' | sed 's/ /,/g' >> data/covid.csv

rm -fv *.out $file
#python3 code/plot_hashtag.py
#python3 code/plot_activity.py
#python3 code/mentions.py
#python3 code/communicators.py
