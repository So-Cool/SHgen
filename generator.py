#! /usr/local/bin/python

import sys
import csv
import datetime
import time
from numpy.random import normal
from math import sqrt, ceil
from random import randint
from pprint import pprint
import argparse

# parse arguments
parser = argparse.ArgumentParser(description='Smart house data generator.')
parser.add_argument('-t', '--time', type=str, nargs=1, required=False, dest="time", default=None, help=('time to use as a starting point in 24h format *Month Day Year hh.mm * e.g. "Jun 1 2005  13.33" (quotation marks are required)'))
parser.add_argument('-f', '--facts', required=False, dest="facts", default=False, action='store_true', help=('generate Aleph positive and negative examples'))
parser.add_argument('adjacency', type=str, nargs=1, help='path to your adjacency matrix')
parser.add_argument('layout', type=str, nargs=1, help='path to your house layout')
parser.add_argument('activities', type=str, nargs=1, help='path to your activities definitions')
parser.add_argument('path', type=str, nargs=1, help='path to your agent script (path)')

# Gaussian generator class
class genGaus:
  def __init__(self, mu, sigma):
    self.mu = mu
    self.sigma = sigma
  def get(self):
    return normal(self.mu, self.sigma)

# Class inspecting sensor status in given room
# ['motion']['sensorID']['location' + 'status']
# ['item'  ]['sensorID']['location' + 'status' + 'activity']
class monitor:
  def __init__(self, location, sensors):
    self.location = location
    self.truthTable           = {}
    self.truthTable['motion'] = {}
    self.truthTable['item']   = {}
    for sensor in sensors:
      if type(sensor[3]) == str:
        self.truthTable['item'][sensor[0]] = {}
        self.truthTable['item'][sensor[0]]['location'] = (sensor[1], sensor[2])
        self.truthTable['item'][sensor[0]]['activity'] = sensor[3]
        self.truthTable['item'][sensor[0]]['status']   = False
      elif type(sensor[3]) == float:
        self.truthTable['motion'][sensor[0]] = {}
        self.truthTable['motion'][sensor[0]]['location'] = (sensor[1], sensor[2], sensor[3])
        self.truthTable['motion'][sensor[0]]['status']   = False
      else:
        print "monitor class initialisation error: unknown sensor type!"
        sys.exit(1)

  def getLocation(self):
    return self.location

  def updateMotionSensor(self, currentPosition):
    firedSensors = []
    # find affected sensors
    for sensor in self.truthTable['motion'].keys():
      sensorLocation = self.truthTable['motion'][sensor]['location']
      sensorStatus   = self.truthTable['motion'][sensor]['status']
      # check if table-status agrees with current readings
      if self.affected(sensorLocation, currentPosition) == sensorStatus: # status agrees
        pass
      else: # status does not agree
        # change status in table
        self.truthTable['motion'][sensor]['status'] = not(sensorStatus)
        # record change
        firedSensors.append( ( sensor, str(self.truthTable['motion'][sensor]['status']).lower()  ) )

    # return list of sensor with changed state
    return firedSensors

  def motionSensorsOn(self, currentPosition):
    firedSensors = []
    # find affected sensors
    for sensor in self.truthTable['motion'].keys():
      sensorStatus   = self.truthTable['motion'][sensor]['status']
      sensorLocation = self.truthTable['motion'][sensor]['location']
      # check if table-status agrees with current readings
      if sensorStatus and self.affected(sensorLocation, currentPosition): # id ON & is within your range
        self.truthTable['motion'][sensor]['status'] = not(sensorStatus)
        firedSensors.append( ( sensor, str(self.truthTable['motion'][sensor]['status']).lower()  ) )

    # return list of sensor with changed state
    return firedSensors

  def affected(self, sensor, position):
    d = sqrt( (position[0]-sensor[0])**2 + (position[1]-sensor[1])**2 )
    # check proximity by inspecting position and radius
    if d <= sensor[2]:
      return True
    else:
      return False

  def display(self):
    return self.truthTable

  def getItemDetails(self, activity):
    for sensorID in self.truthTable['item'].keys():
      if self.truthTable['item'][sensorID]['activity'] == activity:
        return (sensorID, self.truthTable['item'][sensorID]['location'])
    print "Activity *", activity, "* not defined in room ", self.location
    sys.exit(1)

  def activateItem(self, sensorID):
    # if self.truthTable['item'][sensorID]['status'] != False:
    #   print "Item sensor state error A: ", sensorID
    #   sys.exit(1)
    # self.truthTable['item'][sensorID]['status'] = True
    sensorState = 'true'
    return [(sensorID, sensorState)]

  def deactivateItem(self, sensorID):
    # if self.truthTable['item'][sensorID]['status'] != True:
    #   print "Item sensor state error D-A: ", sensorID
    #   sys.exit(1)
    # self.truthTable['item'][sensorID]['status'] = False
    sensorState = 'false'
    return [(sensorID, sensorState)]

# time window length in microsecond (10^-6): 5 seconds
WINDOWLENGTH = 5 * 1000000

# number of different time representations used
TIMEREPRESENTATIONS = 4

# Define predicate name for connected rooms - background knowledge
connected = "connected"
# sensor location(room) keyword for Prolog facts
sensorLocation = "sensorInRoom"
motionSensorInRoom = "motionSensorInRoom"
itemSensorInRoom   = "itemSensorInRoom"
# sensor item assigned to motion sensor keyword for Prolog facts
sensorField = "sensorInField"
# in place at time --- keyword for Prolog facts
spaceTime = "spaceTime"
# activity fixed to sensor keyword for Prolog bg
sensorActivity = "sensorActivity"
# define predicate name for querying place at time
atLocation = "nowAt"
# keyword for Prolog facts about current activity
currentActivity = "activityTime"
# keyword for Prolog activity query mechanism
atActivity      = "nowDo"
# keyword Prolog for person ID
personID = "person"

# Constants
nl = '\n'
fact = '__'
rev  = '_'

interconnected = ""
# interconnected = connected + "(A, B, Path) :-" + nl + "  " + connected + "(A, B, [], Path)."
# interconnected += nl + connected + "(A, B, V, Path) :-" + nl
# interconnected += "  " + connected + rev + "(A, X), not( member(X, V) )," + nl
# interconnected += "  (" + nl + "    " + "B = X, reverse([B,A|V], Path)" + nl + "  " + "; " + connected
# interconnected += "(X, B, [A|V], Path)" + nl + "  " + "), !." + nl + nl

interchangable = ""
# interchangable  = connected + rev + "(A, B) :-" + nl + "  " + connected + fact
# interchangable += "(A, B); " + connected + fact + "(B, A)." + nl + nl

# check where you are
whereAmI = ""
# whereAmI  = atLocation + "(Room, Time, TimeType) :-" + nl
# whereAmI += "  %% there is presence in given room at some time T..." + nl
# whereAmI += "  " + spaceTime + "(Room, TimeType, T)," + nl
# whereAmI += "  %% ...which is before our time of interest..." + nl
# whereAmI += "  T =< Time," + nl
# whereAmI += "  %% ...and we do not move to any other room between *Time* and *T*" + nl
# whereAmI += "  \\+" + atLocation + rev + "(Room, TimeType, T, Time), !." + nl + nl
# ########
# whereAmI += atLocation + rev + "(Room, TimeType, T1, T2) :-" + nl
# whereAmI += "  " + spaceTime + "(OtherRoom, TimeType, Tbound)," + nl
# whereAmI += "  \\+(OtherRoom = Room)," + nl
# whereAmI += "  T1 =< Tbound, Tbound =< T2." + nl + nl

