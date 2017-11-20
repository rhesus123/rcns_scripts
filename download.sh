#!/bin/bash

#BSUB -q basement
#BSUB -J "download"
#BSUB -o out.log
#BSUB -e out.err

~/.local/bin/gdc-client download -d ../bams/ -m /nfs/users/nfs_t/tn5/team219/fusion_breast/pack/gdc_manifest.2017-10-26T08_52_49.606354.txt -t /nfs/users/nfs_t/tn5/team219/fusion_breast/pack/gdc-user-token.2017-11-07T08_19_19.659Z.txt --retry-amount 100 --wait-time 10
