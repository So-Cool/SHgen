; -t "December 06 2015 22.15"

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;day 1 morning
origin(room_1)

; go to room_1 sleep
;sleep{
  return(bed_1)
  wait(32400, 900)
  wander(-1, -1)
;}sleep

; go to wardrobe and get new clothes
;change-1{
 go(wardrobe_1)
 wait(75, 9)
 go(room_1)
 wait(120, 4)
;}change-1

; go to toillet wash hands
go(bathroom)
;use-toilet-2{
  return(toilet)
  wait(300, 30)
;}use-toilet-2

;wash-hands-1{
  return(water_hot_basin)
  start(water_hot_basin)
    wait(90, 15)
  stop(water_hot_basin)
;}wash-hands-1

; go to kitchen prepeare meal - eat in living room - wash up
go(kitchen)
;prepare-breakfast{
  return(fridge)
  wait(120, 15)
  return(toster)
  wait(30, 5)
  start(toster)
    wait(15, 2)
    return(cabinet)
    wait(15, 2)
    start(cabinet)
    wait(15, 2)
    start(bowl)
    wait(15, 2)
    start(oatmeal)
    wait(75, 5)
    stop(oatmeal)
  stop(cabinet)
  wander(-1, -1)
  return(toster)
  stop(toster)
  wait(95, 3)
  return(fridge)
  wait(40, 5)
  return(toster)
  wait(15, 3)
;}prepare-breakfast

;eat-brekfast{
 return(table)
 wait(1200, 50)
;}eat-brekfast

;wash-up-b{
  return(water_cold_sink)
  start(water_cold_sink)
  wait(15, 1)
  start(water_hot_sink)
  wait(300, 20)
  stop(water_cold_sink)
  stop(water_hot_sink)
  wait(120, 15)
  return(cabinet)
  start(cabinet)
  wait(15, 1)
  stop(bowl)
  wait(15, 1)
  wait(15, 1)
  stop(cabinet)
;}wash-up-b

; go to bathroom wash teeth
go(bathroom)
;brush-teeth-1{
 wander(-1, -1)
 return(water_hot_basin)
 ; error
 wait(60, 10)
 start(water_hot_basin)
 wait(25, 5)
 stop(water_hot_basin)
 wait(200, 20)
 start(water_hot_basin)
 wait(25, 5)
 stop(water_hot_basin)
 wait(60, 10)
 wander(0.75, 0)
;}brush-teeth-1

; go take a backpack and pack it in room
go(room_1)
return(desk_1)
wait(240, 20)
wander(-1, -1)
return(desk_1)
wait(45, 5)

; go to work
;work{
  go(outside)
  wait(18000, 900)
  go(hall)
;}work

; enter house and leave your coat and shoes
wait(90, 15)

; go to bedroom_1 and leave backpack
go(room_1)
return(desk_1)
wait(60, 10)

; go to bathroom use toilet wash hands
go(bathroom)
;use-toilet{
  return(toilet)
  wait(300, 30)
;}use-toilet
;wash-hands{
  return(water_hot_basin)
  start(water_hot_basin)
    wait(90, 15)
  stop(water_hot_basin)
;}wash-hands

; go to kitchen prepare a meal relax on sofa watch tv
go(kitchen)

;cook{
  do(fridge)
  return(burner)
  wait(60, 5)
  return(cabinet)
  start(cabinet)
  start(pot)
  stop(cabinet)
  return(water_cold_sink)
  start(water_cold_sink)
  wait(60, 15)
  stop(water_cold_sink)
  return(burner)
  start(burner)
  wait(240, 20)
  go(living_room)
  return(sofa)
  wait(930, 45)
  go(kitchen)
  return(burner)
  stop(burner)
  return(water_cold_sink)
  return(cabinet)
  start(cabinet)
  start(bowl)
  stop(cabinet)
  return(water_cold_sink)
  wait(180, 20)
;}cook

;eat{
 return(table)
 wait(1200, 50)
;}eat

;wash-up{
  return(water_cold_sink)
  start(water_cold_sink)
  wait(15, 1)
  start(water_hot_sink)
  wait(300, 20)
  stop(water_cold_sink)
  stop(water_hot_sink)
  wait(120, 15)
  return(cabinet)
  start(cabinet)
  wait(15, 1)
  stop(bowl)
  wait(15, 1)
  stop(pot)
  wait(15, 1)
  stop(cabinet)
;}wash-up

;watchTV{
  go(living_room)
  return(sofa)
  start(tv)
  wait(9000, 600)
  stop(tv)
;}watchTV

;phone-call{
  return(phone_book)
  start(phone_book)
  wait(160, 10)
  stop(phone_book)
  return(phone)
  start(phone)
  wait(220, 15)
  wander(-1, -1)
  wait(290, 7)
  wander(-1, -1)
  wait(300, 17)
  wander(-1, -1)
  wait(150, 1)
  return(phone)
  stop(phone)
;}phone-call

; go to room_1 and work a bit on desk_1
go(room_1)
;work-home{
  return(desk_1)
  wait(10800, 350)
;}work-home


; eat snack
;snack{
go(kitchen)
return(fridge)
wait(60, 5)
return(toster)
wait(30, 5)
return(microwave)
wait(30, 5)
return(cabinet)
wait(15, 2)
start(cabinet)
wait(30, 5)
start(bowl)
wait(15, 2)
stop(cabinet)
return(toster)
wait(20, 5)
return(microwave)
wait(20, 5)
return(table)
wait(900, 60)
return(toster)
wait(30, 5)
return(fridge)
wait(30, 5)
return(water_hot_sink)
start(water_hot_sink)
wait(120, 15)
stop(water_hot_sink)
wait(15, 1)
return(cabinet)
wait(5, 1)
start(cabinet)
wait(5, 1)
stop(bowl)
wait(5, 1)
stop(cabinet)
;}snack
go(room_1)


; change clothes
;change{
  go(wardrobe_1)
  wait(60, 7)
  go(room_1)
  wait(120, 15)
;}change