whatIDo = ""
# whatIDo  = atActivity + "(Activity, Time, TimeType) :-" + nl
# whatIDo += "  %% the activity is held at some time T..." + nl
# whatIDo += "  " + currentActivity + "(Activity, true, TimeType, T1)," + nl
# whatIDo += "  %% ...which started now or before our time of interest..." + nl
# whatIDo += "  T1 =< Time," + nl
# whatIDo += "  %% ... and has not ended yet." + nl
# whatIDo += "  \\+" + atActivity + rev + "(Activity, Time, TimeType)." + nl + nl
# #######
# whatIDo += atActivity + rev + "(Activity, Time, TimeType) :-" + nl
# whatIDo += "  " + currentActivity + "(Activity, false, TimeType, T)," + nl
# whatIDo += "  T =< Time." + nl + nl

locationSpecifier = ""
# locationSpecifier  = "location_(Time, Location) :-" + nl
# locationSpecifier += "  sensorInRoom(SensorID, Location)," + nl
# locationSpecifier += "  sensor_state(SensorID, true, Time), !." + nl + nl
# #######
# locationSpecifier += "location(Time, Location) :-" + nl
# locationSpecifier += "  (sensorInRoom(SensorID, Location)," + nl
# locationSpecifier += "   sensor_state(SensorID, true, Time)," + nl
# locationSpecifier += "   Time >= 0, !  );" + nl
# locationSpecifier += "  %% think about cut at the end" + nl
# locationSpecifier += "  ( !, Time > 0, location(Time-1, Location) )." + nl + nl
# #####
# locationSpecifier += "location(Time, Location, State) :-" + nl
# locationSpecifier += "  (sensorInRoom(SensorID, Location)," + nl
# locationSpecifier += "   sensor_state(SensorID, State, Time)," + nl
# locationSpecifier += "   Time >= 0, !  );" + nl
# locationSpecifier += "  %% think about cut at the end" + nl
# locationSpecifier += "  ( !, Time > 0, location(Time-1, Location) )." + nl + nl
# #####
# locationSpecifier += "%% return all activities between given times" + nl
# locationSpecifier += "locations(T1, T2, Loc) :-" + nl
# locationSpecifier += "  location(T1, Loc);" + nl
# locationSpecifier += "  (T1<T2, locations(T1+1, T2, Loc))." + nl + nl

deviceSpecifier = ""
# deviceSpecifier  = "device(Time, Device) :-" + nl
# deviceSpecifier += "  sensorActivity(SensorID, Device)," + nl
# deviceSpecifier += "  sensor_state(SensorID, true, Time)." + nl + nl#!
# #####
# deviceSpecifier += "device(Time, Device, State) :-" + nl
# deviceSpecifier += "  sensorActivity(SensorID, Device)," + nl
# deviceSpecifier += "  sensor_state(SensorID, State, Time)." + nl + nl#!
# #####
# deviceSpecifier += "devices(T1, T2, Dev) :-" + nl
# deviceSpecifier += "  device(T1, Dev);" + nl
# deviceSpecifier += "  (T1<T2, devices(T1+1, T2, Dev))." + nl + nl

sensorStateRule = ""
# sensorStateRule  = "sensor_state(SensorID, SensorState, Time) :-" + nl
# sensorStateRule += "  sensor_state(SensorID, SensorState, sequence, Time)." + nl + nl
# ##
# sensorStateRule += "sensor_state(SensorID, SensorState, TimeType, Time) :-"
# sensorStateRule += "  %% there is sensor in given state..." + nl
# sensorStateRule += "  sensor(SensorID, SensorState, TimeType, T1)," + nl
# sensorStateRule += "  % ... before our time of interest..." + nl
# sensorStateRule += "  T1 =< Time," + nl
# sensorStateRule += "  %% ...and its status does not change after that." + nl
# sensorStateRule += "  negate(NotSensor, SensorState),"
# sensorStateRule += "  \\+sensor_state(SensorID, NotSensor, TimeType, T1, Time),!." + nl + nl
# ##
# sensorStateRule += "%% sensor state between T1 and T2 inclusive" + nl
# sensorStateRule += "sensor_state(SensorID, SensorState, TimeType, T1, T2) :-" + nl
# sensorStateRule += "  sensor(SensorID, SensorState, TimeType, T)," + nl
# sensorStateRule += "  T1 =< T, T =< T2." + nl + nl
# ##
# sensorStateRule += "negate(Y, X) :-" + nl
# sensorStateRule += "  (X ->" + nl
# sensorStateRule += "   Y = false;" + nl
# sensorStateRule += "   Y = true)." + nl + nl

sensorModes = ""
# sensorModes = "sensorModes(true)." + nl + "sensorModes(false)." + nl + nl

roomIDs = "roomIDs"
sensorIDs = "sensorsIDs"
deviceIDs = "deviceIDs"
activityIDs = "activityIDs"

# prolog predicate name for activity model
activityRule = "activity"


# Background knowledge file-name
bgFilename = "bg.pl"

# give name WITHOUT extension for positive(ext '.f') and negative(ext '.n') examples
posNegFilename = "data"
posFilename = posNegFilename + ".f"
negFilename = posNegFilename + ".n"

# generated data file-name
dataFilename = "data.txt"

# Define functions
# assign activity/item sensor to motion field sensor
def itemToLocation(sensors, persons):
  readings = []
  # divide into item and motion
  for room in sensors:
    motion = []
    item   = []
    for sensor in sensors[room]['sensor']:
      if type(sensor[3]) == str:
        item.append(sensor)
      elif type(sensor[3]) == float:
        motion.append(sensor)
      else:
        print "Sensor identification error"
        sys.exit(1)
    # for each sensor check...
    fieldFound = False
    for i in item:
      fieldFound = False
      # ...to which field it belongs
      for area in motion:
        d = sqrt( (i[1]-area[1])**2 + (i[2]-area[2])**2 )
        if d <= area[3]:
          fieldFound = True
          readings.append( sensorField + "(" + i[0] + ", " + area[0] + ")." )
      # if no field found
      if not(fieldFound):
        readings.append( sensorField + "(" + i[0] + ", " + "none" + ")." )

  # append persons identifiers
  readings.append('')
  for person in persons:
    pson = person[0].lower() + person[1:]
    readings.append( personID+'(' + pson + ').' )

  # write to file
  with open(bgFilename, 'ab') as bg:
    bg.write( '\n' )
    bg.write( '\n'.join(readings) )
    bg.write( '\n' )


# append current activity to ground truth
def activityToTime(now, origin, sequence, activity, state, persona):
  # get UNIX timestamp
  tsn = time.mktime(now.timetuple())
  # append nano seconds and convert to microseconds
  tsn *= 1000000
  tsn += now.microsecond
  tsn = int(tsn)

  tso = time.mktime(origin.timetuple())
  # append nano seconds and convert to microseconds
  tso *= 1000000
  tso += origin.microsecond
  tso = int(tso)

  # output
  facts = []
  # represent time in 4 different ways
  t = []
  t.append(str(tsn-tso)) # relative
  t.append(str(tsn))     # absolute
  t.append(str(sequence)) # sequence
  t.append(str(get_window(tso, tsn))) # windowed

  # prepare to write to file
  facts.append( currentActivity + "(" + activity + ", " + state + ", " + "relative, " + t[0] + persona + ")." )
  facts.append( currentActivity + "(" + activity + ", " + state + ", " + "absolute, " + t[1] + persona + ")." )
  facts.append( currentActivity + "(" + activity + ", " + state + ", " + "sequence, " + t[2] + persona + ")." )
  facts.append( currentActivity + "(" + activity + ", " + state + ", " + "windowed, " + t[3] + persona + ")." )

  return facts

