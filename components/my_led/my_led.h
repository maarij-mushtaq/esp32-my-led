#pragma once                              // include this header only once per build

#include "esphome.h"                      // ESPHome core (Component, Switch, etc.)
#include "driver/gpio.h"                  // ESP-IDF GPIO API (gpio_set_level, direction)

namespace my_led {                        // keep our names isolated

// A Home Assistant switch that directly drives a single GPIO on ESP32
class LedSwitch : public esphome::Component, public esphome::switch_::Switch {
 public:
  // Choose the pin (e.g., GPIO_NUM_14) and whether logic is inverted (active-low)
  explicit LedSwitch(gpio_num_t pin, bool inverted = false)
      : pin_(pin), inverted_(inverted) {}

  // Runs once at boot
  void setup() override {
    gpio_reset_pin(pin_);                 // clear any previous config on that pin
    gpio_set_direction(pin_, GPIO_MODE_OUTPUT); // make it an OUTPUT pin

    // start OFF (publish_state(false)) while honoring inversion
    const int level = inverted_ ? 1 : 0;  // if inverted, high=OFF; else low=OFF
    gpio_set_level(pin_, level);          // drive the pin to "OFF" level
    this->publish_state(false);           // tell HA we are OFF at start
  }

  // run early (hardware-level)
  float get_setup_priority() const override {
    return esphome::setup_priority::HARDWARE;
  }

 protected:
  // Called when HA toggles the switch (true=ON, false=OFF)
  void write_state(bool state) override {
    const bool level = inverted_ ? !state : state; // map logical state to pin level
    gpio_set_level(pin_, level ? 1 : 0);   // write the pin (1=HIGH, 0=LOW)
    this->publish_state(state);            // report the new state back to HA
  }

 private:
  gpio_num_t pin_;                         // which GPIO we control
  bool inverted_;                          // whether logic is inverted
};

}  // namespace my_led
