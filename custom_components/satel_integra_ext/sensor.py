"""Support for Satel Integra zone states- represented as binary sensors."""
from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .entity import SatelIntegraEntity
from .const import (
    DATA_SATEL,
    CONF_TEMP_SENSORS,
    CONF_TEMP_SENSOR_NAME,
)

_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the Satel Integra temperature sensor devices."""
    if not discovery_info:
        return

    controller = hass.data[DATA_SATEL]

    async_add_entities(
        [SatelIntegraTemperatureSensor(controller, sensor_num, device_config_data[CONF_TEMP_SENSOR_NAME])
            for sensor_num, device_config_data in discovery_info[CONF_TEMP_SENSORS].items()],
        update_before_add=True)

PARALLEL_UPDATES = 0
SCAN_INTERVAL = timedelta(seconds=120)

class SatelIntegraTemperatureSensor(SatelIntegraEntity, SensorEntity):
    """Representation of an Satel Integra temperature sensor."""

    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_should_poll = True

    def __init__(
        self, controller, device_number, device_name
    ):
        """Initialize the sensor."""
        super().__init__(controller, device_number, device_name, "temp")

    async def async_update(self) -> None:
        # generate random temperature between 20.5 and 22.5
        _LOGGER.info("async_update sensor %s", self._device_number)
        import random
        # self._attr_native_value = float(round(random.uniform(20.5, 22.5), 1))

        try:
            self._attr_native_value = await self._satel.read_temp_and_wait(self._device_number)
        except TimeoutError:
            _LOGGER.error("Timeout error while reading temperature %s", self._device_number)

