from machine import Pin
import time

#gpio ühenduste numbrid
echo_ees_pin = 21 # < --- Sisesta gpio pin number mis on ühendatud ultrasonicu echo
trig_ees_pin = 20 # < --- Sisesta gpio pin number mis on ühendatud ultrasonicu trig
echo_taga_pin = 19 # < --- Sisesta gpio pin number mis on ühendatud ultrasonicu echo
trig_taga_pin = 18 # < --- Sisesta gpio pin number mis on ühendatud ultrasonicu trig
buzzer_pin = 17 # < --- Sisesta gpio pin number mis on ühendatud buzzeriga
row_numbers = [0,5,8,3,15,9,14,11] # < --- Sisesta gpio pin numberid ,mis on ühendatud maatriksi ridadega
colum_numbers = [4,10,13,1,12,6,2,7] # < --- Sisesta gpio pin numberid ,mis on ühendatud maatriksi veergudega

#globaalsed muutujad
row_pins = []
colum_pins = []#<--- List colum Pin objektide jaoks
eesmine_list = []#<--List ultrasonic info salvestamiseks 
tagumine_list = []#<---List ultrasonic info salvestamiseks 
dist_cm_ees = 0 
dist_cm_taga = 0 
delay_us = 10 # < --- Andmelehest leitud perioodi aeg
buzzer_time = 0 

#gpio-de initsialiseerimine
#buzzer
buzzer_output=Pin(buzzer_pin,Pin.OUT)
#ultrasonicud
trigger_ees = Pin(trig_ees_pin, Pin.OUT)
echo_ees = Pin(echo_ees_pin, Pin.IN)
trigger_taga = Pin(trig_taga_pin, Pin.OUT)
echo_taga = Pin(echo_taga_pin, Pin.IN)
#led
def init():
    for gpio_colum in colum_numbers:
        pin = Pin(gpio_colum, Pin.OUT)
        colum_pins.append(pin)
        pin.value(1)
    for gpio_row in row_numbers:
        pin = Pin(gpio_row, Pin.OUT)
        row_pins.append(pin)
        pin.value(1) 


"""
Andmeleht LMD08088AUE-102 8x8 led maatriksi jaoks
https://www.tme.eu/Document/e0dbcbcb2f2e4494fa7cbd87531adbd6/LMD08088AUE-102.pdf
"""

#1.led kontroll
def tagumine():
    if dist_cm_taga>75:
        row_pins[3].value(0)
        row_pins[2].value(1)
        row_pins[1].value(1)
        row_pins[0].value(1)
    elif dist_cm_taga>50 and dist_cm_taga<75:
        row_pins[3].value(1)
        row_pins[2].value(0)
        row_pins[1].value(1)
        row_pins[0].value(1)
        
    elif dist_cm_taga>25 and dist_cm_taga<50:
        row_pins[3].value(1)
        row_pins[2].value(1)
        row_pins[1].value(0)
        row_pins[0].value(1)
       
    elif dist_cm_taga<25:
        row_pins[3].value(1)
        row_pins[2].value(1)
        row_pins[1].value(1)
        row_pins[0].value(0)
        
def eesmine():
    if dist_cm_ees>75:
        row_pins[4].value(0)
        row_pins[5].value(1)
        row_pins[6].value(1)
        row_pins[7].value(1)
        
    elif dist_cm_ees>50 and dist_cm_ees<75:
        row_pins[4].value(1)
        row_pins[5].value(0)
        row_pins[6].value(1)
        row_pins[7].value(1)
        
    elif dist_cm_ees>25 and dist_cm_ees<50:
        row_pins[4].value(1)
        row_pins[5].value(1)
        row_pins[6].value(0)
        row_pins[7].value(1)
        
    elif dist_cm_ees<25:
        row_pins[4].value(1)
        row_pins[5].value(1)
        row_pins[6].value(1)
        row_pins[7].value(0)
        
