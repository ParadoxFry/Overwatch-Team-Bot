import random
import pandas as pd
import numpy

#constants
maxTeamSize = 5
maxTanksPerTeam = 1
maxDPSPerTeam = 2
maxSupportPerTeam = 2
roleList = ['TANK', 'DPS', 'SUPPORT']
#How far apart can people be, and still play?
maxRange = 3

#define an exception if there are too many people In a role in the user list
class tooManyInRole(Exception):
    "Raised when too many people want to play the same role"
    pass

class rolesFilled(Exception):
    "Raised when attempting to "
    pass

#Role check!
#Are there too many players of a given role to create the requested number of teams?
def RoleCountCheck(players, teamCount, rolelist, roleList):
    #group the players by role
    roleCheck = players.groupby('Role').count()
    output = ""
    
    for x in roleList:       
        try:
            if x == 'TANK':
                roleCountOK = roleCheck.query("Role == '" + x + "'").iloc[0]['Player Name'] <= teamCount
            else:
                roleCountOK = roleCheck.query("Role == '" + x + "'").iloc[0]['Player Name'] <= teamCount * 2
        except:
            output = output + x + ": There are none"  
            roleCountOK = False
    
        if roleCountOK == True:
            output = output + x + ": OK " 
        else:
            raise tooManyInRole(x)
    return(output)

def CanCreateTeams(registeredPlayers, teamSize):
  #Count the number of players
  intRegisteredPeople = len(registeredPlayers)
  
  #Check if we can create teams, or if someone will be left out
  if intRegisteredPeople%teamSize != 1 :
    print("No one will get left out") 
  else:
    print("Someone will get let out. Try a different size of teams")
    return("Someone will get let out. Try a different size of teams")

  #How Many Teams?
  numOfTeams = intRegisteredPeople/teamSize
  #if there are left over people, we need a team of the leftovers
  if intRegisteredPeople%teamSize == 0:
    numOfTeams = numOfTeams
  else:
    numOfTeams += 1

  try:
    print(RoleCountCheck(registeredPlayers, numOfTeams, roleList))
  except:
    #throw our excpetion for too many in role
    print("There are too many " + "s to make teams.")

  return(numOfTeams)

def MakeATeam(registeredPlayers, teamSize):
  #Sort the list of registered people by rank, and choose the lowest one. 
  dfTeam = pd.DataFrame(registeredPlayers.sort_values('Rank', ascending = True).iloc[0]).transpose()
  #remove that player from the list
  registeredPlayers.drop(0, inplace = True)
  #removing records from the dataframe messes up the index, so reset it. 
  registeredPlayers = registeredPlayers.reset_index(drop=True)
  #get the leader's rank
  leaderRank = dfTeam['Rank'].iloc[0]
  #returns the coposition of the team by role
  comp = CompCheck(dfTeam)
  
  while (comp['Tank'] + comp['Support'] + comp['DPS'] < teamSize) and len(registeredPlayers) > 0:
   #find elegible players
    
    #determine which roles are left
    #build Eligible role list
    eligibleRoles = []
    if comp['Tank'] < 1:
        eligibleRoles.append('TANK')
    if comp['Support'] < 2:
        eligibleRoles.append('SUPPORT')
    if comp['DPS'] < 2:
        eligibleRoles.append('DPS')
        
    #only people of the correct roles can be added
    eligiblePlayers = registeredPlayers[registeredPlayers['Role'].isin(eligibleRoles)]
    
    #and only people who are within the leader's range
    eligiblePlayers = eligiblePlayers[eligiblePlayers['Rank'].between(leaderRank-maxRange, leaderRank+maxRange, inclusive = True)]
    
    #shuffle the remaining players
    eligiblePlayers = eligiblePlayers.sample(frac=1).reset_index(drop=True)
    
    if (len(eligibleRoles)) > 0:
      #fill the next role
      dfTeam = dfTeam.append(eligiblePlayers.iloc[0])
      #removing records from the dataframe messes up the index, so reset it. 
      registeredPlayers = registeredPlayers.reset_index(drop=True)
      #remove the player from the list
      registeredPlayers.drop(0, inplace = True)
      #removing records from the dataframe messes up the index, so reset it. 
      registeredPlayers = registeredPlayers.reset_index(drop=True)
        
      #the new team member that was added keeps its index from its original dataframe. Reset the team index
      dfTeam = dfTeam.reset_index(drop=True)
        
      #update the comp
      comp = CompCheck(dfTeam)

  #return a list of player names in the team
  return(dfTeam['Player Name'])

def CompCheck(dfTeam):
  tankCount = len(dfTeam.query("Role == 'TANK'"))
  DPSCount = len(dfTeam.query("Role == 'DPS'"))
  supportCount = len(dfTeam.query("Role == 'SUPPORT'"))
  comp = {'Tank':tankCount,
          'DPS':DPSCount, 
          'Support':supportCount}
  return(comp)

def MakeTeams(registeredPlayers, teamSize):
  numOfTeams = CanCreateTeams(registeredPlayers, teamSize)
  #create a list of teams
  teams = []
  for i in range(numOfTeams):
    newTeam = MakeATeam(registeredPlayers, teamSize)
    #remove the players that are in the new team from the registeredPlayers
    registeredPlayers = registeredPlayers['Player Name' not in newTeam]
    #add the team to the list of teams
    teams = teams.append(newTeam)

  #we have teams! Return them
  return(teams)
   