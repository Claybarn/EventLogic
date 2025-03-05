import numpy as np
import pytest
from eventlogic import Event, Events

"""
unit testing goal:
all data types (floats, ints, datetimes)
same class and interclass comparisons (Event vs Events)
Single events, multi events
"""
def test_events_initialization():
    # Test single event initialization
    single_event = Event(1, 2)
    events = Events(single_event)
    assert len(events) == 1
    assert events[0] == single_event

    # Test list initialization
    event_list = [Event(1, 2), Event(3, 4), Event(5, 6)]
    events = Events(event_list)
    assert len(events) == 3
    assert events[0] == event_list[0]

def test_events_iteration():
    event_list = [Event(1, 2), Event(3, 4), Event(5, 6)]
    events = Events(event_list)
    for i, event in enumerate(events):
        assert event == event_list[i]

def test_events_str_representation():
    # Test short list
    events_short = Events([Event(1, 2), Event(3, 4)])
    assert str(events_short).count(',') == 3  # Three commas for two events

    # Test long list
    events_long = Events([Event(i, i+1) for i in range(10)])
    assert '...' in str(events_long)

def test_events_comparison_operators():
    events1 = Events([Event(1, 2), Event(3, 4)])
    events2 = Events([Event(5, 6), Event(7, 8)])

    # Test less than
    comparison_matrix = events1 < events2
    assert isinstance(comparison_matrix, np.ndarray)
    assert comparison_matrix.dtype == bool

def test_events_logical_operations():
    events1 = Events([Event(1.0, 2.5),Event(2.9,3.0), Event(5.0, 7.0)]); 
    events2 = Events([Event(2.0, 4.0), Event(6.0, 8.0)])


    # Test intersection
    intersection = events1 & events2
    assert isinstance(intersection, Events)
    assert len(intersection) == 3
    assert all(isinstance(e, Event) for e in intersection)

    # Test union
    union = events1 | events2
    assert isinstance(union, Events)
    assert len(union) == 2
    assert all(isinstance(e, Event) for e in union)

def test_events_contains():
    container = Events([Event(1, 5), Event(7, 10)])
    
    # Test single event containment
    contained_event = Event(2, 4)
    assert contained_event in container
    
    # Test non-contained event
    non_contained = Event(5.5, 6.5)
    assert non_contained not in container

def test_events_merge():
    events = Events([Event(1.0, 2.0),Event(2.5, 3.5),Event(3.7, 4.7),Event(7.0, 8.0)])

    # Test merge with small threshold
    merged_small = events.merge(0.1)
    assert len(merged_small) == 4  # Should not merge any events

    # Test merge with large threshold
    merged_large = events.merge(1.0)
    assert len(merged_large) == 2  # Should merge some events

def test_events_from_arrays():
    ons = np.array([1, 3, 5])
    offs = np.array([2, 4, 6])
    
    events = Events.from_arrays(ons, offs)
    assert len(events) == 3
    assert events[0].on == 1
    assert events[0].off == 2

def test_events_datetime():
    # Test with datetime64 arrays
    dates_on = np.array(['2023-01-01', '2023-01-02'], dtype='datetime64[D]')
    dates_off = np.array(['2023-01-02', '2023-01-03'], dtype='datetime64[D]')

    events = Events.from_arrays(dates_on, dates_off)
    assert len(events) == 2
    assert isinstance(events[0].on, np.datetime64)

def test_invalid_inputs():
    # Test invalid array inputs
    with pytest.raises(AssertionError):
        Events.from_arrays([1, 2], [1])  # Mismatched lengths 