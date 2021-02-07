from timeZone import UTC_offset

def convertTime(userSentTime,userSentTimeZone,userReactedTimeZone,period):

    userSentOffset=UTC_offset(userSentTimeZone)
    userReactedOffset=UTC_offset(userReactedTimeZone)
    day=0
    if ":" not in userSentTime:
        userSentTime+= ":00"
        
    if ":" not in userSentOffset:
        userSentOffset+= ":00"

    if ":" not in userReactedOffset:
        userReactedOffset+= ":00"    

    userTime = userSentTime.split(":")
    userOffsetTime = userSentOffset.split(":")
    requiredOffsetTime= userReactedOffset.split(":")

    userTime= list(map(int,userTime))
    userOffsetTime= list(map(int,userOffsetTime))
    requiredOffsetTime= list(map(int,requiredOffsetTime))

    print(userTime)
    print(userOffsetTime)
    print(requiredOffsetTime)
    print(period)
    utc=[]
    result=[]

    
    for (item1, item2) in zip(userTime, userOffsetTime):
	    utc.append(item1 - item2)
    print("hey")
    print(utc)
    if(userTime[0]==12 and period=="am"):
        period="pm"

    if(userTime[0]==12 and period=="pm"):
        period="am"

    if(utc[1]>=60):
        utc[0]+=utc[1]%60
        utc[1]-=0

    if(utc[1]<0):
        utc[0]-=1
        utc[1]=abs(utc[1])

    if(utc[0]<=0 and period=="am"):
        utc[0]+=12
        utc[1]=abs(utc[1])    
        period="pm"
        day=day-1

    if(utc[0]<=0 and period=="pm"):
        utc[0]+=12
        utc[1]=abs(utc[1])    
        period="am" 
        
    if(utc[0]>12 and period=="am"):
        utc[0]=utc[0]-12
        period="pm"
        day=day-1

    if utc[0]>12 and period=="pm":
        utc[0]=utc[0]-12
        period="am"
        day=day+1

    print(utc,period,day)


    for (item3, item4) in zip(utc, requiredOffsetTime):
	    result.append(item3 + item4)     
    print("result :",result)

    if(result[1]>=60):
        result[0]+=result[1]%60
        result[1]-=60

    if(result[1]<0):
        result[0]-=1
        result[1]=abs(result[1])

    if(result[0]<0 and period=="am"):
        result[0]+=12
        result[1]=abs(result[1])    
        period="pm"
        day=day-1

    if(result[0]<0 and period=="pm"):
        result[0]+=12
        result[1]=abs(result[1])    
        period="am" 
        

    if(result[0]>12 and period=="am"):
        result[0]=result[0]-12
        period="pm"
        day=day-1

    if result[0]>12 and period=="pm":
        result[0]=result[0]-12
        period="am"
        day=day+1

    days={"-1":"previous day","0":"same day","1":"next day"}

    print(result) 
    print(period) 
    print(days.get(str(day))) 

convertTime("12","ist","cst","am")