# generate four different time representation tuple
def generateTimeTuple(now, origin, sequence):
  # get UNIX timestamp
  tsn = time.mktime(now.timetuple())
  # append nano seconds and convert to microseconds
  tsn *= 1000000
  tsn += now.microsecond
  tsn = int(tsn)

  tso = time.mktime(origin.timetuple())
  # append nano seconds and convert to microseconds
  tso *= 1000000
  tso += origin.microsecond
  tso = int(tso)

  # (relative, absolute, sequence, windowed)
  return ( tsn-tso, tsn, sequence, get_window(tso, tsn) )

# get time window of event
def get_window( initTime, currentTime ):
  diff = currentTime - initTime
  # check for negativity
  if diff < 0:
    print "Negative time in get_window()!"
    sys.exit(1)
  # get window: 0--WINDOWLENGTH is 0
  return int(diff/WINDOWLENGTH)


# generate Prolog ground truth of locations at given time
def nowInRoom(now, origin, sequence, current, persona):
  # get UNIX timestamp
  tsn = time.mktime(now.timetuple())
  # append nano seconds and convert to microseconds
  tsn *= 1000000
  tsn += now.microsecond
  tsn = int(tsn)

  tso = time.mktime(origin.timetuple())
  # append nano seconds and convert to microseconds
  tso *= 1000000
  tso += origin.microsecond
  tso = int(tso)

  # output
  facts = []
  # represent time in 4 different ways
  t = []
  t.append(str(tsn-tso)) # relative
  t.append(str(tsn))     # absolute
  t.append(str(sequence)) # sequence
  t.append(str(get_window(tso, tsn))) # windowed

  # prepare to write to file
  facts.append( spaceTime + "(" + current + ", " + "relative, " + t[0] + persona + ")." )
  facts.append( spaceTime + "(" + current + ", " + "absolute, " + t[1] + persona + ")." )
  facts.append( spaceTime + "(" + current + ", " + "sequence, " + t[2] + persona + ")." )
  facts.append( spaceTime + "(" + current + ", " + "windowed, " + t[3] + persona + ")." )

  return facts


## Read in adjacency matrix
def rooms( Fadj ):
  rooms = []
  with open(Fadj, 'rb') as csvfile:
    matrix = csv.reader(csvfile, delimiter=' ', skipinitialspace=True)
    for row in matrix:
      # clean all empty strings
      cleanRow = filter(lambda a: a != '', row)
      rooms.append(cleanRow[1:])

  # Transform layout into dictionary
  ## Extract keys
  keys = rooms[0][:]
  ## Extract adjacency
  adjacency = []
  for i in rooms[1:]:
    row = []
    for j in i:
      row.append( bool(int(j)) )
    adjacency.append(row)
  ## Construct dictionary
  vals = []
  for i in adjacency:
    vals.append( dict(zip(keys, i)) )
  layout = dict(zip(keys, vals))

  facts = [interconnected, interchangable, whereAmI, whatIDo, locationSpecifier, deviceSpecifier, sensorStateRule, sensorModes]
  keys1 = layout.keys()
  keys2 = layout.keys()

  # get the room IDs
  for k in keys1:
    facts.append( roomIDs + "(" + k + ").\n" )
  facts.append("\n")

  for key1 in keys1:
    for key2 in keys2:
      if layout[key1][key2]:
        facts.append( connected + fact + '(' + key1 + ', ' + key2 + ').' + nl )
    # adjacency matrix is symmetric
    keys2.remove(key1)
  # write to file
  with open(bgFilename, 'wb') as bgfile:
    bgfile.write(''.join(facts))

  return layout


# get time generators for activities
def activities( Fact ):
  # load model parameters: assume structure [name mu sigma]
  model = []
  with open(Fact, 'rb') as bgfile:
    parameters = csv.reader(bgfile, delimiter=' ', skipinitialspace=True)
    for row in parameters:
      # clean all empty strings
      cleanRow = filter(lambda a: a != '', row)

      # check for comment or empty line
      if cleanRow == []:
        continue
      if cleanRow[0][0] == ';':
        continue

      try:
        tup = ( cleanRow[0], float(cleanRow[1]), float(cleanRow[2]) )
      except:
        tup = ( cleanRow[0], cleanRow[1], cleanRow[2] )
      model.append( tup )
  # clean from comment line
  if type(model[0][1]) == str and type(model[0][2]) == str:
    model.pop(0)

  # create random generators
  generators = {}
  for gen in model:
    generators[gen[0]] = genGaus(gen[1], gen[2]).get

  return generators


# read in path
def path( Fpath ):
  path = []
  occupiers = {}
  with open(Fpath, 'rb') as pathfile:
    for line in pathfile:
      # strip spaces at the beginning
      line = line.strip()
      # check for comment or empty line
      if line == "":
        continue
      if line[0] == ';':
        continue

      # check for multiple occupiers
      o1 = line.find('>')
      o2 = line.find('<')
      if o1 != -1 and o2 != -1:
        print "Error: personal log starts and ends in the same line!"
        sys.exit(1)
      if o1 != -1:
        # do nothing - collect information to *path* and then append it
        continue
      elif o2 != -1:
        occupiers[line.strip('<')] = path[:]
        path = []
        continue

      # check for blocks
      b1 = line.find('{')
      b2 = line.find('}')
      if b1 != -1 and b2 != -1:
        print "Error: activity block starts and ends in the same line!"
        sys.exit(1)
      if b1 != -1:
        # block begins
        path.append( ('{', line[:b1].strip(' ')) )
        continue
      elif b2 != -1:
        # block ends
        path.append( ('}', line[b2+1:].strip(' ')) )
        continue

      f1 = line.find('(')
      f2 = line.find(')')
      if f1 == -1 or f2 == -1:
        print "Path error: wrong format: ", line
        sys.exit(1)
      command = line[:f1]
      argument = line[f1+1:f2]
      # if there is comma in the argument it must be *wait* command or *wander*
      if command == 'wait':
        # find comma
        f3 = argument.find(',')
        if f3 == -1:
          print "Command wait has wrong argument: no comma in: ", argument
          sys.exit(1)
        argument1 = argument[:f3]
        argument2 = argument[f3+1:]
        argument = (float(argument1), float(argument2))

      if command == 'wander':
        #find comma
        f3 = argument.find(',')
        if f3 == -1:
          print "Command wander has wrong argument: no comma in: ", argument
          sys.exit(1)
        argument1 = argument[:f3]
        argument2 = argument[f3+1:]
        argument = (float(argument1), float(argument2))


      # append tuple to path
      path.append( (command, argument) )

  # if multiple occupiers return occupiers otherwise return path
  if bool(occupiers):
    return occupiers
  else:
    return path


