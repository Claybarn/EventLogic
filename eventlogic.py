# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 13:52:30 2022

@author: Clayton Barnes

EVENT LOGIC

TODO:
add copy method to events

"""

import numpy as np


# Module-level dtype bounds table. Built once at import time rather than once
# per Event/Events instance, which previously dominated construction cost.
_NEG_INF = -np.inf
_POS_INF = np.inf
_TYPE_BOUNDS = {
    # Integer types
    np.dtype('int8'): (np.iinfo(np.int8).min, np.iinfo(np.int8).max),
    np.dtype('int16'): (np.iinfo(np.int16).min, np.iinfo(np.int16).max),
    np.dtype('int32'): (np.iinfo(np.int32).min, np.iinfo(np.int32).max),
    np.dtype('int64'): (np.iinfo(np.int64).min, np.iinfo(np.int64).max),
    np.dtype('uint8'): (np.iinfo(np.uint8).min, np.iinfo(np.uint8).max),
    np.dtype('uint16'): (np.iinfo(np.uint16).min, np.iinfo(np.uint16).max),
    np.dtype('uint32'): (np.iinfo(np.uint32).min, np.iinfo(np.uint32).max),
    np.dtype('uint64'): (np.iinfo(np.uint64).min, np.iinfo(np.uint64).max),

    # Float types
    np.dtype('float32'): (_NEG_INF, _POS_INF),
    np.dtype('float64'): (_NEG_INF, _POS_INF),

    # Datetime64 types - all share same bounds but with different units
    np.dtype('datetime64[Y]'): (np.datetime64('1677', 'Y'), np.datetime64('2262', 'Y')),
    np.dtype('datetime64[M]'): (np.datetime64('1677-09', 'M'), np.datetime64('2262-04', 'M')),
    np.dtype('datetime64[W]'): (np.datetime64('1677-09-21', 'W'), np.datetime64('2262-04-11', 'W')),
    np.dtype('datetime64[D]'): (np.datetime64('1677-09-21', 'D'), np.datetime64('2262-04-11', 'D')),
    np.dtype('datetime64[h]'): (np.datetime64('1677-09-21T00', 'h'), np.datetime64('2262-04-11T23', 'h')),
    np.dtype('datetime64[m]'): (np.datetime64('1677-09-21T00:12', 'm'), np.datetime64('2262-04-11T23:47', 'm')),
    np.dtype('datetime64[s]'): (np.datetime64('1677-09-21T00:12:43', 's'), np.datetime64('2262-04-11T23:47:16', 's')),
    np.dtype('datetime64[ms]'): (np.datetime64('1677-09-21T00:12:43.145', 'ms'), np.datetime64('2262-04-11T23:47:16.854', 'ms')),
    np.dtype('datetime64[us]'): (np.datetime64('1677-09-21T00:12:43.145224', 'us'), np.datetime64('2262-04-11T23:47:16.854775', 'us')),
    np.dtype('datetime64[ns]'): (np.datetime64('1677-09-21T00:12:43.145224192', 'ns'), np.datetime64('2262-04-11T23:47:16.854775807', 'ns')),

    # Timedelta64 types
    np.dtype('timedelta64[ns]'): (np.timedelta64(-2**63 + 1, 'ns'), np.timedelta64(2**63 - 1, 'ns')),
    np.dtype('timedelta64[us]'): (np.timedelta64(-2**63 + 1, 'us'), np.timedelta64(2**63 - 1, 'us')),
    np.dtype('timedelta64[ms]'): (np.timedelta64(-2**63 + 1, 'ms'), np.timedelta64(2**63 - 1, 'ms')),
    np.dtype('timedelta64[s]'): (np.timedelta64(-2**63 + 1, 's'), np.timedelta64(2**63 - 1, 's')),
    np.dtype('timedelta64[m]'): (np.timedelta64(-2**63 + 1, 'm'), np.timedelta64(2**63 - 1, 'm')),
    np.dtype('timedelta64[h]'): (np.timedelta64(-2**63 + 1, 'h'), np.timedelta64(2**63 - 1, 'h')),
    np.dtype('timedelta64[D]'): (np.timedelta64(-2**63 + 1, 'D'), np.timedelta64(2**63 - 1, 'D')),
}


class Event():
    # Class-level alias preserves backward compatibility for any external code
    # that read `event._type_bounds`.
    _type_bounds = _TYPE_BOUNDS

    def __init__(self, on, off):
        self._check_inputs(on, off)
        self.on = on
        self.off = off
    def __repr__(self):
        return 'Event(on='+str(self.on)+', off='+str(self.off)+')'
    #def __str__(self):
    #    return '('+str(self.on)+','+str(self.off)+')'
    def duration(self):
        return self.off-self.on
    @staticmethod
    def _duration_filter(self,lower_bound,upper_bound):
        if self.duration()>lower_bound and self.duration < upper_bound:
            return True
        else:
            return False
    @staticmethod
    def _check_inputs(on,off):
        if (on is None) and (off is None):
            pass
        elif not (np.isscalar(on) and np.isscalar(off)):
            raise ValueError('Inputs must be scalar or datetime64 type.')
        elif on > off:
            raise ValueError('on must be less than or equal to off')
    def exists(self):
        return (self.on is not None) or (self.off is not None)
    def copy(self):
        return Event(self.on,self.off)
    def __lt__(self,other):
        return self.off < other.on
    def __le__(self,other):
        return self.off <= other.on
    def __gt__(self,other):
        return self.on > other.off
    def __ge__(self,other):
        return self.on >= other.off
    def __eq__(self,other):
        return (self.on == other.on) and (self.off == other.off)
    def __ne__(self,other):
        return (self.on != other.on) or (self.off != other.off)
    def not_intersect(self,other):
        return  (self > other) or (self < other)
    def intersect(self,other):
        return not self.not_intersect(other)
    def __and__(self,other):
        new_timestamp = Event(None,None)
        if self.intersect(other):
            new_timestamp.on = max(self.on,other.on)
            new_timestamp.off = min(self.off,other.off)
        return new_timestamp
    def __or__(self,other):
        if self.not_intersect(other):
            return Events([self,other])
        else:
            new_timestamp = Event(None,None)
            new_timestamp.on = min(self.on,other.on)
            new_timestamp.off = max(self.off,other.off)
            return Events([new_timestamp])
    def __xor__(self,other):
        if self.not_intersect(other):
            return (self,other)
        elif self == other:
            return Event(None,None)
        else:
            early_epoch = Event(min(self.on,other.on),max(self.on,other.on))
            late_epoch = Event(min(self.off,other.off),max(self.off,other.off))
            return Events([early_epoch,late_epoch])
    def __contains__(self,other):
        return (other.on >= self.on) & (other.off <= self.off)
    def __invert__(self):
        on,off = (self.on,self.off)
        if on is None or off is None:
            return Events([Event(None, None)])
        dtype = np.array(on).dtype
        # get bounds to handle non float types 
        min_val, max_val = self._type_bounds.get(dtype, (_NEG_INF, _POS_INF))
        # handle circumstances where min and max are extremes
        # allows e==~(~e)
        min_on = True if on == min_val else False
        max_off = True if off == max_val else False
        # handle 4 cases
        if min_on:
            if max_off:
                # min on and max off
                return Events([Event(None,None)])
            else:
                # min on only
                return Events([Event(off,max_val)])
        else:
            if max_off:
                # max off only
                return Events([Event(min_val,on)])
            else:
                # neither
                return Events([Event(min_val,on),Event(off,max_val)])







class Events():
    def __init__(self, events, _presorted=False):
        if isinstance(events, list):
            self.events = events
        else:
            self.events = [events]
        self._check_inputs(self.events, _presorted=_presorted)

    # Class-level alias of the shared dtype bounds table; same object for every
    # instance so construction is O(1).
    _type_bounds = _TYPE_BOUNDS
    def __len__(self):
        return len(self.events)
    def __iter__(self):
        return EventsIterator(self)
    def __getitem__(self, item):
         return self.events[item]
    def __str__(self):
        return_str = ''
        if len(self) <= 6:
            for event in self:
                return_str += event.__str__()
                return_str += ', '
        else:
            for i in range(3):
                return_str += self.events[i].__str__()
                return_str += ', '
            return_str += ' ... , '
            for i in range(-3,0):
                return_str += self.events[i].__str__()
                return_str += ', '
        return return_str[:-2]
    @staticmethod
    def _check_inputs(events, _presorted=False):
        Events._are_events(events)
        if not _presorted:
            Events._ons_are_sorted_same_dtype(events)
    @staticmethod
    def _are_events(events):
        assert isinstance(events, list)
        for e in events:
            assert isinstance(e, Event)
    @staticmethod
    def _ons_are_sorted_same_dtype(events):
        if len(events) == 0:
            return
        ons = np.array([e.on for e in events])
        offs = np.array([e.off for e in events])
        # Mixed-dtype detection: a heterogeneous list yields an object-dtype array.
        if ons.dtype == object or offs.dtype == object or ons.dtype != offs.dtype:
            dtype = type(events[0].on)
            for e in events:
                if type(e.on) is not dtype or type(e.off) is not dtype:
                    raise TypeError(
                        f"All events must be of the same data type. "
                        f"Observed types: {dtype}, {type(e.on)}, {type(e.off)}"
                    )
        if len(ons) > 1 and not np.all(ons[:-1] <= ons[1:]):
            raise TypeError("All events must be sorted")
    @staticmethod
    def _check_vectors(ons, offs):
        assert hasattr(ons, '__iter__')
        assert hasattr(offs, '__iter__')
        assert len(ons) == len(offs)

    # ------------------------------------------------------------------
    # Vectorized comparison operators.
    # Output is intrinsically an (n x m) bool matrix so we cannot beat
    # n*m memory, but we can improve over naive implementations with numpy
    # broadcasting which is dramatically faster.
    # ------------------------------------------------------------------
    def _on_off_arrays(self):
        return self._unravel_events()

    def __lt__(self, other):
        _, self_offs = self._on_off_arrays()
        other_ons, _ = other._on_off_arrays()
        if self_offs is None or other_ons is None:
            return np.zeros((len(self), len(other)), dtype=bool)
        return self_offs[:, None] < other_ons[None, :]
    def __le__(self, other):
        _, self_offs = self._on_off_arrays()
        other_ons, _ = other._on_off_arrays()
        if self_offs is None or other_ons is None:
            return np.zeros((len(self), len(other)), dtype=bool)
        return self_offs[:, None] <= other_ons[None, :]
    def __gt__(self, other):
        self_ons, _ = self._on_off_arrays()
        _, other_offs = other._on_off_arrays()
        if self_ons is None or other_offs is None:
            return np.zeros((len(self), len(other)), dtype=bool)
        return self_ons[:, None] > other_offs[None, :]
    def __ge__(self, other):
        self_ons, _ = self._on_off_arrays()
        _, other_offs = other._on_off_arrays()
        if self_ons is None or other_offs is None:
            return np.zeros((len(self), len(other)), dtype=bool)
        return self_ons[:, None] >= other_offs[None, :]
    def __eq__(self, other):
        self_ons, self_offs = self._on_off_arrays()
        other_ons, other_offs = other._on_off_arrays()
        if self_ons is None or other_ons is None:
            return np.zeros((len(self), len(other)), dtype=bool)
        return ((self_ons[:, None] == other_ons[None, :]) &
                (self_offs[:, None] == other_offs[None, :]))
    def __ne__(self, other):
        return ~self.__eq__(other)

    # ------------------------------------------------------------------
    # Sorted-aware sweeps.
    # All inputs are sorted by `on`, so per-element scans collapse from
    # O(n*m) to O(n+m).
    # ------------------------------------------------------------------
    def intersect(self, other):
        """Boolean vector: does each self[i] intersect any event in other? O(n+m)."""
        n, m = len(self), len(other)
        result = np.zeros(n, dtype=bool)
        if n == 0 or m == 0:
            return result
        self_ons, self_offs = self._unravel_events()
        other_ons, other_offs = other._unravel_events()
        j = 0
        for i in range(n):
            # Skip over events in `other` that end strictly before self[i] starts;
            # they cannot intersect self[i] or any later self event (sorted by on).
            while j < m and other_offs[j] < self_ons[i]:
                j += 1
            if j < m and other_ons[j] <= self_offs[i]:
                result[i] = True
        return result
    def not_intersect(self, other):
        """Boolean vector: ~intersect (semantic clarification of original)."""
        return ~self.intersect(other)
    def __and__(self, other):
        """Pairwise intersection of two sorted Events. O(n+m+k)."""
        n, m = len(self), len(other)
        if n == 0 or m == 0:
            return Events([])
        new_events = []
        i = j = 0
        a = self.events[i]
        b = other.events[j]
        while True:
            on_max = a.on if a.on > b.on else b.on
            off_min = a.off if a.off < b.off else b.off
            if on_max <= off_min:
                new_events.append(Event(on_max, off_min))
            # Advance the interval that ends first; if tied, advance both safely.
            if a.off < b.off:
                i += 1
                if i >= n:
                    break
                a = self.events[i]
            else:
                j += 1
                if j >= m:
                    break
                b = other.events[j]
        return Events(new_events, _presorted=True)
    def self_or(self):
        """Merge all overlapping events within self. O(n) on sorted input."""
        if len(self) <= 1:
            return Events(list(self.events), _presorted=True)
        new_events = []
        cur_on = self.events[0].on
        cur_off = self.events[0].off
        for k in range(1, len(self)):
            e = self.events[k]
            if e.on <= cur_off:
                if e.off > cur_off:
                    cur_off = e.off
            else:
                new_events.append(Event(cur_on, cur_off))
                cur_on, cur_off = e.on, e.off
        new_events.append(Event(cur_on, cur_off))
        return Events(new_events, _presorted=True)
    def __or__(self, other):
        """Union of two sorted Events with overlap merging. O(n+m)."""
        if len(self) == 0:
            return Events(list(other.events), _presorted=True)
        if len(other) == 0:
            return Events(list(self.events), _presorted=True)

        # Merge two on-sorted lists in linear time.
        n, m = len(self), len(other)
        merged = [None] * (n + m)
        i = j = k = 0
        while i < n and j < m:
            if self.events[i].on <= other.events[j].on:
                merged[k] = self.events[i]; i += 1
            else:
                merged[k] = other.events[j]; j += 1
            k += 1
        while i < n:
            merged[k] = self.events[i]; i += 1; k += 1
        while j < m:
            merged[k] = other.events[j]; j += 1; k += 1

        # Single sweep to coalesce overlaps.
        new_events = []
        cur_on = merged[0].on
        cur_off = merged[0].off
        for idx in range(1, len(merged)):
            e = merged[idx]
            if e.on <= cur_off:
                if e.off > cur_off:
                    cur_off = e.off
            else:
                new_events.append(Event(cur_on, cur_off))
                cur_on, cur_off = e.on, e.off
        new_events.append(Event(cur_on, cur_off))
        return Events(new_events, _presorted=True)
    def __xor__(self,other):
        """ or operator. This one is a bit tricky, we can have chained overlapers that all need to be merged together
         nlog(n^2) or n^3 or ? """
        new_events = Events([])
        last_index = 0
        for curr_self in self:
                curr_events = Events([])
                # record if we did not get an intersection
                no_intersection = True
                # keep memory if we saw an intersection, will prevent us from searching too far
                toggle = False
                for it,curr_other in enumerate(other[last_index:]):
                    if curr_self.intersect(curr_other):
                        toggle = True
                        # perform "xor" on pair of "Event"'s 
                        curr_new_events = curr_self ^ curr_other
                        # check if curr_new_events overlaps with any existing events
                        curr_events.extend(curr_new_events)
                    elif toggle:
                        break
                # record where we last left off to not repeat search
                last_index+=it
                if no_intersection:
                    new_events.extend(curr_self)
                else:
                    # perform "xor" recursively until no more merges are necessary
                    curr_events = curr_events ^ curr_events
                    new_events.extend(curr_events)
                    # merge overlapping events
        return new_events
    def __contains__(self, other):
        # For single Event objects, check if it's contained in any event in self
        if isinstance(other, Event):
            for self_event in self:
                if other in self_event:
                    return True
            return False
        else:
            raise TypeError("Use contains_events() for checking multiple events")
    def contains_events(self, other):
        """Boolean array of which events in `other` are contained in some event of self.

        O(n+m) sweep. An event b is contained in some a iff there is an a with
        a.on <= b.on and a.off >= b.off. Because self is sorted by `on`, we can
        scan self forward as `b.on` increases (other is also sorted) and track
        the maximum `off` among self events whose `on` <= current b.on. If that
        max is >= b.off, b is contained.
        """
        if not isinstance(other, Events):
            raise TypeError("contains_events() expects an Events object")
        n, m = len(self), len(other)
        results = np.zeros(m, dtype=bool)
        if n == 0 or m == 0:
            return results
        j = 0
        max_off = None
        for i in range(m):
            ob = other.events[i]
            while j < n and self.events[j].on <= ob.on:
                off = self.events[j].off
                if max_off is None or off > max_off:
                    max_off = off
                j += 1
            if max_off is not None and max_off >= ob.off:
                results[i] = True
        return results
    def __invert__(self):
        ons,offs = self._unravel_events()
        if ons is None or offs is None:
            return Events([Event(None, None)])
        dtype = np.array(ons[0]).dtype
        # get bounds to handle non float types 
        min_val, max_val = self._type_bounds.get(dtype, (_NEG_INF, _POS_INF))
        # handle circumstances where min and max are extremes
        # allows e==~(~e)
        min_on = True if ons[0] == min_val else False
        max_off = True if offs[-1] == max_val else False
        # handle 4 cases
        if min_on:
            if max_off:
                # min on and max off
                new_ons = offs[:-1]
                new_offs = ons[1:]
            else:
                # min on only
                new_ons = offs
                new_offs = np.append(ons[1:],max_val)
        else:
            if max_off:
                # max off only
                new_ons = np.insert(offs[:-1],0,min_val)
                new_offs = ons
            else:
                # neither
                new_ons = np.insert(offs,0,min_val)
                new_offs = np.append(ons,max_val)
        return Events.from_arrays(new_ons,new_offs)
    def extend(self,other):
        if isinstance(other,Events):
            self.events.extend(other.events)
        elif isinstance(other,Event):
            self.events.append(other)
        else:
            raise ValueError(f"other must be of type Events or Event, but got type {type(other)}")
    def _unravel_events(self):
        if not self.events:
            return None, None
        # np.array infers correct dtype (preserves datetime64 unit, int width, etc.)
        # in a single pass, replacing the per-element Python loop.
        ons = np.array([e.on for e in self.events])
        offs = np.array([e.off for e in self.events])
        return ons, offs
    @classmethod
    def from_arrays(cls, ons, offs):
        Events._check_vectors(ons, offs)
        ons = np.asarray(ons)
        offs = np.asarray(offs)
        # Vectorized validation: avoids the O(n) Python loop in
        # _ons_are_sorted_same_dtype that re-builds numpy arrays.
        if len(ons) > 1 and not np.all(ons[:-1] <= ons[1:]):
            raise TypeError("All events must be sorted")
        if len(ons) > 0 and np.any(ons > offs):
            raise ValueError("on must be less than or equal to off")
        events = [Event.__new__(Event) for _ in range(len(ons))]
        for k in range(len(ons)):
            e = events[k]
            e.on = ons[k]
            e.off = offs[k]
        return cls(events, _presorted=True)
    def merge(self, threshold):
        ons, offs = self._unravel_events()
        if ons is None or len(ons) == 0:
            return Events([], _presorted=True)
        if len(ons) == 1:
            return Events.from_arrays(ons.copy(), offs.copy())
        merge_mask = (ons[1:] - offs[:-1]) < threshold
        new_len = len(merge_mask) - int(np.sum(merge_mask)) + 1
        # Preserve input dtype rather than defaulting to float64.
        new_ons = np.empty(new_len, dtype=ons.dtype)
        new_offs = np.empty(new_len, dtype=offs.dtype)
        new_ons[0] = ons[0]
        it = 0
        current_off = offs[0]
        for i in range(len(merge_mask)):
            if merge_mask[i]:
                if offs[i + 1] > current_off:
                    current_off = offs[i + 1]
            else:
                new_offs[it] = current_off
                it += 1
                new_ons[it] = ons[i + 1]
                current_off = offs[i + 1]
        new_offs[it] = current_off
        return Events.from_arrays(new_ons, new_offs)
    def duration_filter(self,lower_bound=0,upper_bound=np.inf):
        return filter(Event._duration_filter(lower_bound,upper_bound),self.events)



class EventsIterator():
    def __init__(self,events):
        self.events=events
        self._index = 0
    def __next__(self):
        if self._index < len(self.events):
            result = self.events.events[self._index]
            self._index += 1
            return result
        else:
            raise StopIteration
