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
fact = 'F'
interchangable = connected + "(A, B) :- " + connected + fact + "(A, B); " + connected + fact + "(B, A)." + nl


if __name__ == '__main__':
  # Check whether file is given as argument
  args = sys.argv
  if len(args) != 5:
    # Fail
    print "No files specified."
    print "usage: constructFacts.py path/to/adjacency path/to/activities path/to/path path/to/layout"
    sys.exit(1)

  Fadj  = args[1]
  Fact  = args[2]
  Fpath = args[3]
  Flay  = args[4]

  # Read in adjacency matrix
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

  # Convert house layout to Prolog
  facts = [interchangable]
  keys1 = layout.keys()
  keys2 = layout.keys()
  for key1 in keys1:
    for key2 in keys2:
      if layout[key1][key2]:
        facts.append( connected + fact + '(' + key1 + ', ' + key2 + ').' + nl )
    # adjacency matrix is symmetric
    keys2.remove(key1)
  # write to file
  # TODO: give some reasonable filename
  with open("bg.pl", 'wb') as bgfile:
    bgfile.write(''.join(facts))

  # load model parameters: assume structure [name mu sigma]
  model = []
  with open(Fact, 'rb') as bgfile:
    parameters = csv.reader(bgfile, delimiter=' ', skipinitialspace=True)
    for row in parameters:
      # clean all empty strings
      cleanRow = filter(lambda a: a != '', row)
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

  # read in path
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

  # read in rooms layout into sensors dictionary
  sensors = {}
  # TODO: Prolog where what sensor is located: location(m01, living_room)
  with open(Flay, 'rb') as layfile:
    # split into rooms: dictionary { rooms: { sensors:[], doors:[] } }
    ## do each activity per room
    keys = layout.keys()
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
        # try:
          try:
            r = float(line[3])
          except:
            r = line[3]
          sensors[roomID]['sensor'].append( (line[0], float(line[1]), float(line[2]), r ) )
        # except:
        #   print "'sensor' format error:"
        #   print line
        #   sys.exit(1)

  ##############################################################################
  pprint( sensors)
  sys.exit(0)
  ##### layout, generators, path, sensors
  # generate random paths with timestamps
  ## e.g. "2008-03-28 13:39:01.470516 M01 ON"
  ## get now
  now = datetime.datetime.now()
  data = []
  # TODO: acitvity what is going on in prolog as ground truth

  # find path in graph: go() + start() commands: current + target
  # find path in corresponding Cartesians
  generators['step']()
  now.strftime( "%Y-%m-%d %H:%M:%S.%f" )
  (now + datetime.timedelta(days, seconds, miliseconds))
  # append sensors and devices(i.e. device sensors) to room layout


  # noise parameter
  # data incompleteness parameter
  # multiple occupiers

  # TODO: give some reasonable filename
  with open("data.txt", 'wb') as datafile:
    datafile.write(''.join(data))
