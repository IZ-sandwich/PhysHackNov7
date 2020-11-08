# McGill Physics Hackathon (2020) - Mathematical Modeling of Animal Patterns

This is our entry for the McGill Physics Hackathon (2020). We built a numerical model to generate patterns commonly seen on animals, fish and flora. Our approach uses a reaction-diffusion model orininally proposed by Alan Turing [1]. We focued mainly on the Gray-Scott model and produced a bunch of graphics which can be seen in the 'output' folder.

<p align="center">
  <img width="460" src="/output/images/fish.jpg">
</p>

The *reaction-diffusion* model leads to a diverse array of patterns defined by three model parameters: diffusion rate, feed rate, and kill rate. Varying these parameters can lead to a variety of stable and unstable states allowing us to closely model animal coat patterns ranging from stripes to dots. 
	
<p align="center">
	<img width="250" src="/output/images/test9.png"/>
	<img width="250" src="/output/images/test15.png"/>
	<img width="250" src="/output/images/test11.png"/>
</p>

In addition to setting invariant model parameter for each run, we've experimented with spatially varying model parameters resulting in the following patterns.

<p align="center">
	<img width="250" src="/output/images/test16.png"/>
	<img width="250" src="/output/images/test10.png"/>
	<img width="250" src="/output/images/test13.png"/>
</p>



### Graphic User Interface

In order to effectively visualize the evolution of the patterns given different initial conditions and model parameters, we created a GUI using pyQt5 in conjunction with matplotlib. The GUI can be run by executing '''/reaction-diffusion-gui/main.py'''. Note that the dependencies are the following: pyQt5, numpy, scipy, sklearn, and matplotlib.

<p align="center">
  <img width="460" src="/output/images/gui.png">
</p>

	
### 3D Printed Model

<p align="center">
  <img width="460" src="/output/images/3d_print.jpg">
</p>

### References

[1] Turing, A. M. (1990). The chemical basis of morphogenesis. Bulletin of mathematical biology, 52(1-2), 153-197.

