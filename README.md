# Legolas

For the STARS project, we need a small walking, rolling robot.  Based on Scorpio,
we know the general type of motion we want.  However, we need to make the robot
small and efficient.  To do that, we'll want to reduce the number of actuators.

Jansen walkers are already a good form of walking linkage.  The provide an
extremely long, flat ground profile.  To achieve Scorpio-like motion, we need to
transition from the normal Jansen motion to a kicking motion, somewhere on the
body.

## Code

The code is structured, roughly, as follows:
```
solver.py:
  code to solve a given linkage, for a particular pose
generator.py
  code to generate a linkage, and solve the entire path
```
