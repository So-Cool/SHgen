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


wardrobe_1 1 2:
m01  0.5 1   1
door 0   1   room_1

room_1 5 4:
m11  1   1   1
m12  3   1   1
m13  4.5 1   1
m14  1   3   1
m15  3   3   1
m16  4.5 3   1
door 0   0.5 hall
door 5   3   wardrobe_1

wardrobe_2 1 2:
m21  0.5 1   1
door 0   1   room_2

room_2 5 4:
m31  1   1   1
m32  3   1   1
m33  4.5 1   1
m34  1   3   1
m35  3   3   1
m36  4.5 3   1
door 0   0.5 hall
door 5   3   wardrobe_2

hall 2.5 5:
m41  1.3 1   2
m42  1.3 3   2
m43  1.3 4.5 2
door 2.5 2   room_1
door 2.5 4   room_2
door 1.3 5   bathroom
door 0   4   cupboard
door 0   2   living_room



cupboard 1 1:
m51  0.5 0.5 1
door 1   0.5 hall

bathroom 2 2:
m61  1   1   1
door 1   0   hall

living_room 6 6:
m71  1   1   1
m72  3   1   1
m73  5   1   1
m74  1   3   1
m75  3   3   1
m76  5   3   1
m77  1   5   1
m78  3   5   1
m79  5   5   1
i78  5.5 0.5 phone_book
table-sensor    1   5   table
asterisk 5.5 0.4 phone
door 6   3   hall
door 3   6   kitchen

kitchen 6 2:
m81   1   1  1
m82   3   1  1
m83   5   1  1
ad1-a 6   1   water_hot
ad1-b 6   1   water_cold
ad1-c 3   2   burner
d81   4   2   cabinet
i81   4   2   oatmeal
i82   4   2   raisins
i83   4   2   brown_sugar
i84   4   2   bowl
i85   4   2   measuring_spoon
i86   4   2   medicine_container
i87   4   2   pot
door  3   0   living_room
