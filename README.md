# Parking sensor
This project was created as part of a Computer Architecture course, where we were required to make a learning video in Estonian. My partner and I decided to create a video demonstrating how to build a parking sensor.

We used an 8x8 LED matrix, a buzzer, two ultrasonic sensors, and a Raspberry Pi Pico to build the sensor. The system measures the distance using the ultrasonic sensors and provides an alert when an object is closer than 75 cm.

The buzzer frequency increases as the distance decreases. The buzzer will sound in intervals, with the frequency increasing every 25 cm. Specifically:

-If an object is less than 25 cm away, the buzzer will sound continuously.
-For distances between 25 cm and 50 cm, the buzzer will beep at a regular interval.
-For distances between 50 cm and 75 cm, the interval will be longer.
-If the object is greater than 75 cm away, the buzzer remains silent, indicating a safe distance.

The 25 cm distance steps are also displayed on the 8x8 LED matrix, giving a visual indication of the object's proximity.

[Watch the Parking Sensor tutorial on YouTube](https://www.youtube.com/watch?v=4RMuGI09aWw)

