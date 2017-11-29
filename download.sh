#!/bin/bash

#BSUB -q basement
#BSUB -J "download"
#BSUB -o out.log
#BSUB -e out.err

~/.local/bin/gdc-client download -d ../wgsbam/ -m /nfs/users/nfs_t/tn5/team219/fusion_breast/pack/gdc_manifest.2017-11-28T14_27_34.552357.txt -t /nfs/users/nfs_t/tn5/team219/fusion_breast/pack/gdc-user-token.2017-11-28T15_28_24+01_00.txt --retry-amount 100 --wait-time 10 --no-related-files
