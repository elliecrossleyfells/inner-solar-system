2D Inner solar system simulation using pygame library 

Download the planet_img.png files in the same location as your code 

<b><u>This sim does:</b></u>
 - Uses mass, acceleration and forces and mathematical constants for the Astronomical Unit (AU), the gravitational constant ect.
 - Size of planets and orbital distances have been accurately scaled
 - Accounts for the force of attraction between each body not just the sun
 - All images of sun/planets are real images from NASA 

<b><u>Flaws & inaccuracies:</b></u>
- Comets: The mass and speeds of Halley and Hale-Bopp are correct however their initial (x,y) are much closer in to the sun than is realistic. In reality their orbits would be more eliptical and much much longer (they would orbit off-screen for the most part.) I have put them in for aesthetic purposes only however they do follow a retrograde orbit relative to the rest of solar system as is seen in reality.
- Nothing happens when a comet and planet collide though it's quite fun to wait and see if they do collide (if your definition of fun is the same as mine)
- I am pretty sure the gravitational pull the sun is feeling from the planets is over-exaggerated however I have left it in as it's a good visual of how the force of attraction acts on both bodies and the sun is not a fixed body in the system. The Sun's motion around the barycenter is generally within 1–2 solar radii (~700,000–1,400,000 km) from its center. My sun doesn't seem to move around a barycenter but instead oscillates between two points on a straight line
- Planet spin is NOT accurate. Venus has retrograde spin in reality and I have not coded this in

I had a lot of fun making this!
