#! /usr/local/bin/python

import sys
import csv
import datetime
import time
from numpy.random import normal
from math import sqrt, ceil
from random import randint
from pprint import pprint

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
    if self.truthTable['item'][sensorID]['status'] != False:
      print "Item sensor state error A: ", sensorID
      sys.exit(1)
    self.truthTable['item'][sensorID]['status'] = True
    sensorState = 'true'
    return [(sensorID, sensorState)]

  def deactivateItem(self, sensorID):
    if self.truthTable['item'][sensorID]['status'] != True:
      print "Item sensor state error D-A: ", sensorID
      sys.exit(1)
    self.truthTable['item'][sensorID]['status'] = False
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

# Constants
nl = '\n'
fact = '__'
rev  = '_'

interconnected = connected + "(A, B, Path) :-" + nl + "  " + connected + "(A, B, [], Path)."
interconnected += nl + connected + "(A, B, V, Path) :-" + nl
interconnected += "  " + connected + rev + "(A, X), not( member(X, V) )," + nl
interconnected += "  (" + nl + "    " + "B = X, reverse([B,A|V], Path)" + nl + "  " + "; " + connected
interconnected += "(X, B, [A|V], Path)" + nl + "  " + "), !." + nl + nl

interchangable  = connected + rev + "(A, B) :-" + nl + "  " + connected + fact
interchangable += "(A, B); " + connected + fact + "(B, A)." + nl + nl

# check where you are
whereAmI  = atLocation + "(Room, Time, TimeType) :-" + nl
whereAmI += "  %% there is presence in given room at some time T..." + nl
whereAmI += "  " + spaceTime + "(Room, TimeType, T)," + nl
whereAmI += "  %% ...which is before our time of interest..." + nl
whereAmI += "  T =< Time," + nl
whereAmI += "  %% ...and we do not move to any other room between *Time* and *T*" + nl
whereAmI += "  \\+" + atLocation + rev + "(Room, TimeType, T, Time), !." + nl + nl
########
whereAmI += atLocation + rev + "(Room, TimeType, T1, T2) :-" + nl
whereAmI += "  " + spaceTime + "(OtherRoom, TimeType, Tbound)," + nl
whereAmI += "  \\+(OtherRoom = Room)," + nl
whereAmI += "  T1 =< Tbound, Tbound =< T2." + nl + nl

whatIDo  = atActivity + "(Activity, Time, TimeType) :-" + nl
whatIDo += "  %% the activity is held at some time T..." + nl
whatIDo += "  " + currentActivity + "(Activity, true, TimeType, T1)," + nl
whatIDo += "  %% ...which started now or before our time of interest..." + nl
whatIDo += "  T1 =< Time," + nl
whatIDo += "  %% ... and has not ended yet." + nl
whatIDo += "  \\+" + atActivity + rev + "(Activity, Time, TimeType)." + nl + nl
#######
whatIDo += atActivity + rev + "(Activity, Time, TimeType) :-" + nl
whatIDo += "  " + currentActivity + "(Activity, false, TimeType, T)," + nl
whatIDo += "  T =< Time." + nl + nl

# Background knowledge file-name
bgFilename = "bg.pl"

# generated data file-name
dataFilename = "data.txt"

# Define functions

# assign activity/item sensor to motion field sensor
def itemToLocation(sensors):
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

  # write to file
  with open(bgFilename, 'ab') as bg:
    bg.write( '\n' )
    bg.write( '\n'.join(readings) )
    bg.write( '\n' )


# append current activity to ground truth
def activityToTime(now, origin, sequence, activity, state):
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
  facts.append( currentActivity + "(" + activity + ", " + state + ", " + "relative, " + t[0] + ")." )
  facts.append( currentActivity + "(" + activity + ", " + state + ", " + "absolute, " + t[1] + ")." )
  facts.append( currentActivity + "(" + activity + ", " + state + ", " + "sequence, " + t[2] + ")." )
  facts.append( currentActivity + "(" + activity + ", " + state + ", " + "windowed, " + t[3] + ")." )

  return facts


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
def nowInRoom(now, origin, sequence, current):
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
  facts.append( spaceTime + "(" + current + ", " + "relative, " + t[0] + ")." )
  facts.append( spaceTime + "(" + current + ", " + "absolute, " + t[1] + ")." )
  facts.append( spaceTime + "(" + current + ", " + "sequence, " + t[2] + ")." )
  facts.append( spaceTime + "(" + current + ", " + "windowed, " + t[3] + ")." )

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

  facts = [interconnected, interchangable, whereAmI, whatIDo]
  keys1 = layout.keys()
  keys2 = layout.keys()
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
  with open(Fpath, 'rb') as pathfile:
    for line in pathfile:
      line = line.strip('\n')
      # strip spaces at the beginning
      line = line[::-1]
      line = line.strip(' ')
      line = line[::-1]
      # check for comment or empty line
      if line == "":
        continue
      if line[0] == ';':
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
        print "Path error: wrong format"
        sys.exit(1)
      command = line[:f1]
      argument = line[f1+1:f2]
      # if there is comma in the argument it must be wait command
      if command == 'wait':
        # find comma
        f3 = argument.find(',')
        if f3 == -1:
          print "Command wait has wrong argument: no comma in: ", argument
          sys.exit(1)
        argument1 = argument[:f3]
        argument2 = argument[f3+1:]
        argument = (float(argument1), float(argument2))
      # append tuple to path
      path.append( (command, argument) )

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
  for k in sensors.keys():
    for r in sensors[k]['sensor']:
      # save sensor location - for motion sensors
      facts1.append( sensorLocation + "(" + r[0] + ", " + k + ")." )
      # if this is item or activity sensor - remember additional activity fixed to sensor
      if type(r[3]) == str:
        facts2.append( sensorActivity + "(" + r[0] + ", " + r[3] + ")." )

  with open(bgFilename, 'ab') as bgfile:
      bgfile.write('\n')
      bgfile.write('\n'.join(facts1))
      bgfile.write('\n\n')
      bgfile.write('\n'.join(facts2))
      bgfile.write('\n')

  return sensors