; go to bathroom: toilet teeth shower
go(bathroom)
;use-toilet-1{
  return(toilet)
  wait(420, 50)
;}use-toilet-1
;brush-teeth{
 wander(-1, -1)
 return(water_hot_basin)
 ; error
 wait(60, 10)
 start(water_hot_basin)
 wait(25, 5)
 stop(water_hot_basin)
 wait(200, 20)
 start(water_hot_basin)
 wait(25, 5)
 stop(water_hot_basin)
 wait(60, 10)
 wander(0.75, 0)
;}brush-teeth
;shower{
 return(water_hot_bath)
 start(water_hot_bath)
 wait(15, 3)
 start(water_cold_bath)
 wait(500, 77)
 stop(water_hot_basin)
 wait(15, 3)
 stop(water_cold_bath)
 wait(45, 5)
 wander(0.75, 0)
 wait(120, 15)
;}shower

; go to room_1 relax in bed
;relax{
  go(room_1)
  return(desk_1)
  wait(1800, 300)
  wander(-1, -1)
  wait(420, 30)
  return(desk_1)
  wait(1000, 150)
;}relax
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;day 1 morning

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;day 2 morning
; go to room_1 sleep
;sleep{
  return(bed_1)
  wait(32400, 900)
  wander(-1, -1)
;}sleep

; go to wardrobe and get new clothes
;change-1{
 go(wardrobe_1)
 wait(75, 9)
 go(room_1)
 wait(120, 4)
;}change-1

; go to toillet wash hands
go(bathroom)
;use-toilet-2{
  return(toilet)
  wait(300, 30)
;}use-toilet-2

;wash-hands-1{
  return(water_hot_basin)
  start(water_hot_basin)
    wait(90, 15)
  stop(water_hot_basin)
;}wash-hands-1

; go to kitchen prepeare meal - eat in living room - wash up
go(kitchen)
;prepare-breakfast{
  return(fridge)
  wait(120, 15)
  return(toster)
  wait(30, 5)
  start(toster)
    wait(15, 2)
    return(cabinet)
    wait(15, 2)
    start(cabinet)
    wait(15, 2)
    start(bowl)
    wait(15, 2)
    start(oatmeal)
    wait(75, 5)
    stop(oatmeal)
  stop(cabinet)
  wander(-1, -1)
  return(toster)
  stop(toster)
  wait(95, 3)
  return(fridge)
  wait(40, 5)
  return(toster)
  wait(15, 3)
;}prepare-breakfast

;eat-brekfast{
 return(table)
 wait(1200, 50)
;}eat-brekfast

;wash-up-b{
  return(water_cold_sink)
  start(water_cold_sink)
  wait(15, 1)
  start(water_hot_sink)
  wait(300, 20)
  stop(water_cold_sink)
  stop(water_hot_sink)
  wait(120, 15)
  return(cabinet)
  start(cabinet)
  wait(15, 1)
  stop(bowl)
  wait(15, 1)
  wait(15, 1)
  stop(cabinet)
;}wash-up-b

; go to bathroom wash teeth
go(bathroom)
;brush-teeth-1{
 wander(-1, -1)
 return(water_hot_basin)
 ; error
 wait(60, 10)
 start(water_hot_basin)
 wait(25, 5)
 stop(water_hot_basin)
 wait(200, 20)
 start(water_hot_basin)
 wait(25, 5)
 stop(water_hot_basin)
 wait(60, 10)
 wander(0.75, 0)
;}brush-teeth-1

; go take a backpack and pack it in room
go(room_1)
return(desk_1)
wait(240, 20)
wander(-1, -1)
return(desk_1)
wait(45, 5)

; go to work
;work{
  go(outside)
  wait(18000, 900)
  go(hall)
;}work

; enter house and leave your coat and shoes
wait(90, 15)

; go to bedroom_1 and leave backpack
go(room_1)
return(desk_1)
wait(60, 10)

; go to bathroom use toilet wash hands
go(bathroom)
;use-toilet{
  return(toilet)
  wait(300, 30)
;}use-toilet
;wash-hands{
  return(water_hot_basin)
  start(water_hot_basin)
    wait(90, 15)
  stop(water_hot_basin)
;}wash-hands

; go to kitchen prepare a meal relax on sofa watch tv
go(kitchen)

;cook{
  do(fridge)
  return(burner)
  wait(60, 5)
  return(cabinet)
  start(cabinet)
  start(pot)
  stop(cabinet)
  return(water_cold_sink)
  start(water_cold_sink)
  wait(60, 15)
  stop(water_cold_sink)
  return(burner)
  start(burner)
  wait(240, 20)
  go(living_room)
  return(sofa)
  wait(930, 45)
  go(kitchen)
  return(burner)
  stop(burner)
  return(water_cold_sink)
  return(cabinet)
  start(cabinet)
  start(bowl)
  stop(cabinet)
  return(water_cold_sink)
  wait(180, 20)
;}cook

;eat{
 return(table)
 wait(1200, 50)
;}eat

;wash-up{
  return(water_cold_sink)
  start(water_cold_sink)
  wait(15, 1)
  start(water_hot_sink)
  wait(300, 20)
  stop(water_cold_sink)
  stop(water_hot_sink)
  wait(120, 15)
  return(cabinet)
  start(cabinet)
  wait(15, 1)
  stop(bowl)
  wait(15, 1)
  stop(pot)
  wait(15, 1)
  stop(cabinet)
;}wash-up

;watchTV{
  go(living_room)
  return(sofa)
  start(tv)
  wait(9000, 600)
  stop(tv)
;}watchTV

;phone-call{
  return(phone_book)
  start(phone_book)
  wait(160, 10)
  stop(phone_book)
  return(phone)
  start(phone)
  wait(220, 15)
  wander(-1, -1)
  wait(290, 7)
  wander(-1, -1)
  wait(300, 17)
  wander(-1, -1)
  wait(150, 1)
  return(phone)
  stop(phone)
;}phone-call

; go to room_1 and work a bit on desk_1
go(room_1)
;work-home{
  return(desk_1)
  wait(10800, 350)
;}work-home


