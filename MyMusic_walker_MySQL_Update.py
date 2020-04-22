#!/usr/bin/env python3
# walker.py by FmG
# Free to use

import mysql.connector
import os
import sys
import time

def humanize_time(secs):
    mins, secs = divmod(secs, 60)
    hours, mins = divmod(mins, 60)
    return '%02d:%02d:%02d' % (hours, mins, secs)
startTime = time.time()
# put here any extension to exlude in the loop
excludeList = [".txt", ".db", ".cache", ".tmp"]

sourcepath = "/mnt/raid1/Plex/Music/Archive/"
mydb = mysql.connector.connect(
                               host="localhost",
                               user="root",
                               passwd="MySql23",
                               database="MyMusic"
                               )
mycursor = mydb.cursor()
recordCount = skipCount = dupCount = 0
logName = "/mnt/raid1/MariaDB/logs" + time.strftime("%Y%m%d%H%M%S", time.localtime(time.time())) + ".log"
dupLog = "/mnt/raid1/MariaDB/logs" + time.strftime("%Y%m%d%H%M%S", time.localtime(time.time())) + "_duplicate.log"
logFile = open(logName, "w")
dupFile = open(dupLog, "w")
sql = "INSERT INTO `MyMusic`(`Name`,`Artist`,`Song`,`Path`,`Extension`, `Requested`) VALUES (%s,%s,%s,%s,%s,%s);"
try:
    for path, subdirs, files in os.walk(sourcepath):
        for name in files:
            fullname = file = os.path.join(sourcepath, name)
            extension = os.path.splitext(file)[1]
            sanitazedName = path
            #sanitazedName = fullname.replace("gluster", "\\vodstp01-smb.svc.dmc-int.net")
            #sanitazedName = sanitazedName.replace(os.sep, '\\')
            cSql = "SELECT COUNT(*) FROM MyMusic where Name=%s"
            cVal = (path,)
            mycursor.execute(cSql, cVal)
            cCheck = mycursor.fetchone()
            if (cCheck[0] > 0) or (extension in excludeList):
                if(extension in excludeList):
                    logFile.write(time.strftime("%H:%M:%S", time.localtime(time.time())) + ": File Skipped - " + sanitazedName + " Reason: Extension type\n")
                elif (cCheck[0] > 0):
                    logFile.write(time.strftime("%H:%M:%S", time.localtime(time.time())) + ": File Skipped - " + sanitazedName + " Reason: Duplicate Record\n")
                    dupFile.write(time.strftime("%H:%M:%S", time.localtime(time.time())) + ": Duplicate File - " + sanitazedName + " \n")
                    dupCount += 1
                else:
                    logFile.write(time.strftime("%H:%M:%S", time.localtime(time.time())) + ": File Skipped - " + sanitazedName + " Reason: Unknown\n")
                skipCount += 1            
            else:
                val = (name, artist, song, path, extension, requested)
                mycursor.execute(sql, val)
                mydb.commit()
                recordCount += 1
            sys.stdout.write("\r" + time.strftime("%H:%M:%S", time.localtime(time.time())) + ' -> Record Inserted. Total Inserted: ' + str(recordCount) + ' Skipped: ' + str(skipCount) + ' (Duplicate: ' + str(dupCount) + ') in: ' + humanize_time(time.time() - startTime))
            sys.stdout.flush()
except:
    print("An exception occurred")
duration = time.time()-startTime
print ("\nJob Completed\n" + str(recordCount) + ' records inserted\n' + str(skipCount) + ' records skipped (Duplicate: ' + dupCount + ')\nDuration: ' + humanize_time(duration) + ' seconds')
logFile.close()
