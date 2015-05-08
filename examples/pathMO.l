>ResidentA>
origin(room_1)
sleep{
  wander(-1, -1)
  wait(10, 1)
  wander(-1, -1)
}sleep
<ResidentA<

>ResidentB>
origin(room_2)
useBathroom{
  go(bathroom)
  wait(400, 10)
  go(room_2)
}useBathroom
wander(-1, -1)
<ResidentB<
