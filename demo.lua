
f={1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1}
w1=1
w2=2
flag=0
function E(o,m,c)
Led_mode_switch(o,m)
Led_set_color(o,c)
end
function run(l,r)
Single_wheel_ctrl(w1,l)
Single_wheel_ctrl(w2,r)
end
function stop()
Single_wheel_stop(w1,1)
Single_wheel_stop(w2,1)
end
function quit()
if Get_key1_data()==1 or Get_key2_data()==1 then
stop()
return 1
end
return 0
end
function reset()
Reset_motor_pos(1)
Reset_motor_pos(2)
pi=0
end
function wait(t)
Delay_ms(t)
end
function delay(t)
while t>0 do
wait(100)
if quit()==1 then
flag=1
return 1
end
t=t-1
end
return 0
end
function turn(lh)
reset()
delay(10)
if lh==0 then
return
end
if lh<0 then
Single_wheel_length(1,-13,168)
Single_wheel_length(2,-13,168)
else
Single_wheel_length(1,13,168)
Single_wheel_length(2,13,168)
end
delay(21)
end
function move()
E(2,3,2)
reset()
delay(10)
Single_wheel_length(1,-14,315)
Single_wheel_length(2,14,315)
delay(19)
wait(100)
Led_set_color(2,0)
return 0
end
function tr()
E(2,3,5)
turn(90)
wait(100)
Led_set_color(2,0)
return 0
end
function tl()
E(2,3,4)
turn(-90)
wait(100)
Led_set_color(2,0)
return 0
end
local s={
[1]=move,
[2]=tr,
[3]=tl
}
i=1
stop()
Delay_ms(10)
repeat
if quit()==1 then
break
end
if flag==1 then
break
end
if s[f[i]]==nil or s[f[i]]()==nil then
Beep_play(26)
wait(200)
Beep_play(25)
wait(200)
break
end
i=i+1
until nil