# read in rooms layout into sensors dictionary
def layout( Flay, keys ):
  sensors = {}
  with open(Flay, 'rb') as layfile:
    # split into rooms: dictionary { rooms: { sensors:[], doors:[] } }
    ## do each activity per room
    for line in layfile:
      line = line.strip('\n')
      # split on *spaces*
      line = line.split(' ')
      # remove empty entries
      line = filter(lambda a: a != '', line)

      # check for comment or empty line
      if line == []:
        continue
      if line[0][0] == ';':
        continue

      # check if first element of line is a keyword
      if line[0] in keys: # add room to dictionary
        # check if there is ':' at the end of the line
        if line[2][-1] != ':':
          print "Header line error in 'layout' file!"
          sys.exit(1)

        roomID = line[0]
        sensors[roomID] = {}

        sensors[roomID]['dimension'] = ( float(line[1]), float(line[2][:-1]) )
        sensors[roomID]['sensor']   = []
        sensors[roomID]['door']   = {}
      elif 'door' in line[0]: # add door information
        try:
          sensors[roomID]['door'][line[3]] = (float(line[1]), float(line[2]))
        except:
          print "'door' format error"
          print line
          sys.exit(1)
      else: # append sensors
        try:
          try:
            r = float(line[3])
          except:
            r = line[3]
          sensors[roomID]['sensor'].append( (line[0], float(line[1]), float(line[2]), r ) )
        except:
          print "'sensor' format error:"
          print line
          sys.exit(1)

  facts1 = []
  facts2 = []

  facts3 = []
  facts4 = []

  facts5 = []
  facts6 = []
  for k in sensors.keys():
    for r in sensors[k]['sensor']:
      # save sensor location - for motion sensors
      facts1.append( sensorLocation + "(" + r[0] + ", " + k + ")." )
      # if this is item or activity sensor - remember additional activity fixed to sensor
      if type(r[3]) == str: # item sensor
        facts2.append( sensorActivity + "(" + r[0] + ", " + r[3] + ")." )

        facts3.append( itemSensorInRoom + "(" + r[0] + ", " + k + ")." )

        facts6.append( deviceIDs + "(" + r[3] + ")." )
      elif type(r[3]) == float: # motion sensor
        facts4.append( motionSensorInRoom + "(" + r[0] + ", " + k + ")." )
      else: # unknown sensor
        print "Unknown sensor type!"
        sys.exit(1)

      facts5.append( sensorIDs + "(" + r[0] + ")." )

  with open(bgFilename, 'ab') as bgfile:
      bgfile.write('\n')
      bgfile.write('\n'.join(facts1))
      bgfile.write('\n\n')
      bgfile.write('\n'.join(facts2))
      bgfile.write('\n\n')
      bgfile.write('\n'.join(facts3))
      bgfile.write('\n\n')
      bgfile.write('\n'.join(facts4))
      bgfile.write('\n\n')
      bgfile.write('\n'.join(facts5))
      bgfile.write('\n\n')
      bgfile.write('\n'.join(facts6))
      bgfile.write('\n')

  return sensors


# generate entries to update sensor readings
def updateOutput(activated, now):
  readings = []
  outDet = []
  for unit in activated:
    # compose entry
    ppp = now.strftime( "%Y-%m-%d %H:%M:%S.%f" ) + " " + unit[0] + " " + unit[1]
    # append to outputData vector
    readings.append( ppp )

    # get output details
    outDet.append( getOutputDetails(unit[0], unit[1], now) )
  return (readings, outDet)


# move within one room
def moveWithinRoom(tt, current_position, target_position, now, generators, sensors, current):
  # sensors readings
  readings = []
  readingsDetails = []
  # Check if you're already there
  if current_position == target_position:
    neededSteps = -1
    activated = tt.motionSensorsOn(current_position)
    # append new activities
    (rs, rsd) = updateOutput(activated, now)
    readings += rs
    readingsDetails += rsd
  else:
    ## search the path
    xa, xb, ya, yb = current_position[0], target_position[0], current_position[1], target_position[1]
    ## get momentum
    momentumX, momentumY = xb-xa, yb-ya

    # what if you move VERTICALLY: temporary workaround -- rotate 90o
    if momentumX == 0:
      xa, xb, ya, yb = ya, yb, xa, xb

    ## TODO: for the moment it is straight line between origin and goal - can be randomised a bit
    slope       = (ya-yb) / (xa-xb)
    intercept   = ya - slope * xa
    ### find the length of path
    distance    = sqrt( (xb-xa)**2 + (yb-ya)**2 )
    ### divide step-wise based on *stepSize*
    #### get stepSize
    stepSize = generators['stepSize']()
    neededSteps = int(ceil( distance / stepSize ))

  ### do steps
  for i in range(neededSteps):

    ### after each step check whether new sensor is activated
    activated = tt.updateMotionSensor(current_position)
    # append new activities
    (rs, rsd) = updateOutput(activated, now)
    readings += rs
    readingsDetails += rsd

    # find new position
    ## increment step along distance form *current* towards *target*
    if momentumX > 0 or momentumX < 0:
      if momentumX > 0:
        x = current_position[0] + sqrt( stepSize**2 / (slope**2 +1) )
        y = slope * x + intercept
      elif momentumX < 0:
        x = current_position[0] - sqrt( stepSize**2 / (slope**2 +1) )
        y = slope * x + intercept

      #Trim new position to room size
      if x > sensors[current]['dimension'][0]:
        x = sensors[current]['dimension'][0]
        y = slope * x + intercept
      elif x < 0:
        x = 0
        y = slope * x + intercept
      if y > sensors[current]['dimension'][1]:
        y = sensors[current]['dimension'][1]
        x = (y - intercept) / slope
      elif y < 0:
        y  = 0
        x = (y - intercept) / slope

    elif momentumX == 0: # what if you move VERTICALLY
      if momentumY > 0:
        y = current_position[1] + sqrt( stepSize**2 / (slope**2 +1) )
        x = slope * y + intercept
      elif momentumY < 0:
        y = current_position[1] - sqrt( stepSize**2 / (slope**2 +1) )
        x = slope * y + intercept
      else:
        print "Internal error: panic attack!"
        sys.exit(1)

      #Trim new position to room size: possible error?
      if y > sensors[current]['dimension'][1]:
        y = sensors[current]['dimension'][1]
        x = slope * y + intercept
      elif y < 0:
        y  = 0
        x = slope * y + intercept
      if x > sensors[current]['dimension'][0]:
        x = sensors[current]['dimension'][0]
        y = (x - intercept) / slope
      elif x < 0:
        x = 0
        y = (x - intercept) / slope

    else:
      print "Internal error: panic attack!"
      sys.exit(1)

    # Trim new position to room size
    if x > sensors[current]['dimension'][0]:
      x = sensors[current]['dimension'][0]
      print "Warning: aftershave!"
    elif x < 0:
      x = 0
      print "Warning: aftershave!"
    if y > sensors[current]['dimension'][1]:
      y = sensors[current]['dimension'][1]
      print "Warning: aftershave!"
    elif y < 0:
      y  = 0
      print "Warning: aftershave!"

    # save position
    current_position = (x, y)

    # update time
    stepTime = generators['stepTime']()
    days, seconds, miliseconds = 0, stepTime, 0
    now += datetime.timedelta(days, seconds, miliseconds)

  # Update sensors after location trimming
  ### after each step check whether new sensor is activated
  activated = tt.updateMotionSensor(current_position)
  # append new activities
  (rs, rsd) = updateOutput(activated, now)
  readings += rs
  readingsDetails += rsd
  # update time
  stepTime = generators['stepTime']()
  days, seconds, miliseconds = 0, stepTime, 0
  now += datetime.timedelta(days, seconds, miliseconds)

  return (readings, current_position, now, readingsDetails)


