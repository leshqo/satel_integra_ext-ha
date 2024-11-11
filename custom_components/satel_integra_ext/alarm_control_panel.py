"""Support for Satel Integra alarm, using ETHM module."""
from __future__ import annotations

import asyncio
from collections import OrderedDict

from satel_integra_ext.satel_integra import AlarmState

import homeassistant.components.alarm_control_panel as alarm
from homeassistant.components.alarm_control_panel import (
    AlarmControlPanelEntityFeature,
    AlarmControlPanelState,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .entity import SatelIntegraEntity
from .const import (
    CONF_ARM_HOME_MODE,
    CONF_DEVICE_PARTITIONS,
    CONF_ZONE_NAME,
    DATA_SATEL,
    SIGNAL_PANEL_MESSAGE,
    _LOGGER
)

STATE_MAP = OrderedDict(
    [
        (AlarmState.TRIGGERED, AlarmControlPanelState.TRIGGERED),
        (AlarmState.TRIGGERED_FIRE, AlarmControlPanelState.TRIGGERED),
        (AlarmState.ENTRY_TIME, AlarmControlPanelState.PENDING),
        (AlarmState.ARMED_MODE3, AlarmControlPanelState.ARMED_HOME),
        (AlarmState.ARMED_MODE2, AlarmControlPanelState.ARMED_HOME),
        (AlarmState.ARMED_MODE1, AlarmControlPanelState.ARMED_HOME),
        (AlarmState.ARMED_MODE0, AlarmControlPanelState.ARMED_AWAY),
        (AlarmState.EXIT_COUNTDOWN_OVER_10, AlarmControlPanelState.PENDING),
        (AlarmState.EXIT_COUNTDOWN_UNDER_10, AlarmControlPanelState.PENDING),
    ]
)

async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up for Satel Integra alarm panels."""
    if not discovery_info:
        return

    configured_partitions = discovery_info[CONF_DEVICE_PARTITIONS]
    controller = hass.data[DATA_SATEL]

    devices = []

    for partition_num, device_config_data in configured_partitions.items():
        zone_name = device_config_data[CONF_ZONE_NAME]
        arm_home_mode = device_config_data.get(CONF_ARM_HOME_MODE)
        device = SatelIntegraAlarmPanel(
            controller, zone_name, arm_home_mode, partition_num
        )
        devices.append(device)

    async_add_entities(devices)


class SatelIntegraAlarmPanel(SatelIntegraEntity, alarm.AlarmControlPanelEntity):
    """Representation of an AlarmDecoder-based alarm panel."""

    _attr_code_format = alarm.CodeFormat.NUMBER
    _attr_should_poll = False
    _attr_supported_features = (
        AlarmControlPanelEntityFeature.ARM_HOME
        | AlarmControlPanelEntityFeature.ARM_AWAY
    )

    def __init__(self, controller, name, arm_home_mode, partition_id):
        """Initialize the alarm panel."""
        super().__init__(controller, partition_id, name, "zone")
        self._arm_home_mode = arm_home_mode
        self._device_number = partition_id
        self._satel_alarm_state = self._read_alarm_state()

    async def async_added_to_hass(self) -> None:
        """Update alarm status and register callbacks for future updates."""
        _LOGGER.debug("Starts listening for panel messages")
        self.async_on_remove(
            async_dispatcher_connect(
                self.hass, SIGNAL_PANEL_MESSAGE, self._update_alarm_status
            )
        )

    @callback
    def _update_alarm_status(self):
        """Handle alarm status update."""
        state = self._read_alarm_state()
        _LOGGER.debug("Got status update, current status: %s", state)
        if state != self._satel_alarm_state:
            self._satel_alarm_state = state
            self.async_write_ha_state()
        else:
           _LOGGER.debug("Ignoring alarm status message, same state")

    def _read_alarm_state(self):
        """Read current status of the alarm and translate it into HA status."""

        # Default - disarmed:
        hass_alarm_status = AlarmControlPanelState.DISARMED

        if not self._satel.connected:
            return None

        _LOGGER.debug("State map of Satel: %s", self._satel.partition_states)

        for satel_state, ha_state in STATE_MAP.items():
            if (
                satel_state in self._satel.partition_states
                and self._device_number in self._satel.partition_states[satel_state]
            ):
                hass_alarm_status = ha_state
                break

        return hass_alarm_status

    async def async_alarm_disarm(self, code: str | None = None) -> None:
        """Send disarm command."""
        if not code:
            _LOGGER.debug("Code was empty or None")
            return

        clear_alarm_necessary = self._satel_alarm_state == AlarmControlPanelState.TRIGGERED

        _LOGGER.debug("Disarming, self._satel_alarm_state: %s", self._satel_alarm_state)

        await self._satel.disarm(code, [self._device_number])

        if clear_alarm_necessary:
            # Wait 1s before clearing the alarm
            await asyncio.sleep(1)
            await self._satel.clear_alarm(code, [self._device_number])

    async def async_alarm_arm_away(self, code: str | None = None) -> None:
        """Send arm away command."""
        _LOGGER.debug("Arming away")

        if code:
            await self._satel.arm(code, [self._device_number])

    async def async_alarm_arm_home(self, code: str | None = None) -> None:
        """Send arm home command."""
        _LOGGER.debug("Arming home")

        if code:
            await self._satel.arm(code, [self._device_number], self._arm_home_mode)

    @property
    def alarm_state(self) -> AlarmControlPanelState | None:
        """Return the state of the entity."""
        _LOGGER.debug("Getting property alarm_state: %s", self._satel_alarm_state)
        return self._satel_alarm_state