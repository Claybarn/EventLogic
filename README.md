# Description
 EventLogic is a lightweight library for performing logical operations on event-style or timestamp data. Logical operations on event-style data are commonplace in many fields. This library seeks to provide a generalized framework and methods for dealing with this data.

# Installation
EventLogic can be installed with `pip`.

```bash
pip install --upgrade pip
pip install eventlogic
```

# Common Usage
The most common way to use EventLogic is through the `Events` class, which handles multiple events simultaneously.

## Creating Events
```python
from eventlogic import Event, Events

#Create from list of events
events1 = Events([Event(1.0, 2.5), Event(2.9, 3.0), Event(5.0, 7.0)])

# Create directly from numpy arrays (recommended)
import numpy as np
ons = np.array([1, 3, 5])
offs = np.array([2, 4, 6])
events2 = Events.from_arrays(ons, offs)

# creating from datetime arrays
dates_on = np.array(['2023-01-01', '2023-01-02'], dtype='datetime64[D]')
dates_off = np.array(['2023-01-02', '2023-01-03'], dtype='datetime64[D]')
datetime_events = Events.from_arrays(dates_on, dates_off)
```

## Logical Operations
```python
#Intersection (find overlapping periods)
intersection = events1 & events2
print(intersection) # Shows all overlapping time periods

#Union (combine events, merging overlaps)
union = events1 | events2
print(union) # Shows combined events with overlaps merged

#Check if events are contained within other events
events1 = Events([Event(1, 5), Event(7, 10)])
events2 = Events([Event(2, 4), Event(8, 9)])
contained = events1.contains_events(events2) # Returns boolean array
```

## Merging & Filtering
```python
#Merge events that are close together
merged = events1.merge(threshold=5) # Merges events less than 5 units apart

#Filter events by duration
filtered = events1.duration_filter(lower_bound=0.5, upper_bound=2.0)
```
# Examples

#### There are 9 flavors of event interactions:
| Case | Events |
| ------ | ------ |
| 1 |  ![Case 1 Image](docs/case1.png?raw=true) |
| 2 |  ![Case 2 Image](docs/case2.png?raw=true) |
| 3 |  ![Case 3 Image](docs/case3.png?raw=true) |
| 4 |  ![Case 4 Image](docs/case4.png?raw=true) |
| 5 |  ![Case 5 Image](docs/case5.png?raw=true) |
| 6 |  ![Case 6 Image](docs/case6.png?raw=true) |
| 7 |  ![Case 7 Image](docs/case7.png?raw=true) |
| 8 |  ![Case 8 Image](docs/case8.png?raw=true) |
| 9 |  ![Case 9 Image](docs/case9.png?raw=true) |

# Usage
The Event class represents an event with a start (on) and end (off) time. It supports various logical operations:

| Operation Class | Symbols |
| ------ | ------ |
| Comparison Operators | >, <, >=, <=, ==, != |
|Logical Operators | &, \|, ^  |
| Containment| in, not in |

## Creating an Event
```python
from eventlogic import Event
event = Event(on=1, off=5)
```

## Event Duration
```python
duration = event.duration()  # Returns the duration of the event
```

## Copying an Event
```python
event_copy = event.copy()
```

## Event Existence
```python
exists = event.exists()  # Checks if the event is defined
```

## Comparison Operators
If we look at case 1:
```python
from eventlogic import Event
a = Event(3,4)
b = Event(1,2)
a > b # True
a < b # False
```

## Logical Operations
```python
event1 = Event(on=1, off=5)
event2 = Event(on=4, off=6)
```
### Intersection
```python
intersection = event1 & event2  # Returns (4,5)
```
### Union
```python
union = event1 | event2  # Returns [(1,6)]
```
#### xor
```python
xor = event1 ^ event2  # Returns ((1,4), (5,6))
```
## Containment Operators
If we look at case 9:
```python
from eventlogic import Event
a = Event(3,4)
b = Event(2,5)
a in b # True
a not in b # False
```

# Working with `numpy.datetime64`
```python
import numpy as np
from eventlogic import Event

a = Event(np.datetime64('2023-01-01T12:00'), np.datetime64('2023-01-01T14:00'))
b = Event(np.datetime64('2023-01-01T13:00'), np.datetime64('2023-01-01T15:00'))

print(a & b)  # (2023-01-01T13:00,2023-01-01T14:00)
print(a | b)  # [(2023-01-01T12:00,2023-01-01T15:00)]
print(a > b)  # False
print(a < b)  # False
```
# Event Container
The `Events` class allows for handling multiple events at once.
```python
from eventlogic import Event, Events
events = Events([Event(1, 2), Event(3, 4), Event(5, 6)])
print(len(events))  # 3
print(events)  # [(1,2), (3,4), (5,6)]
```
And importantly, the creation of `Events` from numpy arrays (including datetime!).
```python
import numpy as np
from eventlogic import Events

ons = np.array([1,3,5])
offs = np.array([2,4,6])
events = Events.from_arrays(ons,offs)
print(len(events))  # 3
print(events)  # [(1,2), (3,4), (5,6)]
```

# Merging Events
```python
merged_events = events.merge(threshold=0.5)
print(merged_events)
```

# Filtering Events by Duration
```python
filtered_events = events.duration_filter(lower_bound=0.5, upper_bound=2.0)
print(filtered_events)
```
