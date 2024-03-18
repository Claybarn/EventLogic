# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 20:23:21 2022

@author: Clayton
"""

from eventlogic import Event,Events
import numpy as np

""" 
9 possibilities of event interactions:
    
Case:   Event:    On Off Times:
        
                              
1        a:            |------|
         b: |------|   
         
         
2        a:            |------|
         b:     |------|
        
        
3        a:            |------|
         b:       |------|
         
         
4        a:             |------|
         b:             |------|
         
         
5        a:            |------|
         b:                 |------|
         
         
6        a:            |------|
         b:                   |------|
          
         
7        a:            |------|
         b:                      |------|  
        
        
8        a:            |------|
         b:             |---|  

9        a:            |------|
         b:          |----------|  
            
"""




""" 
case 1:
                             a:            |------|
                             b: |------|   
"""

a = Event(3,4)
b = Event(1,2)
assert a.exists() == True
assert (a < b) == False
assert (a <= b) == False
assert (a > b) == True
assert (a >= b) == True
assert (a==b) == False
assert (a!=b) == True
assert a.not_intersect(b) == True
assert a.intersect(b) == False
assert (a & b).exists() == False
assert len(a | b) == 2
assert (a | b)[0] == a
assert (a | b)[1] == b
assert len(a ^ b) == 2
assert (a ^ b)[0] == a
assert (a ^ b)[1] == b
assert (a in b) == False
assert len(~a) == 2
assert (~a)[0] == Event(np.NINF,a.on)
assert (~a)[1] == Event(a.off,np.inf)

"""
case 2
                             a:            |------|
                             b:     |------|
"""

a = Event(3,4)
b = Event(1,3)
assert (a < b) == False
assert (a <= b) == False
assert (a > b) == False
assert (a >= b) == True
assert (a==b) == False
assert (a!=b) == True
assert a.not_intersect(b) == False
assert a.intersect(b) == True
assert (a & b).exists() == True
assert len(a | b) == 1
assert (a | b)[0] == Event(b.on,a.off)
assert len(a ^ b) == 2
assert (a in b) == False
assert (a ^ b)[0] == b
assert (a ^ b)[1] == a

"""
case 3
                             a:            |------|
                             b:       |------|
"""

a = Event(3,4)
b = Event(1,3.5)
assert (a < b) == False
assert (a <= b) == False
assert (a > b) == False
assert (a >= b) == False
assert (a==b) == False
assert (a!=b) == True
assert a.not_intersect(b) == False
assert a.intersect(b) == True
assert (a & b).exists() == True
assert len(a | b) == 1
assert (a | b)[0] == Event(b.on,a.off)
assert len(a ^ b) == 2
assert (a ^ b)[0] == Event(b.on,a.on)
assert (a ^ b)[1] == Event(b.off,a.off)
assert (a in b) == False

"""
case 4
                             a:             |------|
                             b:             |------|
"""

a = Event(3,4)
b = Event(3,4)
assert (a < b) == False
assert (a <= b) == False
assert (a > b) == False
assert (a >= b) == False
assert (a==b) == True
assert (a!=b) == False
assert a.not_intersect(b) == False
assert a.intersect(b) == True
assert (a & b).exists() == True
assert len(a | b) == 1
assert (a | b)[0] == Event(a.on,a.off)
assert len(a ^ b) == 1
assert (a ^ b)[0].exists() == False 
assert (a in b) == True

"""
case 5
                             a:            |------|
                             b:                 |------|
"""

a = Event(3,4)
b = Event(3.5,5)
assert (a < b) == False
assert (a <= b) == False
assert (a > b) == False
assert (a >= b) == False
assert (a==b) == False
assert (a!=b) == True
assert a.not_intersect(b) == False
assert a.intersect(b) == True
assert (a & b).exists() == True
assert len(a | b) == 1
assert (a | b)[0] == Event(a.on,b.off)
assert len(a ^ b) == 2
assert (a ^ b)[0] == Event(a.on,b.on) 
assert (a ^ b)[1] == Event(a.off,b.off) 
assert (a in b) == False

"""
case 6 
                             a:            |------|
                             b:                   |------|
"""

a = Event(3,4)
b = Event(4,5)
assert (a < b) == False
assert (a <= b) == True
assert (a > b) == False
assert (a >= b) == False
assert (a==b) == False
assert (a!=b) == True
assert a.not_intersect(b) == False
assert a.intersect(b) == True
assert (a & b).exists() == True
assert len(a | b) == 1
assert (a | b)[0] == Event(a.on,b.off)
assert len(a ^ b) == 2
assert (a ^ b)[0] == Event(a.on,b.on) 
assert (a ^ b)[1] == Event(a.off,b.off)
assert (a in b) == False

"""
case 7
                             a:            |------|
                             b:                      |------|  
"""

a = Event(3,4)
b = Event(5,6)
assert (a < b) == True
assert (a <= b) == True
assert (a > b) == False
assert (a >= b) == False
assert (a==b) == False
assert (a!=b) == True
assert a.not_intersect(b) == True
assert a.intersect(b) == False
assert (a & b).exists() == False
assert len(a | b) == 2
assert (a | b)[0] == Event(a.on,a.off)
assert (a | b)[1] == Event(b.on,b.off)
assert len(a ^ b) == 2
assert (a ^ b)[0] == Event(a.on,a.off) 
assert (a ^ b)[1] == Event(b.on,b.off) 
assert (a in b) == False

"""
case 8
                             a:            |------|
                             b:             |---|  
"""

a = Event(3,4)
b = Event(3.25,3.75)
assert (a < b) == False
assert (a <= b) == False
assert (a > b) == False
assert (a >= b) == False
assert (a==b) == False
assert (a!=b) == True
assert a.not_intersect(b) == False
assert a.intersect(b) == True
assert (a & b).exists() == True
assert len(a | b) == 1
assert (a | b)[0] == Event(a.on,a.off)
assert len(a ^ b) == 2
assert (a ^ b)[0] == Event(a.on,b.on) 
assert (a ^ b)[1] == Event(b.off,a.off) 
assert (a in b) == False

""" 
case 9
                             a:            |------|
                             b:          |----------|  
"""

a = Event(3,4)
b = Event(2,5)
assert (a < b) == False
assert (a <= b) == False
assert (a > b) == False
assert (a >= b) == False
assert (a==b) == False
assert (a!=b) == True
assert a.not_intersect(b) == False
assert a.intersect(b) == True
assert (a & b).exists() == True
assert len(a | b) == 1
assert (a | b)[0] == Event(b.on,b.off)
assert len(a ^ b) == 2
assert (a ^ b)[0] == Event(b.on,a.on) 
assert (a ^ b)[1] == Event(a.off,b.off) 
assert (a in b) == True