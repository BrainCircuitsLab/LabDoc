#!/bin/bash
# Define the output file name
output_file="jobfile"
# Remove the file if it already exists to start fresh
rm -f "$output_file"
# Loop from __ to __ with an interval of __
for x in $(seq START STEPSIZE END); do
# An example for one subject. You can expand it to multple subjects
    echo "python script.py --Group AD --Caseid 0306A --G $x" >> "$output_file"
done
echo "Commands have been written to $output_file"