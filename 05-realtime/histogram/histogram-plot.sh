#!/usr/bin/bash

## Use the following shebang line if you want to run this script on a specific CPU core
#/usr/bin/env -S taskset -c 1 bash

# This file is copied from:
# https://www.osadl.org/Create-a-latency-plot-from-cyclictest-hi.bash-script-for-latency-plot.0.html
# With the following changes:
# 1. Reduce the number of iterations
# 2. Fetch the number of cores from the system

# 1. Run cyclictest
dur=1
echo "Running cyclictest for $dur minute"
cyclictest -D"$dur"m -m -Sp90 -i200 -h400 -q >output

# 2. Get maximum latency
max=$(grep "Max Latencies" output | tr " " "\n" | sort -n | tail -1 | sed s/^0*//)

# 3. Grep data lines, remove empty lines and create a common field separator
grep -v -e "^#" -e "^$" output | tr " " "\t" >histogram

# 4. Set the number of cores
cores=$(nproc)

# 5. Create two-column data sets with latency classes and frequency values for each core, for example
for i in $(seq 1 $cores); do
  column=$(expr $i + 1)
  cut -f1,$column histogram >histogram$i
done

# 6. Create plot command header
echo -n -e "set title \"Latency plot\"\n\
set terminal png\n\
set xlabel \"Latency (us), max $max us\"\n\
set logscale y\n\
set xrange [0:400]\n\
set yrange [0.8:*]\n\
set ylabel \"Number of latency samples\"\n\
set output \"out/plot.png\"\n\
plot " >plotcmd

# 7. Append plot command data references
for i in $(seq 1 $cores); do
  if test $i != 1; then
    echo -n ", " >>plotcmd
  fi
  cpuno=$(expr $i - 1)
  if test $cpuno -lt 10; then
    title=" CPU$cpuno"
  else
    title="CPU$cpuno"
  fi
  echo -n "\"histogram$i\" using 1:2 title \"$title\" with histeps" >>plotcmd
done
#
# 8. Make sure output directory exists
mkdir -p out

# 9. Execute plot command
gnuplot -persist <plotcmd
echo "Histogram plot saved in $PWD/out/plot.png"
