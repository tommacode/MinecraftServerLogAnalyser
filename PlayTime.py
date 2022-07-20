import datetime

#Replace the file name with the name of the file you want to use
f = open('log.txt','r')
f = f.readlines()

def PlayTime(f):
    Players = []
    Time = []
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
            

    return Players,Time

Players,Time = PlayTime(f)

#Change time into hours, minutes, seconds
for i in range(0,len(Time)):
    Time[i] = str(datetime.timedelta(seconds=Time[i]))

#Print the results
for i in range(0,len(Players)):
    print(f'{Players[i]} played {Time[i]} hours')

input('Press enter to exit')


