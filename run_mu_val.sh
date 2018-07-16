#!/bin/bash

for i in AHNAK2 AKAP9 DNAH11 DNAH2 DNAH5 HERC2 KMT2C KMT2D MUC16 PDE4DIP PIK3CA RYR2 SYNE1 TG TP53 USH2A
do
	/var/www/html/drupal-7.56/sites/all/modules/mutarget/powermw -t onegroup -r $i -g /var/www/html/drupal-7.56/sites/all/modules/mutarget/mut.3.1.12.tsv -v /var/www/html/drupal-7.56/sites/all/modules/mutarget/exp.3.1.tsv -o $i.tcga.tsv
	/var/www/html/drupal-7.56/sites/all/modules/mutarget/powermw -t onegroup -r $i -g /var/www/html/drupal-7.56/sites/all/modules/mutarget/mut.3.2.12.tsv -v /var/www/html/drupal-7.56/sites/all/modules/mutarget/exp.3.2.tsv -o $i.meta.tsv
done
