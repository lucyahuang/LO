from LargeOffice_FMU_coEfficients import LargeOffice
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsRegressor
import joblib

startDay        = 1  # day of year --> 1=Jan; 32=Feb; 60=Mar; 91=Apr; 121=May; 152=Jun; 182=Jul; 213=Aug; 244=Sep; 274=Oct; 305=Nov; 335=Dec;
duration        = 1   # number of days


# TODO:temporary read in from CSVs, eventually read in from FNCS
TO = np.genfromtxt('./core/_temp/TO.csv', delimiter=',',max_rows=(startDay - 1 + duration)*1440+1)[(startDay-1)*1440+1:,1] 
WS = np.genfromtxt('./core/_temp/windSpeed.csv', delimiter=',',max_rows=(startDay - 1 + duration)*1440+1)[(startDay-1)*1440+1:,1] 

weather_init = {"TO":TO[0],"windSpeed":WS[0]}

# initialize an instance of large office model
LO1 = LargeOffice(startDay, duration, weather_init) 
 
# for final plotting
plotting = {"time":[],"T_zones":[],"P_total":[],"TO":[]}
    
# start simulation
model_time = LO1.startTime 
while(model_time < LO1.stopTime): #fmu uses second of year as model_time
    currentDay = int(model_time/86400)
    currentHour = int((model_time-currentDay*86400)%86400/3600)
    currentMin = int((model_time-(currentDay*86400+currentHour*3600))/60)
    currentSec = int((model_time-(currentDay*86400+currentHour*3600))%60)

    TO_current = TO[(model_time-LO1.startTime)/60] #TODO:replace with input from FNCS
    WS_current = WS[(model_time-LO1.startTime)/60] #TODO:replace with input from FNCS

    weather_current={'TO':TO_current,'windSpeed':WS_current}
    control_inputs={} #use default control inputs, or define dynamic values here
    P_total,T_room = LO1.step(model_time,weather_current,control_inputs)

    plotting["time"].append(model_time)
    plotting["TO"].append(TO_current)
    if model_time == LO1.startTime:
        plotting["T_zones"]=T_room
    else:
        plotting["T_zones"]=np.vstack((plotting["T_zones"],T_room))
    plotting["P_total"].append(P_total)

    model_time = model_time + 60

    #end of simulation and terminate the fmu instance
LO1.terminate()
print("=======================Simulation Done=======================")
