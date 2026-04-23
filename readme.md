# Complex function plotter

This script takes a complex function f(z) and plots it using domain coloring and a few visual tricks. The script is written in Python, with the specific intent of using the complex functions of numpy and scipy, and to be used with LaTeX to generate pretty graphs of complex functions for theses, dissertations, papers, and any other technical or academic document that can be written in laTeX.

In very simple terms, the phase of f(z) is plotted as a hue change, while the magnitude is plotted in a brightness change. The hue colors can be settable using Python's colormaps, and then imported into LaTeX using pgfplots. The brightness changes are also adjustable in levels.

The first trick is done by a discontinuous color on the brightness, showing magnitude steps with color brightness. There are functions in the code to generate logarithmic levels of brightness. This is because the (probably) most used functions will more often tend to infinity (see Liouville's Theorem). Meromorhpic functions tend to infinity at poles, and some functions of interest have essential singularities. Therefore it makes sense to plot orders of magnitude. If you want to give a customized array of levels this can also be done. If, however, you want to use specific levels, you can also supply those to the main function. You can have a single level by simply using the levels of minimum and maximum absolute value of the function in the particular region you are considering.

The script will show the plot and save it to an image "complex_data.png". If it already exists the script will overwrite; so if you like the picture you generated be sure to save it before running the script again.

This script was based on the [website by Samuel Li](https://samuelj.li/complex-function-plotter) which source code can be found [here](https://github.com/wgxli/complex-function-plotter). The links were last accessed on april 22, 2026. For an interactive plotter, you are probably better off using the website rather than this script because it will take at least a couple seconds and, given enough points in the mesh, hours (do not ask me how I know). While I did not use any source code from Samuel's tool, it uses the GNUPLv3, so if Python or LaTeX are not your cup of coffee and you just want to look at pretty plots you are again better off using his tool. As beforesaid I wrote this tool for a quite specific application of writing academic papers and theses, to focus on visualization of complex-variable functions. And yes, as you have already probably noticed I have the weirdest procrastinations that include numerical complex analysis and software development.

This script is licensed under the [Creative Commons Attribution 4.0 International  license](https://creativecommons.org/licenses/by/4.0/deed.en), whereby you can use this code even commercially but must credit it.

There are a ton of options the script gives but I do not have time (or inclination) to write documentation, so read the code I guess. Or reach out. The options should be fairly self-explanatory.

The folder 'latex_application' shows a minimal working example of a LaTeX application of the plots generated using pgfplots and TikZ, which are quite powerful, so you can tune it to your liking. The MWE includes a colorbar for the phase hue, and a grid. To see the immediate results of that code, hop into the folder and type `make pdf`, which will use the bash script included to generate the final file for you in a `build` folder. Again, if you use snippets from that code please cite this repository.

Some examples:

	f(z) = exp(conj(z)) - z^2
![](images/expconjz_minus_zsquared.png)

	f(z) = exp(z) - z^2
![](images/expz_minus_zsquared.png)
