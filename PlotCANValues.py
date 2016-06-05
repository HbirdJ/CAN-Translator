# -*- coding: utf-8 -*-
"""
@author: Bradford Johnson
Takes text files from VSI-2534 logs
Translates hex data into engineering units
Saves plot of requested values
"""
import datetime
import matplotlib.pyplot as plt  

#Input file names
#raw data log and faux .dbc file; possibly build an file selector later?
filename='GPS Constant.txt'
translator='TranslateSpeed.txt'

textfile=open('Data/%s' %filename, 'r')
datalines=textfile.readlines()
textfile.close()

DLCs={} #Data length Code Dictionary that will be used to find all IDs.
timeList=[] #store the timestamp from the log file
IDList=[] #store the IDs in sequence
rawData=[] #Store the data fields in sequence

for line in datalines[8:]: #iterate through the entire file starting at line 8 (skips header)
    elements=line.split() #Separate the entries

    #time stamps
    s = elements[1]
    
    new = s[:12] + s[13:]
    times=datetime.datetime.strptime(new, "%H:%M:%S:%f")
    
    #adjustment for time offset
    if len(timeList) == 0:
        initialTime=times
    times=(times-initialTime).total_seconds()*1.388

    timeList.append(times)
          
    
    ID=elements[0] #extract the text associated with the CAN identifier
    IDList.append(ID) #add the ID to a list       
    
    DLC=elements[3] #Data length
    DLCs[ID]=DLC #Dictionary of IDs
    
    Datalength=4+int(DLC)
    
    rawData.append(elements[4:Datalength]) #store the data field as a list of text strings
  
IDs=DLCs.keys() #the keys in the DLCs dictionary are all the unique IDs that have not been duplicated.


print('Number of Unique IDs: %i' %len(IDs)) #display the total number of messages

#Get data translation from faux .dbc file (currently a .csv produced by hand)
textfile=open('Translators/%s' %translator, 'r')
legend=textfile.readlines()
textfile.close()

xaxis=[]
yaxis=[]

f1=plt.figure(1)

#build time and engineering data for each requested value
for line in legend[1:]:
    
    elements=line.split(',')
    time=[]
    processed=[]
    raw=[]
    yaxis.append(elements[0])
    xaxis.append('time'+elements[0])
    
    #build time list
    for i in range(len(IDList)):
        if IDList[i] in [elements[1]]:
            time.append(timeList[i])
            raw.append(rawData[i])
            
    vars()['time'+elements[0]]=time
    
    #Turn Raw CAN bytes into engineering units
    #Currently reads byte location from faux .dbc file, future iterations should base from bit location        
    for line in raw:
        hexdata=""        
        
        #reads length of data and concatinates hex bytes
        for x in range(0,int(elements[3])):
            hexdata+=line[int(elements[4+x])]
            
        conversion=int(hexdata,16)*float(elements[2])
        processed.append(conversion)
        
    vars()[elements[0]]=processed
    plt.plot(time, processed, marker='o', linestyle='-',markersize=3)
    #plt.plot(time, processed, 'o')

#Plot formatting
plt.xlabel('Time (seconds)')
plt.ylabel('Speed (km/h)')
plt.legend(yaxis,bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.grid()
ttl=plt.title('Data from Toyota Prius %s' %filename)
ttl.set_y(1.03) #pushes the title up as to not crowd the axis labels
plt.savefig('Plots/%s.png' %filename[:-4],dpi=100,transparent=False, bbox_inches='tight', pad_inches=0.05)