# Complex function plotter, written by Gondolindrim
# For information, read the repository https://github.com/gondoresearch/complex_function_plotter
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.colors as mcolors
from matplotlib.colors import hsv_to_rgb

# Generates logarithmic levels spaced linearly in each decade and include the first level of the next decade.
# For instance, generate_log_levels(0.2,1) will yield an array [0.01,0.02,0.03,...,0.09,0.1,0.2,0.3,...,0.9,1]
# In other words, you will receive a array of appended values of the form [1e(-k),2e(-k),3e(-k),...,9e(-k)].
# This is useful to quickly generate levels for functions that explode at infinity or particular values.
def generate_log10_levels(start_pow, end_pow):
	levels = []
	for p in range(start_pow, end_pow): levels.extend(np.arange(1, 10) * (10.**p))
	levels.append(10.**end_pow)
	return np.array(levels)

# This generates levels on a particular base. For instance, 
# generate_log_levels(-2,2,2) yields [0.25,0.5,1,2,4] and
# generate_log_levels(-1,3,10) yields [-1,1,10,100,1000].
def generate_log_levels(start_pow, end_pow, base):
	levels = []
	for p in range(start_pow, end_pow): levels.append(base**p)
	return np.array(levels)


# Brightness normalization that applies the "discontinuous brightness ladder" trick
def normalize_brightness(abs_val, levels, min_v=0.1):
	lvls = np.sort(levels)
	v = np.zeros_like(abs_val)
	def scale(data, low, high):
		norm = (data - low) / (high - low)
		return min_v + (1.0 - min_v) * norm

	# Fixed broadcasting logic
	mask_low = abs_val < lvls[0]
	v[mask_low] = scale(abs_val[mask_low], 0, lvls[0])
	for i in range(len(lvls) - 1):
		low, high = lvls[i], lvls[i+1]
		mask = (abs_val >= low) & (abs_val < high)
		v[mask] = scale(abs_val[mask], low, high)
	v[abs_val >= lvls[-1]] = 1.0
	return np.clip(v, 0, 1)

# The main function. Plots the given function and exports it to a PNG
def export_with_custom_cmap(f, levels, cmap_name='viridis', filename="complex_data.png", x_range=(-12, 12), y_range=(-12, 12), res=2000):
	# Define coordinate grid
	x = np.linspace(x_range[0], x_range[1], res)
	y = np.linspace(y_range[0], y_range[1], res)
	X, Y = np.meshgrid(x, y)

	# Calculate function
	Z = X + 1j*Y
	W = f(Z)
	
	# Map phase to [0, 1]
	phase_norm = (np.angle(W) + np.pi) / (2 * np.pi)
	
	# Get colors from given colormap
	if isinstance(cmap_name, str): cmap = mpl.colormaps[cmap_name] # If using the colormap by name
	else: cmap = cmap_name # If passing the colormap object itself
	# This gives an (res, res, 4) RGBA array
	base_rgba = cmap(phase_norm)
	base_rgb = base_rgba[..., :3] # Strip alpha
	
	# Modulate brightness and get leveled brightness mask
	v = normalize_brightness(np.abs(W), levels, min_v=0.5)
	
	# Apply brightness: multiply the RGB colors by the brightness mask
	# We add an axis to v so it broadcasts across (res, res, 3)
	final_rgb = base_rgb * v[..., np.newaxis]
	
	# Save and show
	plt.imsave(filename, final_rgb, origin='lower')
	
	fig, ax = plt.subplots()
	ax.imshow(final_rgb, extent=[*x_range, *y_range], origin='lower', interpolation='lanczos')
	
	# Make phase colorbar match the custom map
	sm = mpl.cm.ScalarMappable(cmap=cmap, norm=mpl.colors.Normalize(vmin=-np.pi, vmax=np.pi))
	cbar = fig.colorbar(sm, ax=ax, ticks=[-np.pi, -np.pi/2, 0, np.pi/2, np.pi])
	cbar.ax.set_yticklabels([r'$-\pi$', r'$-\pi/2$', r'0', r'$\pi/2$', r'$\pi$'])
	
	plt.show()

# Regarding colormaps: thus function generates LaTeX-ready RGB points from the colormaps, in case they are not defined in pgfplots.
# The colormap used in the reference website is HSV. The problem with HSV is that it is cyclic, that is, the border between -pi and pi is
# blurred because both ends are red in color. Particularly, I like gist_rainbow because it still has the "rainbow" effect, but
# it is not cyclic, so that one can see the angle changes between -pi and pi.
# Colormap	Python		pgfplots		Description
# Viridis	cmap='viridis'	colormap/viridis	Perceptually uniform
# Hot		cmap='hot'	colormap/hot		Black to red to yellow to white
# Cool		cmap='cool'	colormap/cool		Cyan to magenta transition
# Copper	cmap='copper'	colormap/copper		Black to copper/light brown
# Bone		cmap='bone'	colormap/bone		Gray with a hint of blue; similar to MATLAB
# HSV		cmap='hsv'	colormap/hsv		Classic cyclic rainbow
# Jet		cmap='jet'	colormap/jet		Classic non-uniform rainbow
# Gray		cmap='gray'	colormap/blackwhite	Standard grayscale
#
# If you want to use a customized colormap, use this function to generate a ready-to-use colormap definition for pgfplots. Specifically for the
#	gist_raibow, this script should accompany a definition file "gist_rainbow_latexdef.tex" that you can just use in your tex file by adding
#	\input{gist_rainbow_latexdef.tex} in your preamble.
def generate_latex_colormap(cmap_name, samples=256):
	cmap = plt.get_cmap(cmap_name)
	colors = cmap(np.linspace(0, 1, samples))
	
	print(f"\\pgfplotsset{{\n colormap={{{cmap_name}}}{{\n", end="")
	for r, g, b, a in colors: print(f"rgb=({r:.4f},{g:.4f},{b:.4f})")
	print("	}\n}")

# Example execution
levels = generate_log_levels(-1, 8, np.e)
cmap = 'gist_rainbow'
export_with_custom_cmap(lambda z: np.exp(np.conj(z)) - z**2, levels, res=2000, x_range=(-12,12),y_range=(-12,12), cmap_name=cmap)

generate_latex_colormap(cmap)