#2.buzzer kontroll
def buzzer():
    global buzzer_time
    if dist_cm_ees < 25 or dist_cm_taga < 25:
        buzzer_output.value(1)
               
    elif dist_cm_ees < 50 and dist_cm_ees > 25 or dist_cm_taga < 50 and dist_cm_taga > 25:
        buzzer_output.value(0)
        if time.time()-buzzer_time>=0.1:
            buzzer_output.value(1)
            buzzer_time=time.time()
            
    elif dist_cm_ees < 75 and dist_cm_ees > 50 or dist_cm_taga < 75 and dist_cm_taga > 50:
        buzzer_output.value(0)
        if time.time()-buzzer_time>=2:
            buzzer_output.value(1)
            buzzer_time=time.time()
    elif dist_cm_ees > 75 or dist_cm_taga > 75:
        buzzer_output.value(0)

"""
Andmeleht Ultrasonic Ranging Module HC - SR04 jaoks
https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf
"""
#3.ultrasonic
def get_ultrasonic_reading(trigger,echo):
    timeout_us=100_000#<--- funktsiooni jooksmise ülempiir 
    default_value=-1#<--- väärtus vigase lugemise korral 
    method_start_us = time.ticks_us()#<--- aeg mikrosekundites
    trigger.high()#<--- Saadab välja signaali 
    time.sleep_us(delay_us)#<-- Programm ootab 10 mikrosekundit
    trigger.low()
    signal_rise = time.ticks_us()
    signal_fall = signal_rise
    while echo.value() == 0:#kontrollime ,et echo oleks ikka 1 mitte 0 kui 0 siis seame algus aja hetke ajaks
        signal_rise = time.ticks_us()
        if time.ticks_diff(signal_rise, method_start_us) > timeout_us:#<---kontrollib kaua ultrasonic signaali ei ole saanud ja kas peaks lõpetama selle kuulamise
            return default_value

    while echo.value() == 1:#kontrollime kas signaal on tagasi jõudnud
        signal_fall = time.ticks_us()
        if time.ticks_diff(signal_fall, method_start_us) > timeout_us:#<--- kontrollib kaua ultrasonic signaali saab ja kas peaks lõpetama selle kuulamise
            return default_value

    duration_us = signal_fall - signal_rise #<-- Arvutab aja välja läinud signaali ja tagasi tulnud signaali vahel

    return duration_us


def get_distance_in_cm(duration_us):
    if duration_us == -1:
        return 100
    #distance_from_object_in_cm=duration_us/2 * 0.0343 <--- võib ka seda valemit kasutada
    distance_from_object_in_cm = duration_us/58#<---Valem ultrasonicu andmelehest
    return distance_from_object_in_cm

def average_filter(reading,reading_list):
     global eesmine_list
     global tagumine_list
     pikkus = 30#<-- mitme elemendi peale tahame average-it votta
     tagastus=0#<-- tagastus vaartus
     reading_list.append(reading)
     
     if len(reading_list)>=pikkus:  #<-- elementide koguse kontroll             
         if len(reading_list)>pikkus:#<-- elementide koguse kontroll kui rohkem kui maaratud pikkus eemaldame esimese elemendi 
             reading_list.pop(0)
         
         tagastus=sum(reading_list)/len(reading_list)
     else:
         tagastus=sum(reading_list)/len(reading_list)
     return tagastus

#MAIN
def main():
    global dist_cm_ees, dist_cm_taga
    init()
    while True:
        try:
            #ultrasonic
            duration_us_ees = get_ultrasonic_reading(trigger_ees,echo_ees)
            duration_us_taga = get_ultrasonic_reading(trigger_taga,echo_taga)

            dist_cm_ees = average_filter(get_distance_in_cm(duration_us_ees),eesmine_list)
            dist_cm_taga = average_filter(get_distance_in_cm(duration_us_taga),tagumine_list)
            
            #print(f"ees:{dist_cm_ees}  taga:{dist_cm_taga}")
            
            #led 
            eesmine()
            tagumine()
            #buzzer
            buzzer()
            #time.sleep_ms(60)   #<--- juhul kui teil peaksid tekkima mõõtevead lisage see rida ja vähendage average funktsioonis muutujat pikkus 10 või vähema peale
        except KeyboardInterrupt:
            break 

if __name__ == "__main__":
    # Run the main function
    main()
    #Paneb ledid ja buzzeri kinni kui programm kinni läheb
    for row_pin in row_pins:
        row_pin.value(1)
    buzzer_output.value(0)
    