# change data into microsecond stamp
def handleDate(s):
  # d = ['2015-03-11 21:21:11', '471417']
  d = ' '.join(s.split(' ')[:2])
  return datetime.datetime.strptime( d, "%Y-%m-%d %H:%M:%S.%f" )


def getOutputDetails(sensor, state, now):
  tsn = time.mktime(now.timetuple())
  # append nano seconds and convert to microseconds
  tsn *= 1000000
  tsn += now.microsecond
  tsn = int(tsn)
  s = True if state == 'true' else False
  return (sensor, s, tsn)


# pathfinder
def pathFinder(roomLayout, generators, pathpp, sensors, dicKey, startTime):
  def getPerson(sp):
    if sp == "":
      return sp
    else:
      return ", " + sp[0].lower() + sp[1:]

  if type(pathpp) == dict:
    # path = pathpp.pop(dicKey, None)
    path = pathpp[dicKey]
    persona = getPerson( dicKey )
    detailedOutput = []
  else:
    path = pathpp
    persona = ""
    detailedOutput = None

  ## initialise location variables
  current = None
  ## initialise sensor watchdog
  tt = None
  ## remember previous position
  previous_position = None
  ## time increment for block: act{...}act
  blockIncrements = []
  # initialise time
  if type(startTime) != datetime.datetime:
    now = theVeryBegining = datetime.datetime.now()
  else:
    now = theVeryBegining = startTime
  ## get output data stream
  outputSensorData = []
  ## get output data stream for Prolog ground truth
  bindLocationTime = []
  bindActivityTime = []
  ## memorise activities facts
  activityFacts = []
  ## memorise activities ground truth: positives and negative
  activityPosNeg = []
  for move in path:
    if   move[0] == 'origin': # location
      current = move[1]
      # get position in start room with cm accuracy
      ## get dimensions
      dims = sensors[current]['dimension']
      ## change from meters to cent-meters
      dims = tuple( [100*x for x in dims] )
      ## get random position
      current_position = ( float(randint(0, dims[0]))/100.0, float(randint(0, dims[1]))/100.0 )


      # Now you are in new room but haven't moved yet: check sensors
      tt = monitor(current, sensors[current]['sensor'])
      activated = tt.updateMotionSensor(current_position)
      # append new activities
      (ua, uwn) = updateOutput(activated, now)
      if detailedOutput != None:
        detailedOutput += uwn
      ###
      # generate Prolog ground truth of locations: DO NOT MOVE
      bindLocationTime += nowInRoom(now, theVeryBegining, len(outputSensorData), current, persona)
      ##DONOTMOVE
      if len(ua) != 0:
        dt = handleDate(ua[0])
        ## mark beginning of activity block: needed to get true values
        while len(blockIncrements) > 0:
          trueValue = blockIncrements.pop(0)
          bindActivityTime += activityToTime( dt, theVeryBegining, len(outputSensorData), trueValue[0], trueValue[1], persona )

          # memorise activity start & end for PosNeg generation #Aleph
          gtt = generateTimeTuple(dt, theVeryBegining, len(outputSensorData))
          activityPosNeg.append( (trueValue[0], trueValue[1], gtt, persona) )
      ##DONOTMOVE
      outputSensorData += ua
    elif move[0] == 'go': # location
      # move from current to new_location
      ## Find path in adjacency matrix -- BFS
      goal  = move[1]
      # queue contains tuples indicating paths
      queue = [ [current] ]
      # get paths through adjacency matrix
      solutions = []
      while len(queue) != 0:
        # get first element
        q  = queue.pop(-1)
        qL = q[-1]
        # find connected rooms and no backsies
        newLevel = [room for room in roomLayout[qL].keys() if roomLayout[qL][room] and room not in q ]
        # check if any of this is a solution
        if goal in newLevel:
          # solution is found
          solutions.append( q + [goal] )
          # TODO if there are no cycles goal can be removed form *newLevel*
        # append  newbies
        partialPaths = [q+[r] for r in newLevel]
        # in this order to preserve BFS
        queue = partialPaths + queue

      ## Go through all needed rooms in given order: aim at door - Cartesian
      # TODO: if no cycles only one solution should be returned
      # TODO: it doesn't matter - the shortest is chosen
      sequence = solutions[0]

      # get start of route
      if sequence.pop(0) != current:
        print "Internal error: origin does not match!"
        sys.exit(1)

      for room in sequence:
        # initialise truth table for current location
        ## check if already initialised
        if tt != None:
          # check if it is already the room you are in
          if current == tt.getLocation(): # it is already initialised to the location you are in
            pass # you're already there do not change *monitor*: tt=tt
            # remember to clean the room on exit
          else: # initialise new as room does not match
            # clean old room
            # on room exit switch off sensors which havent switched off & are within you range
            activated = tt.motionSensorsOn(previous_position)
            # append new activities
            (ua, uwn) = updateOutput(activated, now)
            if detailedOutput != None:
              detailedOutput += uwn
            ##DONOTMOVE
            if len(ua) != 0:
              dt = handleDate(ua[0])
              ## mark beginning of activity block: needed to get true values
              while len(blockIncrements) > 0:
                trueValue = blockIncrements.pop(0)
                bindActivityTime += activityToTime( dt, theVeryBegining, len(outputSensorData), trueValue[0], trueValue[1], persona )

                # memorise activity start & end for PosNeg generation #Aleph
                gtt = generateTimeTuple(dt, theVeryBegining, len(outputSensorData))
                activityPosNeg.append( (trueValue[0], trueValue[1], gtt, persona) )
            ##DONOTMOVE
            outputSensorData += ua
            # initialise new room

            # generate Prolog ground truth of locations: DO NOT MOVE
            bindLocationTime += nowInRoom(now, theVeryBegining, len(outputSensorData), current, persona)

            tt = monitor(current, sensors[current]['sensor'])
        else:
          tt = monitor(current, sensors[current]['sensor'])

          # generate Prolog ground truth of locations: DO NOT MOVE
          bindLocationTime += nowInRoom(now, theVeryBegining, len(outputSensorData), current, persona)

        # go from location in previous to door to *room*
        ## find location of door
        target_position = sensors[current]['door'][room]

        # move within a room
        (readings, current_position, now, uwnn) = moveWithinRoom(tt, current_position, target_position, now, generators, sensors, current)
        if detailedOutput != None:
          detailedOutput += uwnn
        ##DONOTMOVE
        if len(readings) != 0:
          dt = handleDate(readings[0])
          ## mark beginning of activity block: needed to get true values
          while len(blockIncrements) > 0:
            trueValue = blockIncrements.pop(0)
            bindActivityTime += activityToTime( dt, theVeryBegining, len(outputSensorData), trueValue[0], trueValue[1], persona )

            # memorise activity start & end for PosNeg generation #Aleph
            gtt = generateTimeTuple(dt, theVeryBegining, len(outputSensorData))
            activityPosNeg.append( (trueValue[0], trueValue[1], gtt, persona) )
        ##DONOTMOVE
        outputSensorData += readings

        # memorise last position in previous room
        previous_position = current_position
        ## remember to position at door when going to next room
        current_position = sensors[room]['door'][current] #target_position
        # memorise current location - use later to navigate to activity
        current          = room


      # Check whether old room has been cleaned
      activated = tt.motionSensorsOn(previous_position)
      # append new activities
      (ua, uwn) = updateOutput(activated, now)
      if detailedOutput != None:
        detailedOutput += uwn
      ##DONOTMOVE
      if len(ua) != 0:
        dt = handleDate(ua[0])
        ## mark beginning of activity block: needed to get true values
        while len(blockIncrements) > 0:
          trueValue = blockIncrements.pop(0)
          bindActivityTime += activityToTime( dt, theVeryBegining, len(outputSensorData), trueValue[0], trueValue[1], persona )

          # memorise activity start & end for PosNeg generation #Aleph
          gtt = generateTimeTuple(dt, theVeryBegining, len(outputSensorData))
          activityPosNeg.append( (trueValue[0], trueValue[1], gtt, persona) )
      ##DONOTMOVE
      outputSensorData += ua

      # generate Prolog ground truth of locations: DO NOT MOVE
      bindLocationTime += nowInRoom(now, theVeryBegining, len(outputSensorData), current, persona)

      # Now you are in new room but haven't moved yet: check sensors
      tt = monitor(current, sensors[current]['sensor'])
      activated = tt.updateMotionSensor(current_position)
      # append new activities
      (ua, uwn) = updateOutput(activated, now)
      if detailedOutput != None:
        detailedOutput += uwn
      ##DONOTMOVE
      if len(ua) != 0:
        dt = handleDate(ua[0])
        ## mark beginning of activity block: needed to get true values
        while len(blockIncrements) > 0:
          trueValue = blockIncrements.pop(0)
          bindActivityTime += activityToTime( dt, theVeryBegining, len(outputSensorData), trueValue[0], trueValue[1], persona )

          # memorise activity start & end for PosNeg generation #Aleph
          gtt = generateTimeTuple(dt, theVeryBegining, len(outputSensorData))
          activityPosNeg.append( (trueValue[0], trueValue[1], gtt, persona) )
      ##DONOTMOVE
      outputSensorData += ua

      # check for reaching the target
      if current != goal:
        print "Path did not converge!"
        sys.exit(1)
    elif move[0] == 'do': # action: item & activity sensors
      # find position of sensor in current room
      (sensorID, target_position) = tt.getItemDetails(move[1])

      # move within a room: go to this position: remember to update current_position & previous_position !!!!
      (readings, current_position, now, uwnn) = moveWithinRoom(tt, current_position, target_position, now, generators, sensors, current)
      if detailedOutput != None:
        detailedOutput += uwnn
      ##DONOTMOVE
      if len(readings) != 0:
        dt = handleDate(readings[0])
        ## mark beginning of activity block: needed to get true values
        while len(blockIncrements) > 0:
          trueValue = blockIncrements.pop(0)
          bindActivityTime += activityToTime( dt, theVeryBegining, len(outputSensorData), trueValue[0], trueValue[1], persona )

          # memorise activity start & end for PosNeg generation #Aleph
          gtt = generateTimeTuple(dt, theVeryBegining, len(outputSensorData))
          activityPosNeg.append( (trueValue[0], trueValue[1], gtt, persona) )
      ##DONOTMOVE
      outputSensorData += readings


      # IN CASE YOU DIDN'T HAVE TO MOCE MEMORISE IT FOR SENSOR ACTIVITY
      ## mark beginning of activity block: needed to get true values
      while len(blockIncrements) > 0:
        trueValue = blockIncrements.pop(0)
        bindActivityTime += activityToTime( dt, theVeryBegining, len(outputSensorData), trueValue[0], trueValue[1], persona )

        # memorise activity start & end for PosNeg generation #Aleph
        gtt = generateTimeTuple(dt, theVeryBegining, len(outputSensorData))
        activityPosNeg.append( (trueValue[0], trueValue[1], gtt, persona) )


      # do the activity: emulate sensors
      ## save ground truth: ON
      bindActivityTime += activityToTime(now, theVeryBegining, len(outputSensorData), move[1], "true", persona)

      ## activate sensor
      activated = tt.activateItem(sensorID)
      ### append new activities
      (uaww, uwn) = updateOutput(activated, now)
      if detailedOutput != None:
        detailedOutput += uwn
      outputSensorData += uaww
      ## emulate activity time
      stepTime = generators[move[1]]()
      days, seconds, miliseconds = 0, stepTime, 0
      now += datetime.timedelta(days, seconds, miliseconds)

      ## save ground truth: OFF
      bindActivityTime += activityToTime(now, theVeryBegining, len(outputSensorData), move[1], "false", persona)

      ## turn of activity sensor
      activated = tt.deactivateItem(sensorID)
      ### append new activities
      (uaww, uwn) = updateOutput(activated, now)
      if detailedOutput != None:
        detailedOutput += uwn
      outputSensorData += uaww
    elif move[0] == 'start':
      # find position of sensor in current room
      (sensorID, target_position) = tt.getItemDetails(move[1])

      # move within a room: go to this position: remember to update current_position & previous_position !!!!
      (readings, current_position, now, uwnn) = moveWithinRoom(tt, current_position, target_position, now, generators, sensors, current)
      if detailedOutput != None:
        detailedOutput += uwnn
      ##DONOTMOVE
      if len(readings) != 0:
        dt = handleDate(readings[0])
        ## mark beginning of activity block: needed to get true values
        while len(blockIncrements) > 0:
          trueValue = blockIncrements.pop(0)
          bindActivityTime += activityToTime( dt, theVeryBegining, len(outputSensorData), trueValue[0], trueValue[1], persona )

          # memorise activity start & end for PosNeg generation #Aleph
          gtt = generateTimeTuple(dt, theVeryBegining, len(outputSensorData))
          activityPosNeg.append( (trueValue[0], trueValue[1], gtt, persona) )
      ##DONOTMOVE
      outputSensorData += readings


      # IN CASE YOU DIDN'T HAVE TO MOCE MEMORISE IT FOR SENSOR ACTIVITY
      ## mark beginning of activity block: needed to get true values
      while len(blockIncrements) > 0:
        trueValue = blockIncrements.pop(0)
        bindActivityTime += activityToTime( dt, theVeryBegining, len(outputSensorData), trueValue[0], trueValue[1], persona )

        # memorise activity start & end for PosNeg generation #Aleph
        gtt = generateTimeTuple(dt, theVeryBegining, len(outputSensorData))
        activityPosNeg.append( (trueValue[0], trueValue[1], gtt, persona) )


      # do the activity: emulate sensors
      ## save ground truth: ON
      bindActivityTime += activityToTime(now, theVeryBegining, len(outputSensorData), move[1], "true", persona)
      ## activate sensor
      activated = tt.activateItem(sensorID)
      ### append new activities
      (uaww, uwn) = updateOutput(activated, now)
      if detailedOutput != None:
        detailedOutput += uwn
      outputSensorData += uaww
    elif move[0] == 'stop':
      # find position of sensor in current room
      (sensorID, target_position) = tt.getItemDetails(move[1])

      # move within a room: go to this position: remember to update current_position & previous_position !!!!
      (readings, current_position, now, uwnn) = moveWithinRoom(tt, current_position, target_position, now, generators, sensors, current)
      if detailedOutput != None:
        detailedOutput += uwnn
      ##DONOTMOVE
      if len(readings) != 0:
        dt = handleDate(readings[0])
        ## mark beginning of activity block: needed to get true values
        while len(blockIncrements) > 0:
          trueValue = blockIncrements.pop(0)
          bindActivityTime += activityToTime( dt, theVeryBegining, len(outputSensorData), trueValue[0], trueValue[1], persona )

          # memorise activity start & end for PosNeg generation #Aleph
          gtt = generateTimeTuple(dt, theVeryBegining, len(outputSensorData))
          activityPosNeg.append( (trueValue[0], trueValue[1], gtt, persona) )
      ##DONOTMOVE
      outputSensorData += readings

      # IN CASE YOU DIDN'T HAVE TO MOCE MEMORISE IT FOR SENSOR ACTIVITY
      ## mark beginning of activity block: needed to get true values
      while len(blockIncrements) > 0:
        trueValue = blockIncrements.pop(0)
        bindActivityTime += activityToTime( dt, theVeryBegining, len(outputSensorData), trueValue[0], trueValue[1], persona )

        # memorise activity start & end for PosNeg generation #Aleph
        gtt = generateTimeTuple(dt, theVeryBegining, len(outputSensorData))
        activityPosNeg.append( (trueValue[0], trueValue[1], gtt, persona) )

      ## save ground truth: OFF
      bindActivityTime += activityToTime(now, theVeryBegining, len(outputSensorData), move[1], "false", persona)

      ## turn of activity sensor
      activated = tt.deactivateItem(sensorID)
      ### append new activities
      (uaww, uwn) = updateOutput(activated, now)
      if detailedOutput != None:
        detailedOutput += uwn
      outputSensorData += uaww
    elif move[0] == '{':
      # get yourself a space and prepare to get true values
      blockIncrements += [ (move[1], "true") ]

      # memorise facts
      memid = activityIDs + "(" + move[1] + ")."
      if not(memid in activityFacts):
        activityFacts.append( memid )
    elif move[0] == '}':
      # check whether there was any activity to mark the beginning
      beg = False
      for aa in bindActivityTime:
        if 'true' in aa and move[1] in aa:
          beg = True
          break
      # if no beginning found append it now
      if beg == False:
        print "WARNING: no support for beginning of activity for block!"
        bindActivityTime += activityToTime(now, theVeryBegining, len(outputSensorData)-1, move[1], "true", persona)
        # memorise activity start & end for PosNeg generation #Aleph
        gtt = generateTimeTuple(now, theVeryBegining, len(outputSensorData)-1)
        activityPosNeg.append( (move[1], 'true', gtt, persona) )
        # clean block beginning memory
        blockIncrements = []

      # mark end of activity block
      bindActivityTime += activityToTime(now, theVeryBegining, len(outputSensorData)-1, move[1], "false", persona)

      # memorise facts
      memid = activityIDs + "(" + move[1] + ")."
      if not(memid in activityFacts):
        activityFacts.append( memid )

      # memorise activity start & end for PosNeg generation #Aleph
      gtt = generateTimeTuple(now, theVeryBegining, len(outputSensorData)-1)
      activityPosNeg.append( (move[1], 'false', gtt, persona) )
    elif move[0] == 'wait':

      ## mark beginning of activity block: needed to get true values
      if len(blockIncrements) > 0:
        print "Command *wait* cannot be the first element of block!", move[1]
        sys.exit(1)

      ## emulate time
      ### if standard deviation is zero do not use randomness
      if float(move[1][1]) != 0.0:
        seconds = normal(move[1][0], move[1][1])
      else:
        seconds = move[1][0]
      days, miliseconds = 0, 0
      now += datetime.timedelta(days, seconds, miliseconds)
    elif move[0] == 'return':
      # find position of sensor in current room
      (sensorID, target_position) = tt.getItemDetails(move[1])

      # move within a room: go to this position: remember to update current_position & previous_position !!!!
      (readings, current_position, now, uwnn) = moveWithinRoom(tt, current_position, target_position, now, generators, sensors, current)
      if detailedOutput != None:
        detailedOutput += uwnn
      ##DONOTMOVE
      if len(readings) != 0:
        dt = handleDate(readings[0])
        ## mark beginning of activity block: needed to get true values
        while len(blockIncrements) > 0:
          trueValue = blockIncrements.pop(0)
          bindActivityTime += activityToTime( dt, theVeryBegining, len(outputSensorData), trueValue[0], trueValue[1], persona )

          # memorise activity start & end for PosNeg generation #Aleph
          gtt = generateTimeTuple(dt, theVeryBegining, len(outputSensorData))
          activityPosNeg.append( (trueValue[0], trueValue[1], gtt, persona) )
      ##DONOTMOVE
      outputSensorData += readings
    elif move[0] == 'wander':
      target_position = move[1]

      if target_position[0] == -1 and target_position[1] == -1:
        dims = sensors[current]['dimension']
        ## change from meters to cent-meters
        dims = tuple( [100*x for x in dims] )
        ## get random position
        target_position = ( float(randint(0, dims[0]))/100.0, float(randint(0, dims[1]))/100.0 )

      # move within a room: go to this position: remember to update current_position & previous_position !!!!
      (readings, current_position, now, uwnn) = moveWithinRoom(tt, current_position, target_position, now, generators, sensors, current)
      if detailedOutput != None:
        detailedOutput += uwnn
      ##DONOTMOVE
      if len(readings) != 0:
        dt = handleDate(readings[0])
        ## mark beginning of activity block: needed to get true values
        while len(blockIncrements) > 0:
          trueValue = blockIncrements.pop(0)
          bindActivityTime += activityToTime( dt, theVeryBegining, len(outputSensorData), trueValue[0], trueValue[1], persona )

          # memorise activity start & end for PosNeg generation #Aleph
          gtt = generateTimeTuple(dt, theVeryBegining, len(outputSensorData))
          activityPosNeg.append( (trueValue[0], trueValue[1], gtt, persona) )
      ##DONOTMOVE
      outputSensorData += readings
    else:
      print "Action: *", move[0], "* not recognised!"
      print "> ", move, " <"
      sys.exit(1)

  return (outputSensorData, bindLocationTime, bindActivityTime, activityFacts, activityPosNeg, detailedOutput)

