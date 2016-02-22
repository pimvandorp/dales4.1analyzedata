import numpy as np

cp = 1004.703 
g = 9.81
Rd = 287.06  
Rv = 461.5
p0 = 1.e5
Lv = 2.5008e6

exnr = ((pres/p0)**(Rd/cp))
tmpl = thl*exnr
tmp = tmpl + (Lv/cp)*ql
esat = 610.78 * np.exp ((17.2694*(tmp-273.16))/(tmp-35.86))
rsat = Rd/Rv * esat/(pres-esat)
qsat = rsat/(1+rsat)
RELH = e/esat

