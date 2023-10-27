[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)

# Satel Integra Extended

The integration is based on build in Home Assistant [Satel Integra integration](https://www.home-assistant.io/integrations/satel_integra/).
It provides the following additional features comparing to the mainstream integration:

The `satel_integra_ext` integration will allow Home Assistant users who own a Satel Integra alarm panel to leverage their alarm system and its sensors to provide Home Assistant with information about their homes. Connectivity between Home Assistant and the alarm is accomplished through a ETHM extension module that must be installed in the alarm. Compatible with ETHM-1 Plus module with firmware version > 2.00 (version 2.04 confirmed).

There is currently support for the following device types within Home Assistant:

- Binary Sensor: Reports on zone or output statuses
- Switch: allows for setting states of selected outputs
- Alarm Control Panel: represents the zones (in Polish: "strefa"). Reports its status, and can be used to arm/disarm the partition

The module communicates via Satel's open TCP protocol published on their website. It subscribes for new events coming from alarm system and reacts to them immediately.

## Setup

Please note that **ETHM-1 module is currently not supported**: it does not provide functionality used by this extension. At the moment only ETHM-1 Plus module is supported. That might change in the future, but no promises are given.

A list of all partition, zone and output IDs can be acquired by running DloadX program and connecting to your alarm.

For the Binary Sensor check the [type/class](https://www.home-assistant.io/integrations/binary_sensor/) list for a possible visualization of your zones. Note: If no zones or outputs are specified, Home Assistant will not load any binary_sensor components.

### Manual installation
 - copy `custom_componetns/satel_integra_ext` to your Home Assistant configuration folder
 - update `configuration.yaml` (see below)
 - restart Home Assistant

### Installation with HACS

 - add the repository `https://github.com/leshqo/satel_integra_ext-ha` to the [HACS custom repositories](https://hacs.xyz/docs/faq/custom_repositories)
 - in HACS look for Satel Integra and install the integration
 - update `configuration.yaml` (see below)
 - restart Home Assistant

### Removal

Uninstall in HACS or manually remove `satel_integra_ext` folder from `custom_components`. After this, restart Home Assistant.

## Configuration

The configuration is compatible with the original [Satel Integra](https://www.home-assistant.io/integrations/satel_integra/). And the only change needed to use this integration is to change  `satel_integra` to `satel_integra_ext`new features.

A `satel_integra_ext` section must be present in the `configuration.yaml` file:

```yaml
# Example configuration.yaml entry
satel_integra_ext:
  host: IP_ADDRESS
```

### Configuration Variables
#### host
The IP address of the Satel Integra ETHM module on your home network, if using socket type.
  - *required*: true
  - *default*: localhost
  - *type*: string

#### port
The port on which the ETHM module listens for clients using integration protocol.
  - *required*: false
  - *default*: 7094
  - *type*: integer

#### code
User password, it's needed for making use of the switchable_outputs. It's recommended not to use admin password.
  - *required*: false
  - *type*: string

#### integration_key
Integration key for encrypted communication. If not specified then communication will not be encrypted.
Set the same value as configured in Satel Integra system (check manual for more information)

  - *required*: false
  - *type*: string


#### partitions
List of the partitions to operate on.
  - *required*: false
  - *type*: [integer, list]


&nbsp;&nbsp;&nbsp;&nbsp;**name**

&nbsp;&nbsp;&nbsp;&nbsp;Name of the partition.

- *required*: true
- *type*: string

&nbsp;&nbsp;&nbsp;&nbsp;**arm_home_mode**

&nbsp;&nbsp;&nbsp;&nbsp;The mode in which the partition is armed when 'arm home' is used. Possible options are `1`,`2` or `3`.

&nbsp;&nbsp;&nbsp;&nbsp;For more information on what the differences are between them, please refer to Satel Integra manual.

  - *required*: false
  - *default*: 1
  - *type*: integer

#### zones
This parameter lists the zones (or inputs) that will be visible by Home Assistant. For each zone, a proper ID must be given as well as its name. The name is arbitrary and does not need to match the one specified in Satel Integra alarm configuration.

  - *required*: false
  - *type*: [integer, list]

&nbsp;&nbsp;&nbsp;&nbsp;**name**

&nbsp;&nbsp;&nbsp;&nbsp;Name of the zone.

  - *required*: true
  - *type*: string

&nbsp;&nbsp;&nbsp;&nbsp;**type**

&nbsp;&nbsp;&nbsp;&nbsp;The zone type.

  - *required*: false
  - *default*: motion
  - *type*: string

#### outputs
Very similar to zones, but with outputs. Satel Integra uses outputs to inform external systems about different events. For example power failure, or that alarm started counting for exit or some other user-defined condition. They may be used for simple alarm-based automation. For more information please refer to Satel homepage and forums.

  - *required*: false
  - *type*: [integer, list]

&nbsp;&nbsp;&nbsp;&nbsp;**name**

&nbsp;&nbsp;&nbsp;&nbsp;Name of the output.

  - *required*: true
  - *type*: string

&nbsp;&nbsp;&nbsp;&nbsp;**type**

&nbsp;&nbsp;&nbsp;&nbsp;The type of the device - just for presentation.

  - *required*: false
  - *default*: motion
  - *type*: string

#### switchable_outputs
Switchable outputs. These will show up as switches within Home Assistant.

  - *required*: false
  - *type*: [integer, list]

&nbsp;&nbsp;&nbsp;&nbsp;**name**

&nbsp;&nbsp;&nbsp;&nbsp;Name of the output.

  - *required*: true
  - *type*: string

## Full examples

```yaml
# Example configuration.yaml entry
satel_integra_ext:
  host: 192.168.1.100
  port: 7094
  partitions:
    01:
      name: "House"
      arm_home_mode: 2
    02:
      name: "Garage"
  zones:
    01:
      name: "Bedroom"
      type: "motion"
    02:
      name: "Hall"
      type: "motion"
    30:
      name: "Kitchen - smoke"
      type: "smoke"
    113:
      name: "Entry door"
      type: "opening"
  outputs:
    05:
      name: "Garden lights trigger"
      type: "light"
    09:
      name: "Gate opening trigger"
      type: "opening"
    30:
      name: "Alarm triggered"
      type: "safety"
    32:
      name: "Alarm power problem"
      type: "safety"
  switchable_outputs:
    05:
      name: "Gate open"
    06:
      name: "Gate close"
    14:
      name: "Garden light"

```

Having configured the zones and the outputs, you can use them for automation, such as to react on the movement in your bedroom.
For example:

```yaml
  alias: "Flick the input switch when movement in bedroom detected"
  trigger:
      platform: state
      entity_id: "binary_sensor.bedroom"
      to: "on"
  action:
      service: input_boolean.turn_on
      target:
        entity_id: input_boolean.movement_detected
```
