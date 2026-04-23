# Complex function plotter, written by Gondolindrim
# For information, read the repository https://github.com/gondoresearch/complex_function_plottetr
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
def export_with_custom_cmap(
		f, # The function
		levels, # The levels of absolute values that define the brightness discontinuities
		cmap_name='viridis',
		filename="complex_data.png",
		xrange=(-12, 12),
		yrange=(-12, 12),
		res=2000, # Number of points on each coordinate
		grid_mapping = True, # Yes or no to gridmapping. The grid_* params are not used if this is false.
		grid_spacing=10.0, # Size of the squares of the grid mapping
		grid_opacity=0.5, # The grid mapping is a "checkerboard" pattern on top of the plot, so adjusting opacity is good
		# If the plot brightness is above this value, gives directly 1. This can be used to limit how the checkerboard patter transforms the brightness around some discontinuities
		grid_brightness=0.5,
		grid_threshold=0.8 # To prevent artifacts
	):
	# Define coordinate grid
	x = np.linspace(xrange[0], xrange[1], res)
	y = np.linspace(yrange[0], yrange[1], res)
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

	# Gridmapping
	if grid_mapping:
		# Create a checkerboard pattern based on the real and imaginary parts of W
		# The % 2 operation creates the alternating pattern
		grid_re = (np.real(W) // grid_spacing) % 2
		grid_im = (np.imag(W) // grid_spacing) % 2

		abs_W = np.abs(W) 

		grid_re = (np.real(W) // grid_spacing) % 2
		grid_im = (np.imag(W) // grid_spacing) % 2
		chess_mask = np.logical_xor(grid_re, grid_im)
		
		# Gridmapping with artifact prevention: when f(z) explodes, generally at infinity or around a pole, its
		# absolute value is such that the squares of the gridmapping fall below the pixel resolution, creating a noisy blurry artifact.
		# This defines a threshold for where the grid starts to look "noisy enough", as a fraction of the highest level defined.
		# This probably will need some tuning to look good, and is tied to the highest level or the resolution of exporting.
		high_mag_threshold = np.max(levels) * grid_threshold
		
		# Create a smooth fade-out factor for the grid based on magnitude
		# grid_fade is 1.0 (full grid) at low values and 0.0 (no grid) at high values
		grid_fade = np.clip((high_mag_threshold - abs_W) / (high_mag_threshold * 0.2), 0, 1)
		
		# Calculate the darkened grid layer
		grid_multiplier = np.where(chess_mask, grid_brightness, 1.0)
		grid_rgb = final_rgb * grid_multiplier[..., np.newaxis]
		
		# Apply the grid with magnitude-dependent opacity
		# Total Opacity = User Set Opacity * Fade Factor
		effective_opacity = grid_opacity * grid_fade[..., np.newaxis]
		final_rgb = (1 - effective_opacity) * final_rgb + (effective_opacity * grid_rgb)
	
	# Save and show
	plt.imsave(filename, final_rgb, origin='lower')
	
	fig, ax = plt.subplots()
	ax.imshow(final_rgb, extent=[*xrange, *yrange], origin='lower', interpolation='lanczos')
	
	# Make phase colorbar match the colormap given
	sm = mpl.cm.ScalarMappable(cmap=cmap, norm=mpl.colors.Normalize(vmin=-np.pi, vmax=np.pi))
	cbar = fig.colorbar(sm, ax=ax, ticks=[-np.pi, -np.pi/2, 0, np.pi/2, np.pi])
	cbar.ax.set_yticklabels([r'$-\pi$', r'$-\pi/2$', r'0', r'$\pi/2$', r'$\pi$'])
	
	plt.show()

def generate_latex_colormap(cmap_name, samples=256):
	cmap = plt.get_cmap(cmap_name)
	colors = cmap(np.linspace(0, 1, samples))
	
	print(f"\\pgfplotsset{{\n colormap={{{cmap_name}}}{{\n", end="")
	for r, g, b, a in colors: print(f"rgb=({r:.4f},{g:.4f},{b:.4f})")
	print("	}\n}")

# Example execution
levels = generate_log_levels(-1, 8, np.e)
cmap = 'gist_rainbow'
export_with_custom_cmap(lambda z: np.exp(np.conj(z)) - z**2, levels, res=2000, xrange=(-12,12),yrange=(-12,12), cmap_name=cmap,grid_mapping = True, grid_threshold=0.3)

generate_latex_colormap(cmap)
