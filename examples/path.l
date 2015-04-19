origin(hall)
go(kitchen)

cook{
  start(cabinet)
    do(oatmeal)
    do(raisins)
    do(brown_sugar)
    do(bowl)
    do(measuring_spoon)
    do(medicine_container)
    do(pot)
  stop(cabinet)
  do(water_cold)
  start(burner)

  watchTV{
    go(living_room)
    do(tv)
    go(kitchen)
  }watchTV

  stop(burner)
}cook

go(living_room)

eat{
  start(table)
  wait(300, 50)
  stop(table)
  phone_call{
    do(phone)
    wander(5, 5)
    wander(1, 5)
    wander(5, 1)
  }phone_call
  start(table)
  wait(1020, 75)
  stop(table)
}eat

go(kitchen)

wash-up{
  do(water_hot)
}wash-up

go(hall)



; be careful
; wait cannot be used just before activity-block ends
; wait must be used within **start** **stop**
; you have to be in a room to use a sensor
; be care-full not to use the same names for blocks and sensors
