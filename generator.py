#! /usr/local/bin/python

import sys
import csv
import datetime
from numpy.random import normal
from pprint import pprint

# Gaussian generator class
class genGaus:
  def __init__(self, mu, sigma):
    self.mu = mu
    self.sigma = sigma
  def get(self):
    return normal(self.mu, self.sigma)

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

interchangable = connected + rev + "(A, B) :-" + nl + "  " + connected + fact + "(A, B); " + connected + fact + "(B, A)." + nl + nl

# sensor location keyword for Prolog facts
sensorLocation = "sensorIn"
# activity fixed to sensor keyword for Prolog bg
sensorActivity = "sensorActivity"

# Background knowledge file name
bgFilename = "bg.pl"

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
        sensors[roomID]['door']   = []
      elif 'door' in line[0]: # add door information
        try:
          sensors[roomID]['door'].append( (line[3], float(line[1]), float(line[2])) )
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
  origin  = None
  current = None
  ## initialise time
  now = datetime.datetime.now()
  ## get output data stream
  outputSensorData = []
  # TODO: activity what is going on in Prolog as ground truth
  #
  # TODO: Add prior posterior for the directions!!!!!!
  for move in path:
    if move[0] == 'start': # location
      origin = current = move[1]
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
      for room in sequence:
        generators['step']()
        ## Check for sensors activation and record to file
        p1 = now.strftime( "%Y-%m-%d %H:%M:%S.%f" )
        p2 = "sensor ID"
        p3 = "sensor state"
        # update time
        (now + datetime.timedelta(days, seconds, miliseconds))
        # append to outputData vector
        outputSensorData.append( "lol" )
        # get location memory
      currnet = goal
    elif move[0] == 'do': # action
      # find position of sensor in current room
      # go to this position 
      # do the ativity: emulate snesors
      pass
    else:
      print "Action is not 'start', 'go', 'do'!"
      print "> ", move, " <"
      sys.exit(1)
  
  pprint( sensors)
  sys.exit(0)

  # TODO: give some reasonable file-name
  with open("data.txt", 'wb') as datafile:
    datafile.write('\n'.join(data))

  # TODO: noise parameter
  # TODO: data incompleteness parameter
  # TODO: multiple occupiers
