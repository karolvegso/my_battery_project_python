import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
# path to measured data
path_to_meas_data="D:/programs_work/Python/keithley_6221_elcurrent_source_2182_nanovoltmeter/240624_evaluation/Cu_ITO_LPSCl_Li_04_data_stiching/240624_Cu_ITO_LPSCl_Li_04_data_stiching.txt"
# path to save data
path_to_save_data="D:/programs_work/Python/keithley_6221_elcurrent_source_2182_nanovoltmeter/240624_evaluation/Cu_ITO_LPSCl_Li_04_data_stiching/240624_Cu_ITO_LPSCl_Li_04_accum_charge.txt"
# load measured data to numpy array
meas_data=np.loadtxt(path_to_meas_data,delimiter='\t',dtype=float)
# print measured data
#print(meas_data)
# find peaks in measured data
peaks,properties=find_peaks(meas_data[:,1],height=0.05,distance=283)
# plot found peaks
plt.plot(meas_data[:,0],meas_data[:,1])
plt.plot(meas_data[peaks,0],meas_data[peaks,1],"x")
plt.show()
# equally distribute charge for plating events
# electric current
electric_current=1.0e-5 #3.9e-4 1.0e-5
# time of plating in hours
plating_time=float(283/3600) #(7.3/3600)
# single minimum deposited charge in mAh
single_plated_charge=electric_current*plating_time*1000
# calculate size of peaks
no_platings=peaks.size
# find tau times of charge plating
# initialize tau numpy array
tau=np.zeros((no_platings+1),dtype=float)
tau[0]=0.0
tau[1:(no_platings+1)]=meas_data[peaks,0]
# distribute plating events as numpy array
plating_events_array=np.ones((no_platings+1),dtype=float)*single_plated_charge
# initialize accumulated charge numpy array
accum_charge_array=np.zeros((no_platings+1),dtype=float)
# calculate accumulated charge during platings
for index_0 in range(no_platings+1):
    accum_charge_array[index_0]=np.sum(plating_events_array[0:(index_0+1)])
    #accum_charge_array[index_0]=(index_0+1)*single_plated_charge
plt.plot(tau,accum_charge_array)
plt.show()
# save accumulated charge data
accum_charge_data=np.zeros([no_platings+1,2],dtype=float)
accum_charge_data[:,0]=tau
accum_charge_data[:,1]=accum_charge_array
np.savetxt(path_to_save_data,accum_charge_data,delimiter='\t')
