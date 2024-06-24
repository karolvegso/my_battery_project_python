import numpy as np
# specify path to data
path_to_data='d:/programs_work/Python/keithley_6221_elcurrent_source_2182_nanovoltmeter/240624_evaluation/Cu_ITO_LPSCl_Li_05 (3)/Cu_ITO_LPSCl_Li_05/'
# root name of plating data
root_name_plating='meas_data_plating'
# root name of ocp data
root_name_ocp='meas_data_ocp'
# folder number - start
no_folder_start=0
# folder number - stop
no_folder_stop=383
# folder number - step
no_folder_step=1
# number of folders to evaluate
no_folders=int((no_folder_stop-no_folder_start)/no_folder_step)+1
# number of folder digits
no_folder_digits=9
# path to save data
path_to_folder_save_data='d:/programs_work/Python/keithley_6221_elcurrent_source_2182_nanovoltmeter/240624_evaluation/Cu_ITO_LPSCl_Li_05_data_stiching/'
# root name for save data
root_name_save_data='240624_Cu_ITO_LPSCl_Li_05_data_stiching'
# full path to save data
path_to_save_data=path_to_folder_save_data+root_name_save_data+'.txt'
# create buffer to store measurement data as numpy array
buffer = np.array([], dtype=float)
# initialize last time value
last_time_value=0.0
# initialize time constant for plating
time_const_plating=0.1
# initialize time constant for ocp
time_const_ocp=1
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
    # acquite plating data shape
    plating_data_shape=plating_data.shape
    # print shape of plating data
    print(plating_data_shape)
    # number of plating points
    no_plating_points=int(plating_data_shape[0])
    # print number of plating points
    print(no_plating_points)
    # import ocp data as numpy array
    ocp_data=np.loadtxt(path_to_ocp_data)
    #print(ocp_data)
    # acquite ocp data shape
    ocp_data_shape=ocp_data.shape
    # print shape of ocp data
    print(ocp_data_shape)
    # number of ocp points
    no_ocp_points=int(ocp_data_shape[0])
    # print number of ocp points
    print(no_ocp_points)
    for index_1 in range(no_plating_points):
        plating_data[index_1][0]=last_time_value+(index_1+1)*time_const_plating
        if (index_1 == (no_plating_points-1)):
            last_time_value=last_time_value+(index_1+1)*time_const_plating
    for index_2 in range(no_ocp_points):
        ocp_data[index_2][0]=last_time_value+(index_2+1)*time_const_ocp
        if (index_2 == (no_ocp_points-1)):
            last_time_value=last_time_value+(index_2+1)*time_const_ocp
    #print(plating_data)
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
# correct time coordinates to hours
for index_3 in range(no_meas):
    buffer_reshaped[index_3][0]=float(buffer_reshaped[index_3][0]/3600)
# save all data as numpy array in text file
np.savetxt(path_to_save_data, buffer_reshaped, delimiter='\t')
