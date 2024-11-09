"""Support for Satel Integra modifiable outputs represented as switches."""
from __future__ import annotations

import logging

from homeassistant.helpers.entity import Entity

from .const import (
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

class SatelIntegraEntity(Entity):
    """Base class for Satel entities."""

    _attr_should_poll = False

    def __init__(self, controller, device_number, device_name, device_type):
        """Initialize the binary_sensor."""
        self._device_number = device_number
        self._name = device_name
        self._satel = controller
        self._device_type = device_type
        self._attr_unique_id = f"${DOMAIN}.{device_type}${device_number}"
        _LOGGER.info("SatelIntegraEntity.__init__ ### %s - %s", self._attr_unique_id, self._name)

    @property
    def name(self):
        """Return the name of the switch."""
        return self._name
