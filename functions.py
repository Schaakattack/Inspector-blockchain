#import nltk
#from nltk.cluster.kmeans import KMeansClusterer 

import sqlite3
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn import cluster
from sklearn.metrics import silhouette_score, silhouette_samples
from sklearn.preprocessing import StandardScaler, PowerTransformer, FunctionTransformer
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
import random
from sklearn.cluster import KMeans
import matplotlib.cm as cm
from mpl_toolkits.mplot3d import Axes3D
import time
from sklearn.manifold import TSNE


def load_data_from_inspector_db(filename):

    conn = sqlite3.connect(filename)
    
    # all data
    sql = """
            SELECT sender,
                   receiver,
                   SUM(tokens) AS tokens,
                   COUNT(sender) AS num_of_transactions
            FROM transactions
            GROUP BY sender, receiver;
        """

    df = pd.read_sql(sql, conn)
  
    return df

def data_pipeline(df):
    #strip address column
    data = df.iloc[:,1:]
    log = FunctionTransformer(func=np.log1p, inverse_func=np.expm1, validate=True)
    scale = StandardScaler()
    pca =PCA(n_components=data.shape[1])
    

    #build pipeline
    pipe = Pipeline([('log', log ),
                     ('scale', scale ),
                     ('PCA', pca)])

    results = pipe.fit_transform(data)
    return pipe, results

def cluster(results, n_clusters):
    cl = KMeans(n_clusters, n_init=20, max_iter=500,n_jobs=-1, verbose=0)
    return cl.fit(results)
    
    

def assign_cluster_to_data(df, dflabel, cl):
    lbls = []
    addrs = list(df['address'].values)
    for i, row in dflabel.iterrows():
        addr = row['address']
        if row['address'] in addrs:
            lbls.append(addrs.index(row['address']))
        else:
            lbls.append(False)

    dflabel['cluster'] = [cl.labels_[i] for i in lbls]
    return None

def calc_tsne(results, n_components=2, perplexity=20, n_iter=300,verbose=1):
    '''
    Calculated tsne for dataset'''
    time_start = time.time()
    tsne = TSNE(n_components=n_components, perplexity=perplexity, n_iter=n_iter,verbose=verbose,learning_rate=100)
    tsne_results = tsne.fit_transform(results)
    print('t-SNE done! Time elapsed: {} seconds'.format(time.time()-time_start))
    return tsne_results


def plot_tsne(cl, tsne_results ):
    '''
    plot'''
    
    NUM_COLORS = cl.n_clusters
    cm = plt.get_cmap('nipy_spectral')

    fig = plt.figure(figsize=(15,12))
    ax = fig.add_subplot(111)
    ax.set_color_cycle([cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])


    for c in np.unique(cl.labels_):
        mask = cl.labels_==c
        if np.sum(mask) <1:
            lbl = '_nolegend_'
        else:
            lbl = c
        plt.scatter(tsne_results[mask][:,0], tsne_results[mask][:,1], s=20, alpha=.4,label=lbl)

    leg = plt.legend(bbox_to_anchor=(1, 1))
    for lh in leg.legendHandles: 
        lh.set_alpha(1)




    plt.title('T-SNE', fontsize=20)
    plt.xlabel('first principal component')
    plt.ylabel('second principal component')
    plt.show()
    
    
def find_category_of_cluster(cl,dflabel, category="Exchange"):
    #assign cluster number with the most exchanges
    type_cluster = 0
    num_of_type = 0
    lbl_density=0
    print(category)
    for clust in np.unique(cl.labels_):
        size_of_cluster = np.sum(cl.labels_==clust)
        
        
        mask = dflabel['cluster']==clust
        d = dflabel[mask]
        num = np.sum(d['category']==category)
        density = num / size_of_cluster
        if num > num_of_type:
            lbl_density=density
            num_of_type = num
            type_cluster = clust
        print('cluster number   {}   number of type found: {}    cluster size: {}   label density: {}'.format(clust,num,size_of_cluster,density))
    return type_cluster

