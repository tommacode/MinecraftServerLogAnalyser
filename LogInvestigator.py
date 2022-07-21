import datetime

StartTime = datetime.datetime.now()
#Replace the file name with the name of the file you want to use
f = open('log.txt','r')
f = f.readlines()

def PlayTime(f):
    Players = []
    Time = []
    Sessions = []
    #Go through the log file
    for i in range(0,len(f)):
    #Go through each joining event
        if 'joined the game\n' in f[i]:
            #Get the time of the event
            joinlog = f[i].split(' ')
            JoinTime = joinlog[0].lstrip('[').rstrip(']')
            #Get the player name
            Player = joinlog[3]
            #If the player is not in the list, add them
            if Player not in Players:
                Players.append(Player)
                Time.append(0)
                Sessions.append(0)
            #Get the time that they left
            for ii in range(i,len(f)):
                if f'{Player} lost connection: Disconnected\n' in f[ii]:
                    leavelog = f[ii].split(' ')
                    LeaveTime = leavelog[0].lstrip('[').rstrip(']')
                    #Get the time difference
                    LeaveTime = datetime.datetime.strptime(LeaveTime,'%H:%M:%S')
                    JoinTime = datetime.datetime.strptime(str(JoinTime),'%H:%M:%S')
                    td = (LeaveTime-JoinTime)
                    break
            #Add the seconds to the total time for that player
            Time[Players.index(Player)] += td.seconds
            Sessions[Players.index(Player)] += 1
            

    return Players,Time,Sessions

#def PlayerIP(f,Players):
#    IP = []
#    for i in range(0,len(Players)):
#        #Loop through the log from back to front
#        for ii in range(len(f)-1,0,-1):
#        #find the player join event
#            if f'{Players[i]} joined the game\n' in f[ii]:
#                #Get the IP address
#                IPlog = f[ii+1].split(' ')
#                print(IPlog)
#                IP.append(IPlog[3])
#                break
#    return IP

def CommandsIssued(Players,f):
    CommandsIssued = [0]*len(Players)
    for i in range(0,len(f)):
        if 'issued server command' in f[i]:
            #Get the player name
            Player = f[i].split(' ')[3]
            CommandsIssued[Players.index(Player)] += 1
    return CommandsIssued




Players,Time,Sessions = PlayTime(f)
CommandsIssued = CommandsIssued(Players,f)

#IP = PlayerIP(f,Players)



#Change time into hours
for i in range(0,len(Time)):
    Time[i] = round(Time[i]/3600,1)

#Console output
#for i in range(0,len(Players)):
#    print(f'{Players[i]} played {Time[i]} hours in {Sessions[i]} sessions meaning an average session length of {round(Time[i]/Sessions[i],1)} hours')
#print(f'Total Play time: {sum(Time)} hours')

#csv output
o = open('Output.csv','w')
o.write('Player,Play Time,Sessions,Average Session Length,Commands issued,Time Between Commands (Avg)\n')
for i in range(0,len(Players)):
    if CommandsIssued[i] == 0:
        CommandsIssued[i] = 1
    o.write(f'{Players[i]},{Time[i]},{Sessions[i]},{round(Time[i]/Sessions[i],1)},{CommandsIssued[i]-1},{round(Time[i]*60/CommandsIssued[i],1)}\n')
o.write(f'{len(Players)},{sum(Time)},{sum(Sessions)},{round(sum(Time)/sum(Sessions),1)},{sum(CommandsIssued)},{round(sum(Time)*60/sum(CommandsIssued),1)}\n')
o.close()
Endtime = datetime.datetime.now()
print(f'Time taken: {Endtime-StartTime}')

input('Press enter to exit')
