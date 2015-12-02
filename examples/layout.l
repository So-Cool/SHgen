;;;;;;;;;;;;;;;;;;;;;;;;;
; room_name width height
; sensor_name width height range
; sensor_name width height activity_name
; door_to width height
;;;;;;;;;;;;;;;;;;;;;;;;;
; __sensors_motion__position__range__
; __sensors_device__position__activity_name__
; __doors__
;;;;;;;;;;;;;;;;;;;;;;;;;

;;;
; prune
; i11
; i12
; i31
; i32
; i61
; i77
; i79
; i88
;;;;;


wardrobe_1 1 2:
m01  0.5 1   1
door 0   1   room_1

room_1 3 3:
m11  1   1   1
m12  2   1   1
m13  1   2   1
m15  2   2   1
i11  1   2   bed_1
i12  2.5 0.5 desk_1
door 0   0.5 hall
door 3   2.5 wardrobe_1

wardrobe_2 1 2:
m21  0.5 1   1
door 0   1   room_2

room_2 3 3:
m31  1   1   1
m32  2   1   1
m33  1   2   1
m35  2   2   1
i31  1   2   bed_2
i32  2.5 0.5 desk_2
door 0   0.5 hall
door 3   2.5 wardrobe_2

outside 1 1:
door 0.5 1 hall

hall 1 4:
m41  0.5 1   2
m42  0.5 3   2
door 0.5 0   outside
door 1   3.5 room_1
door 2.5 2.5 room_2
door 0.5 4   bathroom
door 0   3.5 cupboard
door 0   2.5 living_room

cupboard 1 1:
m51  0.5 0.5 1
door 1   0.5 hall

bathroom 2 2:
m61  1   1   1
ad0-a 0.5 1.7 water_hot_bath
ad0-b 0.5 1.7 water_cold_bath
i61  1.25 1.7 toilet
ad0-c 1.7 1.7 water_hot_basin
ad0-d 1.7 1.7 water_cold_basin
door  0.75 0   hall

living_room 4 3:
m71  1   0.75 1
m72  3   0.75 1
m73  1   2.25 1
m74  3   2.25 1
i79  1   0.5 sofa
i76  1   1.5 tv
i78  3.7 0.5 phone_book
asterisk 3.7 0.5 phone
door 4   2.5 hall
door 1.5 3   kitchen

kitchen 3 3:
m81   0.75 0.75 1
m83   2.25 0.75 1
m82   0.75 2.25 1
m84   2.25 2.25 1
ad1-a 2.75 2.25 water_hot_sink
ad1-b 2.75 2.25 water_cold_sink
ad1-c 1.5 2.75 burner
d81   2.50 2.75 cabinet
i81   2.50 2.75 oatmeal
i82   2.50 2.75 raisins
i83   2.50 2.75 brown_sugar
i84   2.50 2.75 bowl
i85   2.50 2.75 measuring_spoon
i86   2.50 2.75 medicine_container
i87   2.50 2.75 pot
i88   0.50 2.75 fridge
i89   0.75 2.75 toster
i80   2.50 2.75 ketle
i8a   2.75 2.75 microwave
i8b  0.6 0.4 table
door  1.5  0   living_room