; eat snack
;snack{
go(kitchen)
return(fridge)
wait(60, 5)
return(toster)
wait(30, 5)
return(microwave)
wait(30, 5)
return(cabinet)
wait(15, 2)
start(cabinet)
wait(30, 5)
start(bowl)
wait(15, 2)
stop(cabinet)
return(toster)
wait(20, 5)
return(microwave)
wait(20, 5)
return(table)
wait(900, 60)
return(toster)
wait(30, 5)
return(fridge)
wait(30, 5)
return(water_hot_sink)
start(water_hot_sink)
wait(120, 15)
stop(water_hot_sink)
wait(15, 1)
return(cabinet)
wait(5, 1)
start(cabinet)
wait(5, 1)
stop(bowl)
wait(5, 1)
stop(cabinet)
;}snack
go(room_1)


; change clothes
;change{
  go(wardrobe_1)
  wait(60, 7)
  go(room_1)
  wait(120, 15)
;}change

; go to bathroom: toilet teeth shower
go(bathroom)
;use-toilet-1{
  return(toilet)
  wait(420, 50)
;}use-toilet-1
;brush-teeth{
 wander(-1, -1)
 return(water_hot_basin)
 ; error
 wait(60, 10)
 start(water_hot_basin)
 wait(25, 5)
 stop(water_hot_basin)
 wait(200, 20)
 start(water_hot_basin)
 wait(25, 5)
 stop(water_hot_basin)
 wait(60, 10)
 wander(0.75, 0)
;}brush-teeth
;shower{
 return(water_hot_bath)
 start(water_hot_bath)
 wait(15, 3)
 start(water_cold_bath)
 wait(500, 77)
 stop(water_hot_basin)
 wait(15, 3)
 stop(water_cold_bath)
 wait(45, 5)
 wander(0.75, 0)
 wait(120, 15)
;}shower

; go to room_1 relax in bed
;relax{
  go(room_1)
  return(desk_1)
  wait(1800, 300)
  wander(-1, -1)
  wait(420, 30)
  return(desk_1)
  wait(1000, 150)
;}relax
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;day 2 morning

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;day 3 afternoon
; go to room_1 sleep
;sleep{
  return(bed_1)
  wait(32400, 900)
  wander(-1, -1)
;}sleep

; go to wardrobe and get new clothes
;change-1{
 go(wardrobe_1)
 wait(75, 9)
 go(room_1)
 wait(120, 4)
;}change-1

; go to toillet wash hands
go(bathroom)
;use-toilet-2{
  return(toilet)
  wait(300, 30)
;}use-toilet-2

;wash-hands-1{
  return(water_hot_basin)
  start(water_hot_basin)
    wait(90, 15)
  stop(water_hot_basin)
;}wash-hands-1

; go to kitchen prepeare meal - eat in living room - wash up
go(kitchen)
;prepare-breakfast{
  return(fridge)
  wait(120, 15)
  return(toster)
  wait(30, 5)
  start(toster)
    wait(15, 2)
    return(cabinet)
    wait(15, 2)
    start(cabinet)
    wait(15, 2)
    start(bowl)
    wait(15, 2)
    start(oatmeal)
    wait(75, 5)
    stop(oatmeal)
  stop(cabinet)
  wander(-1, -1)
  return(toster)
  stop(toster)
  wait(95, 3)
  return(fridge)
  wait(40, 5)
  return(toster)
  wait(15, 3)
;}prepare-breakfast

;eat-brekfast{
 return(table)
 wait(1200, 50)
;}eat-brekfast

;wash-up-b{
  return(water_cold_sink)
  start(water_cold_sink)
  wait(15, 1)
  start(water_hot_sink)
  wait(300, 20)
  stop(water_cold_sink)
  stop(water_hot_sink)
  wait(120, 15)
  return(cabinet)
  start(cabinet)
  wait(15, 1)
  stop(bowl)
  wait(15, 1)
  wait(15, 1)
  stop(cabinet)
;}wash-up-b

; go to bathroom wash teeth
go(bathroom)
;brush-teeth-1{
 wander(-1, -1)
 return(water_hot_basin)
 ; error
 wait(60, 10)
 start(water_hot_basin)
 wait(25, 5)
 stop(water_hot_basin)
 wait(200, 20)
 start(water_hot_basin)
 wait(25, 5)
 stop(water_hot_basin)
 wait(60, 10)
 wander(0.75, 0)
;}brush-teeth-1


; go to room_1 and work a bit on desk_1
go(room_1)
;work-home{
  return(desk_1)
  wait(10800, 350)
;}work-home

;watchTV{
  go(living_room)
  return(sofa)
  start(tv)
  wait(3600, 300)
  stop(tv)
;}watchTV

; eat snack
;snack{
go(kitchen)
return(fridge)
wait(60, 5)
return(toster)
wait(30, 5)
return(microwave)
wait(30, 5)
return(cabinet)
wait(15, 2)
start(cabinet)
wait(30, 5)
start(bowl)
wait(15, 2)
stop(cabinet)
return(toster)
wait(20, 5)
return(microwave)
wait(20, 5)
return(table)
wait(900, 60)
return(toster)
wait(30, 5)
return(fridge)
wait(30, 5)
return(water_hot_sink)
start(water_hot_sink)
wait(120, 15)
stop(water_hot_sink)
wait(15, 1)
return(cabinet)
wait(5, 1)
start(cabinet)
wait(5, 1)
stop(bowl)
wait(5, 1)
stop(cabinet)
;}snack



; go take a backpack and pack it in room
go(room_1)
return(desk_1)
wait(240, 20)
wander(-1, -1)
return(desk_1)
wait(45, 5)

; go to work
;work{
  go(outside)
  wait(18000, 900)
  go(hall)
;}work

; enter house and leave your coat and shoes
wait(90, 15)

; go to bedroom_1 and leave backpack
go(room_1)
return(desk_1)
wait(60, 10)

