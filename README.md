# Smart Houses spatio-temporal data generator #

This small `Python` script: `generator.py`, simulates smart house data feed based on basic house specification. It takes: *room layout*, *sensor layout*, *sensor specification* and *path* to simulate as input; and outputs *data* in [CASAS](http://ailab.wsu.edu/casas/datasets.html) format together with *ground truth* as `Prolog` facts (see *Input* & *Output* sections for details).

## Assumptions ##

The application assumes:

* no cycles in room connections,
* motion in straight lines,
* 360 degree motion sensors with fixed radius,
* no dimensions of objects: *point-like* sensors,
* perfect sensing: no data noise,
* normal time distribution for all actions,
* the activities are simulated by first finding the path from current location to specified room in adjacency matrix; then simulating steps in each room from current position within it to chosen door and checking motion sensors being in range,
* to use defined item agent **must** in the room that the item is available,
* the items are simulated by first going from current location within the room to sensor location and then fast-forwarding the clock based on activity generator.


Due to `Prolog` data generation all sensors and activities **must** start with *lower case letter*.

## Usage ##
To run the script on *example* input files call:
```Bash
    python ./generator.py examples/rooms.l examples/layout.l examples/activities.l examples/path.l
```
with each file as described below.

## Input ##
The script takes 4 specification files in presented order:

### Connections between rooms ###
This file specifies connections between rooms in form of adjacency matrix (e.g. `examples/rooms.l`).

```
[X]          wardrobe_1 room_1 wardrobe_2 room_2 hall cupboard bathroom living_room kitchen 
wardrobe_1  0 1 0 0 0 0 0 0 0
room_1      1 0 0 0 1 0 0 0 0
wardrobe_2  0 0 0 1 0 0 0 0 0
room_2      0 0 1 0 1 0 0 0 0
hall        0 1 0 1 0 1 1 1 0
cupboard    0 0 0 0 1 0 0 0 0
bathroom    0 0 0 0 1 0 0 0 0
living_room 0 0 0 0 1 0 0 0 1
kitchen     0 0 0 0 0 0 0 1 0
```
The file **must** start with `[X]` symbol.

### Sensors and doors layout within rooms ###
This file specifies the location and parameters of each sensor (e.g. `examples/layout.l`).

```
kitchen 6 2:
m81   1   1   1
m82   3   1   1
m83   5   1   1
ad1-a 6   1   water_hot
ad1-b 6   1   water_cold
ad1-c 3   2   burner
d81   4   2   cabinet
i81   4   2   oatmeal
i82   4   2   raisins
i83   4   2   brown_sugar
i84   4   2   bowl
i85   4   2   measuring_spoon
i86   4   2   medicine_container
i87   4   2   pot
door  3   0   living_room
```

To specify details of given room line with its **name** (used in file above) needs to be placed together with **width**(X) and **height**(Y) of room finished with **`:`** symbol. The dimensions are in *meters* and the **`:`** symbol must be placed right after **height** with ***no spaces in-between***.

```
kitchen 6 2:
```

The positioning of each sensor is based on Cartesian coordinates with origin in bottom left corner.

The **least** specification needed for each room defined in the file above are **doors**. The doors are defined via **`door`** keyword followed by its position **X**, **Y** and **location** to where they lead.

```
door  3   0   living_room
```

Sensors are described by **sensor ID** followed by its position **X**, **Y**. The difference between *motion* and *item* sensors is third parameter.  
The third parameter of *motion sensor* is **radius** defining area in which sensor can be activated.

```
m82   3   1  1
```

On the other hand, the third parameter of *item sensor* is **item ID** that is used to specify time generator for item and to perform action on the item.

```
ad1-a 6   1   water_hot
```

### Time and space generators ###
This file specifies **stepTime**, **stepSize** and **item time** generators' parameters (e.g. `examples/activities.l`).  
Each activity is simulated by fast-forwarding the clock. Two **necessary** parameters are:

* **stepTime** - *mean* and *standard deviation* of duration of each step in *seconds*: `stepTime 2 0.01`,
* **stepSize** - *mean* and *standard deviation* of length of each step in *meters*: `stepSize 0.5 0.05`.

Additionally *time* (in *seconds*) generators: *mean* and *standard deviation*, for each defined item should be defined by using **itemID** specified above: `water_cold 100 1`.

```
stepTime   2      0.01
stepSize   0.5    0.05

water_hot  10     0.01
water_cold 100    1
burner     10000  0.1
```

### Path ###
The data are generated based on specified path and tasks (e.g. `examples/path.l`).

```
origin(hall)
go(kitchen)

meal{
  cook{
    do(water_hot)

    start(hob)
      wait(100, 0.1)
      go(living_room)
      do(tv)
      go(kitchen)
    stop(hob)
  }cook
  go(living_room)
  do(eat)
}meal

go(hall)
```

The following commands can be used:

* `origin(place)` - room where path should be started,
* `go(place)` - go to given room,
* `do(item)` - approach the *item*, turn the sensor *on*, simulate corresponding time, turn the sensor *off*,
* `start(item)` - approach the *item* and turn the sensor *on*,
* `wait(mu, sigma)` - fast forward the clock by generating time (in seconds) according to normal distribution with parameters *mean* and *standard deviation*; the agent does not move,
* `stop(item)` - approach the *item* and turn the sensor *off*,
* `return(item) - go to the place the *item* is located,
* `wander(x, y)` - go to (x, y) position within current room; (-1, -1) generates random position in the room,
* `activityName{...}activityName` - activity blocks starting with `activityName{` and finished with `}activityName`; used only for ground truth generation.

In above commands `place` is room name as specified above and `item` is sensor identifier as specified above.

*Block names* are only used for ground truth generation. *Items* are used for sensor firings.

This file **must** start with **`origin(...)`** keyword specifying beginning of the path; the location within this room is randomly generated. `go(...)` command places the agent at the door position in specified room. **One** command per line should be specified. *Block names* and *item IDs* mustn't overlap.

## Output ##
The script outputs two files `data.txt` and `bg.pl` (example files available in `examples` directory: `examples/data.txt`, `examples/bg.pl`). The first one contains sensor readings based on simulated activity. Each line consists of:  
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

The later file: `bg.pl`, is `Prolog` database containing ground truth and predicates to query room connectivity, activity and location at given time:

* `nowAt(Room, Time, TimeType).` - position at given time,
* `nowDo(Activity, Time, TimeType).` - activity at given time,
* `connected(RoomA, RoomB, Path).` - connections between rooms,
* `sensorInRoom(m31, room_2).` - location of each sensor,
* `sensorActivity(i78, phone_book).` - activity or item name assigned to corresponding sensors,
* `sensorInField(i78, m73).` - activity sensor in field of motion sensor.

Time is represented in four different ways:

* relative - counted in *microseconds* since first sensor reading,
* absolute - counted in *microseconds* and counted since Thursday, 1 January 1970 (UNIX timestamp * 10^6),
* sequence - sequential number of recorded sensor reading,
* windowed - number of window that event falls in (window-length *5 seconds*, first window starts with first reading).

## To do: ##
Introduce:

- [ ] noise & incompleteness (e.g. throw away some readings)
- [ ] multiple occupiers
- [ ] obstacles (furniture)
- [ ] improve 'stepping' <!--each step randomly generated; no distance calculation at the beginning; step until you're there--->
- [ ] update *output* section of `README.md` file: positives and negatives
- [ ] update README: *wait* command cannot be the first command in block
- [ ] write about *fifth sparse column (activity indicator)*
