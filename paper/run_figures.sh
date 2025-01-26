# !/bin/bash

# Script to run figures
screen -dmSL fig2 bash -c \
'jupyter nbconvert --execute --to fig2.ipynb --inplace fig2.ipynb'
screen -dmSL S1 bash -c \
'jupyter nbconvert --execute --to figS1-monkey-behavior.ipynb --inplace figS1-monkey-behavior.ipynb'
screen -dmSL S3-monkey bash -c \
'jupyter nbconvert --execute --to figS3-example-cca.ipynb --inplace figS3-example-cca.ipynb'
screen -dmSL S4 bash -c \
'jupyter nbconvert --execute --to figS4-decoding.ipynb --inplace figS4-decoding.ipynb'
