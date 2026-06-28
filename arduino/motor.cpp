#include "motor.h"
#include <Arduino.h>
#include <math.h>

namespace motors
{

  Motor::Motor(const char* name, uint8_t f_pin, uint8_t b_pin,
               uint8_t e_pin,int max_speed)
  :
  name_(name),
  f_pin_(f_pin),
  b_pin_(b_pin),
  e_pin_(e_pin),
  max_speed_(max_speed),
  is_stopped_(true)
  {
    //these are output from the Arduino and into
    //the L298N bridge
    pinMode(f_pin_,OUTPUT);
    pinMode(b_pin_,OUTPUT);
    pinMode(e_pin_,OUTPUT);
  }



  void 
  Motor::stop(){
  
    digitalWrite(f_pin_,LOW);
    digitalWrite(b_pin_,LOW);
    is_stopped_ = true;
  }

  void 
  Motor::enable(){
    digitalWrite(e_pin_,HIGH);
  }
  
  void 
  Motor::disable(){
    digitalWrite(e_pin_,LOW);
  }



  void 
  Motor::forward(int speed){
    
    digitalWrite(f_pin_,HIGH);
    digitalWrite(b_pin_,LOW);

    //here speed specifies the duty cycle and should be
    //between [0,255] 0 = always off, 255 = always on

    if(speed < 0)
      speed = 0;
    if(speed > 255)
      speed = 255;
    
    analogWrite(e_pin_,speed);
  }

  void 
  Motor::backward(int speed){
    digitalWrite(f_pin_,LOW);
    digitalWrite(b_pin_,HIGH);

    if(speed < 0)
      speed = 0;
    if(speed > 255)
      speed = 255;
    
    analogWrite(e_pin_,speed);
  }
}


