%matplotlib widget
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import LassoSelector, RectangleSelector
from matplotlib.path import Path
from scipy import interpolate

# Set interactive mode on
plt.ion()

# Sample data
np.random.seed(42)
x = np.random.rand(100)
y = np.random.rand(100)
colors = np.ones(len(x))  # Initial colors (all the same)

# Create the figure and axes
fig, ax = plt.subplots(figsize=(10, 8))
plt.subplots_adjust(bottom=0.2)  # Make room for buttons

# Initial scatter plot
scatter = ax.scatter(x, y, c=colors, s=100, alpha=0.6)
ax.set_title('Interactive Selection Demo - Use Tools Below', fontsize=14)

# Selected points indices
selected_points = []

# Function to update plot after selection
def update_scatter():
    global colors
    colors = np.ones(len(x))  # Reset colors
    if len(selected_points) > 0:  # Check length instead of array directly
        colors[selected_points] = 0.5  # Highlight selected points
    scatter.set_facecolors(plt.cm.viridis(colors))
    fig.canvas.draw_idle()

# Lasso selection callback
def onselect_lasso(verts):
    global selected_points
    path = Path(verts)
    selected_points = np.where(path.contains_points(np.vstack((x, y)).T))[0]
    update_scatter()
    
    # Store the original lasso vertices (the trace)
    lasso_trace_original = np.array(verts)
    
    # Smooth the lasso trace using spline interpolation
    lasso_trace = smooth_lasso_trace(lasso_trace_original)
    
    # Make the traces available globally
    globals()['lasso_trace_original'] = lasso_trace_original
    globals()['lasso_trace'] = lasso_trace
    
    # Get the coordinates of selected points
    selected_coords = [(x[i], y[i]) for i in selected_points]
    globals()['selected_coords'] = selected_coords
    
    # Display information about selected points and lasso trace
    selection_text = f'Selected {len(selected_points)} points'
    if len(selected_points) > 0:
        selection_text += f'\nSelected points available in: selected_coords'
    
    selection_info.set_text(selection_text)
    
    # Print info about the lasso trace
    print(f"Original lasso trace: {len(lasso_trace_original)} vertices")
    print(f"Smoothed lasso trace: {len(lasso_trace)} vertices")
    print("Available variables:")
    print("- lasso_trace: smoothed outline")
    print("- lasso_trace_original: original outline")
    print("- selected_coords: selected data points")
    
    # Plot both the original and smoothed traces
    if hasattr(ax, 'lasso_trace_line'):
        ax.lasso_trace_line.remove()
    if hasattr(ax, 'lasso_trace_orig'):
        ax.lasso_trace_orig.remove()
        
    # Draw the original trace as a thin, faded line
    ax.lasso_trace_orig = ax.plot(lasso_trace_original[:, 0], lasso_trace_original[:, 1], 
                                 'b-', lw=1, alpha=0.3, label='Original')[0]
    
    # Draw the smoothed trace as a more prominent line
    ax.lasso_trace_line = ax.plot(lasso_trace[:, 0], lasso_trace[:, 1], 
                                  'r-', lw=2, alpha=0.8, label='Smoothed')[0]
    
    # Add a small legend
    if not hasattr(ax, 'trace_legend'):
        ax.trace_legend = ax.legend(loc='upper right', framealpha=0.7)
    else:
        ax.legend(loc='upper right', framealpha=0.7)
        
    fig.canvas.draw_idle()
    
    return lasso_trace, selected_coords

