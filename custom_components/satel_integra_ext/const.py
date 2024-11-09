import logging

_LOGGER = logging.getLogger(__package__)

DOMAIN = "satel_integra_ext"

DEFAULT_ALARM_NAME = "satel_integra"
DEFAULT_PORT = 7094
DEFAULT_CONF_ARM_HOME_MODE = 1
DEFAULT_DEVICE_PARTITION = 1
DEFAULT_ZONE_TYPE = "motion"
DATA_SATEL = "satel_integra"

CONF_DEVICE_CODE = "code"
CONF_DEVICE_PARTITIONS = "partitions"
CONF_ARM_HOME_MODE = "arm_home_mode"
CONF_ZONE_NAME = "name"
CONF_ZONE_TYPE = "type"
CONF_ZONES = "zones"
CONF_OUTPUTS = "outputs"
CONF_TEMP_SENSORS = "temperature_sensors"
CONF_SWITCHABLE_OUTPUTS = "switchable_outputs"
CONF_INTEGRATION_KEY = "integration_key"
CONF_TEMP_SENSOR_NAME = "name"
ZONES = "zones"
SIGNAL_PANEL_MESSAGE = "satel_integra.panel_message"
SIGNAL_PANEL_ARM_AWAY = "satel_integra.panel_arm_away"
SIGNAL_PANEL_ARM_HOME = "satel_integra.panel_arm_home"
SIGNAL_PANEL_DISARM = "satel_integra.panel_disarm"
SIGNAL_ZONES_UPDATED = "satel_integra.zones_updated"
SIGNAL_OUTPUTS_UPDATED = "satel_integra.outputs_updated"