; go to bathroom use toilet wash hands
go(bathroom)
;use-toilet{
  return(toilet)
  wait(300, 30)
;}use-toilet
;wash-hands{
  return(water_hot_basin)
  start(water_hot_basin)
    wait(90, 15)
  stop(water_hot_basin)
;}wash-hands

; go to kitchen prepare a meal relax on sofa watch tv
go(kitchen)

;cook{
  do(fridge)
  return(burner)
  wait(60, 5)
  return(cabinet)
  start(cabinet)
  start(pot)
  stop(cabinet)
  return(water_cold_sink)
  start(water_cold_sink)
  wait(60, 15)
  stop(water_cold_sink)
  return(burner)
  start(burner)
  wait(240, 20)
  go(living_room)
  return(sofa)
  wait(930, 45)
  go(kitchen)
  return(burner)
  stop(burner)
  return(water_cold_sink)
  return(cabinet)
  start(cabinet)
  start(bowl)
  stop(cabinet)
  return(water_cold_sink)
  wait(180, 20)
;}cook

;eat{
 return(table)
 wait(1200, 50)
;}eat

;wash-up{
  return(water_cold_sink)
  start(water_cold_sink)
  wait(15, 1)
  start(water_hot_sink)
  wait(300, 20)
  stop(water_cold_sink)
  stop(water_hot_sink)
  wait(120, 15)
  return(cabinet)
  start(cabinet)
  wait(15, 1)
  stop(bowl)
  wait(15, 1)
  stop(pot)
  wait(15, 1)
  stop(cabinet)
;}wash-up

;watchTV{
  go(living_room)
  return(sofa)
  start(tv)
  wait(5400, 600)
  stop(tv)
;}watchTV

;phone-call{
  return(phone_book)
  start(phone_book)
  wait(160, 10)
  stop(phone_book)
  return(phone)
  start(phone)
  wait(220, 15)
  wander(-1, -1)
  wait(290, 7)
  wander(-1, -1)
  wait(300, 17)
  wander(-1, -1)
  wait(150, 1)
  return(phone)
  stop(phone)
;}phone-call



; change clothes
;change{
  go(wardrobe_1)
  wait(60, 7)
  go(room_1)
  wait(120, 15)
;}change

; go to bathroom: toilet teeth shower
go(bathroom)
;use-toilet-1{
  return(toilet)
  wait(420, 50)
;}use-toilet-1
;brush-teeth{
 wander(-1, -1)
 return(water_hot_basin)
 ; error
 wait(60, 10)
 start(water_hot_basin)
 wait(25, 5)
 stop(water_hot_basin)
 wait(200, 20)
 start(water_hot_basin)
 wait(25, 5)
 stop(water_hot_basin)
 wait(60, 10)
 wander(0.75, 0)
;}brush-teeth
;shower{
 return(water_hot_bath)
 start(water_hot_bath)
 wait(15, 3)
 start(water_cold_bath)
 wait(500, 77)
 stop(water_hot_basin)
 wait(15, 3)
 stop(water_cold_bath)
 wait(45, 5)
 wander(0.75, 0)
 wait(120, 15)
;}shower

; go to room_1 relax in bed
;relax{
  go(room_1)
  return(desk_1)
  wait(1800, 300)
  wander(-1, -1)
  wait(420, 30)
  return(desk_1)
  wait(1000, 150)
;}relax
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;day 3 afternoon

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;day 4 afternoon
; go to room_1 sleep
;sleep{
  return(bed_1)
  wait(32400, 900)
  wander(-1, -1)
;}sleep

; go to wardrobe and get new clothes
;change-1{
 go(wardrobe_1)
 wait(75, 9)
 go(room_1)
 wait(120, 4)
;}change-1

; go to toillet wash hands
go(bathroom)
;use-toilet-2{
  return(toilet)
  wait(300, 30)
;}use-toilet-2

;wash-hands-1{
  return(water_hot_basin)
  start(water_hot_basin)
    wait(90, 15)
  stop(water_hot_basin)
;}wash-hands-1

; go to kitchen prepeare meal - eat in living room - wash up
go(kitchen)
;prepare-breakfast{
  return(fridge)
  wait(120, 15)
  return(toster)
  wait(30, 5)
  start(toster)
    wait(15, 2)
    return(cabinet)
    wait(15, 2)
    start(cabinet)
    wait(15, 2)
    start(bowl)
    wait(15, 2)
    start(oatmeal)
    wait(75, 5)
    stop(oatmeal)
  stop(cabinet)
  wander(-1, -1)
  return(toster)
  stop(toster)
  wait(95, 3)
  return(fridge)
  wait(40, 5)
  return(toster)
  wait(15, 3)
;}prepare-breakfast

;eat-brekfast{
 return(table)
 wait(1200, 50)
;}eat-brekfast

;wash-up-b{
  return(water_cold_sink)
  start(water_cold_sink)
  wait(15, 1)
  start(water_hot_sink)
  wait(300, 20)
  stop(water_cold_sink)
  stop(water_hot_sink)
  wait(120, 15)
  return(cabinet)
  start(cabinet)
  wait(15, 1)
  stop(bowl)
  wait(15, 1)
  wait(15, 1)
  stop(cabinet)
;}wash-up-b

; go to bathroom wash teeth
go(bathroom)
;brush-teeth-1{
 wander(-1, -1)
 return(water_hot_basin)
 ; error
 wait(60, 10)
 start(water_hot_basin)
 wait(25, 5)
 stop(water_hot_basin)
 wait(200, 20)
 start(water_hot_basin)
 wait(25, 5)
 stop(water_hot_basin)
 wait(60, 10)
 wander(0.75, 0)
;}brush-teeth-1


; go to room_1 and work a bit on desk_1
go(room_1)
;work-home{
  return(desk_1)
  wait(10800, 350)
;}work-home

;watchTV{
  go(living_room)
  return(sofa)
  start(tv)
  wait(3600, 300)
  stop(tv)
;}watchTV

