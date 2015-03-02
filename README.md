# Smart Houses spatio-temporal data generator #
This small `Python` script: `generator.py`, simulates smart house data feed based on basic house specification. blah blah blah...

## Assumptions ##

no cycles  
point door  
sensors  
normal distribution  
use small letters for sensors and activities

## Input ##
Generate labelled spatio-temporal data from:

### connection between rooms ###
examples/rooms.l

### sensors and doors layout within rooms ###
examples/layout.l

### specification of time and space generators ###
examples/activities.l

### Path to follow ###
examples/path.l

File specifying tasks to be simulated. The program allows the following commands to be used:

1. `origin(place)`
1. `go(place)`
1. `do(atomicActivity)`
1. `start(atomicActivity)`
1. `wait(mu, sigma)`
1. `stop(atomicActivity)`
1. Activity blocks starting with `activityName{` and finished with `}activityName`

One command per line can be used

```
|---------|-------|------------------------------------|
|Cook     |Eat    |TV             |Phone |TV           |
|---------|-------|---------------|------|-------------|
```

## Usage ##
To run the script on *example* input files call:
```Bash
    python ./generator.py examples/rooms.l examples/layout.l examples/activities.l examples/path.l
```
with each file as described above.

## Output ##
The script outputs two files `data.txt` and `bg.pl`. The first one contains sensor readings based on simulated activity. Each line consists of:  
`Year-Month-Day hour:minute:second.microsecond sensorID sensorState`,  
where time is in 24-hour system and `sensorState` can be either `true` or `false`.

```
2015-02-28 15:42:22.245004 m42 true
2015-02-28 15:42:22.245004 m43 true
2015-02-28 15:42:24.254649 m41 true
2015-02-28 15:42:30.243752 m43 false
2015-02-28 15:42:34.243050 m42 false
2015-02-28 15:42:34.243050 m41 false
2015-02-28 15:42:34.243050 m76 true
2015-02-28 15:42:40.247056 m76 false
2015-02-28 15:42:40.247056 m79 true
2015-02-28 15:42:46.262147 m79 false
2015-02-28 15:42:46.262147 m78 true
2015-02-28 15:42:50.261578 m78 false
2015-02-28 15:42:50.261578 m82 true
2015-02-28 15:42:54.286933 m82 false
2015-02-28 15:42:56.278847 m83 true
2015-02-28 15:43:06.265207 ad1-a true
2015-02-28 15:44:46.377413 m83 false
2015-02-28 15:44:46.377413 ad1-a false
2015-02-28 15:44:46.377413 m83 true
2015-02-28 15:44:54.407373 m83 false
2015-02-28 15:44:58.419168 m82 true
2015-02-28 15:45:00.432291 ad1-c true
2015-02-28 15:45:10.568524 ad1-c false
2015-02-28 15:45:18.539605 m82 false
2015-02-28 15:45:18.539605 m78 true
2015-02-28 15:45:24.564310 m79 true
2015-02-28 15:45:24.564310 m78 false
2015-02-28 15:45:30.557255 m76 true
2015-02-28 15:45:30.557255 m79 false
2015-02-28 15:45:34.551865 m76 false
2015-02-28 15:45:34.551865 m42 true
2015-02-28 15:45:34.551865 m41 true
```

The later file: `bg.pl`, is `Prolog` database containing ground truth of:

* position at given time,
* activity at given time,
* connections between rooms,
* location of each sensor: `sensorInRoom(m31, room_2).`,
* activity or item name assigned to corresponding sensors: `sensorActivity(i78, phone_book).`,
* activity sensor in field of motion sensor: `sensorInField(i78, m73).`.

The file also contains predicates to query room connectivity and activity & location at given time.
nowAt(Room, Time, TimeType).
nowDo(Activity, Time, TimeType).
connected(RoomA, RoomB, Path).

Time is represensted in 4 different ways:
relative,
absolute,
sequence,
windowed.

 generated from input data and .

## To do: ##
Introduce:

* noise & incompleteness
* multiple occupiers
