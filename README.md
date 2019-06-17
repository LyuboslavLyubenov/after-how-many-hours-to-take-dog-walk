# after-how-many-hours-to-take-dog-walk
Fuzzy logic for determing my parent's dog walking schedule. It help with deciding when dog should get extra walk.

## Requirements
- python3
- numpy
- skfuzzy

## Usage
```python
hours_passed_after_pee = '' #how much time is passed after last walk (or in this case after last bathroom walk). Measured in hours. Must be positive integer.
crying_intensity = '' #how annoyning his sobbing is. He is sometimes sobbing for attention. Measured in annoying points (from 0 to 10) (its subjective). Must be integer. 
when_should_i_walk_him = approximate_time_remaining_until_walk(hours_passed_after_pee, crying_intensity)

print(when_should_i_walk_him) #'now' if you havent go for a walk this day or integer representing after how many hours you should take him for a walk (example: 0.5 (this means after 30 mins))
```
