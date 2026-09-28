# Illuminance Sensor

Creates a `sensor` entity that estimates outdoor illuminance based on either sun elevation or time of day.
In either case, the value can be further adjusted based on current weather conditions or cloud coverage obtained from another, existing entity.


## Modes of operation
Three modes are available: normal, irradiance & simple.

### Normal/Irradiance modes - Sun elevation
These modes use an algorithm from the US Naval Observatory[^1] for estimating sun illuminance or irradiance based on the sun's elevation (aka altitude.) The maximum illuminance value is about 150,000 lx, and the maximum irradiance value is about 1,250 Watts/M².
Below is an example of what the illuminance might look like over a three day period.

<p align="center">
  <img src=images/normal.png>
</p>

[^1]: Janiczek, P. M., and DeYoung, J. A. _Computer Programs for Sun and Moon Illuminance With Contingent Tables and Diagrams_. Circular No. 171. Washington, D. C.: United States Naval Observatory, 1987 [Google Scholar](https://scholar.google.com/scholar_lookup?title=Computer%20programs%20for%20sun%20and%20moon%20illuminance%20with%20contingent%20tables%20and%20diagrams&author=P.%20M.%20Janiczek&author=J.%20A.%20Deyoung&publication_year=1987&book=Computer%20programs%20for%20sun%20and%20moon%20illuminance%20with%20contingent%20tables%20and%20diagrams)

### Simple mode - Time of day
At night the value is 10 lx. From a little before sunrise to a little after the value is ramped up to whatever the current conditions indicate. The same happens around sunset, except the value is ramped down. For historical reasons, the maximum value is 10,000 lx. Below is an example of what that might look like over a three day period.

<p align="center">
  <img src=images/simple.png>
</p>

## Supported weather sources
Any weather entity that uses the [standard list of conditions](https://www.home-assistant.io/integrations/weather/#condition-mapping), or that provides a cloud coverage percentage, should work with this integration.
The following sources of weather data are known to be supported:

Integration | Notes
-|-
[AccuWeather](https://www.home-assistant.io/integrations/accuweather/) | `weather`
[Buienradar](https://www.home-assistant.io/integrations/buienradar/) | `weather`
[ecobee](https://www.home-assistant.io/integrations/ecobee/) |
[Meteorologisk institutt (Met.no)](https://www.home-assistant.io/integrations/met/) | `weather`
[OpenWeatherMap](https://www.home-assistant.io/integrations/openweathermap/) | `weather`; cloud_coverage & condition `sensor`

## Installation

The integration software must first be installed as a custom component.
You can use HACS to manage the installation and provide update notifications.
Or you can manually install the software.

<details>
<summary>With HACS</summary>

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://hacs.xyz/)

1. Add this repo as a [custom repository](https://hacs.xyz/docs/faq/custom_repositories/):
   It should then appear as a new integration. Click on it. If necessary, search for "illuminance" or "ha_illuminance".
   ```text
   https://github.com/4lexjm/ha-illuminance
   ```
   Or use this button:
  
   [![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=4lexjm&repository=ha-illuminance&category=integration)

1. Download the integration using the appropriate button.

</details>

<details>
<summary>Manual Installation</summary>

Place a copy of the files from [`custom_components/ha_illuminance`](custom_components/ha_illuminance)
in `<config>/custom_components/ha_illuminance`,
where `<config>` is your Home Assistant configuration directory.

>__NOTE__: When downloading, make sure to use the `Raw` button from each file's page.

</details>

### Post Installation

After it has been downloaded you will need to restart Home Assistant.

### Versions

This custom integration supports HomeAssistant versions 2024.8.3 or newer.

---

## Migration from the old integration

> ⚠️ **Important**: Starting with version 6.0.0, this integration uses the `ha_illuminance` domain instead of `illuminance` to resolve the conflict with Home Assistant Core (*"Custom integration that replaces a Core component"*).
> If you had the old integration installed (domain `illuminance`), follow the steps below to migrate.

### Step 1 — Note your current configuration

Before making any changes, note down the following information:

- The **names**, **weather data entities**, and **modes** (`normal`, `simple`, `irradiance`) of your existing illuminance sensors.
- If you use YAML, locate your `illuminance:` block in `configuration.yaml`.
- The **services** called in your automations (e.g. `illuminance.reload`).

### Step 2 — Update YAML configuration (if applicable)

If you configured your sensors in `configuration.yaml`, update the root key from `illuminance:` to `ha_illuminance:`:

```yaml
# Before:
# illuminance:
#   - unique_id: outdoor_light
#     entity_id: weather.home

# After:
ha_illuminance:
  - unique_id: outdoor_light
    name: Outdoor Illuminance
    entity_id: weather.home
    mode: normal
    scan_interval: 5
```

### Step 3 — Remove the old HACS repository (if installed via HACS)

1. In Home Assistant, go to **HACS → Integrations**.
2. Find **Illuminance** (the old version from `pnbruckner/ha-illuminance`).
3. Click the three dots `⋮` → **Remove** (or **Uninstall**).
4. Do **not** restart Home Assistant yet.

*(If you installed manually, delete the folder `<config>/custom_components/illuminance` from your configuration directory.)*

### Step 4 — Add this repository in HACS

If not already done:

1. In **HACS**, click the three dots `⋮` in the top right corner.
2. Select **Custom repositories**.
3. In the **Repository** field, enter: `https://github.com/4lexjm/ha-illuminance`
4. In the **Category** field, select: `Integration`.
5. Click **Add**.

### Step 5 — Install the new integration

1. In **HACS → Integrations**, search for **Illuminance** (or `ha-illuminance`).
2. Click **Download** (version 6.0.0 or later).
3. **Restart Home Assistant**.

### Step 6 — Verify configuration & Automatic migration

- **Automatic migration**: On startup, the integration will automatically detect and migrate any existing UI config entries from the old `illuminance` domain to `ha_illuminance`, preserving your sensor configurations and unique IDs.
- **UI Configuration (manual fallback)**: If you prefer to re-create them manually or if you are setting up new sensors, go to **Settings → Devices & Services → Add Integration**, search for **Illuminance**, and enter your options.
- Verify that your sensor entities are active in **Settings → Devices & Services → Entities**.

### Step 7 — Update your automations and dashboards

Entity IDs should be preserved (e.g. `sensor.illuminance` or `sensor.outdoor_illuminance`). Check and update:

- **Entities** in your Lovelace dashboards if any entity ID changed.
- **Services** in your automations and scripts:

  | Old service | New service |
  |---|---|
  | `illuminance.reload` | `ha_illuminance.reload` |

---

## Services

### `ha_illuminance.reload`

Reloads Illuminance from the YAML-configuration. Also adds `HA_ILLUMINANCE` to the Developers Tools -> YAML page.

## Configuration variables

A list of configuration options for one or more sensors. Each sensor can be configured in the UI (**Settings -> Devices & Services -> Add Integration -> Illuminance**) or via YAML in `configuration.yaml`.

### YAML Configuration Example

```yaml
ha_illuminance:
  - unique_id: outdoor_illuminance
    name: Outdoor Illuminance
    entity_id: weather.home
    mode: normal
    scan_interval: 5
```

### Options

Key | Optional | Description
-|-|-
`unique_id` | no | Unique identifier for sensor. This allows any of the remaining options to be changed without looking like a new sensor. (Only required for YAML-based configuration.)
`entity_id` | yes | Entity ID of another entity that indicates current weather conditions or cloud coverage percentage
`fallback` | yes | Illuminance divisor to use when weather data is not available. Must be in the range of 1 (clear) through 10 (dark.) Default is 10 if `entity_id` is used, or 1 if not.
`mode` | yes | Mode of operation. Choices are `normal` (default) which uses sun elevation, `simple` which uses time of day and `irradiance` which is the same as `normal`, except the value is expressed as irradiance in Watts/M².
`name` | yes | Name of the sensor. Default is `Illuminance`.
`scan_interval` | yes | Update interval. Minimum is 30 seconds. Default is 5 minutes.

## Releases Before 2.1.0
See https://github.com/pnbruckner/homeassistant-config/blob/master/docs/illuminance.md.
