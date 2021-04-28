#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 11:51:35 2021

@author: emilymitchell
"""

import requests 
import re
import csv

def main():
       
    #column headers for csv
    csvFields = ["student_id", "name", "meet_id", "meet", "event_id", "event", "place", "grade", "school_id", "school", "mark"]  
    #write data to csv file
    with open('trackData.csv', 'w') as csvFile:
        csvWriter = csv.writer(csvFile)
        csvWriter.writerow(csvFields)
        csvFile.close()

     #create unique id's
    event_idVisited = []
    event_id = 0  
    student_idVisited = []
    student_id = 0   
    meet_idVisited = []
    meet_id = 0   
    school_idVisited = []
    school_id = 0 

    #create stack and visited lists
    stak = list()
    visited = list()
    stak.append("http://ciacsports.com/site") #home site
    visited.append("http://ciacsports.com/site")
    
    #get first html
    link = stak.pop()
    r = requests.get(link)
    html = r.text
    
    #find outdoor TF page
    outdoorTF = re.findall(r'href="(.*)?".*Outdoor Track', html)
    #get url and append to stak and visited
    for url in outdoorTF:
        if url not in visited:
            stak.append(url)
            visited.append(url)
     

    #find indoor TF home page
    indoorTF = re.findall(r'href="(.*)?".*Indoor Track', html)
    #get url and append to stak ad visited 
    for url in indoorTF:
       if url not in visited:
           stak.append(url)
           visited.append(url)

   
    #create new stack and visited to hold results links
    stakResult = list()
    visitedResult = list()
    
   
    
    #pop everything in stak
    while stak:
         link = stak.pop()
         r = requests.get(link)
         html = r.text
         #range of years you want results from 
         for x in range(15,21):
            year = str(x)
            #get all relevant links
            results = re.findall(r'href="(https://content.ciacsports.com/.*'+year+'[^dh].*html)"', html) 
            #get url and append to new stak and visited
            for url in results:
                if url not in visitedResult:
                    stakResult.append(url)
                    visitedResult.append(url)
    #print(stakResult) #now stak has all links to results for desired years
    
    m_id = [50, 51, 52, 53, 54, 55, 39, 40, 41, 42, 43, 44, 28, 29, 30, 31, 32, 33, 17, 18, 19, 20, 21, 22, 6, 7, 8, 9, 10 , 11, 45, 46, 47, 48, 49, 34, 35, 36, 37, 38, 23, 24, 25, 26, 27, 12, 13, 14, 15, 16, 1, 2, 3, 4, 5]

    while stakResult: 
        link = stakResult.pop()
        #print(link)
        r = requests.get(link)
        html = r.text
            
    
        eventResults = re.findall(r'Event Results[\s\S]*<pre>[\s\S]*', html)
    
        #get meet name
        title = re.findall(r'<title>([\s\S]*)?</title>', html)
        meetName = ""
        for element in title:
            meetName += element
    

        #split by event
        for string in eventResults:
            event = re.split(r'(?=Girls)|(?=Boys)|(?=Women)|(?=Men)', string) #event has all information
   
     
        #get event name and just event results
        eventName = []
        #finalEventName = []
        eventBodyList = []
        finalEventBody = []
        visitedEvent = []

        
        for i in range (1, len(event)):
            #get name of event
            eventNameList = event[i].split("\n") #event name list steps through every line in each event
            if len(eventNameList[0].split(" ")) > 2 and "4x" not in eventNameList[0] and "(" not in eventNameList[0] and "<" not in eventNameList[0] and "Prelims" not in eventNameList[0] and "Dev" not in eventNameList[0]:
                if "Boys " in eventNameList[0] or "Girls " in eventNameList[0] or "Women " in eventNameList[0] or "Men " in eventNameList[0]:
                    if "Women " in eventNameList[0] or "Girls " in eventNameList[0]:
                        alterW = eventNameList[0].split(" ");
                        newName = "Girls " + str(alterW[1]) + " " + str(alterW[2])
                        eventName.append(newName)
                        #eventBodyList += re.findall(r'(1 [\s\S]*)', event[i])
                    elif "Men " in eventNameList[0] or "Boys " in eventNameList[0]:
                        alterM = eventNameList[0].split(" ");
                        #print(alterM)
                        newName = "Boys " + str(alterM[1]) + " " + str(alterM[2])
                        eventName.append(newName)
                        #eventBodyList += re.findall(r'(1 [\s\S]*)', event[i])
                    else:
                        eventName.append(eventNameList[0])
                    eventBodyList += re.findall(r'(1 [\s\S]*)', event[i])


        for j in range(0, len(eventName)):
            try:
                if(eventName[j] == eventName[j+1]):
                    pass
                else:
                    if eventName[j] in visitedEvent:
                        pass
                    else:
                        visitedEvent.append(eventName[j])
                        #finalEventName.append(eventName[j])
                        finalEventBody.append(eventBodyList[j])
            except:
                pass


        #create meet list
        meet = [[[]] for i in range(len(finalEventBody))]
    
        #add event and person to meet list
        for i in range (0, len(finalEventBody)):
            newList = ""
            newList += finalEventBody[i]
            person = newList.splitlines()
            meet[i] = person
    
        #create row list for csv file
        rows = []
    
        
        #get relevant info
        for i in range(0, len(finalEventBody)): 
            for j in range(0, len(meet[i])): 
                #split by spaces then get rid of empty strings
                text = meet[i][j].split(" ")
                finalText = [x for x in text if x.strip()]
                
                #get rid of extra stuff
                try:
                    place = int(finalText[0]) #get place 
                    eName = visitedEvent[i] #get event name
                    #athlete has two names
                    if finalText[3].startswith(("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")):
                        athleteName = finalText[1] + " " + finalText[2]
                        grade = int(finalText[3]) #get grade year
                        #if school is one word
                        if finalText[5].startswith(("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")): 
                            school = finalText[4]
                            finalMark = finalText[6]
                        #if school is two words
                        else:
                            school = finalText[4] + " " + finalText[5] 
                            finalMark = finalText[7]
                    #if athlete has three names
                    else:
                        athleteName = finalText[1] + " " + finalText[2] + " " + finalText[3] 
                        grade = int(finalText[4]) #get grade year
                        #if school is one word
                        if finalText[6].startswith(("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")): 
                            school = finalText[5]
                            finalMark = finalText[7]
                        #if school is two words
                        else:
                            school = finalText[5] + " " + finalText[6] 
                            finalMark = finalText[8]
                            
                    #get rid of special characters
                    finalMark = finalMark.replace("#", "")
                    finalMark = finalMark.replace("*", "")
                    finalMark = finalMark.replace("J", "") 
                    finalMark = convertToInt(finalMark)


                    #populate unique id's
                    if eName in event_idVisited:
                        event_id = event_idVisited.index(eName) + 1
                    else:
                        event_idVisited.append(eName)
                        event_id = event_idVisited.index(eName) + 1

                    if athleteName in student_idVisited:
                        student_id = student_idVisited.index(athleteName) + 1
                    else:
                        student_idVisited.append(athleteName)
                        student_id = student_idVisited.index(athleteName) + 1
                    
                    if meetName in meet_idVisited:
                        meet_id = meet_idVisited.index(meetName) + 1
                    else:
                        meet_idVisited.append(meetName)
                        meet_id = meet_idVisited.index(meetName) + 1
                    
                    if school in school_idVisited:
                        school_id = school_idVisited.index(school) + 1
                    else:
                        school_idVisited.append(school)
                        school_id = school_idVisited.index(school) + 1
                      
                    
                    trueMeet_id = m_id[meet_id - 1]
                    #create list of current entry
                    entry = [student_id, athleteName, trueMeet_id, meetName, event_id, eName, place, grade, school_id, school, finalMark] 
                    #append entry to rows
                    rows.append(entry) 
                
                #pass non-needed info
                except: 
                    pass #pass when place not given
         
        writeToCSV(rows, meetName)
        #writeToExcel(wb, rows, meetName)

def convertToInt(finalMark):
    try:
        return float(finalMark)
    except:
        if ":" in finalMark:
            time = finalMark.split(":")
            minute = float(time[0])
            seconds = minute * 60
            finalMark = seconds + float(time[1])
            return finalMark
        
        elif "-" in finalMark:
            length = finalMark.split("-")
            feet = float(length[0])
            inches = feet * 12
            finalMark = inches + float(length[1])
            return finalMark
        

def writeToCSV(rows, meetName):
    #column headers for csv
    #csvFields = ["Name", "Meet", "Event", "Place", "Grade", "School", "Mark"]  
    #write data to csv file
    with open('trackData.csv', 'a') as csvFile:
        csvWriter = csv.writer(csvFile)
        #csvWriter.writerow(csvFields)
        csvWriter.writerows(rows)
        csvFile.close()
      
main()