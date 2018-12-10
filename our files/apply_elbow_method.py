
def apply_elbow(dataset):

    wcss = []

    
    for i in range(1, 11):
        kmeans = KMeans(n_clusters = i, init = 'k-means++')
        kmeans.fit(dataset)
        wcss.append(kmeans.inertia_)

    return wcss


# Applying elbow method for information data set
score_list_ids = apply_elbow(information_ds_persist['dataset'])


# Applying elbow method for description data set
score_list_dds = apply_elbow(description_ds_persist['dataset'])

print("Plot for IDS: ")

plt.plot(range(1,11), score_list_ids)

print("Plot for DDS: ")

plt.plot(range(1,11), score_list_dds)


distances = []

# from 2 clusters 
p1=np.array([2,wcss[1]])
p2=np.array([10,wcss[9]])

for i in range(1,10):
    p3 = np.array([i+1,wcss[i]])
    d = abs(np.cross(p2-p1,p3-p1)/np.linalg.norm(p2-p1))
    distances.append(d)

plt.plot(range(2,11), wcss[1:])
plt.plot([2, 10],[wcss[1], wcss[9]] )