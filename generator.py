#! /usr/local/bin/python

import sys
import csv
import datetime
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

  def updateItemSensor(self, currentPosition):
    pass
    

# Define predicate name for connected rooms - background knowledge
connected = "connected"
# Constants
nl = '\n'
fact = '__'
rev  = '_'

interconnected = connected + "(A, B) :-" + nl + "  " + connected + "(A, B, [])."
interconnected += nl + connected + "(A, B, V) :-" + nl
interconnected += "  " + connected + rev + "(A, X), not( member(X, V) )," + nl
interconnected += "  (" + nl + "    " + "B = X" + nl + "  " + "; " + connected
interconnected += "(X, B, [A|V])" + nl + "  " + "), !." + nl + nl

interchangable  = connected + rev + "(A, B) :-" + nl + "  " + connected + fact
interchangable += "(A, B); " + connected + fact + "(B, A)." + nl + nl

# sensor location keyword for Prolog facts
sensorLocation = "sensorIn"
# activity fixed to sensor keyword for Prolog bg
sensorActivity = "sensorActivity"

# Background knowledge file-name
bgFilename = "bg.pl"

# generated data file-name
dataFilename = "data.txt"

# step size in meters
stepSize = .5

# Define functions
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

  facts = [interconnected, interchangable]
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

      # check for comment or empty line
      if line == []:
        continue
      if line[0][0] == ';':
        continue

      f1 = line.find('(')
      f2 = line.find(')')
      if f1 == -1 or f2 == -1:
        print "Path error: wrong format"
        sys.exit(1)
      command = line[:f1]
      argument = line[f1+1:f2]
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

  facts = []
  for k in sensors.keys():
    for r in sensors[k]['sensor']:
      # save sensor location - for motion sensors
      facts.append( sensorLocation + "(" + r[0] + ", " + k + ")." )
      # if this is item or activity sensor - remember additional activity fixed to sensor
      if type(r[3]) == str:
        facts.append( sensorActivity + "(" + r[0] + ", " + r[3] + ")." )

  with open(bgFilename, 'ab') as bgfile:
      bgfile.write('\n')
      bgfile.write('\n'.join(facts))
      bgfile.write('\n')

  return sensors


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
  # initialise time
  now = datetime.datetime.now()
  ## get output data stream
  outputSensorData = []
  # TODO: activity what is going on in Prolog as ground truth
  # TODO: Add prior posterior for the directions!!!!!!
  for move in path:
    if move[0] == 'start': # location
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
            pass # do not change it
          else: # initialise new as room does not match
            # clean old room
            # on room exit switch off sensors which havent switched off & are within you range
            activated = tt.motionSensorsOn(previous_position)
            for unit in activated:
              # compose entry
              ppp = now.strftime( "%Y-%m-%d %H:%M:%S.%f" ) + " " + unit[0] + " " + unit[1]
              # append to outputData vector
              outputSensorData.append( ppp )
            # initialise new room
            tt = monitor(current, sensors[current]['sensor'])
        else:
          tt = monitor(current, sensors[current]['sensor'])

        # go from location in previous to door to *room*
        ## find location of door
        target_position = sensors[current]['door'][room]

        # Check if you're already there!!!!!!!!!!!!!
        if current_position == target_position:
          neededSteps = -1
          activated = tt.motionSensorsOn(current_position)
          for unit in activated:
            # compose entry
            ppp = now.strftime( "%Y-%m-%d %H:%M:%S.%f" ) + " " + unit[0] + " " + unit[1]
            # append to outputData vector
            outputSensorData.append( ppp )
        else:
          ## search the path
          xa, xb, ya, yb = current_position[0], target_position[0], current_position[1], target_position[1]
          ## get momentum
          momentumX, momentumY = xb-xa, yb-ya
          ## TODO: division by 0 if you are already there
          ## TODO: for the moment it is straight line between origin and goal - can be randomised a bit
          slope       = (ya-yb) / (xa-xb)
          intercept   = ya - slope * xa
          ### find the length of path
          distance    = sqrt( (xb-xa)**2 + (yb-ya)**2 )
          ### divide step-wise based on *stepSize*
          neededSteps = int(ceil( distance / stepSize ))

        ### do steps +1 for current position
        for i in range(neededSteps+1):
          
          ### after each step check whether new sensor is activated
          activated = tt.updateMotionSensor(current_position)

          for unit in activated:
            # compose entry
            ppp = now.strftime( "%Y-%m-%d %H:%M:%S.%f" ) + " " + unit[0] + " " + unit[1]
            # append to outputData vector
            outputSensorData.append( ppp )

          # find new position
          if momentumX > 0:
            x = current_position[0] + sqrt( stepSize**2 / (slope**2 +1) )
          else:
            x = current_position[0] - sqrt( stepSize**2 / (slope**2 +1) )
          y = slope * x + intercept
          ## increment step along distance form *current* towards *target*
          
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
          stepTime = generators['step']()
          days, seconds, miliseconds = 0, stepTime, 0
          now += datetime.timedelta(days, seconds, miliseconds)

        # memorise last position in previous room
        previous_position = current_position
        ## remember to position at door when going to next room
        current_position = sensors[room]['door'][current] #target_position
        # memorise current location - use later to navigate to activity
        current          = room

      # Now you are in new room but haven't moved yet: check sensors
      tt = monitor(current, sensors[current]['sensor'])
      activated = tt.updateMotionSensor(current_position)
      for unit in activated:
        # compose entry
        ppp = now.strftime( "%Y-%m-%d %H:%M:%S.%f" ) + " " + unit[0] + " " + unit[1]
        # append to outputData vector
        outputSensorData.append( ppp )


      # MARK YOUR PRESENCE AFTER YOU REAHED THE DESTNATION ROOM
      # fix error - if you move VERTICALLY
      # fix item & activity sensoros
      # generate prolog ground truth of loctions
      # Prolog rule: activity-a in sensor field m01
      # add noise + incompleteness

      # check for reaching the target
      if current != goal:
        print "Path did not converge!"
        sys.exit(1)
    elif move[0] == 'do': # action
      # find position of sensor in current room
      for i in sensors[current]['sensor']:
        if move[1] == i[3]:
          target          = current
          target_position = (i[1], i[2])
          break
      # go to this position 
      # go()
      # do the activity: emulate sensors
      pass
    else:
      print "Action is not 'start', 'go', 'do'!"
      print "> ", move, " <"
      sys.exit(1)

  # write generated data to file
  with open(dataFilename, 'wb') as datafile:
    datafile.write('\n'.join(outputSensorData))
    datafile.write('\n')
