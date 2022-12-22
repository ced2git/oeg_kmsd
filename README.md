# oeg_kmsd

### Introduction 

The KMS-D+ is  heating "controller" module that allow you to "upgrade" your old heating systems with a regulation based on 
on external temperatures. 

https://www.oeg.net/fr/r-gulation-de-chauffage-kms-d-212000040

The module do provide a mini USB interface exposing a series of sensors and settings that might be of an interest to collect
into a home automation software. 

Interface

The Miniusb interface on the KMS-D is based on the MODBUS ASCII protocol and emulate a serial interface.

The Serial parameters to iniate a connections are 

Baudrate :  9600
Parity : Even
Bytesize: 1

Protocol : MODBUS ASCII
Register address: 128 (hex 0x80)
Holding Register: Type 3

### Registers

.... Work in progress .....

While the OEG will answer a series of register from 1 to 1000, interesting values are between 1 and 60. I've not figure out all
of the them but here are the most important ones: 

Please refer to the KMS-D manuel (available on their web sites) to understand the various sensor and limits 

Register:Value

* 38:T1 Sensor
* 39:T2 Sensor
* 40:T3 Sensor
* 41: T4 Sensor
* 42: T5 Sensor
* 47: Planning 
* 49: T1 Limit
* 50: T2 limit
* 51: T3 Limit
* 52: T4 Limit
* 53: T5 Limit
* 58: Planning
* 59: TD2

Based on the instruction manual and some screenshot of the software sold by OEG, i understnad that there probably ways to 
progrma the KMS-D or at least to overide the current planning. I haven't yet, how it works. 

Small sample

I've done a small sample to extract the Modbus informations and publish them on a MQTT broker. This is enough for me 
to monitor the KMS-D. 

### KS2W Registers

(Could be valid for models KSW-E*, KSW* too as they share the same documentation)

The following registers have been identified with the KS2W model and might differ from the KMS-D+ registers.
This is the result of querying registers up to 10000 to check which returned values. All registers listed below can be 
read using the `read_register` method with the default `function_code` 3 and are signed. Some are decimal values, in which 
case `decimals` should be set to 1, some others are enumerations, typically described by integer values starting at 0.

| Range | Description |
| --- | --- |
| 0 - 59 | Various information including date, temperatures, circulations |
| 100 - 135 | Unknown |
| 400 - 459 | Unknown |
| 700 - 867 | Could be time programming: 28 blocks of 6 registers for 7 days * 4 programs |
| 400 - 459 | Unknown |
| 1000 - 1199 | Settings current values |
| 1200 - 1399 | Unknown |
| 1400 - 1799 | Settings minimums and maximums |
| 1800 - 2200 | Unknown |

##### Interesting registers for current data
| Register | Description |
| --- | --- |
| 0-5 | Could be time. Register 0 definitely tracks seconds and when it reaches its maximum value, it resets to 0 and value of register 1 is incremented by 1 |
| 6 | Mode: 1=Off; 9=Automatic |
| 13 | Set point temperature - Tank bottom |
| 15 | Set point temperature - Tank top |
| 29 | Language setting (2=French) |
| 31 | Circulator R2 status: 0=OFF; 1=40%; 2=55%; 3=70%, 4=85%, 5=ON. Could possibly depend on how the circulator is controlled (RPM, ON/OFF, PWM), see setting S3.1 |
| 34 | Circulators modes: see table below |
| 35 | Circulators ON/OFF: see table below |
| 38 | T1 |
| 39 | T2 |
| 40 | T3 |
| 41 | T4 |
| 58 | Circulators intensity |

###### Circulators

* Modes Auto/Manual

    | Register 34 | R1 | R2 | R3 |
    | --- | --- |--- | --- |
    | 0 | AUTO | AUTO | AUTO | 
    | 1 | MANUAL | AUTO | AUTO | 
    | 2 | AUTO | MANUAL | AUTO | 
    | 3 | MANUAL | MANUAL | AUTO | 
    | 4 | AUTO | AUTO | MANUAL | 
    | 5 | MANUAL | AUTO | MANUAL | 
    | 6 | AUTO | MANUAL | MANUAL | 
    | 7 | MANUAL | MANUAL | MANUAL | 

