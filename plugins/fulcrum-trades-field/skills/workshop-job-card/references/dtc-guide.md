# Explaining diagnostic trouble codes

A diagnostic trouble code (DTC) records a condition a control module detected. It points to a circuit or system, not a failed part. Explain codes to customers in plain language and always pair them with the technician's confirmation step.

## Reading the code

Format: one letter and four characters, for example `P0420`.

| Position | Meaning |
| --- | --- |
| 1st letter | P powertrain (engine, transmission), B body (airbags, seats, lighting), C chassis (ABS, steering, suspension), U network (communication between modules) |
| 2nd character | 0 generic (the same meaning across makes); 1 manufacturer-specific. 2 and 3 vary by system and range, so check the manufacturer's reference |
| 3rd character (P codes) | Subsystem: 1 and 2 fuel and air metering, 3 ignition and misfire, 4 auxiliary emission controls, 5 speed and idle control, 6 computer and output circuits, 7 to 9 transmission, A hybrid |
| Last two | The specific fault |

For manufacturer-specific codes, use the manufacturer's service information. Independent workshops can access it under the motor vehicle service and repair information scheme. Do not guess a manufacturer-specific meaning from a generic list.

## Code status matters

| Status | What it means | How to explain it |
| --- | --- | --- |
| Pending | Seen once; not yet confirmed on a second drive cycle | "The car noticed something once. We'll check whether it comes back." |
| Confirmed or stored | Seen enough times to set the code; the warning light may be on | "The car has confirmed a fault in this system." |
| Permanent | Cannot be cleared with a scan tool; it clears itself once the system passes its own test | "This will clear on its own after the repair once the car re-tests the system on the road." |
| History | Was present and is no longer active | "It happened in the past; we'll check whether it is still relevant." |

Record freeze-frame data (engine temperature, speed, load, fuel trims at the moment the code set). It helps the technician reproduce the fault.

## Explanation pattern

> **{code} ({status}): {standard description}.**
> In plain terms: {one or two sentences about what the system does and what the car noticed}.
> Common causes the technician will check: {two to four causes, cheapest and most likely first}.
> A code tells us what the computer saw, not which part failed. {tech_name} will confirm the cause with testing before we replace anything.

## Common generic codes

Use these as a starting point only. Confirm the description against the scan tool or service information for the vehicle.

| Code | Standard description | Plain language | Common causes to check |
| --- | --- | --- | --- |
| P0300 | Random or multiple cylinder misfire detected | The engine is not firing evenly | Spark plugs, ignition coils, vacuum leak, fuel delivery, low compression. A flashing check-engine light means a severe misfire: advise the customer to stop driving, as it can damage the catalytic converter. |
| P0301–P0308 | Cylinder 1–8 misfire detected | One particular cylinder is misfiring | Plug, coil or injector on that cylinder; compression test if those check out |
| P0171 | System too lean (bank 1) | The engine is getting too much air for the fuel | Vacuum or intake leak, dirty or faulty airflow sensor, low fuel pressure, exhaust leak before the oxygen sensor |
| P0420 | Catalyst system efficiency below threshold (bank 1) | The exhaust catalytic converter is not cleaning the exhaust as well as it should | Exhaust leak, oxygen sensor fault, previous misfires, then the converter itself. Do not replace a converter on this code alone. |
| P0128 | Coolant temperature below thermostat regulating temperature | The engine is taking too long to warm up | Thermostat stuck open, coolant temperature sensor |
| P0442 | Evaporative emission system small leak detected | The system that traps fuel vapour has a small leak | Fuel cap seal, purge or vent valve, cracked hose |
| P0455 | Evaporative emission system large leak detected | The fuel vapour system has a large leak | Fuel cap missing or loose, disconnected hose, faulty valve |
| P0562 | System voltage low | The car's electrical system is running below normal voltage | Battery condition, alternator output, corroded or loose connections |
| P0700 | Transmission control system malfunction | The transmission computer has stored its own fault | Read the transmission module codes; this code alone says little |
| U0100 | Lost communication with engine control module | Two of the car's computers have stopped talking to each other | Wiring and connectors, module power and earth, then the module itself |

## Never

- Recommend or price a part from the code alone.
- Clear codes before recording them and the freeze-frame data.
- Tell the customer a code is "nothing to worry about" unless the technician has said so.