# mark activity beginning and end in the data script
def markBE(activityPosNeg, outputSensorData):
  # add fifth sparse column to data - it indicates activities start and end
  for (iname, istate, imeasure, pID) in activityPosNeg:
    seq = imeasure[2]
    st = 'begin' if istate == 'true' else 'end'
    # depending on one or multiple residents
    if pID == "":
      addon = ' ' + iname + ' ' + st
    else:
      # remove comma from personID
      addon = ' ' + pID[2:] + "_" + iname + ' ' + st
    outputSensorData[seq] += addon

  return outputSensorData

# generate positives and negatives - generate only for *sequence*
def posNegGen(activityPosNeg_, outputSensorData_):
  activityPosNeg   = activityPosNeg_[:]
  outputSensorData = outputSensorData_[:]
  pos = []
  neg = []
  farEnd = len(outputSensorData)
  while len(activityPosNeg) != 0:
    # get first
    a = []
    a += [activityPosNeg.pop(0)]
    # find all the rest of the activity
    for i in range(len(activityPosNeg))[::-1]:
      if activityPosNeg[i][0] == a[0][0]:
        a.append( activityPosNeg.pop(i) )

    # for the moment forbid the same activity repeated within one file
    # or the list does not start with *{* and finishes with *}*
    if len(a) != 2 or a[0][1] != 'true' or a[1][1] != 'false':
      print "The same block name used more than once: *", a[0][0], "* !"
      print "or"
      print "Wrong block structure!"
      print ">\n", a
      sys.exit(1)

    # use only *sequence*
    beginning = a[0][2][2]
    end = a[1][2][2]
    # generate for all the events
    for i in range(beginning):
      neg.append( activityRule + "(" + a[0][0] + ", " + str(i) + a[0][3] + ")." )
    for i in range(beginning, end):
      pos.append( activityRule + "(" + a[0][0] + ", " + str(i) + a[0][3] + ")." )
    for i in range(end, farEnd):
      neg.append( activityRule + "(" + a[0][0] + ", " + str(i) + a[0][3] + ")." )
    ## generate for one event with range
    # neg.append( activityRule + "(" + a[0][0] + ", " + str(0) + ", " + str(beginning-1) + ")." )
    # pos.append( activityRule + "(" + a[0][0] + ", " + str(beginning) + ", " + str(end-1) + ")." )
    # neg.append( activityRule + "(" + a[0][0] + ", " + str(end) + ", " + str(farEnd) + ")." )

  return (pos, neg)

