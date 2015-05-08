origin(hall)
go(living_room)

phonecall{
  do(phone_book)
  do(phone)
  go(kitchen)
}phonecall

cook{
  start(burner)
  wander(-1, -1)
  wait(300, 10)
  wander(-1, -1)
  stop(burner)
}cook

go(hall)