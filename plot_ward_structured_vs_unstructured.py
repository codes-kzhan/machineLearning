'''
plot_ward_structured_vs_unstructured.py
Hierarchical clustering: structured vs unstructured ward
'''

import time as time 
import numpy as np 
import matplotlib.pyplot as plt 
import mpl_toolkits.mplot3d.axes3d as p3 
from sklearn.cluster import AgglomerativeClustering 
from sklearn.datasets.samples_generator import make_swiss_roll 

# generate data (swiss roll dataset)
n_samples = 1500 
noise = 0.05 
X, _ = make_swiss_roll(n_samples, noise)
# make it thinner 
X[:, 1] *= 0.5 

# compute clustering 
print('Compute unstructured hierarchical clustering ...')
st = time.time()
ward = AgglomerativeClustering(n_clusters=6, linkage='ward').fit(X)
elapsed_time = time.time() - st 
label = ward.labels_ 
print('Elapsed time: %.2fs' % elapsed_time)
print('Number of points: %i' % label.size)

# plot result 
fig = plt.figure()
ax = p3.Axes3D(fig)
ax.view_init(7, -80)
for l in np.unique(label):
    ax.plot3D(
        X[label == l, 0], 
        X[label == l, 1],
        X[label == l, 2], 
        'o',
        color = plt.cm.jet(np.float(l) / np.max(label + 1))
    )

plt.title('Without connectivity constraints (time %.2fs)' 
    % elapsed_time)

'''
Define the structure a of the data.
Hrer a 10 nearest neighbors 
'''
from sklearn.neighbors import kneighbors_graph 
connectivity = kneighbors_graph(
    X, 
    n_neighbors=10, 
    include_self=False
)

print('Compute structured hierarchical clustering ...')
st = time.time()
ward = AgglomerativeClustering(
    n_clusters=6,
    connectivity = connectivity,
    linkage='ward').fit(X)

elapsed_time = time.time() - st 
label = ward.labels_ 
print('Elapsed time: %.2fs' % elapsed_time)
print('Number of points: %i' % label.size)

# plot result 
fig = plt.figure()
ax = p3.Axes3D(fig)
ax.view_init(7, -80)
for l in np.unique(label):
    ax.plot3D(
        X[label == l, 0], 
        X[label == l, 1],
        X[label == l, 2],
        'o',
        color = plt.cm.jet(float(l) / np.max(label + 1))
    )

plt.title('With connectivity constraints (time %.2fs)' 
    % elapsed_time)

plt.show()
