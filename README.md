
<p align="center">
  <img src="Assets/Aether - banner.png" width="800">
</p>

# Aether

Aether is a real-time gravitational N-body simulation built with Python and Pygame. It simulates orbital motion, collisions, and dynamic celestial systems using Newtonian gravity, with a focus on stability, interactivity, and visual clarity.

The project is designed as an experimental physics sandbox where users can explore how planetary systems evolve over time.


## Physics

Aether computes motion entirely from physics. Every object influences every other object through gravity, meaning orbits, instability, and collisions emerge naturally from the system.

This allows the simulation to behave like a small evolving universe rather than a scripted animation.


## Features

Aether includes a time scaling system that allows the simulation to be sped up or slowed down.

---

This enables:

- Fast-forwarding long orbital cycles  
- Studying slow gravitational interactions  
- Pausing the universe completely  
- Fine-tuning system evolution in real time  

---

## Adding Bodies

Users can dynamically add new objects into the simulation:

---

- Planets (normal mass bodies)  
- Stars (high-mass gravitational anchors)  
- Black holes and white holes (extreme gravity, high attraction radius)  
- Custom objects with adjustable mass and velocity  

---

## Collision System

This is not the most physically perfect system, but it is designed to be stable and fun to experiment with.

When two bodies collide:

---

- They merge into a single object  
- Mass is combined  
- Momentum is conserved (based on velocity vectors)  
- New orbit is recalculated automatically  

---

## Controls

---

- Mouse drag → Move camera  
- Scroll → Zoom in/out  
- Click body → Inspect object  
- Space → Pause simulation / Resume simulation 
- R → Reset system
- D → Add planets/stars....
- Up / Down arrows → Change time speed  
- C → Reset camera position 

---

## Modes

Currently, there are two modes:

### Sandbox Mode

---

A free simulation mode where you can:
- Watch the solar system evolve  
- Add custom bodies  
- Observe energy changes and numerical drift  

---

### Real Orbit Mode
Uses NASA-based orbital data (Horizon system) to approximate real planetary positions.

You can:

---

- View realistic solar system orbits  
- Travel through time using the time machine
- Compare real orbital data with simulated physics  

---

## Note

---

This project is not intended to be a perfect astrophysical simulator.

It is an educational and experimental physics sandbox built for learning, experimentation, and visual exploration of gravity systems.

and it's also just a simple project in python, so have fun !

---