# generate entries to update sensor readings
def updateOutput(activated, now):
  readings = []
  for unit in activated:
    # compose entry
    ppp = now.strftime( "%Y-%m-%d %H:%M:%S.%f" ) + " " + unit[0] + " " + unit[1]
    # append to outputData vector
    readings.append( ppp )
  return readings

# move within one room
def moveWithinRoom(tt, current_position, target_position, now, generators, sensors):
  # sensors readings
  readings = []
  # Check if you're already there
  if current_position == target_position:
    neededSteps = -1
    activated = tt.motionSensorsOn(current_position)
    # append new activities
    readings += updateOutput(activated, now)
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
    readings += updateOutput(activated, now)

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
    else:
      print "Internal error: panic attack!"
      sys.exit(1)
    
    
    
    # Trim new position to room size
    if x > sensors[current]['dimension'][0]:
      x = sensors[current]['dimension'][0]
    elif x < 0:
      x = 0
    if y > sensors[current]['dimension'][1]:
      y = sensors[current]['dimension'][1]
    elif y < 0:
      y  = 0
    # save position
    current_position = (x, y)

    # update time
    stepTime = generators['stepTime']()
    days, seconds, miliseconds = 0, stepTime, 0
    now += datetime.timedelta(days, seconds, miliseconds)

  return (readings, current_position, now)

