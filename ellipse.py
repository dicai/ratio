import numpy as np
import tabular as tb
import pylab

from matplotlib.patches import Ellipse

def _get_theta(x, y):
	return np.arccos( _dot(x, y) / _norm(x) / _norm(y) )

def _dot(x, y):
	return (x * y).sum()

def _norm(x):
	return np.sqrt(_dot(x, x))

def _rad_to_deg(theta):
	return theta * 180 / np.pi

def get_ellipse(x, y):
	a = np.column_stack((x, y))
	a = a - np.repeat(a.mean(axis=0), a.shape[0]).reshape(a.shape[1], a.shape[0]).T	# mean center
	(w, v) = np.linalg.eig(np.cov(a.T))
	i = np.nonzero((-w).argsort()==0)[0][0]		# indices for the top 2 eigenvalues
	j = np.nonzero((-w).argsort()==1)[0][0]	
	xy = (np.mean(x), np.mean(y))
	width = np.sqrt(w[i]) * 2
	height = np.sqrt(w[j]) * 2
	unit = np.array([1, 0])
	vi = v[:,i]
	#vi = vi / _norm(vi)		# already normalized
	theta = _get_theta(vi, unit)
	angle = _rad_to_deg(theta)
	return (xy, width, height, angle)

def plot_ellipse(x, y, ax, color):
	(xy, width, height, angle) = get_ellipse(x, y)
	e = Ellipse(xy, width, height, angle)
	ax.add_artist(e)
	#e.set_clip_box(ax.bbox)
	e.set_alpha(0.2)
	e.set_facecolor(color)