def plot_tsne_with_labels(tsne_results,df, dflabel,categs,colors):
    #need to mask df based on which results were kept from the reclustering
    
    labeled_addresses = dflabel['address'].values
    labelmask = np.array([addr in labeled_addresses for addr in df['address'] ] )
    #helper function for category mask
    def cat(addr, labeled_addresses, dflabel):
        if addr not in labeled_addresses:
            return False
        else:
            idx = int(np.where(labeled_addresses==addr)[0][0])
            return dflabel['category'][idx]

    subset, not_subset  = tsne_results[labelmask] , tsne_results[~labelmask]
    fig = plt.figure(figsize=(15,12))
    #not labelled points
    plt.scatter(not_subset[:,0], not_subset[:,1], s=20, c='gray', alpha=.3)

    #categories
    cats = np.array([cat(addr, labeled_addresses, dflabel) for addr in df['address']])#[address_mask] ]) #added address mask for all clusters

    # # #labelled points

    # ax = fig.add_subplot(111)
    # ax.set_color_cycle([cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])

    for c in list(dflabel['category'].unique()):
        mask = dflabel['category']==c
        if np.sum(mask) <1:
            lbl = '_nolegend_'
        else:
            lbl = c

        #category mask
        catmask = cats == c

        if c in categs:
            idx=categs.index(c)
            color = colors[idx]

            plt.scatter(tsne_results[(labelmask & catmask)][:,0], tsne_results[(labelmask & catmask)][:,1], s=100,c=color, alpha=1,label=lbl)

    leg = plt.legend(bbox_to_anchor=(1, 1))
    for lh in leg.legendHandles: 
        lh.set_alpha(1)

    plt.title('T-SNE', fontsize=20)
    plt.xlabel('first principal component')
    plt.ylabel('second principal component')
    plt.show()


def plot_tsne_with_labeled_clusters(tsne_results, cl, clusters, categs, colors):
    fig = plt.figure(figsize=(15,12))
    ax = fig.add_subplot(111)


    for c in np.unique(cl.labels_):
        mask = cl.labels_==c

        if c in clusters:
            idx = clusters.index(c)
            lbl = categs[idx]
            color = colors[idx]

            plt.scatter(tsne_results[mask][:,0], tsne_results[mask][:,1], s=100,c=color,alpha=.4,label=('Cluster {} - "{}" '.format(c,lbl) ))
        else:
             plt.scatter(tsne_results[mask][:,0], tsne_results[mask][:,1], c='gray',s=20, alpha=.3)

    leg = plt.legend(bbox_to_anchor=(1, 1))
    for lh in leg.legendHandles: 
        lh.set_alpha(1)




    plt.title('T-SNE', fontsize=20)
    plt.xlabel('first principal component')
    plt.ylabel('second principal component')
    plt.show()
    
def recluster(df, cl, clusters, n_clusters):
    lbls = cl.labels_
    mask = np.array([False for i in range(len(lbls))])
    for c in clusters:
        mask |= lbls==c
    subpipe, results = data_pipeline(df[mask])
    
    ##use cosine similarity! NLTK clustering implementation
    #KMeans cluster object as carrier for consistency
    subcl = cluster(results, n_clusters)
    kclusterer = KMeansClusterer(n_clusters, distance=nltk.cluster.util.cosine_distance, repeats=50)
    assigned_clusters = kclusterer.cluster(results, assign_clusters=True)
    #assign new cluster labels and cluster centroids
    subcl.labels_ = np.array(assigned_clusters)
    subcl.cluster_centers_ = np.array(kclusterer.means())
    
    return subpipe, subcl, results, df[mask]

def plot_all(tsne_results,cl,df,dflabel,clusters,categs,colors ):
    plot_tsne(cl, tsne_results)
    plot_tsne_with_labeled_clusters(tsne_results, cl, clusters, categs, colors)
    plot_tsne_with_labels(tsne_results,df, dflabel,categs,colors)
    


    