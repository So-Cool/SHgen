; activities as described in CASAS
origin(hall) ; make random for many rooms

; Make a phone call
make-a-phone-call{
  go(living_room)

  return(phone_book)
  start(phone_book)
  wait(100, 40)
  stop(phone_book)

  return(phone)
  start(phone)
  wait(240, 20)
  wander(-1, -1)
  return(phone)
  stop(phone)
}make-a-phone-call

; Wash hands
wash-hands{
  go(kitchen)

  return(water_hot)
  start(water_hot) ;shuffle water order
  wait(3, 0)
  start(water_cold)
  wait(30, 5)
  stop(water_hot)
  wait(3, 0)
  stop(water_cold)
  wander(-1, -1)
}wash-hands

; cook
cook{
  return(cabinet)
  start(cabinet)
  wait(5, 0.1)
  start(raisins);shuffle items them
  wait(5, 0.1)
  start(brown_sugar)
  wait(5, 0.1)
  start(oatmeal)
  wait(5, 0.1)
  start(measuring_spoon)
  wait(5, 0.1)
  start(bowl)
  wait(5, 0.1)
  start(pot)
  wait(5, 0.1)
  stop(cabinet)

  return(water_cold)
  start(water_cold)
  wait(40, 7)
  stop(water_cold)

  return(burner)
  start(burner)
  wait(300, 10)
  wander(-1, -1)
  wait(300, 10)
  wander(-1, -1)
  wait(300, 10)
  wander(-1, -1)
  wait(300, 10)
  wander(-1, -1)
  wait(300, 10)
  return(burner)
  stop(burner)
}cook

; eat
eat{
  return(cabinet)
  start(cabinet)
  wait(5, 0.1)
  start(medicine_container)
  wait(5, 0.1)
  stop(cabinet)

  go(living_room)
  return(table)
  wait(900, 60)
}eat

; clean
clean{
  go(kitchen)

  return(water_hot)
  start(water_cold)
  wait(4, 0)
  start(water_hot)
  wait(300, 10)
  stop(water_cold)
  wait(3, 0)
  stop(water_hot)

  return(cabinet)
  start(cabinet) ; shuffle it
  wait(4, 0.5)
  stop(raisins)
  wait(4, 0.5)
  stop(measuring_spoon)
  wait(4, 0.5)
  stop(medicine_container)
  wait(4, 0.5)
  stop(pot)
  wait(4, 0.5)
  stop(oatmeal)
  wait(4, 0.5)
  stop(bowl)
  wait(4, 0.5)
  stop(brown_sugar)
  wait(4, 0.5)
  stop(cabinet)
}clean

go(hall)