* Status On/Off

    | Register 35 | R1 | R2 | R3 |
    | --- | --- |--- | --- |
    | 0 | OFF | OFF | OFF | 
    | 1 | ON | OFF | OFF | 
    | 2 | OFF | ON | OFF | 
    | 3 | ON | ON | OFF | 
    | 4 | OFF | OFF | ON | 
    | 5 | ON | OFF | ON | 
    | 6 | OFF | ON | ON | 
    | 7 | ON | ON | ON | 

* Intensity

  /!\ Presumably depends on the selected hydraulic scheme. The following appears to be true for scheme 236, with the two solar circulator pumps are managed in % of their total intensity.
  
  Intensity of both circulator pumps R2 and R3 can be read at register 58:

    | Intensity R2 | R3 ON | R3 OFF |
    | --- | --- | --- |
    | R2 ON | {register 58} % 256 | {register 58} - 1280 |
    | R2 OFF | 0 | 0 |

    | Intensity R3 | R2 ON | R2 OFF |
    | --- | --- | --- |
    | R3 ON | {register 58} // 256 | {register 58} / 256 |
    | R3 OFF | 0 | 0 |
    
    where // is the floor division and / the division

##### Settings
Minimum and maximum values should probably not be written to.
Available settings depend on the hydraulic schema currently in use.
The whole range might not be in use if there are less than 20 settings in the section.

| Settings | Minimum | Current value | Maximum |
| --- | --- |--- | --- |
| S1 | 1400-1419 | 1000-1019 | 1600-1619 |
| S2 | 1420-1439 | 1020-1039 | 1620-1639 |
| S3 | 1440-1459 | 1040-1049 | 1640-1659 |
| P1 | 1460-1479 | 1060-1079 | 1660-1679 |
| P2 | 1480-1499 | 1080-1099 | 1680-1699 |
| P3 | 1500-1510 | 1100-1110 | 1700-1710 |
| W | 1520-1531 | 1120-1131 | 1720-1731 |
| F1 | 1540-1559 | 1140-1159 | 1740-1759 |
| F2 | 1560-1579 | 1160-1179 | 1760-1779 |
| F3? | 1580-1599 | 1180-1199 | 1780-1799 |

The provided range represents all settings available in a section. 
For example the current value of S1.1 is in 1000, S1.2 is in 1001, etc.

##### Sending commands

It seems possible to change the behavior remotely, by writing values to registers.

With my current settings and hydraulic scheme, I can turn the system on and off by writing registers 6 to 23:

* Turning off:

```text
Function: 16 (0x10) - Write Multiple Registers 
    Starting Address: 6 
    Quantity: 18 
    Byte Count: 36 
    Values: 00 01 00 00 00 00 00 00 00 00 00 78 01 f4 02 bc 01 f4 01 f4 01 f4 01 f4 ff ff ff ff ff ff ff ff ff ff ff ff  
        Register6: 1 
        Register7: 0 
        Register8: 0 
        Register9: 0 
        Register10: 0 
        Register11: 120 
        Register12: 500 
        Register13: 700 
        Register14: 500 
        Register15: 500 
        Register16: 500 
        Register17: 500 
        Register18: 65535 
        Register19: 65535 
        Register20: 65535 
        Register21: 65535 
        Register22: 65535 
        Register23: 65535 
```

* Turning on:

```text
Function: 16 (0x10) - Write Multiple Registers 
    Starting Address: 6 
    Quantity: 18 
    Byte Count: 36 
    Values: 00 09 00 00 00 00 00 00 00 00 00 78 01 f4 02 bc 01 f4 01 f4 01 f4 01 f4 ff ff ff ff ff ff ff ff ff ff ff ff  
        Register6: 9 
        Register7: 0 
        Register8: 0 
        Register9: 0 
        Register10: 0 
        Register11: 120 
        Register12: 500 
        Register13: 700 
        Register14: 500 
        Register15: 500 
        Register16: 500 
        Register17: 500 
        Register18: 65535 
        Register19: 65535 
        Register20: 65535 
        Register21: 65535 
        Register22: 65535 
        Register23: 65535 
```

The only value that is changed is register 6. Seeing as I don't know what the other registers represent, I can't tell if their values would be different on other installations.