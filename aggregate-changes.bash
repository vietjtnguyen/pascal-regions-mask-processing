#!/bin/bash
set=$1
shift
echo "Processing set '$set'..."
rm -r aggregate/$set
cp -r orig/$set aggregate/$set
for person in $@
do
  echo "Processing $person..."
  shasum per-person/$person/$set/* | sed -r 's/per-person\/.+\/.+\///g' > per-person/$person-$set-list.txt
  sdiff -w 256 per-person/$person-$set-list.txt orig-$set-list.txt | grep '|' > per-person/$person-$set-diff.txt
  sed -r 's/.*([0-9]{4}_[0-9]{6}).*/\1/g' per-person/$person-$set-diff.txt > per-person/$person-$set-changes.txt
  for file in $(cat per-person/$person-$set-changes.txt)
  do
    echo "cp per-person/$person/$set/$file.mat aggregate/$set/$file.mat"
    cp per-person/$person/$set/$file.mat aggregate/$set/$file.mat
  done
done
cat per-person/*-$set-diff.txt > all-$set-diff.txt
sed -r 's/.*([0-9]{4}_[0-9]{6}).*/\1/g' all-$set-diff.txt > all-$set-changes.txt
shasum aggregate/$set/* | sed -r 's/aggregate\/.+\///g' > aggregate-$set-list.txt
sdiff -w 256 aggregate-$set-list.txt orig-$set-list.txt | grep '|' > aggregate-$set-diff.txt
