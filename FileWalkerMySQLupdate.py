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
excludeList = [".lnk", ".db", ".cache", ".dmc-tvt-ddinfo", ".fail", ".crdownload", ".aspera-ckpt", ".partial", ".tmp1", ".tmp"]

path = "/gluster/"
mydb = mysql.connector.connect(host="localhost",user="outgestuser",passwd="FT2tALfgZ72gZ39B",database="outgest")
mycursor = mydb.cursor()
idClient = 2
idTransfer = 1
recordCount = skipCount = dupCount = 0
logName = "/var/www/html/outgest/logs/walker_" + time.strftime("%Y%m%d%H%M%S", time.localtime(time.time())) + ".log"
dupLog = "/var/www/html/outgest/logs/walker_" + time.strftime("%Y%m%d%H%M%S", time.localtime(time.time())) + "_duplicate.log"
logFile = open(logName, "w")
dupFile = open(dupLog, "w")
sql = "INSERT INTO `files`(`Fullname`,`Filename`,`Extension`,`Size`,`Status`,`idClient`,`readyForTransfer`,`transferMethod`,`lastUpdate`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);"
try:
    for path, subdirs, files in os.walk(path):
        for name in files:
            fullname = file = os.path.join(path, name)
            size = os.path.getsize(file)
            extension = os.path.splitext(file)[1]
            # sanitazedName = fullname.replace("/", "\\")
            sanitazedName = fullname.replace("gluster", "\\vodstp01-smb.svc.dmc-int.net")
            sanitazedName = sanitazedName.replace(os.sep, '\\')
            cSql = "SELECT COUNT(*) FROM files where Fullname=%s"
            cVal = (sanitazedName,)
            mycursor.execute(cSql, cVal)
            cCheck = mycursor.fetchone()
            if (cCheck[0] > 0) or (extension in excludeList) or (name[:12] == "#chkpt_file#") or (name[:11] == "#work_file#"):
                if(extension in excludeList):
                    logFile.write(time.strftime("%H:%M:%S", time.localtime(time.time())) + ": File Skipped - " + sanitazedName + " Reason: Extension type\n")
                elif (name[:12] == "#chkpt_file#") or (name[:11] == "#work_file#"):
                    logFile.write(time.strftime("%H:%M:%S", time.localtime(time.time())) + ": File Skipped - " + sanitazedName + " Reason: Work File\n")
                elif (cCheck[0] > 0):
                    logFile.write(time.strftime("%H:%M:%S", time.localtime(time.time())) + ": File Skipped - " + sanitazedName + " Reason: Duplicate Record\n")
                    dupFile.write(time.strftime("%H:%M:%S", time.localtime(time.time())) + ": Duplicate File - " + sanitazedName + " \n")
                    dupCount += 1
                else:
                    logFile.write(time.strftime("%H:%M:%S", time.localtime(time.time())) + ": File Skipped - " + sanitazedName + " Reason: Unknown\n")
                skipCount += 1            
            else:
                val = (sanitazedName, name, extension, size, "2", idClient, time.time(), idTransfer, time.time())
                mycursor.execute(sql, val)
                mydb.commit()
                recordCount += 1
            sys.stdout.write("\r" + time.strftime("%H:%M:%S", time.localtime(time.time())) + ' -> Record Inserted. Total Inserted: ' + str(recordCount) + ' Skipped: ' + str(skipCount) + ' (Duplicate: ' + str(dupCount) + ') in: ' + humanize_time(time.time() - startTime))
            sys.stdout.flush()
except:
    print("An exception occurred")
duration = time.time()-startTime
print ("\nJob Completed\n" + str(recordCount) + ' records inserted\n' + str(skipCount) + ' records skipped (Duplicate: ' + str(dupCount) + ')\nDuration: ' + humanize_time(duration) + ' seconds')
logFile.close()
