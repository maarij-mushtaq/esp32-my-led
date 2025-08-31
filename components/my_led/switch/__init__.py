import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import switch
from esphome.const import CONF_ID, CONF_PIN, CONF_INVERTED

# Bind to the C++ class in the my_led namespace
my_led_ns = cg.esphome_ns.namespace("my_led")
LedSwitch = my_led_ns.class_("LedSwitch", cg.Component, switch.Switch)

# YAML schema for:
# switch:
#   - platform: my_led
#     name: "Employee Outer Hall LED"
#     pin: 14
#     inverted: false
CONFIG_SCHEMA = switch.switch_schema(LedSwitch).extend({
    cv.Required(CONF_PIN): cv.int_,
    cv.Optional(CONF_INVERTED, default=False): cv.boolean,
})

async def to_code(config):
    # Create the C++ object with (pin, inverted)
    var = cg.new_Pvariable(config[CONF_ID], config[CONF_PIN], config[CONF_INVERTED])
    # Register as a component and a switch entity
    await cg.register_component(var, config)
    await switch.register_switch(var, config)