; eat snack
;snack{
go(kitchen)
return(fridge)
wait(60, 5)
return(toster)
wait(30, 5)
return(microwave)
wait(30, 5)
return(cabinet)
wait(15, 2)
start(cabinet)
wait(30, 5)
start(bowl)
wait(15, 2)
stop(cabinet)
return(toster)
wait(20, 5)
return(microwave)
wait(20, 5)
return(table)
wait(900, 60)
return(toster)
wait(30, 5)
return(fridge)
wait(30, 5)
return(water_hot_sink)
start(water_hot_sink)
wait(120, 15)
stop(water_hot_sink)
wait(15, 1)
return(cabinet)
wait(5, 1)
start(cabinet)
wait(5, 1)
stop(bowl)
wait(5, 1)
stop(cabinet)
;}snack



; go take a backpack and pack it in room
go(room_1)
return(desk_1)
wait(240, 20)
wander(-1, -1)
return(desk_1)
wait(45, 5)

; go to work
;work{
  go(outside)
  wait(18000, 900)
  go(hall)
;}work

; enter house and leave your coat and shoes
wait(90, 15)

; go to bedroom_1 and leave backpack
go(room_1)
return(desk_1)
wait(60, 10)

; go to bathroom use toilet wash hands
go(bathroom)
;use-toilet{
  return(toilet)
  wait(300, 30)
;}use-toilet
;wash-hands{
  return(water_hot_basin)
  start(water_hot_basin)
    wait(90, 15)
  stop(water_hot_basin)
;}wash-hands

; go to kitchen prepare a meal relax on sofa watch tv
go(kitchen)

;cook{
  do(fridge)
  return(burner)
  wait(60, 5)
  return(cabinet)
  start(cabinet)
  start(pot)
  stop(cabinet)
  return(water_cold_sink)
  start(water_cold_sink)
  wait(60, 15)
  stop(water_cold_sink)
  return(burner)
  start(burner)
  wait(240, 20)
  go(living_room)
  return(sofa)
  wait(930, 45)
  go(kitchen)
  return(burner)
  stop(burner)
  return(water_cold_sink)
  return(cabinet)
  start(cabinet)
  start(bowl)
  stop(cabinet)
  return(water_cold_sink)
  wait(180, 20)
;}cook

;eat{
 return(table)
 wait(1200, 50)
;}eat

;wash-up{
  return(water_cold_sink)
  start(water_cold_sink)
  wait(15, 1)
  start(water_hot_sink)
  wait(300, 20)
  stop(water_cold_sink)
  stop(water_hot_sink)
  wait(120, 15)
  return(cabinet)
  start(cabinet)
  wait(15, 1)
  stop(bowl)
  wait(15, 1)
  stop(pot)
  wait(15, 1)
  stop(cabinet)
;}wash-up

;watchTV{
  go(living_room)
  return(sofa)
  start(tv)
  wait(5400, 600)
  stop(tv)
;}watchTV

;phone-call{
  return(phone_book)
  start(phone_book)
  wait(160, 10)
  stop(phone_book)
  return(phone)
  start(phone)
  wait(220, 15)
  wander(-1, -1)
  wait(290, 7)
  wander(-1, -1)
  wait(300, 17)
  wander(-1, -1)
  wait(150, 1)
  return(phone)
  stop(phone)
;}phone-call



; change clothes
;change{
  go(wardrobe_1)
  wait(60, 7)
  go(room_1)
  wait(120, 15)
;}change

; go to bathroom: toilet teeth shower
go(bathroom)
;use-toilet-1{
  return(toilet)
  wait(420, 50)
;}use-toilet-1
;brush-teeth{
 wander(-1, -1)
 return(water_hot_basin)
 ; error
 wait(60, 10)
 start(water_hot_basin)
 wait(25, 5)
 stop(water_hot_basin)
 wait(200, 20)
 start(water_hot_basin)
 wait(25, 5)
 stop(water_hot_basin)
 wait(60, 10)
 wander(0.75, 0)
;}brush-teeth
;shower{
 return(water_hot_bath)
 start(water_hot_bath)
 wait(15, 3)
 start(water_cold_bath)
 wait(500, 77)
 stop(water_hot_basin)
 wait(15, 3)
 stop(water_cold_bath)
 wait(45, 5)
 wander(0.75, 0)
 wait(120, 15)
;}shower

; go to room_1 relax in bed
;relax{
  go(room_1)
  return(desk_1)
  wait(1800, 300)
  wander(-1, -1)
  wait(420, 30)
  return(desk_1)
  wait(1000, 150)
;}relax
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;day 4 afternoon

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;day 5 afternoon
; go to room_1 sleep
;sleep{
  return(bed_1)
  wait(32400, 900)
  wander(-1, -1)
;}sleep

; go to wardrobe and get new clothes
;change-1{
 go(wardrobe_1)
 wait(75, 9)
 go(room_1)
 wait(120, 4)
;}change-1

; go to toillet wash hands
go(bathroom)
;use-toilet-2{
  return(toilet)
  wait(300, 30)
;}use-toilet-2

;wash-hands-1{
  return(water_hot_basin)
  start(water_hot_basin)
    wait(90, 15)
  stop(water_hot_basin)
;}wash-hands-1

; go to kitchen prepeare meal - eat in living room - wash up
go(kitchen)
;prepare-breakfast{
  return(fridge)
  wait(120, 15)
  return(toster)
  wait(30, 5)
  start(toster)
    wait(15, 2)
    return(cabinet)
    wait(15, 2)
    start(cabinet)
    wait(15, 2)
    start(bowl)
    wait(15, 2)
    start(oatmeal)
    wait(75, 5)
    stop(oatmeal)
  stop(cabinet)
  wander(-1, -1)
  return(toster)
  stop(toster)
  wait(95, 3)
  return(fridge)
  wait(40, 5)
  return(toster)
  wait(15, 3)
;}prepare-breakfast

;eat-brekfast{
 return(table)
 wait(1200, 50)
;}eat-brekfast

