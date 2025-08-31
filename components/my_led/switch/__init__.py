import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import switch
from esphome.const import CONF_ID, CONF_PIN, CONF_INVERTED

my_led_ns = cg.esphome_ns.namespace("my_led")
LedSwitch = my_led_ns.class_("LedSwitch", cg.Component, switch.Switch)

CONFIG_SCHEMA = switch.switch_schema(LedSwitch).extend({
    cv.Required(CONF_PIN): cv.int_,
    cv.Optional(CONF_INVERTED, default=False): cv.boolean,
})

async def to_code(config):
    # Include your header into main.cpp (no trailing semicolon)
    cg.add(cg.RawStatement('#include "components/my_led/my_led.h"'))

    var = cg.new_Pvariable(config[CONF_ID], config[CONF_PIN], config[CONF_INVERTED])
    await cg.register_component(var, config)
    await switch.register_switch(var, config)
