python3 hashtag.py
awk '{a[i++]=$0} END {for (j=i-1; j>=0;) print a[j--] }' stream.out | sed 's/\//,/g' | sed 's/:/,/g' | sed 's/ /,/g' >> hashtag.csv

#python3 promotion.py
#awk '{a[i++]=$0} END {for (j=i-1; j>=0;) print a[j--] }' panelstream.out | sed 's/\//,/g' | sed     's/:/,/g' | sed 's/ /,/g' | sed "s/(/'(/g" | sed "s/,)/)/g" | sed "s/)/)'/g" >> promotion.csv

rm -fv *.out
#python3 plot_hashtag.py
#python3 mentions.py
