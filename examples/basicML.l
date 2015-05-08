origin(hall)
go(kitchen)

cook{
  start(burner)

  go(living_room)
  phonecall{
    do(phone_book)
    do(phone)
  }phonecall
  go(kitchen)

  stop(burner)
}cook

go(hall)