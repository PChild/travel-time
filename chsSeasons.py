from schedules import FRCEvent, Schedule
from typing import List

blacksburg = FRCEvent('VABLA', 'Blacksburg High School, Blacksburg, VA', 32)
ashland = FRCEvent('VAASH', 'Patrick Henry High School, Ashland, VA', 36)
portsmouth = FRCEvent('VAPOR', 'Churchland High School, Portsmouth, VA', 36)
glenAllen = FRCEvent('VAGLE', 'Deep Run High School, Glen Allen, VA', 36)
severn = FRCEvent('MDSEV', 'Archbishop Spalding High School, Severn, MD', 36)
fallsChurch = FRCEvent('VAFAL', 'Meridian High School, Falls Church, VA', 36)
owingsMills = FRCEvent('MDOWI', 'McDonogh School, Owings Mills, MD', 32)
edgewater = FRCEvent('MDEDG', 'South River High School, Edgewater, MD', 36)
hayfield = FRCEvent('VAALE', 'Hayfield Secondary School, Alexandria, VA', 36)
bethesda = FRCEvent('MDBET', 'Walt Whitman High School, Bethesda, MD', 36)

real2024 = Schedule(name="real2024",
                    week1=[blacksburg, ashland],
                    week2=[portsmouth],
                    week3=[glenAllen, severn],
                    week4=[fallsChurch, owingsMills])

edge2024 = Schedule(name="edge2024",
                    week1=[blacksburg],
                    week2=[portsmouth, edgewater],
                    week3=[glenAllen, severn],
                    week4=[fallsChurch, owingsMills])

vaale2024 = Schedule(name="vaale2024",
                     week1=[blacksburg],
                     week2=[portsmouth, hayfield],
                     week3=[glenAllen, severn],
                     week4=[fallsChurch, owingsMills])

six2024 = Schedule(name="six2024",
                   week1=[blacksburg],
                   week2=[portsmouth],
                   week3=[glenAllen, severn],
                   week4=[fallsChurch, owingsMills])

mdbet2024 = Schedule(name="mdbet2024",
                     week1=[blacksburg],
                     week2=[portsmouth, bethesda],
                     week3=[glenAllen, severn],
                     week4=[fallsChurch, owingsMills])


shift2024 = Schedule(name="shift2024",
                     week1=[blacksburg, fallsChurch],
                     week2=[portsmouth],
                     week3=[glenAllen, severn],
                     week4=[ashland, owingsMills])


options2024 = [real2024, edge2024, vaale2024, six2024, mdbet2024, shift2024]

all_events: List[FRCEvent] = [blacksburg, ashland, portsmouth, glenAllen,
                              severn, fallsChurch, owingsMills, edgewater, hayfield, bethesda]