;wash-up-b{
  return(water_cold_sink)
  start(water_cold_sink)
  wait(15, 1)
  start(water_hot_sink)
  wait(300, 20)
  stop(water_cold_sink)
  stop(water_hot_sink)
  wait(120, 15)
  return(cabinet)
  start(cabinet)
  wait(15, 1)
  stop(bowl)
  wait(15, 1)
  wait(15, 1)
  stop(cabinet)
;}wash-up-b

; go to bathroom wash teeth
go(bathroom)
;brush-teeth-1{
 wander(-1, -1)
 return(water_hot_basin)
 ; error
 wait(60, 10)
 start(water_hot_basin)
 wait(25, 5)
 stop(water_hot_basin)
 wait(200, 20)
 start(water_hot_basin)
 wait(25, 5)
 stop(water_hot_basin)
 wait(60, 10)
 wander(0.75, 0)
;}brush-teeth-1


; go to room_1 and work a bit on desk_1
go(room_1)
;work-home{
  return(desk_1)
  wait(10800, 350)
;}work-home

;watchTV{
  go(living_room)
  return(sofa)
  start(tv)
  wait(3600, 300)
  stop(tv)
;}watchTV

; eat snack
;snack{
go(kitchen)
return(fridge)
wait(60, 5)
return(toster)
wait(30, 5)
return(microwave)
wait(30, 5)
return(cabinet)
wait(15, 2)
start(cabinet)
wait(30, 5)
start(bowl)
wait(15, 2)
stop(cabinet)
return(toster)
wait(20, 5)
return(microwave)
wait(20, 5)
return(table)
wait(900, 60)
return(toster)
wait(30, 5)
return(fridge)
wait(30, 5)
return(water_hot_sink)
start(water_hot_sink)
wait(120, 15)
stop(water_hot_sink)
wait(15, 1)
return(cabinet)
wait(5, 1)
start(cabinet)
wait(5, 1)
stop(bowl)
wait(5, 1)
stop(cabinet)
;}snack



; go take a backpack and pack it in room
go(room_1)
return(desk_1)
wait(240, 20)
wander(-1, -1)
return(desk_1)
wait(45, 5)

; go to work
;work{
  go(outside)
  wait(18000, 900)
  go(hall)
;}work

; enter house and leave your coat and shoes
wait(90, 15)

; go to bedroom_1 and leave backpack
go(room_1)
return(desk_1)
wait(60, 10)

; go to bathroom use toilet wash hands
go(bathroom)
;use-toilet{
  return(toilet)
  wait(300, 30)
;}use-toilet
;wash-hands{
  return(water_hot_basin)
  start(water_hot_basin)
    wait(90, 15)
  stop(water_hot_basin)
;}wash-hands

; go to kitchen prepare a meal relax on sofa watch tv
go(kitchen)

;cook{
  do(fridge)
  return(burner)
  wait(60, 5)
  return(cabinet)
  start(cabinet)
  start(pot)
  stop(cabinet)
  return(water_cold_sink)
  start(water_cold_sink)
  wait(60, 15)
  stop(water_cold_sink)
  return(burner)
  start(burner)
  wait(240, 20)
  go(living_room)
  return(sofa)
  wait(930, 45)
  go(kitchen)
  return(burner)
  stop(burner)
  return(water_cold_sink)
  return(cabinet)
  start(cabinet)
  start(bowl)
  stop(cabinet)
  return(water_cold_sink)
  wait(180, 20)
;}cook

;eat{
 return(table)
 wait(1200, 50)
;}eat

;wash-up{
  return(water_cold_sink)
  start(water_cold_sink)
  wait(15, 1)
  start(water_hot_sink)
  wait(300, 20)
  stop(water_cold_sink)
  stop(water_hot_sink)
  wait(120, 15)
  return(cabinet)
  start(cabinet)
  wait(15, 1)
  stop(bowl)
  wait(15, 1)
  stop(pot)
  wait(15, 1)
  stop(cabinet)
;}wash-up

;watchTV{
  go(living_room)
  return(sofa)
  start(tv)
  wait(5400, 600)
  stop(tv)
;}watchTV

;phone-call{
  return(phone_book)
  start(phone_book)
  wait(160, 10)
  stop(phone_book)
  return(phone)
  start(phone)
  wait(220, 15)
  wander(-1, -1)
  wait(290, 7)
  wander(-1, -1)
  wait(300, 17)
  wander(-1, -1)
  wait(150, 1)
  return(phone)
  stop(phone)
;}phone-call



; change clothes
;change{
  go(wardrobe_1)
  wait(60, 7)
  go(room_1)
  wait(120, 15)
;}change

; go to bathroom: toilet teeth shower
go(bathroom)
;use-toilet-1{
  return(toilet)
  wait(420, 50)
;}use-toilet-1
;brush-teeth{
 wander(-1, -1)
 return(water_hot_basin)
 ; error
 wait(60, 10)
 start(water_hot_basin)
 wait(25, 5)
 stop(water_hot_basin)
 wait(200, 20)
 start(water_hot_basin)
 wait(25, 5)
 stop(water_hot_basin)
 wait(60, 10)
 wander(0.75, 0)
;}brush-teeth
;shower{
 return(water_hot_bath)
 start(water_hot_bath)
 wait(15, 3)
 start(water_cold_bath)
 wait(500, 77)
 stop(water_hot_basin)
 wait(15, 3)
 stop(water_cold_bath)
 wait(45, 5)
 wander(0.75, 0)
 wait(120, 15)
;}shower

; go to room_1 relax in bed
;relax{
  go(room_1)
  return(desk_1)
  wait(1800, 300)
  wander(-1, -1)
  wait(420, 30)
  return(desk_1)
  wait(1000, 150)
;}relax
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;day 5 afternoon

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;day 6
; go to room_1 sleep - sleep late Friday/Saturday - an hour extra
;sleep{
  return(bed_1)
  wait(36000, 900)
  wander(-1, -1)
;}sleep

; go to wardrobe and get new clothes
;change-1{
 go(wardrobe_1)
 wait(75, 9)
 go(room_1)
 wait(120, 4)
;}change-1

