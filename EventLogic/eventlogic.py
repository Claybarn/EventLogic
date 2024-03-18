# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 13:52:30 2022

@author: Clayton Barnes

EVENT LOGIC

"""

import numpy as np
import operator

class Event():
    def __init__(self,on,off):
        self._check_inputs(on,off)
        self.on = on
        self.off = off
    def __repr__(self):
        return '('+str(self.on)+','+str(self.off)+')'
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
    def _check_inputs(self,on,off):
        if (on is None) and (off is None):
            pass
        elif not (np.isscalar(on) and np.isscalar(off)):
            raise ValueError('Inputs must be scalar.')
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
        return (new_timestamp)
    def __or__(self,other):
        if self.not_intersect(other):
            return (self,other)
        else:
            new_timestamp = Event(None,None)
            new_timestamp.on = min(self.on,other.on)
            new_timestamp.off = max(self.off,other.off)
            return [new_timestamp]  
    def __xor__(self,other):
        if self.not_intersect(other):
            return (self,other)
        elif self == other:
            return (Event(None,None))
        else:
            early_epoch = Event(min(self.on,other.on),max(self.on,other.on))
            late_epoch = Event(min(self.off,other.off),max(self.off,other.off))
            return (early_epoch,late_epoch)
    def __contains__(self,other):
        return (other.on >= self.on) & (other.off <= self.off)
    def __invert__(self):
        return (Event(np.NINF,self.on),Event(self.off,np.inf))


class Events():
    def __init__(self,events):
        if (type(events) == list):
            self.events = events
        else:
            self.events = [events]
        self._check_inputs(self.events)
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
            for i in range(3):
                return_str += self.events[-i].__str__()     
                return_str += ', '
        return return_str[:-2]
    def _check_inputs(self,events):
        self._are_events(events);
        self._is_sorted_and_non_overlapping(events)
    def _are_events(self,events):
        assert isinstance(events,list)
        for it in range(len(events)):
            assert isinstance(events[0],Event)
    def _is_sorted_and_non_overlapping(self,events):
        on_off_vector = np.empty(2*len(events))
        for it in range(len(events)):
            on_off_vector[it*2] = events[it].on
            on_off_vector[it*2+1] = events[it].off
        assert np.all(on_off_vector[:-1] <= on_off_vector[1:])
    def _check_vectors(self,ons,offs):
        assert hasattr(ons,'__iter__')
        assert hasattr(offs,'__iter__')
        assert len(ons) == len(offs)
    def _generic_O_of_N2(self,other,operator_function):
        matrix = np.empty((len(self),len(other)),dtype=bool)
        for it1, curr_self in enumerate(self):
                for it2, curr_other in enumerate(other):
                    matrix[it1,it2] = operator_function(self,other)
        return matrix
    def __lt__(self,other):
        return self.generic_O_of_N2(other,operator.lt)
    def __le__(self,other):
        return self.generic_O_of_N2(other,operator.le)
    def __gt__(self,other):
        return self.generic_O_of_N2(other,operator.gt)
    def __ge__(self,other):
        return self.generic_O_of_N2(other,operator.ge)
    def __eq__(self,other):
        return self.generic_O_of_N2(other,operator.eq)
    def __ne__(self,other):
        return self.generic_O_of_N2(other,operator.ne)
    def not_intersect(self,other):
        not_intersect_matrix = np.empty((len(self),len(other)),dtype=bool)
        for it1, curr_self in enumerate(self):
                for it2, curr_other in enumerate(other):
                    not_intersect_matrix[it1,it2] = curr_self.not_intersect(other)
        return not_intersect_matrix
    def intersect(self,other):
        intersect_matrix = np.empty((len(self),len(other)),dtype=bool)
        for it1, curr_self in enumerate(self):
                for it2, curr_other in enumerate(other):
                    intersect_matrix[it1,it2] = curr_self.intersect(other)
        return intersect_matrix
    def __and__(self,other): 
        new_events = []
        for curr_self in self:
            for curr_other in other:
                new_timestamp = curr_self & curr_other
                if new_timestamp.exists():
                    new_events.append(new_timestamp)
        return new_events
    def __or__(self,other): 
        new_events = []
        for curr_self in self:
             for curr_other in other:
                 new_timestamp = curr_self | curr_other
                 if new_timestamp.exists():
                     new_events.append(new_timestamp)
        return new_events
    def __xor__(self,other): 
        new_events = []
        for curr_self in self:
             for curr_other in other:
                 new_timestamp_s = curr_self ^ curr_other
                 for new_timestamp in new_timestamp_s:
                     if new_timestamp.exists():
                         new_events.append(new_timestamp)
        return new_events
    def __invert__(self):
        ons,offs = self._unravel_events()
        new_ons = np.insert(offs,0,np.NINF)
        new_offs = np.append(ons,np.inf)
        new_events = Events(Event(None,None))
        new_events.from_vectors(new_ons,new_offs)
        return new_events
    def _unravel_events(self):
        ons = np.empty(len(self))
        offs = np.empty_like(ons)
        for it,timestamp in enumerate(self):
            ons[it] = timestamp.on
            offs[it] = timestamp.off
        return ons, offs
    def from_vectors(self,ons,offs):
        self._check_vectors(ons,offs)
        events = []
        for times in zip(ons,offs):
            events.append(Event(times[0],times[1]))
        self._check_inputs(events)
        self.events = events
    def merge(self,threshold):
        ons, offs = self._unravel_events()
        merge_mask = (ons[1:]-offs[:-1])<threshold
        new_len = len(merge_mask)-np.sum(merge_mask)+1
        new_ons = np.empty(new_len)
        new_offs = np.empty(new_len)
        new_ons[0] = ons[0]
        new_offs[0] = offs[0]
        it = 0
        for i in range(len(merge_mask)):
          if merge_mask[i]:
              new_offs[it] = offs[i]
          else:
              it += 1
              new_ons[it] = ons[i+1]
              new_offs[it] = offs[i+1]
        self.from_vectors(new_ons,new_offs)
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
            

def events_from_vectors(ons,offs):
    events = Events(Event(1,2))
    events.from_vectors(ons,offs)
    return events




