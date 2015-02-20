#! /usr/local/bin/python

import sys
import csv
import datetime
from numpy.random import normal
# from pprint import pprint

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
  if len(args) != 3:
    # Fail
    print "No files specified."
    print "usage: constructFacts.py path/to/adjacency path/to/activities"
    sys.exit(1)

  Fadj = args[1]
  Fact = args[2]

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

  # Convert to Prolog
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

  # create generators
  generators = {}
  for gen in model:
    generators[gen[0]] = genGaus(gen[1], gen[2]).get

  # generate random paths with timestamps
  ## e.g. "2008-03-28 13:39:01.470516 M01 ON"
  ## get now
  now = datetime.datetime.now()
  data = []

  generators['step']()
  now.strftime( "%Y-%m-%d %H:%M:%S.%f" )
  (now + datetime.timedelta(days, seconds, miliseconds))

  # TODO: give some reasonable filename
  with open("data.txt", 'wb') as datafile:
    datafile.write(''.join(data))