; go to toillet wash hands
go(bathroom)
;use-toilet-2{
  return(toilet)
  wait(300, 30)
;}use-toilet-2

;wash-hands-1{
  return(water_hot_basin)
  start(water_hot_basin)
    wait(90, 15)
  stop(water_hot_basin)
;}wash-hands-1

; go to kitchen prepeare meal - eat in living room - wash up
go(kitchen)
;prepare-breakfast{
  return(fridge)
  wait(120, 15)
  return(toster)
  wait(30, 5)
  start(toster)
    wait(15, 2)
    return(cabinet)
    wait(15, 2)
    start(cabinet)
    wait(15, 2)
    start(bowl)
    wait(15, 2)
    start(oatmeal)
    wait(75, 5)
    stop(oatmeal)
  stop(cabinet)
  wander(-1, -1)
  return(toster)
  stop(toster)
  wait(95, 3)
  return(fridge)
  wait(40, 5)
  return(toster)
  wait(15, 3)
;}prepare-breakfast

;eat-brekfast{
 return(table)
 wait(1200, 50)
;}eat-brekfast

;wash-up-b{
  return(water_cold_sink)
  start(water_cold_sink)
  wait(15, 1)
  start(water_hot_sink)
  wait(300, 20)
  stop(water_cold_sink)
  stop(water_hot_sink)
  wait(120, 15)
  return(cabinet)
  start(cabinet)
  wait(15, 1)
  stop(bowl)
  wait(15, 1)
  wait(15, 1)
  stop(cabinet)
;}wash-up-b

; go to bathroom wash teeth
go(bathroom)
;brush-teeth-1{
 wander(-1, -1)
 return(water_hot_basin)
 ; error
 wait(60, 10)
 start(water_hot_basin)
 wait(25, 5)
 stop(water_hot_basin)
 wait(200, 20)
 start(water_hot_basin)
 wait(25, 5)
 stop(water_hot_basin)
 wait(60, 10)
 wander(0.75, 0)
;}brush-teeth-1


; go outiside - shopping
;shopping{
  go(outside)
  wait(12600, 1800)
  go(hall)
;}shopping


; enter house and leave your coat and shoes
wait(90, 15)


; go to kitchen and unpack shoppings
go(kitchen)
return(cabinet)
start(cabinet)
wait(300, 20)
stop(cabinet)
return(fridge)
wait(300, 20)
return(burner)
wait(120, 10)


; go to bathroom use toilet wash hands
go(bathroom)
;use-toilet{
  return(toilet)
  wait(300, 30)
;}use-toilet
;wash-hands{
  return(water_hot_basin)
  start(water_hot_basin)
    wait(90, 15)
  stop(water_hot_basin)
;}wash-hands

; go to kitchen prepare a meal relax on sofa watch tv
go(kitchen)

;cook{
  do(fridge)
  return(burner)
  wait(60, 5)
  return(cabinet)
  start(cabinet)
  start(pot)
  stop(cabinet)
  return(water_cold_sink)
  start(water_cold_sink)
  wait(60, 15)
  stop(water_cold_sink)
  return(burner)
  start(burner)
  wait(240, 20)
  go(living_room)
  return(sofa)
  wait(930, 45)
  go(kitchen)
  return(burner)
  stop(burner)
  return(water_cold_sink)
  return(cabinet)
  start(cabinet)
  start(bowl)
  stop(cabinet)
  return(water_cold_sink)
  wait(180, 20)
;}cook

;eat{
 return(table)
 wait(1200, 50)
;}eat

;wash-up{
  return(water_cold_sink)
  start(water_cold_sink)
  wait(15, 1)
  start(water_hot_sink)
  wait(300, 20)
  stop(water_cold_sink)
  stop(water_hot_sink)
  wait(120, 15)
  return(cabinet)
  start(cabinet)
  wait(15, 1)
  stop(bowl)
  wait(15, 1)
  stop(pot)
  wait(15, 1)
  stop(cabinet)
;}wash-up

;watchTV{
  go(living_room)
  return(sofa)
  start(tv)
  wait(7200, 600)
  stop(tv)
;}watchTV

;phone-call{
  return(phone_book)
  start(phone_book)
  wait(60, 10)
  stop(phone_book)
  return(phone)
  start(phone)
  wait(220, 15)
  wander(-1, -1)
  wait(290, 7)
  wander(-1, -1)
  wait(300, 17)
  wander(-1, -1)
  wait(250, 1)
  return(phone)
  stop(phone)
;}phone-call

; go to room_1 and work a bit on desk_1
go(room_1)
;work-home{
  return(desk_1)
  wait(9000, 350)
;}work-home

; go to bathroom: toilet teeth shower
go(bathroom)
;use-toilet-1{
  return(toilet)
  wait(420, 50)
;}use-toilet-1
;brush-teeth{
 wander(-1, -1)
 return(water_hot_basin)
 ; error
 wait(60, 10)
 start(water_hot_basin)
 wait(25, 5)
 stop(water_hot_basin)
 wait(200, 20)
 start(water_hot_basin)
 wait(25, 5)
 stop(water_hot_basin)
 wait(60, 10)
 wander(0.75, 0)
;}brush-teeth
;shower{
 return(water_hot_bath)
 start(water_hot_bath)
 wait(15, 3)
 start(water_cold_bath)
 wait(500, 77)
 stop(water_hot_basin)
 wait(15, 3)
 stop(water_cold_bath)
 wait(45, 5)
 wander(0.75, 0)
 wait(120, 15)
;}shower

; change clothes
;change{
  go(wardrobe_1)
  wait(60, 7)
  go(room_1)
  wait(120, 15)
;}change


; party
;party{
go(outside)
wait(18000, 500)
;}party

; wash teeth
go(bathroom)
;brush-teeth{
 wander(-1, -1)
 return(water_hot_basin)
 ; error
 wait(60, 10)
 start(water_hot_basin)
 wait(25, 5)
 stop(water_hot_basin)
 wait(200, 20)
 start(water_hot_basin)
 wait(25, 5)
 stop(water_hot_basin)
 wait(60, 10)
 wander(0.75, 0)
;}brush-teeth

