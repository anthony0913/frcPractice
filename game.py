#Controls: q,w,a,s,z,x,c,rb1,rb2,rb3,bb1,bb2,bb3
#More: rf1,rf2,rf3,bf1,bf2,bf3,rl,bl,r,b,r-,b-,p
import threading
import time

#General Variables (Storage: Force, Levitate, Boost, ForceTimer, BoostTimer)
scoreboard,sensors,redPowerups, bluePowerups,handicaps,pause = [0,0,150],[0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0],False

#Point Assigner (Calculates and returns points to add after multipliers)
def getPoints(increment, team, redPowerups, bluePowerups):
  if increment == "switch":
    if team == "red":
      if redPowerups[2]==1 or redPowerups[2]==3:
        return 2
      else:
        return 1
    elif team == "blue":
      if bluePowerups[2]==1 or bluePowerups[2]==3:
        return 2
      else:
        return 1
  elif increment == "scale":
    if team == "red":
      if redPowerups[2]>1:
        return 2
      else:
        return 1
    if team == "blue":
      if bluePowerups[2]>1:
        return 2
      else:
        return 1
def addPoints(redSwitch, blueSwitch, scale, redPowerups, bluePowerups):
  tempCalc = [0,0] #redPoints, bluePoints
  if redSwitch==1 or redPowerups[0]==1 or redPowerups[0]==3:
    tempCalc[0] = tempCalc[0] + getPoints("switch", "red", redPowerups, bluePowerups)
  if blueSwitch==1 or bluePowerups[0]==1 or bluePowerups[0]==3:
    tempCalc[1] = tempCalc[1] + getPoints("switch", "blue", redPowerups, bluePowerups)
  if (scale==1 or redPowerups[0]>1) and bluePowerups[0]<2:
    tempCalc[0] = tempCalc[0] + getPoints("scale", "red", redPowerups, bluePowerups)
  if (scale==-1 or bluePowerups[0]>1) and redPowerups[0]<2:
    tempCalc[1] = tempCalc[1] + getPoints("scale", "blue", redPowerups, bluePowerups)
  return tempCalc

#Input Thread (Determines Input)
def command():
  global sensors,pause,scoreboard
  i = input("")
  if i == "q":
    sensors[0] = 1
  elif i == "w":
    sensors[0] = 0
  elif i == "a":
    sensors[1] = 1
  elif i == "s":
    sensors[1] = 0
  elif i == "z":
    sensors[2] = 1
  elif i == "x":
    sensors[2] = 0
  elif i == "c":
    sensors[2] = -1
  elif i == "rf1":
    redPowerups[0],redPowerups[3] = 1,10
  elif i == "rf2":
    redPowerups[0],redPowerups[3] = 2,10
  elif i == "rf3":
    redPowerups[0],redPowerups[3] = 3,10
  elif i == "rb1":
    redPowerups[2],redPowerups[4] = 1,10
  elif i == "rb2":
    redPowerups[2],redPowerups[4] = 2,10
  elif i == "rb3":
    redPowerups[2],redPowerups[4] = 3,10
  elif i == "bf1":
    bluePowerups[0],bluePowerups[3] = 1,10
  elif i == "bf2":
    bluePowerups[0],bluePowerups[3] = 2,10
  elif i == "bf3":
    bluePowerups[0],bluePowerups[3] = 3,10
  elif i == "bb1":
    bluePowerups[2],bluePowerups[4] = 1,10
  elif i == "bb2":
    bluePowerups[2],bluePowerups[4] = 2,10
  elif i == "bb3":
    bluePowerups[2],bluePowerups[4] = 3,10
  elif i == "rl":
    redPowerups[1] = 1
  elif i == "bl":
    bluePowerups[1] = 1

  #Special Commands
  elif i == "r": #Give red 5 points
    scoreboard[0] = scoreboard[0] + 5
  elif i == "b": #Give blue 5 points
    scoreboard[1] = scoreboard[1] + 5
  elif i == "r-": #Take 5 points from red
    scoreboard[0] = scoreboard[0] - 5
  elif i == "b-": #Take 5 points from blue
    scoreboard[1] = scoreboard[1] - 5
  #elif i == "p": #Exit
  #  pause = True
  elif i == "t": #Time Skip Full
    scoreboard[2] = 10
  elif i == "t-": #10 Less Seconds
    scoreboard[2] = scoreboard[2] - 10
  elif i == "t+": #10 More Seconds
    scoreboard[2] = scoreboard[2] + 10
  #Thread Rebooter
  threading.Thread(target = command).run()

#Powerup Timer (Ensures Powerups are turned off after time limit)
def powerTime():
  global redPowerups,bluePowerups
  if redPowerups[3]!=0:
    redPowerups[3]=redPowerups[3]-1
  elif redPowerups[3]==0:
    redPowerups[0]=0
  if redPowerups[4]!=0:
    redPowerups[4]=redPowerups[4]-1
  elif redPowerups[4]==0:
    redPowerups[2]=0
  if bluePowerups[3]!=0:
    bluePowerups[3]=bluePowerups[3]-1
  elif bluePowerups[3]==0:
    bluePowerups[0]=0
  if bluePowerups[4]!=0:
    bluePowerups[4]=bluePowerups[4]-1
  elif bluePowerups[4]==0:
    bluePowerups[2]=0

#Game Sequence (Runs the game for 1 second)
def gameSequence():
  global scoreboard, sensors, redPowerups, bluePowerups
  seqPoints = addPoints(sensors[0], sensors[1], sensors[2], redPowerups,bluePowerups)
  scoreboard[0],scoreboard[1],scoreboard[2] = scoreboard[0]+seqPoints[0],scoreboard[1]+seqPoints[1],scoreboard[2]-1
  time.sleep(0.998)
  print ("Scoreboard:"+str(scoreboard)+"     \t  Monitor:"+str(sensors)+","+str(redPowerups)+","+str(bluePowerups)+"\tDiff: "+str(abs(scoreboard[0]-scoreboard[1])))
  powerTime()
  if scoreboard[2]<=0:
    print("\n\n\nFinish"+"\nRed Levitate: "+str(redPowerups[1])+"\nBlue Levitate: "+str(bluePowerups[1]))

#Start Loop (Uses Game Sequence to play until end)
def start():
  while scoreboard[2]>0 and pause == False:
    gameSequence()

#Actual Game (Begins the game)
threading.Thread(target = command).start()
start()
