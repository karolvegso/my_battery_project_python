import pyvisa
import time
import numpy as np
import os
# path to folder to save measured data
path_to_save_meas_data="d:/programs_work/Python/keithley_6221_elcurrent_source_2182_nanovoltmeter/measured_data_03/"
# root name to save plating measured data
root_name_plating='meas_data_plating'
# root name to save ocp measured data
root_name_ocp='meas_data_ocp'
# number of f=digits in folder name
no_folder_digits=6
# start pyVISA Resource manager
rm = pyvisa.ResourceManager()
print(rm)
# acquire and print possible connections
rm.list_resources()
print(rm.list_resources())
# open TCPIP SOCKET connection to the Keithley 6221 electric current source
keithley6221_inst = rm.open_resource('TCPIP0::147.213.112.152::1394::SOCKET')
# termination characters for reading and writing
keithley6221_inst.read_termination = '\n'
keithley6221_inst.write_termination = '\n'
# identify device - electric current source
keithley6221_inst.write("*IDN?")
# print information about electric current source
print(keithley6221_inst.read())
# set number of repetition cycles or measurements
no_cycles=3
# turns ON Keithely 6221(electric current source) and sets output level to zero
keithley6221_inst.write('CLEar')
# enables auto range on Keithely 6221(electric current source)
keithley6221_inst.write('CURRent:RANGe:AUTO ON')
# set current on Keithely 6221(electric current source)
keithley6221_inst.write('CURRent 1.0e-6')
# set volatge compliance to 10 V
keithley6221_inst.write('CURRent:COMPliance 10')
# wait certain time for plating in seconds
# this is time during which Keithely 6221(electric current source) is ON
# total time of application plating in seconds
total_time_plating=60
# duration of single plating measurement in seconds
wait_time_plating=1
# number of plating measurements
no_plating_meas=int(total_time_plating/wait_time_plating)
# wait ceratin time after electric current source is in ON in seconds
wait_time_on=1
# wait ceratin time after electric current source is in OFF in seconds
wait_time_off=1
# open USB connection to the Keithley 2100 Digit Multimeter
keithley_inst = rm.open_resource('GPIB0::22::INSTR')
# perform identification of keithley 2182A
print(keithley_inst.query('*IDN?'))
# set channel 1
keithley_inst.write(':SENS:CHAN 1')
# specify threshold voltage in Volts
volt_threshold=0.202478
# wait time between voltage measurememts in seconds
wait_time_ocp=1.0
# event counter threshold for OCP
ocp_event_counter_threshold=2
# main for loop
for index_0 in range(no_cycles):
    # number of current folder
    no_folder_str=str(index_0)
    # fill empty spaces in folder name with zeros
    no_folder_str=no_folder_str.rjust(no_folder_digits, '0')
    # create path to folder
    path_to_folder=path_to_save_meas_data + no_folder_str
    # create folder
    os.mkdir(path_to_folder)
    # specify path to plating measurement file
    path_to_file_plating=path_to_folder + '/' + root_name_plating + '_' + no_folder_str + '.txt'
    # specify path to ocp measurement file
    path_to_file_ocp=path_to_folder + '/' + root_name_ocp + '_' + no_folder_str + '.txt'
    # create buffer to store plating measurement data as numpy array
    buffer_plating = np.array([], dtype=float)
    # create buffer to store ocp measurement data as numpy array
    buffer_ocp = np.array([], dtype=float)
    # turns ON Keithely 6221 - electric current source
    keithley6221_inst.write('OUTPut ON')
    # wait certain time after TURN ON electric current source
    time.sleep(wait_time_on)
    # print start of plating
    print("This is the start of plating: ", index_0)
    for index_1 in range(no_plating_meas):
        # acquire voltage measurements with range 10 Volts and resolution 1 microVolts
        volt_value = keithley_inst.query(':FETCH?')
        print(float(volt_value))
        # insert first voltage value to the plating buffer
        buffer_plating=np.append(buffer_plating, [float(index_1)*wait_time_plating, float(volt_value)])
        # wait ceratin time between voltage measurements
        time.sleep(wait_time_plating)
    # turns OFF Keithely 6221 - electric current source
    #keithley6221_inst.write('OUTPut OFF')
    # wait certain time after TURN OFF electric current source
    time.sleep(wait_time_off)
    # print end of plating
    print("This is the end of plating: ", index_0)
    # size of buffer numpy array for plating data
    buffer_size_plating = np.size(buffer_plating)
    # print buffer size for plating
    print(buffer_size_plating)
    # number of rows for plating data
    no_rows_plating=int(buffer_size_plating/2)
    # reshape buffer numpy array for plating
    buffer_plating_reshaped = np.reshape(buffer_plating, (no_rows_plating, 2))
    # save reshaped buffer numpy array for plating
    np.savetxt(path_to_file_plating, buffer_plating_reshaped, delimiter='\t')
    # print the beginning of OCP measurement
    print('This is beginning of OCP measurement: ', index_0)
    # acquire voltage measurements with range 10 Volts and resolution 1 microVolts
    volt_value = keithley_inst.query(':FETCH?')
    print(float(volt_value))
    # insert first voltage value to the OCP buffer
    buffer_ocp=np.append(buffer_ocp, [float(1.0)*wait_time_ocp, float(volt_value)])
    # create counter to count measurement
    counter=2
    # OCP event counter
    if (float(volt_value) < volt_threshold):
        print('Dont increase ocp event counter.')
        ocp_event_counter=0
    else:
        # increase of OCP event counter
        print('Increase ocp event counter.')
        ocp_event_counter=1
    # wait ceratin time between volatge measurements
    time.sleep(wait_time_ocp)
    # main while loop for OCP
    while (ocp_event_counter < ocp_event_counter_threshold):
        # acquire voltage measurements with range 10 Volts and resolution 1 microVolts
        volt_value = keithley_inst.query(':FETCH?')
        print(float(volt_value))
        # append new volatge measurement to the data
        buffer_ocp=np.append(buffer_ocp, [float(counter)*wait_time_ocp, float(volt_value)])
        # increase counter
        counter+=1
        if (float(volt_value) < volt_threshold):
            print('Dont increase ocp event counter.')
        else:
            # increase of OCP event counter
            print('Increase ocp event counter.')
            ocp_event_counter+=1
        # wait ceratin time between voltage measurements
        time.sleep(wait_time_ocp)
    # print the end of OCP measurement
    print('This is the end of OCP measurement:', index_0)
    # size of buffer numpy array
    buffer_size_ocp = np.size(buffer_ocp)
    # print buffer size for OCP
    print(buffer_size_ocp)
    no_rows_ocp=int(buffer_size_ocp/2)
    # reshape buffer numpy array
    buffer_ocp_reshaped = np.reshape(buffer_ocp, (no_rows_ocp, 2))
    # save reshaped buffer numpy array
    np.savetxt(path_to_file_ocp, buffer_ocp_reshaped, delimiter='\t')