go(room_1)
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;day 6

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;day 7
; go to room_1 sleep - sleep late Friday/Saturday - an hour extra
;sleep{
  return(bed_1)
  wait(36000, 900)
  wander(-1, -1)
;}sleep

; go to wardrobe and get new clothes
;change-1{
 go(wardrobe_1)
 wait(75, 9)
 go(room_1)
 wait(120, 4)
;}change-1

; go to toillet wash hands
go(bathroom)
;use-toilet-2{
  return(toilet)
  wait(300, 30)
;}use-toilet-2

;wash-hands-1{
  return(water_hot_basin)
  start(water_hot_basin)
    wait(90, 15)
  stop(water_hot_basin)
;}wash-hands-1

; go to kitchen prepeare meal - eat in living room - wash up
go(kitchen)
;prepare-breakfast{
  return(fridge)
  wait(120, 15)
  return(toster)
  wait(30, 5)
  start(toster)
    wait(15, 2)
    return(cabinet)
    wait(15, 2)
    start(cabinet)
    wait(15, 2)
    start(bowl)
    wait(15, 2)
    start(oatmeal)
    wait(75, 5)
    stop(oatmeal)
  stop(cabinet)
  wander(-1, -1)
  return(toster)
  stop(toster)
  wait(95, 3)
  return(fridge)
  wait(40, 5)
  return(toster)
  wait(15, 3)
;}prepare-breakfast

;eat-brekfast{
 return(table)
 wait(1200, 50)
;}eat-brekfast

;wash-up-b{
  return(water_cold_sink)
  start(water_cold_sink)
  wait(15, 1)
  start(water_hot_sink)
  wait(300, 20)
  stop(water_cold_sink)
  stop(water_hot_sink)
  wait(120, 15)
  return(cabinet)
  start(cabinet)
  wait(15, 1)
  stop(bowl)
  wait(15, 1)
  wait(15, 1)
  stop(cabinet)
;}wash-up-b

; go to bathroom wash teeth
go(bathroom)
;brush-teeth-1{
 wander(-1, -1)
 return(water_hot_basin)
 ; error
 wait(60, 10)
 start(water_hot_basin)
 wait(25, 5)
 stop(water_hot_basin)
 wait(200, 20)
 start(water_hot_basin)
 wait(25, 5)
 stop(water_hot_basin)
 wait(60, 10)
 wander(0.75, 0)
;}brush-teeth-1

;watchTV{
  go(living_room)
  return(sofa)
  start(tv)
  wait(9000, 900)
  stop(tv)
;}watchTV

; go to room_1 and work a bit on desk_1
go(room_1)
;work-home{
  return(desk_1)
  wait(10800, 350)
;}work-home

; go to bathroom use toilet wash hands
go(bathroom)
;use-toilet{
  return(toilet)
  wait(300, 30)
;}use-toilet
;wash-hands{
  return(water_hot_basin)
  start(water_hot_basin)
    wait(90, 15)
  stop(water_hot_basin)
;}wash-hands

; go to kitchen prepare a meal relax on sofa watch tv
go(kitchen)

;cook{
  do(fridge)
  return(burner)
  wait(60, 5)
  return(cabinet)
  start(cabinet)
  start(pot)
  stop(cabinet)
  return(water_cold_sink)
  start(water_cold_sink)
  wait(60, 15)
  stop(water_cold_sink)
  return(burner)
  start(burner)
  wait(240, 20)
  go(living_room)
  return(sofa)
  wait(930, 45)
  go(kitchen)
  return(burner)
  stop(burner)
  return(water_cold_sink)
  return(cabinet)
  start(cabinet)
  start(bowl)
  stop(cabinet)
  return(water_cold_sink)
  wait(180, 20)
;}cook

;eat{
 return(table)
 wait(1200, 50)
;}eat

;wash-up{
  return(water_cold_sink)
  start(water_cold_sink)
  wait(15, 1)
  start(water_hot_sink)
  wait(300, 20)
  stop(water_cold_sink)
  stop(water_hot_sink)
  wait(120, 15)
  return(cabinet)
  start(cabinet)
  wait(15, 1)
  stop(bowl)
  wait(15, 1)
  stop(pot)
  wait(15, 1)
  stop(cabinet)
;}wash-up

;readBook{
  go(living_room)
  return(sofa)
  wait(5400, 600)
;}readBook

; change clothes
;change{
  go(wardrobe_1)
  wait(60, 7)
  go(room_1)
  wait(120, 15)
;}change

; go to bathroom: toilet teeth shower
go(bathroom)
;use-toilet-1{
  return(toilet)
  wait(420, 50)
;}use-toilet-1
;brush-teeth{
 wander(-1, -1)
 return(water_hot_basin)
 ; error
 wait(60, 10)
 start(water_hot_basin)
 wait(25, 5)
 stop(water_hot_basin)
 wait(200, 20)
 start(water_hot_basin)
 wait(25, 5)
 stop(water_hot_basin)
 wait(60, 10)
 wander(0.75, 0)
;}brush-teeth
;shower{
 return(water_hot_bath)
 start(water_hot_bath)
 wait(15, 3)
 start(water_cold_bath)
 wait(500, 77)
 stop(water_hot_basin)
 wait(15, 3)
 stop(water_cold_bath)
 wait(45, 5)
 wander(0.75, 0)
 wait(120, 15)
;}shower

; go to room_1 relax in bed
;relax{
  go(room_1)
  return(desk_1)
  wait(1800, 300)
  wander(-1, -1)
  wait(420, 30)
  return(desk_1)
  wait(1000, 150)
;}relax
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;day 7

; go to room_1 sleep - sleep late Friday/Saturday - an hour extra
;sleep{
  return(bed_1)
  wait(32400, 900)
  wander(-1, -1)
;}sleep

; be careful
; wait cannot be used just before activity-block ends
; wait must be used within **start** **stop**
; you have to be in a room to use a sensor
; be care-full not to use the same names for blocks and sensors
