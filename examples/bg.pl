connected(A, B, Path) :-
  connected(A, B, [], Path).
connected(A, B, V, Path) :-
  connected_(A, X), not( member(X, V) ),
  (
    B = X, reverse([B,A|V], Path)
  ; connected(X, B, [A|V], Path)
  ), !.

connected_(A, B) :-
  connected__(A, B); connected__(B, A).

nowAt(Room, Time, TimeType) :-
  %% there is presence in given room at some time T...
  spaceTime(Room, TimeType, T),
  %% ...which is before our time of interest...
  T =< Time,
  %% ...and we do not move to any other room between *Time* and *T*
  \+nowAt_(Room, TimeType, T, Time), !.

nowAt_(Room, TimeType, T1, T2) :-
  spaceTime(OtherRoom, TimeType, Tbound),
  \+(OtherRoom = Room),
  T1 =< Tbound, Tbound =< T2.

nowDo(Activity, Time, TimeType) :-
  %% the activity is held at some time T...
  activityTime(Activity, true, TimeType, T1),
  %% ...which started now or before our time of interest...
  T1 =< Time,
  %% ... and has not ended yet.
  \+nowDo_(Activity, Time, TimeType).

nowDo_(Activity, Time, TimeType) :-
  activityTime(Activity, false, TimeType, T),
  T =< Time.

connected__(room_2, wardrobe_2).
connected__(room_2, hall).
connected__(bathroom, hall).
connected__(room_1, wardrobe_1).
connected__(room_1, hall).
connected__(cupboard, hall).
connected__(living_room, hall).
connected__(living_room, kitchen).

sensorInRoom(m31, room_2).
sensorInRoom(m32, room_2).
sensorInRoom(m33, room_2).
sensorInRoom(m34, room_2).
sensorInRoom(m35, room_2).
sensorInRoom(m36, room_2).
sensorInRoom(m61, bathroom).
sensorInRoom(m11, room_1).
sensorInRoom(m12, room_1).
sensorInRoom(m13, room_1).
sensorInRoom(m14, room_1).
sensorInRoom(m15, room_1).
sensorInRoom(m16, room_1).
sensorInRoom(m51, cupboard).
sensorInRoom(m71, living_room).
sensorInRoom(m72, living_room).
sensorInRoom(m73, living_room).
sensorInRoom(m74, living_room).
sensorInRoom(m75, living_room).
sensorInRoom(m76, living_room).
sensorInRoom(m77, living_room).
sensorInRoom(m78, living_room).
sensorInRoom(m79, living_room).
sensorInRoom(i78, living_room).
sensorInRoom(table-sensor, living_room).
sensorInRoom(asterisk, living_room).
sensorInRoom(m21, wardrobe_2).
sensorInRoom(m01, wardrobe_1).
sensorInRoom(m41, hall).
sensorInRoom(m42, hall).
sensorInRoom(m43, hall).
sensorInRoom(m81, kitchen).
sensorInRoom(m82, kitchen).
sensorInRoom(m83, kitchen).
sensorInRoom(ad1-a, kitchen).
sensorInRoom(ad1-b, kitchen).
sensorInRoom(ad1-c, kitchen).
sensorInRoom(d81, kitchen).
sensorInRoom(i81, kitchen).
sensorInRoom(i82, kitchen).
sensorInRoom(i83, kitchen).
sensorInRoom(i84, kitchen).
sensorInRoom(i85, kitchen).
sensorInRoom(i86, kitchen).
sensorInRoom(i87, kitchen).

sensorActivity(i78, phone_book).
sensorActivity(table-sensor, table).
sensorActivity(asterisk, phone).
sensorActivity(ad1-a, water_hot).
sensorActivity(ad1-b, water_cold).
sensorActivity(ad1-c, burner).
sensorActivity(d81, cabinet).
sensorActivity(i81, oatmeal).
sensorActivity(i82, raisins).
sensorActivity(i83, brown_sugar).
sensorActivity(i84, bowl).
sensorActivity(i85, measuring_spoon).
sensorActivity(i86, medicine_container).
sensorActivity(i87, pot).

sensorInField(i78, m73).
sensorInField(table-sensor, m77).
sensorInField(asterisk, m73).
sensorInField(ad1-a, m83).
sensorInField(ad1-b, m83).
sensorInField(ad1-c, m82).
sensorInField(d81, none).
sensorInField(i81, none).
sensorInField(i82, none).
sensorInField(i83, none).
sensorInField(i84, none).
sensorInField(i85, none).
sensorInField(i86, none).
sensorInField(i87, none).

activityTime(cook, true, relative, 44020203).
activityTime(cook, true, absolute, 1425138186265207).
activityTime(cook, true, sequence, 15).
activityTime(cook, true, windowed, 8).
activityTime(eat, true, relative, 44020203).
activityTime(eat, true, absolute, 1425138186265207).
activityTime(eat, true, sequence, 15).
activityTime(eat, true, windowed, 8).
activityTime(water_hot, true, relative, 44020203).
activityTime(water_hot, true, absolute, 1425138186265207).
activityTime(water_hot, true, sequence, 15).
activityTime(water_hot, true, windowed, 8).
activityTime(water_hot, false, relative, 144132409).
activityTime(water_hot, false, absolute, 1425138286377413).
activityTime(water_hot, false, sequence, 17).
activityTime(water_hot, false, windowed, 28).
activityTime(eat, false, relative, 144132409).
activityTime(eat, false, absolute, 1425138286377413).
activityTime(eat, false, sequence, 17).
activityTime(eat, false, windowed, 28).
activityTime(burner, true, relative, 158187287).
activityTime(burner, true, absolute, 1425138300432291).
activityTime(burner, true, sequence, 21).
activityTime(burner, true, windowed, 31).
activityTime(burner, false, relative, 168323520).
activityTime(burner, false, absolute, 1425138310568524).
activityTime(burner, false, sequence, 22).
activityTime(burner, false, windowed, 33).
activityTime(cook, false, relative, 168323520).
activityTime(cook, false, absolute, 1425138310568524).
activityTime(cook, false, sequence, 22).
activityTime(cook, false, windowed, 33).

spaceTime(hall, relative, 0).
spaceTime(hall, absolute, 1425138142245004).
spaceTime(hall, sequence, 0).
spaceTime(hall, windowed, 0).
spaceTime(living_room, relative, 11998046).
spaceTime(living_room, absolute, 1425138154243050).
spaceTime(living_room, sequence, 6).
spaceTime(living_room, windowed, 2).
spaceTime(kitchen, relative, 28016574).
spaceTime(kitchen, absolute, 1425138170261578).
spaceTime(kitchen, sequence, 12).
spaceTime(kitchen, windowed, 5).
spaceTime(living_room, relative, 176294601).
spaceTime(living_room, absolute, 1425138318539605).
spaceTime(living_room, sequence, 24).
spaceTime(living_room, windowed, 35).
spaceTime(hall, relative, 192306861).
spaceTime(hall, absolute, 1425138334551865).
spaceTime(hall, sequence, 30).
spaceTime(hall, windowed, 38).