if __name__ == '__main__':
  # Check whether file is given as argument
  args = parser.parse_args()
  Fadj, Flay, Fact, Fpath = args.adjacency[0], args.layout[0], args.activities[0], args.path[0]
  if args.time != None:
    inputTime = datetime.datetime.strptime(args.time[0], "%B %d %Y %H.%M")
  else:
    inputTime = args.time

  # args = sys.argv
  # if len(args) != 5:
    # # Fail
    # print "No files specified."
    # print "usage: constructFacts.py path/to/adjacency path/to/activities path/to/path path/to/layout"
    # sys.exit(1)
  # # load files
  # Fadj, Flay, Fact, Fpath  = args[1], args[2], args[3], args[4]

  # read in house specification
  roomLayout = rooms( Fadj )
  generators = activities( Fact )
  path = path( Fpath )
  sensors = layout( Flay, roomLayout.keys() )

  persons = path.keys() if type(path) == dict else []
  # assign locations to sensor for Prolog ground truth
  itemToLocation(sensors, persons)

  # generate random paths with timestamps
  ## e.g. "2008-03-28 13:39:01.470516 M01 ON"
  # do path finding: (outputSensorData, bindLocationTime, bindActivityTime, activityFacts, activityPosNeg)
  outputDic = None
  if type(path) == list:
    # check correctness of input
    if path[0][0] != 'origin':
      print "First action is not 'origin'!"
      sys.exit(1)

    # extract sensors
    (outputSensorData, bindLocationTime, bindActivityTime, activityFacts, activityPosNeg, detailedOutput) = pathFinder(roomLayout, generators, path, sensors, "", inputTime)
    ## update sensor output with activity indicators
    outputSensorData = markBE(activityPosNeg, outputSensorData)
    ## generate positives and negatives
    (pos, neg) = posNegGen(activityPosNeg, outputSensorData)

  elif type(path) == dict:
    # check correctness of input
    for key in path:
      if path[key][0][0] != 'origin':
        print "First action of " + key + " is not 'origin'!"
        sys.exit(1)

    # extract sensors
    outputDic = {}
    # outputDic => pos | neg X
    posnegDic = {}
    pos = None
    neg = None
    bindActivityTime = None
    bindLocationTime = None
    #
    activityFacts = []

    for key in path:
      odi = pathFinder(roomLayout, generators, path, sensors, key, inputTime)
      outputDic[key] = odi

    # mash-up the output and overwrite (outputSensorData, bindLocationTime, bindActivityTime, activityFacts, activityPosNeg, detailedOutput)
    allTheTimes = []
    for key in outputDic:
      ## get time information
      for tms in outputDic[key][5]:
        allTheTimes.append( tms[2] )

      ## update sensor output with activity indicators
      osd = markBE(outputDic[key][4], outputDic[key][0][:])
      del outputDic[key][0][:]
      outputDic[key][0].extend(osd)

      # generate positives and negatives
      posnegDic[key] = posNegGen(outputDic[key][4], outputDic[key][0])

      # combine activity facts
      activityFacts += list(set(outputDic[key][3]) - set(activityFacts))

      # print key, ": ", len(outputDic[key][0]); pprint( outputDic[key][0] ); print "\n"

    # remove duplicates
    allTheTimes = list(set(allTheTimes))
    # and sort
    allTheTimes.sort()



    # merge data
    ## create sensor supervisor
    sensorSupervisor = {} # (state, #)
    ##### memorise only [key] & [index]
    keyInd = [] # (key, index)
    ## memorise activity markings lost in merge
    mergedActivities = []
    #
    outputSensorData = []
    for tms in allTheTimes: # allTiems => outputsensordata
      # find all sensor activity happening at that moment
      for key in outputDic:
        # get IDs of the element
        for i, (sr, se, te) in enumerate(outputDic[key][5]):
          if te < tms:
            continue
          elif te > tms:
            break

          # memorise sensors changes
          ## if change or not_exists: add to list | else pass
          try:
            if sensorSupervisor[sr][0] == se: #se - swap T->F or F->T
              # add another entry
              sensorSupervisor[sr] = (se, sensorSupervisor[sr][1]+1)
              #!!!!!!!!!!what if multiple things happen and reading is discarded
              sptd = outputDic[key][0][i].split()
              if len(sptd) >= 6:
                mergedActivities.append( (len(keyInd)-1, sptd[4:]) )
            else: # != se
              if sensorSupervisor[sr][1] > 1:
                # discard reading: more than 1 person in range
                sensorSupervisor[sr] = (sensorSupervisor[sr][0], sensorSupervisor[sr][1]-1)
                #!!!!!!!!!!what if multiple things happen and reading is discarded
                sptd = outputDic[key][0][i].split()
                if len(sptd) >= 6:
                  mergedActivities.append( (len(keyInd)-1, sptd[4:]) )
              elif sensorSupervisor[sr][1] == 1:
                sensorSupervisor[sr] = (None, sensorSupervisor[sr][1]-1)
                keyInd.append( (key, i) )
              elif sensorSupervisor[sr][1] == 0 and sensorSupervisor[sr][0] == None:
                sensorSupervisor[sr] = (se, 1)
                keyInd.append( (key, i) )
              elif sensorSupervisor[sr][1] <= 0:
                print "Data error: One to many!"
                sys.exit(1)

          except KeyError: #not_exists
            # add
            sensorSupervisor[sr] = (se, 1)
            keyInd.append( (key, i) )

    ## introduce readings to outputSensorData
    for k, i in keyInd:
      outputSensorData.append( outputDic[k][0][i] )
    ## fix any outstanding activity beg/end markings
    for k, l in mergedActivities:
      outputSensorData[k] += ' ' + ' '.join(l)

    # print "all: ", len(outputSensorData); pprint( outputSensorData ); print "\n"

  else:
    print "Weird error #803, please contact support."
    sys.exit(1)

  # Write positive and negative examples
  if args.facts:
    if pos != None:
      with open(posFilename, 'wb') as pf:
        pf.write( '\n'.join(pos) )
        pf.write('\n')
    if neg != None:
      with open(negFilename, 'wb') as nf:
        nf.write( '\n'.join(neg) )
        nf.write('\n')

  # write down Prolog rules
  with open(bgFilename, 'ab') as bgf:
    bgf.write('\n')
    bgf.write( '\n'.join(activityFacts) )
    if bindActivityTime != None:
      bgf.write('\n\n')
      bgf.write( '\n'.join(bindActivityTime) )
    if bindLocationTime != None:
      bgf.write('\n\n')
      bgf.write( '\n'.join(bindLocationTime) )
    bgf.write('\n')

  # write generated data to file
  with open(dataFilename, 'wb') as datafile:
    datafile.write('\n'.join(outputSensorData))
    datafile.write('\n')
