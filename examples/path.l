origin(hall)
go(kitchen)
; do cooking

; do(cooking){
  ; do(cabinet)
  ; do(bowl)
; }
cook{
  eat{
    start(water_hot)
    wait(100, 0.1)
    stop(water_hot)
  }eat
  do(burner)
}cook

; go(living_room)
; table == eat
; do(table)
; go(kitchen)
; hot_water == wash_up
; do(water_hot)
go(hall)



; be careful
; wait cannot be used just before activity-block ends
; wait must be used within **start** **stop**
; you have to be in a room to use a sensor
; be care-full not to use the same names for blocks and sensors
