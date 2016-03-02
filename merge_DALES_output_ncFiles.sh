#!/bin/bash
# This file patches the mpi subdomain files together

exp=217
levels=('0003' '0010' '0020' '0035' '0050' '0100' '0200')
varsxy=('uxy' 'vxy' 'wxy' 'thlxy' 'thvxy' 'qtxy' 'qlxy' 'buoyxy' 'qrxy' 'nrxy' 'cloudnrxy')
varsyz=('uyz' 'vyz' 'wyz' 'thlyz' 'thvyz' 'qtyz' 'qlyz' 'buoyyz' 'qryz' 'nryz' 'cloudnryz')
indir=/nobackup/users/lochbihl/model/DALES/J1_bull
outdir=/nobackup/users/lochbihl/model/DALES/J1_bull/combined_fields

# check if outdir exists
if [ ! -d "${outdir}" ]; then
  mkdir ${outdir}
  if [ $? != 0 ];then 
    echo "Cannot create outdir! Check permissions! Exit"
    exit 126
  fi
  mkdir ${outdir}/tmp
fi

# patch fielddump files together
if [ -f ${indir}/fielddump.000.${exp}.nc ];then
  cdo -v gather ${indir}/fielddump.*.${exp}.nc ${outdir}/fielddump.comb.${exp}.nc
fi

# patch cape files together
if [ -f ${indir}/cape.000.${exp}.nc ];then
  cdo -v gather ${indir}/cape.*.${exp}.nc ${outdir}/cape.comb.${exp}.nc
fi

# patch xy crosssections together
for i in ${levels[@]}
do
  if [ -f ${indir}/crossxy.${i}.000.${exp}.nc ];then
    files=$(ls ${indir}/crossxy.${i}.*.${exp}.nc)
    for k in ${varsxy[@]}
    do
      for j in ${files}
      do
        cdo -v selname,${k} ${indir}/${j##*/} ${outdir}/tmp/${j##*/}
      done
      cdo -v gather  ${outdir}/tmp/crossxy.${i}.*.${exp}.nc ${outdir}/crossxy.${i}.${k}.${exp}.nc
      rm ${outdir}/tmp/crossxy.${i}.[0-9][0-9][0-9].${exp}.nc
    done
  fi
done

# patch yz crosssection together
if [ -f ${indir}/crossyz.000.${exp}.nc ];then
  files=$(ls ${indir}/crossyz.*.${exp}.nc)
  for k in ${varsyz[@]}
  do
    for j in ${files}
    do
      cdo -v selname,${k} ${indir}/${j##*/} ${outdir}/tmp/${j##*/}
    done
    cdo -v gather  ${outdir}/tmp/crossyz.*.${exp}.nc ${outdir}/crossyz.${k}.${exp}.nc
    rm ${outdir}/tmp/crossyz.[0-9][0-9][0-9].${exp}.nc
  done
fi

# move crossxz to outdir
if [ -f ${indir}/crossxz.000.${exp}.nc ];then
  mv ${indir}/crossxz.000.${exp}.nc ${outdir}
fi

exit
