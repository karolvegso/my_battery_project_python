import numpy as np
# specify path to data
path_to_data='d:/programs_work/Python/keithley_6221_elcurrent_source_2182_nanovoltmeter/090524_development/Cu_Li3N_LPSCl_Li/'
# root name of plating data
root_name_plating='meas_data_plating'
# root name of ocp data
root_name_ocp='meas_data_ocp'
# folder number - start
no_folder_start=0
# folder number - stop
no_folder_stop=182
# folder number - step
no_folder_step=1
# number of folders to evaluate
no_folders=int((no_folder_stop-no_folder_start)/no_folder_step)+1
# number of folder digits
no_folder_digits=6
# path to save data
path_to_folder_save_data='d:/programs_work/Python/keithley_6221_elcurrent_source_2182_nanovoltmeter/090524_development/evaluation/'
# root name for save data
root_name_save_data='Cu_Li3N_LPSCl_Li_all_data'
# full path to save data
path_to_save_data=path_to_folder_save_data+root_name_save_data+'.txt'
# create buffer to store measurement data as numpy array
buffer = np.array([], dtype=float)
# main for loop
for index_0 in range(no_folders):
    # calculate current folder string
    current_folder_no=no_folder_start+index_0*no_folder_step
    folder_no_str=str(current_folder_no)
    folder_no_str=folder_no_str.rjust(no_folder_digits, '0')
    print(folder_no_str)
    # get path to folder
    path_to_folder=path_to_data+folder_no_str
    print(path_to_folder)
    # get path to plating data
    name_plating_data=root_name_plating+'_'+folder_no_str+'.txt'
    path_to_plating_data=path_to_folder+'/'+name_plating_data
    print(path_to_plating_data)
    # get path to ocp data
    name_ocp_data=root_name_ocp+'_'+folder_no_str+'.txt'
    path_to_ocp_data=path_to_folder+'/'+name_ocp_data
    print(path_to_ocp_data)
    # import plating data as numpy array
    plating_data=np.loadtxt(path_to_plating_data)
    #print(plating_data)
    # import ocp data as numpy array
    ocp_data=np.loadtxt(path_to_ocp_data)
    #print(ocp_data)
    # append single measurement data to buffer - plating data
    buffer=np.append(buffer, plating_data)
    # append single measurement data to buffer - ocp data
    buffer=np.append(buffer, ocp_data)
# get shape of buffer
buffer_shape=buffer.shape
print(buffer_shape)
# number of measurements
no_meas=int(buffer_shape[0])
no_meas=int(no_meas/2)
print(no_meas)
# reshape buffer
buffer_reshaped = np.reshape(buffer, (no_meas, 2))
# correct time coordinates
time_constant=1.0
for index_1 in range(no_meas):
    buffer_reshaped[index_1][0]=float(index_1*time_constant)
# save all data as numpy array in text file
np.savetxt(path_to_save_data, buffer_reshaped, delimiter='\t')
