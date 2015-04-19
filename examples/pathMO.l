>ResidentA>
origin(room_1)
sleep{
  wander(-1, -1)
  wait(6000, 10)
  wander(-1, -1)
}sleep
<ResidentA<

>ResidentB>
origin(room_2)
useBathroom{
  go(bathroom)
  wait(300, 10)
  go(room_2)
}useBathroom
<ResidentB<