if __name__ == '__main__':
  # Check whether file is given as argument
  args = sys.argv
  if len(args) != 5:
    # Fail
    print "No files specified."
    print "usage: constructFacts.py path/to/adjacency path/to/activities path/to/path path/to/layout"
    sys.exit(1)

  # load files
  Fadj, Fact, Fpath, Flay = args[1], args[2], args[3], args[4]

  # read in house specification
  roomLayout = rooms( Fadj )
  generators = activities( Fact )
  path = path( Fpath )
  sensors = layout( Flay, roomLayout.keys() )

  # assign locations to sensor for Prolog ground truth
  itemToLocation(sensors)

  # generate random paths with timestamps
  ## e.g. "2008-03-28 13:39:01.470516 M01 ON"
  if path[0][0] != 'start':
    print "First action is not 'start'!"
    sys.exit(1)
  ## initialise location variables
  current = None
  ## initialise sensor watchdog
  tt = None
  ## remember previous position
  previous_position = None
  ## time increment for block: act{...}act 
  blockIncrementsCounter = 0
  blockIncrements1 = []
  blockIncrements2 = []
  # initialise time
  now = theVeryBegining = datetime.datetime.now()
  ## get output data stream
  outputSensorData = []
  ## get output data stream for Prolog ground truth
  bindLocationTime = []
  bindActivityTime = []
  # TODO: Add prior posterior for the directions!!!!!!
  for move in path:
    if   move[0] == 'start': # location
      current = move[1]
      # get position in start room with cm accuracy
      ## get dimensions
      dims = sensors[current]['dimension']
      ## change from meters to cent-meters
      dims = tuple( [100*x for x in dims] )
      ## get random position
      current_position = ( float(randint(0, dims[0]))/100.0, float(randint(0, dims[1]))/100.0 )
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
            outputSensorData += updateOutput(activated, now)
            # initialise new room

            # generate Prolog ground truth of locations: DO NOT MOVE
            bindLocationTime += nowInRoom(now, theVeryBegining, len(outputSensorData), current)

            tt = monitor(current, sensors[current]['sensor'])
        else:
          tt = monitor(current, sensors[current]['sensor'])
          
          # generate Prolog ground truth of locations: DO NOT MOVE
          bindLocationTime += nowInRoom(now, theVeryBegining, len(outputSensorData), current)

        # go from location in previous to door to *room*
        ## find location of door
        target_position = sensors[current]['door'][room]

        # move within a room
        (readings, current_position, now) = moveWithinRoom(tt, current_position, target_position, now, generators, sensors)
        outputSensorData += readings

        # memorise last position in previous room
        previous_position = current_position
        ## remember to position at door when going to next room
        current_position = sensors[room]['door'][current] #target_position
        # memorise current location - use later to navigate to activity
        current          = room


      # Check whether old room has been cleaned
      print "Gerronimo, ", previous_position
      pprint(tt.display())
      activated = tt.motionSensorsOn(previous_position)
      pprint(tt.display())
      # append new activities
      outputSensorData += updateOutput(activated, now)

      # generate Prolog ground truth of locations: DO NOT MOVE
      bindLocationTime += nowInRoom(now, theVeryBegining, len(outputSensorData), current)

      # Now you are in new room but haven't moved yet: check sensors
      tt = monitor(current, sensors[current]['sensor'])
      activated = tt.updateMotionSensor(current_position)
      # append new activities
      outputSensorData += updateOutput(activated, now)

      # check for reaching the target
      if current != goal:
        print "Path did not converge!"
        sys.exit(1)
    elif move[0] == 'do': # action: item & activity sensors
      # find position of sensor in current room
      (sensorID, target_position) = tt.getItemDetails(move[1])

      # go to this position: remember to update current_position & previous_position
      # move within a room
      print move[1], " : ", sensorID, " : ", target_position
      (readings, current_position, now) = moveWithinRoom(tt, current_position, target_position, now, generators, sensors)
      outputSensorData += readings

      # do the activity: emulate sensors
      ## save ground truth: ON
      bindActivityTime += activityToTime(now, theVeryBegining, len(outputSensorData), move[1], "true")

      ## mark begining of activity block: needed to get true values
      for trueValue in range(blockIncrementsCounter):
        blockIncrements1.append( (now, theVeryBegining, len(outputSensorData)) )
      blockIncrementsCounter = 0

      ## activate sensor
      activated = tt.activateItem(sensorID)
      ### append new activities
      outputSensorData += updateOutput(activated, now)
      ## emulate activity time
      stepTime = generators[move[1]]()
      days, seconds, miliseconds = 0, stepTime, 0
      now += datetime.timedelta(days, seconds, miliseconds)

      ## save ground truth: OFF
      bindActivityTime += activityToTime(now, theVeryBegining, len(outputSensorData), move[1], "false")

      ## turn of activity sensor
      activated = tt.deactivateItem(sensorID)
      ### append new activities
      outputSensorData += updateOutput(activated, now)
    elif move[0] == 'start':
      pass
    elif move[0] == 'stop':
      pass
    elif move[0] == '{':
      # get yourself a space and prepare to get true values
      bindActivityTime += [-1] #activityToTime(-1, -1, -1, move[1], "true")
      blockIncrements2 += [ (move[1], "true") ]
      blockIncrementsCounter += 1
    elif move[0] == '}':
      # mark end of activity block
      bindActivityTime += activityToTime(now, theVeryBegining, len(outputSensorData)-1, move[1], "false")
    elif move[0] == 'wait':
      ## emulate time
      seconds = normal(move[1][0], move[1][1])
      days, miliseconds = 0, 0
      now += datetime.timedelta(days, seconds, miliseconds)
    else:
      print "Action is not 'start', 'go', 'do'!"
      print "> ", move, " <"
      sys.exit(1)

  # update block activities with true values
  # check filler completeness
  if len(blockIncrements1) != len(blockIncrements2) or blockIncrementsCounter != 0:
    print "Filler part does not agree! ", blockIncrementsCounter
    sys.exit(1)
  quickFix = []
  for counter, item in enumerate(bindActivityTime):
    # fill gap if missing
    if item == -1:
      quickFix.append(counter)

  quickFix.reverse() # reverse to pre... indexing
  blockIncrements1.reverse()
  blockIncrements2.reverse()
  for qf in quickFix:
    p1 = blockIncrements1.pop(0)
    p2 = blockIncrements2.pop(0)
    bindActivityTime.pop(qf)
    appendix = activityToTime(p1[0], p1[1], p1[2], p2[0], p2[1])
    appendix.reverse()
    for entry in appendix:
      bindActivityTime.insert(qf, entry)
  if len(blockIncrements1) != len(blockIncrements2) or len(blockIncrements2) != 0:
    print "Popping failed!"
    sys.exit(1)

  # write down Prolog rules
  with open(bgFilename, 'ab') as bgf:
    bgf.write('\n')
    bgf.write( '\n'.join(bindActivityTime) )
    bgf.write('\n\n')
    bgf.write( '\n'.join(bindLocationTime) )
    bgf.write('\n')

  # write generated data to file
  with open(dataFilename, 'wb') as datafile:
    datafile.write('\n'.join(outputSensorData))
    datafile.write('\n')
