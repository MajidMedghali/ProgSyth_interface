#!/bin/bash

current_directory=$(pwd)

synth_file_directory="$current_directory/synth_file"

echo "Suppression des fichiers .csv dans $current_directory"
find "$current_directory" -maxdepth 1 -type f -name "*.csv" -delete

echo "Vidage du répertoire $synth_file_directory"
rm -rf "$synth_file_directory"/*

echo "Opération terminée."
