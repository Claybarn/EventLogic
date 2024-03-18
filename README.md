## Description
 EventLogic is a lightweight library for performing logical operations on event-style or timestamp data. Logical operations on event-style data are commonplace in many fields. This library seeks to provide a generalized framework and methods for dealing with this data.

## Installation
EventLogic can be installed with `pip`.

```bash
pip install --upgrade pip
pip install eventlogic
```

## Examples

#There are 9 flavors of event interactions:
    
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


#If we look at case 1: 
```from eventlogic import Event
a = Event(3,4)
b = Event(1,2)
a > b
a < b
a | b
```

#If we look at case 9: 
```from eventlogic import Event
a = Event(3,4)
b = Event(2,5)
a in b
a not in b
c = a & b
```


