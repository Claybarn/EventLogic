# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 13:52:30 2022

@author: Clayton Barnes

EVENT LOGIC

TODO:
add copy method to events

"""

import numpy as np
import operator




class Event():
    def __init__(self,on,off):
        self._check_inputs(on,off)
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
        min_val, max_val = self._type_bounds.get(dtype, (np.NINF, np.inf))
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
    def __init__(self,events):
        if (type(events) == list):
            self.events = events
        else:
            self.events = [events]
        self._check_inputs(self.events)
        self._type_bounds = {
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
            np.dtype('float32'): (np.NINF, np.inf),
            np.dtype('float64'): (np.NINF, np.inf),
            
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
            np.dtype('timedelta64[ns]'): (np.timedelta64(-2**63+1, 'ns'), np.timedelta64(2**63-1, 'ns')),
            np.dtype('timedelta64[us]'): (np.timedelta64(-2**63+1, 'us'), np.timedelta64(2**63-1, 'us')),
            np.dtype('timedelta64[ms]'): (np.timedelta64(-2**63+1, 'ms'), np.timedelta64(2**63-1, 'ms')),
            np.dtype('timedelta64[s]'): (np.timedelta64(-2**63+1, 's'), np.timedelta64(2**63-1, 's')),
            np.dtype('timedelta64[m]'): (np.timedelta64(-2**63+1, 'm'), np.timedelta64(2**63-1, 'm')),
            np.dtype('timedelta64[h]'): (np.timedelta64(-2**63+1, 'h'), np.timedelta64(2**63-1, 'h')),
            np.dtype('timedelta64[D]'): (np.timedelta64(-2**63+1, 'D'), np.timedelta64(2**63-1, 'D')),
        }
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
    def _check_inputs(events):
        Events._are_events(events);
        Events._ons_are_sorted_same_dtype(events)
    @staticmethod
    def _are_events(events):
        assert isinstance(events,list)
        for it in range(len(events)):
            assert isinstance(events[0],Event)
    @staticmethod
    def _ons_are_sorted_same_dtype(events):
        if len(events)>0:
            ons = np.empty(len(events))
            offs = np.empty(len(events))
            dtype = type(events[0].on)
            # relaxed definition for non overlapping for some applications, but might be better to have different event classes for the different definitions
            #on_off_vector = np.empty(2*len(events))
            for it,e in enumerate(events):
                ons[it] = e.on
                offs[it] = e.off
                if type(e.on) != dtype or type(e.off) != dtype:
                    raise TypeError(f"All events must be of the same data type. Observed types: {dtype}, {type(e.on)}, {type(e.off)}")
            if not np.all(ons[:-1] <= ons[1:]):
                raise TypeError("All events must be sorted")
    @staticmethod
    def _check_vectors(ons,offs):
        assert hasattr(ons,'__iter__')
        assert hasattr(offs,'__iter__')
        assert len(ons) == len(offs)
    def _generic_O_of_N2(self,other,operator_function):
        matrix = np.empty((len(self),len(other)),dtype=bool)
        for it1, curr_self in enumerate(self):
                for it2, curr_other in enumerate(other):
                    matrix[it1,it2] = operator_function(curr_self,curr_other)
        return matrix
    def __lt__(self,other):
        return self._generic_O_of_N2(other,operator.lt)
    def __le__(self,other):
        return self._generic_O_of_N2(other,operator.le)
    def __gt__(self,other):
        return self._generic_O_of_N2(other,operator.gt)
    def __ge__(self,other):
        return self._generic_O_of_N2(other,operator.ge)
    def __eq__(self,other):
        return self._generic_O_of_N2(other,operator.eq)
    def __ne__(self,other):
        return self._generic_O_of_N2(other,operator.ne)
    def not_intersect(self,other):
        # nlog(n)
        not_intersect_vector = np.zeros((len(self),),dtype=bool)
        last_index = 0
        for it, curr_self in enumerate(self):
                for curr_other in other[last_index:]:
                    if curr_self.not_intersect(curr_other):
                        not_intersect_vector[it] = True
                        last_index+=it
                        break
        return not_intersect_vector
    def intersect(self,other):
        # nlog(n)
        intersect_vector = np.zeros((len(self),),dtype=bool)
        last_index = 0
        for it, curr_self in enumerate(self):
                for curr_other in other[last_index:]:
                    if curr_self.intersect(curr_other):
                        intersect_vector[it] = True
                        last_index+=it
                        break
        return intersect_vector
    def __and__(self,other):
        new_events = []
        for curr_self in self:
            for curr_other in other:
                new_timestamp = curr_self & curr_other
                if new_timestamp.exists():
                    new_events.append(new_timestamp)
        return Events(new_events)
    def self_or(self):
        """Merges all overlapping events within this Events object.
        Avoids comparing an event with itself."""
        if len(self) <= 1:
            return Events(self.events.copy())
            
        new_events = []
        i = 0
        while i < len(self):
            curr_event = self.events[i]
            merged = curr_event
            j = i + 1
            
            while j < len(self):
                if merged.intersect(self.events[j]):
                    # Merge the events if they intersect
                    merged = (merged | self.events[j])[0]  # Take first event since or returns Events
                    j += 1
                else:
                    # If no intersection found, we've merged all possible events
                    break
                    
            new_events.append(merged)
            i = j if j > i + 1 else i + 1
            
        return Events(new_events)
    def __or__(self, other):
        """Or operator that merges all overlapping events between two Events objects"""
        if len(self) == 0:
            return Events(other.events.copy())
        if len(other) == 0:
            return Events(self.events.copy())
            
        new_events = Events([])
        i = 0  # Index for self
        j = 0  # Index for other
        
        while i < len(self) or j < len(other):
            if i >= len(self):
                # Add remaining events from other
                new_events.extend(other[j:])
                break
            if j >= len(other):
                # Add remaining events from self
                new_events.extend(self[i:])
                break
                
            # Get current events to compare
            curr_self = self[i]
            curr_other = other[j]
            
            if curr_self.intersect(curr_other):
                # If events intersect, collect all events that overlap with either
                merged = curr_self | curr_other
                merged = merged[0]  # Get the single merged event
                
                # Look ahead in self for more overlapping events
                next_i = i + 1
                while next_i < len(self) and merged.intersect(self[next_i]):
                    merged = (merged | self[next_i])[0]
                    next_i += 1
                    
                # Look ahead in other for more overlapping events
                next_j = j + 1
                while next_j < len(other) and merged.intersect(other[next_j]):
                    merged = (merged | other[next_j])[0]
                    next_j += 1
                    
                new_events.extend(merged)
                i = next_i
                j = next_j
            else:
                # If no intersection, add the earlier event and advance its index
                if curr_self.on < curr_other.on:
                    new_events.extend(curr_self)
                    i += 1
                else:
                    new_events.extend(curr_other)
                    j += 1
                    
        return new_events
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
        """Returns boolean array indicating which events in other are contained in self"""
        if not isinstance(other, Events):
            raise TypeError("contains_events() expects an Events object")
        results = np.zeros(len(other), dtype=bool)
        for i, other_event in enumerate(other):
            for self_event in self:
                if other_event in self_event:
                    results[i] = True
                    break
        return results
    def __invert__(self):
        ons,offs = self._unravel_events()
        if ons is None or offs is None:
            return Events([Event(None, None)])
        dtype = np.array(ons[0]).dtype
        # get bounds to handle non float types 
        min_val, max_val = self._type_bounds.get(dtype, (np.NINF, np.inf))
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
        if self.events:
            ons = np.empty(len(self),dtype=type(self.events[0].on))
            offs = np.empty_like(ons)
            for it,timestamp in enumerate(self):
                ons[it] = timestamp.on
                offs[it] = timestamp.off
            return ons, offs
        else:
            return None,None
    @classmethod
    def from_arrays(cls,ons,offs):
        Events._check_vectors(ons,offs)
        events = []
        for times in zip(ons,offs):
            events.append(Event(times[0],times[1]))
        Events._check_inputs(events)
        return cls(events)
    def merge(self, threshold):
        ons, offs = self._unravel_events()
        merge_mask = (ons[1:] - offs[:-1]) < threshold
        new_len = len(merge_mask) - np.sum(merge_mask) + 1
        new_ons = np.empty(new_len)
        new_offs = np.empty(new_len)
        new_ons[0] = ons[0]
        it = 0
        
        # Keep track of the current merged off time
        current_off = offs[0]
        
        for i in range(len(merge_mask)):
            if merge_mask[i]:
                # Update the current off time to the later of the two
                current_off = offs[i+1]
            else:
                # No merge, save current segment and start new one
                new_offs[it] = current_off
                it += 1
                new_ons[it] = ons[i+1]
                current_off = offs[i+1]
        
        # Save the final off time
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