# Function to smooth the lasso trace
def smooth_lasso_trace(original_trace, smoothing_factor=0.3, num_points=100):
    """
    Smooth the lasso trace using B-spline interpolation
    
    Parameters:
    - original_trace: numpy array of shape (n, 2) with x,y coordinates
    - smoothing_factor: controls the smoothness (0=straight lines, 1=very smooth)
    - num_points: number of points in the smoothed output
    
    Returns:
    - smoothed_trace: numpy array of shape (num_points, 2)
    """
    # Check if we have enough points to smooth
    if len(original_trace) < 4:
        return original_trace  # Not enough points to smooth
    
    # Make sure the lasso is closed
    if not np.array_equal(original_trace[0], original_trace[-1]):
        original_trace = np.vstack([original_trace, original_trace[0]])
    
    # Create a parameter along the trace
    t = np.zeros(len(original_trace))
    for i in range(1, len(original_trace)):
        t[i] = t[i-1] + np.linalg.norm(original_trace[i] - original_trace[i-1])
    
    # Normalize parameter to [0, 1]
    if t[-1] > 0:
        t = t / t[-1]
    
    # Create the spline interpolation for x and y coordinates
    s = len(original_trace) * smoothing_factor  # Smoothing parameter
    try:
        tck, _ = interpolate.splprep([original_trace[:, 0], original_trace[:, 1]], 
                                     s=s, k=3, per=True)
        
        # Evaluate the spline at evenly spaced points
        u_new = np.linspace(0, 1, num_points)
        smoothed_points = np.array(interpolate.splev(u_new, tck)).T
        
        return smoothed_points
    except:
        # If splprep fails (can happen with self-intersections), fall back to simpler smoothing
        print("Spline smoothing failed, using simpler method")
        # Make a copy to avoid modifying the original
        smoothed = np.copy(original_trace)
        
        # Simple moving average for each coordinate
        window = max(3, len(original_trace) // 10)  # Dynamic window size
        if window % 2 == 0:
            window += 1  # Ensure odd window size
            
        for i in range(len(smoothed)):
            # Calculate indices for the window, handling wrap-around
            indices = [(i + j) % len(smoothed) for j in range(-window//2, window//2 + 1)]
            # Apply moving average
            smoothed[i] = np.mean(original_trace[indices], axis=0)
            
        return smoothed

# Rectangle selection callback
def onselect_rectangle(eclick, erelease):
    global selected_points
    x0, y0 = eclick.xdata, eclick.ydata
    x1, y1 = erelease.xdata, erelease.ydata
    
    # Find points within the rectangle
    selected_points = np.where(
        (x >= min(x0, x1)) & (x <= max(x0, x1)) & 
        (y >= min(y0, y1)) & (y <= max(y0, y1))
    )[0]
    update_scatter()
    
    # Get the coordinates of selected points
    selected_coords = [(x[i], y[i]) for i in selected_points]
    
    # Display information about selected points
    selection_text = f'Selected {len(selected_points)} points'
    if len(selected_points) > 0:
        selection_text += f'\nSelected points are available in variable: selected_coords'
        # Print to console/output for easy access
        print(f"Selected {len(selected_points)} points:")
        print(f"selected_coords = {selected_coords}")
    
    selection_info.set_text(selection_text)
    
    # Make the coordinates available globally
    globals()['selected_coords'] = selected_coords
    
    return selected_coords

# Create a text element for displaying selection info
selection_info = ax.text(0.05, 0.05, '', transform=ax.transAxes,
                         bbox=dict(boxstyle="round,pad=0.5", fc="yellow", alpha=0.7))

# Create lasso selector
lasso = LassoSelector(
    ax, 
    onselect_lasso,
    props=dict(color='black', linewidth=2),
    useblit=True,
    button=1  # Left mouse button
)
lasso.set_active(False)  # Initially inactive

# Create rectangle selector with smoother appearance
rect_selector = RectangleSelector(
    ax,
    onselect_rectangle,
    useblit=True,
    button=1,  # Left mouse button
    minspanx=5, minspany=5,
    spancoords='pixels',
    interactive=True,
    props=dict(facecolor='blue', edgecolor='black', alpha=0.2, linewidth=2)
)
rect_selector.set_active(False)  # Initially inactive

# Function to reset selection
def reset_selection(event):
    global selected_points
    selected_points = []
    update_scatter()
    selection_info.set_text('')

# Add control buttons
ax_lasso = plt.axes([0.15, 0.05, 0.2, 0.075])
ax_rectangle = plt.axes([0.4, 0.05, 0.2, 0.075])
ax_reset = plt.axes([0.65, 0.05, 0.2, 0.075])

button_lasso = plt.Button(ax_lasso, 'Lasso Select')
button_rectangle = plt.Button(ax_rectangle, 'Rectangle Select')
button_reset = plt.Button(ax_reset, 'Reset Selection')

# Button click handlers
def activate_lasso(event):
    lasso.set_active(True)
    rect_selector.set_active(False)
    ax.set_title('Lasso Selection Mode - Click and drag to select points', fontsize=14)
    
def activate_rectangle(event):
    lasso.set_active(False)
    rect_selector.set_active(True)
    ax.set_title('Rectangle Selection Mode - Click and drag to select points', fontsize=14)

button_lasso.on_clicked(activate_lasso)
button_rectangle.on_clicked(activate_rectangle)
button_reset.on_clicked(reset_selection)

plt.show()
