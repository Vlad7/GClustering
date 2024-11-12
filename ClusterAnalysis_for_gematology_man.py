import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from enum import Enum
#import webcolors as wc
import skfuzzy as fuzz
from sklearn.model_selection import train_test_split
from sklearn.cluster import KMeans
from mpl_toolkits.mplot3d import Axes3D
from sklearn.model_selection import train_test_split
from scipy.spatial.distance import cdist


class Feature(Enum):
    MCH = 1
    MCHC = 2
    MCV = 3
    MPV = 4
    PDW = 5
    RDW = 6
    Hematocrit = 7
    Hemoglobin = 8
    Granulocytes = 9
    Red_blood_cells = 10
    Leukocytes = 11
    Lymphocytes = 12
    Monocyte = 13
    Thrombocrit = 14
    Thrombocytes = 15
    ESR = 16

class ClusterAnalysis:
    
    def __init__ (self, path, sex):

        self.df_male = pd.read_excel(path,
                          sheet_name=sex,
                          names=['Age',
                                 'MCH',
                                 'MCHC',
                                 'MCV',
                                 'MPV',
                                 'PDW',
                                 'RDW',
                                 'Hematocrit',
                                 'Hemoglobin',
                                 'Granulocytes',
                                 'Red blood cells',
                                 'Leukocytes',
                                 'Lymphocytes',
                                 'Monocyte',
                                 'Thrombocrit',
                                 'Thrombocytes',
                                 'ESR'])

        print('Data was imported')

        #Biomarkers
        
        #features1 = [for e in Feature]
        features1=[
                                 'MCH',
                                 'MCHC',
                                 'MCV',
                                 'MPV',
                                 'PDW',
                                 'RDW',
                                 'Hematocrit',
                                 'Hemoglobin',
                                 'Granulocytes',
                                 'Red blood cells',
                                 'Leukocytes',
                                 'Lymphocytes',
                                 'Monocyte',
                                 'Thrombocrit',
                                 'Thrombocytes',
                                 'ESR']

        print (features1)

        #Pisaruk

        
        features2 = ['RDW',
            'Hematocrit',
            'Hemoglobin',
            'Thrombocytes',
            'ESR']

        features = features2

        self.data = self.df_male
       

        self.train_data, self.test_data, self.train_ages, self.test_ages = self.split_on_train_and_test_datasets(self.data)
        
        # Separating out the features
        self.train_features = self.train_data.loc[:, features]
        print(self.train_features)

        self.scale()

        # Separating out the ages
        self.Ages = self.train_ages
        print(self.Ages)


        print(len(self.train_features))



    def scale (self):
        
        # Scaling

        std_scaler = StandardScaler()
        self.train_features_set_scaled = std_scaler.fit_transform(self.train_features.values)
        
        
    def split_on_train_and_test_datasets(self, dataframe, age_bins=False):

        # Пустые DataFrame'ы для тренировочной и тестовой выборки
        train_data = pd.DataFrame()
        test_data = pd.DataFrame()

        train_ages = pd.DataFrame()
        test_ages = pd.DataFrame()
        
        if age_bins:
            # Разбиваем на возрастные бины
            bins = [20, 30, 40, 50, 60, 70, 80, 90]
            labels = ['20-30', '30-40', '40-50', '50-60', '60-70', '70-80', '80-90']
            dataframe['AgeBin'] = pd.cut(dataframe['Age'], bins=bins, labels=labels)

            # Пропорциональное разбиение для каждого бина
            for bin_label in labels:
                bin_data = dataframe[dataframe['AgeBin'] == bin_label]

                # Пропорциональный размер тестового набора зависит от количества данных в бине
                if len(bin_data) > 1:  # Проверяем, что есть больше одного элемента для разделения
                    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    test_size = min(0.3, 1 / len(bin_data))  # Чем меньше данных, тем меньший тестовый набор
                    print(test_size)

                    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    train_bin, test_bin = train_test_split(bin_data, test_size=test_size, random_state=42)

                    train_data = pd.concat([train_data, train_bin], axis=0)
                    test_data = pd.concat([test_data, test_bin], axis=0)

        else:
            # Вхідні дані (біомаркери)
            X = dataframe.drop('Age', axis=1)

            # Цільова змінна (вік)
            y = dataframe['Age']

            # Розбиваємо вибірку на навчальний та тестовий набори
            # test_size=0.1 означає, що 10% даних піде у тестовий набір
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

            # Перевірка розмірів вибірок
            print(f'Розмір навчального набору: {X_train.shape}')
            print(f'Розмір тестового набору: {X_test.shape}')

            train_data = pd.concat([train_data, X_train], axis=0)
            test_data = pd.concat([test_data, X_test], axis=0)

            train_ages = pd.concat([train_ages, y_train], axis=0)
            test_ages = pd.concat([test_ages, y_test], axis=0)
            ##############################!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            ########## Зробити повернення вікових даних
           

        # Сбрасываем индексы
        #train_data = train_data.reset_index(drop=True)
        #test_data = test_data.reset_index(drop=True)

        train_data = train_data.sort_index()
        test_data = test_data.sort_index()

        train_ages = train_ages.sort_index()
        test_ages = test_ages.sort_index()



        print("Training data:")
        print(train_data)
        print("\nTest data:")
        print(test_data)

        return train_data, test_data, train_ages, test_ages
        #print(self.data['AgeBin'])

        #X_train, X_test, y_train, y_test = train_test_split(self.train_features, self.Ages.iloc[:,0],
        #                                                    test_size=0.2, random_state=42, stratify=self.Ages.iloc[:,0])
        #print(X_train)




    def ages_distribution(self):

        # Припустимо, що у вас є колонка 'Age' з віковими даними
        n, bins, patches = plt.hist(self.data['Age'], bins=10)
        plt.title('Розподіл вікових груп')
        plt.xlabel('Вік')
        plt.ylabel('Кількість')
        # Додаємо сітку по границям бінів
        plt.grid(True, which='both', axis='x')
        
        plt.xticks(bins)  # Встановлюємо мітки по границям бінів

        plt.show()


        # Створюємо гістограму та отримуємо дані про бінінг






        # !!! Треба по групам, а не просто по вікам.
        age_distribution = self.data['Age'].value_counts()
        print(age_distribution)

    def biological_age (self, analysis):

        # Add normalisation for biomarkers !!!!!!!!!!!!!!!!!!!!!!
        min_dist = 100000000000
        min_index = 0
        for index, row in self.train_features.iterrows():
            dist = np.linalg.norm(row-analysis)
            if dist < min_dist:
                min_dist = dist
                min_index = index

        print(self.Ages.values[min_index])

    ###################################################################
    ###################################################################
    ###################################################################
   
    def pca(self, features_set, n_components_=2):
        """ PCA

            input:
                - features_set - dataframe with features
                - n_components - number of principal components
            output:
                principal components
        """
        
        # Principal component analisys for 3 components
        pca = PCA(n_components=n_components_)
        principalComponents = pca.fit_transform(features_set)

        sufixes = []

        if n_components_ == 2:
            sufixes.append("2nd")
        elif n_components_ == 3:
            sufixes.append("3rd")
        else:
            raise Exception("Number of components must be 2 or 3!")
            
                
        print("PCA explained variance ratio (1st, " + ', '.join(sufixes) + "): ", pca.explained_variance_ratio_)

        return principalComponents













    def plot_pca(self, features_set, membership_matrix=None, centers=None, show_indexes=False, show_ages=False):
        """ Principal component analisys for plot clustered data

            input:
                - features_set - dataframe with features
                - labels = labels from classified class
                - show_indexes - show texts of indexes near data points on plot

            method complete!!! maybe same scale of different axis
        """
        # Create dataframe with principal components
        principalDf = pd.DataFrame(data = self.pca(features_set, 3)
             , columns = ['principal component 1', 'principal component 2', 'principal component 3'])

        labels = None

        if membership_matrix is None:

            # Transform labels list to np.array and numeration from 1
            labels = np.array([0] * len(self.train_features))

        elif membership_matrix.ndim==1:

            labels = membership_matrix

        else:

            labels = np.argmax(membership_matrix, axis=0)

        labels = np.array(labels) + 1


        # Create target dataframe with one column with labels and named 'Age category
        target = pd.DataFrame(data=labels, columns = ['Age category'])

        """
        #Classification with only one class
        #target = pd.DataFrame(data=np.array(['0']*len(self.Ages.values)).transpose(), columns = ['Age category'])
        """
        
        #Create dataframe from concatenation of two along x axis
        finalDf = pd.concat([principalDf, target], axis = 1)

        """
        #finalDf.index = np.arange(1, len(finalDf) + 1)
        """

        
        # Установить параметр для вывода всех строк
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)

        # Отображение данных на графике
        fig = plt.figure(figsize = (8,8))
        ax = fig.add_subplot(projection='3d') 
        ax.set_xlabel('Principal Component 1', fontsize = 15)
        ax.set_ylabel('Principal Component 2', fontsize = 15)
        ax.set_zlabel('Principal Component 3', fontsize = 15)
        ax.set_title('3 component PCA', fontsize = 20)

        """
        #targets = ['Iris-setosa', 'Iris-versicolor', 'Iris-virginica']
        #colors = ['r', 'g', 'b']
        """
        
        # Alphabeta of classes
        
        #targets = np.unique(labels)
        targets = set(labels)

        """
        #targets = [0, 1, 2, 3, 4]
        #colors = ['b', 'y','r','g','c']
        """
        
        # Взять из палитры len(targets) цветов.
        colors = plt.get_cmap('tab10', len(targets)).colors  # Используем палитру 'tab10'

        """
        #for class_ in targets:
        #    colors.append(wc.rgb_to_hex((int(255 * class_ / len (targets)), int(255 * class_ / len (targets)), int(255 * class_ / len (targets)))))
        """
        print(targets)


        for target, color in zip(targets,colors):
       
            # Select all indexes of humans with targeting classes
        
            indicesToKeep = finalDf['Age category'] == target
     
            ax.scatter(finalDf.loc[indicesToKeep, 'principal component 1']
                       , finalDf.loc[indicesToKeep, 'principal component 2']
                       , finalDf.loc[indicesToKeep, 'principal component 3']
                       , c = color
                       , s = 50)





            if (show_indexes):
                # Добавляем метки с номерами объектов рядом с точками
                for i in finalDf[indicesToKeep].index:
                    ax.text(finalDf.loc[i, 'principal component 1'],
                            finalDf.loc[i, 'principal component 2'],
                            finalDf.loc[i, 'principal component 3'],
                    str(i),  # Здесь str(i) будет выводить номер объекта (индекс)
                    fontsize=9, color='black')

            """
            if (show_ages):
                # Добавляем метки с возрастами объектов рядом с точками
                for i in finalDf[indicesToKeep].index:
                     ax.text(finalDf.loc[self.test_ages[i], 'principal component 1'],
                            finalDf.loc[self.test_ages[i], 'principal component 2'],
                            finalDf.loc[self.test_ages[i], 'principal component 3'],
                    str(i),  # Здесь str(i) будет выводить номер объекта (индекс)
                    fontsize=9, color='black')
            """

            """
            # Mark the center of each fuzzy cluster
            if centers is not None:
                
                for pt in centers:
                    pca_pt = self.pca(pt, 3)
                    ax.plot(pca_pt[0, 0], pca_pt[0, 1], pca_pt[0, 2], 'rs')
            
            """



        """
        for i, point in enumerate(features_set):
            # Определение цвета на основе принадлежности кластерам
            color = np.dot(u[i],
                           [[1, 0, 0], [0, 1, 0], [0, 0, 1]])  # RGB на основе степеней принадлежности
            ax.plot(point[0], point[1], marker='o', markersize=5, color=color)
        
        # Отображение центров кластеров
        ax.scatter(centers[:, 0], centers[:, 1], marker='x', s=100, c='black', label='Кластерные центры')
        plt.legend()
        """
                
        # Генерируем подписи для каждого класса с использованием list comprehension
        if len (targets) > 1:
            labels = [f'{target} class' for target in targets]
            ax.legend(labels)
       
            
        ax.grid()

        ax.set_xlim([finalDf['principal component 1'].min(), finalDf['principal component 1'].max()])
        ax.set_ylim([finalDf['principal component 2'].min(), finalDf['principal component 2'].max()])
        ax.set_zlim([finalDf['principal component 3'].min(), finalDf['principal component 3'].max()])

        plt.show()







    ###################################################################
    ###################################################################
    ###################################################################    

    def plot_pca_cumulative(self):
        # Principal component analisys for 3 components

        pca = PCA(n_components=len(features))
        principalComponents = pca.fit_transform(scaled_df)
        explained = pca.explained_variance_ratio_

        exp_var_pca = pca.explained_variance_ratio_
        #
        # Cumulative sum of eigenvalues; This will be used to create step plot
        # for visualizing the variance explained by each principal component.
        #
        cum_sum_eigenvalues = np.cumsum(exp_var_pca)

        plt.bar(range(1,len(exp_var_pca) + 1), exp_var_pca, alpha=0.5, align='center', label='Індивідуальна пояснена дисперсія')
        plt.step(range(1,len(cum_sum_eigenvalues) + 1), cum_sum_eigenvalues, where='mid',label='Кумулятивна пояснена дисперсія')
        plt.ylabel('Частка поясненої дисперсії')
        plt.xlabel('Індекс головної компоненти')
        plt.legend(loc='best')
        plt.tight_layout()
        plt.grid()
        plt.show()


    ####################################################################
    ####################################################################
    ####################################################################
        
    def kmeans_clustering_factory(self):
        """OK"""

        """Доробити алгоритм k-means"""

        data = self.train_features_set_scaled

        clasters_number = int(input("Enter clusters number: "))
        print("Clasters number: ", clasters_number)

        centers, labels = self.kmeans_clustering(data, clasters_number)

        """
        classes_number = len(set(labels))
        persons_number = len(labels)

        u = np.zeros((classes_number, persons_number))

        for i in range(len(labels)):
            u[labels[i]][i] = 1
        """


        indexes = self.clusters_patient_indexes(labels)
        clusters_bio_age = self.clusters_bio_age(self.train_ages, indexes)

        print(indexes)
        print(clusters_bio_age)

        self.plot_pca(data, labels, centers, show_ages=True)
        

    def kmeans_clustering(self, data, clusters_number):

        """ Kmeans clusterning

            input: clusters_number
                    features dataframe
            output: clusters_labels
            
        """
              
        #x = [4, 5, 10, 4, 3, 11, 14 , 6, 10, 12]
        #y = [21, 19, 24, 17, 16, 25, 24, 22, 21, 21]
        #data = list(zip(x, y))
         
        kmeans = KMeans(n_clusters=clusters_number, init='k-means++')
        kmeans.fit(data)


        return kmeans.cluster_centers_, kmeans.labels_

        #indexes = self.clusters_patient_indexes(kmeans.labels_)
        #self.clusters_bio_age(self.Ages, indexes)

        #plt.scatter(self.data['MCH'], self.df_male['MCHC'], c=kmeans.labels_)
        #plt.show()


    def elbow(self):
     
        from yellowbrick.cluster import KElbowVisualizer      

        # Instantiate the clustering model and visualizer
        km = KMeans(random_state=42, init='k-means++')
        visualizer = KElbowVisualizer(km, k=(2,10))
         
        visualizer.fit(self.train_features_set_scaled)        # Fit the data to the visualizer
        visualizer.show()        # Finalize and render the figure



   ##################################### K-means algorithm ###################################################

    def clusters_patient_indexes (self, labels):

        """ Find list of patient indexes for each cluster. """

        clusters_patient_indexes = {key: [] for key in dict.fromkeys(np.unique(labels))}

        for index, claster_number in enumerate(labels):

            clusters_patient_indexes[claster_number].append(index)

        return clusters_patient_indexes


    def clusters_bio_age(self, train_ages_dataframe, indexes_of_persons_in_clusters):
        
        """ Mean ariphmetic by each cluster bio age """
        
        clusters_bio_age = {}
        
        for cluster_number in indexes_of_persons_in_clusters.keys():

            summ = 0

            persons_indexes = indexes_of_persons_in_clusters[cluster_number]

            for person_index in persons_indexes:

                summ += train_ages_dataframe['Age'].values[person_index]

            summ = summ / len(persons_indexes)

            clusters_bio_age[cluster_number] = summ


        return clusters_bio_age
       
            
      


    ####################################################################
    ####################################################################
    ####################################################################


    def initialize_centers_kmeans_pp(self, data, num_clusters):
        centers = []
        centers.append(data[np.random.randint(0, len(data))])

        for _ in range(1, num_clusters):
            distances = np.array([min(np.linalg.norm(x - center) ** 2 for center in centers) for x in data])
            probabilities = distances / distances.sum()
            cumulative_probs = probabilities.cumsum()
            r = np.random.rand()

            for idx, prob in enumerate(cumulative_probs):
                if r < prob:
                    centers.append(data[idx])
                    break

        return np.array(centers)

    def calculate_initial_membership_matrix(self, X, centers, m):
        # Число точек данных и число кластеров
        n_samples = X.shape[0]
        n_clusters = centers.shape[0]

        # Вычисляем расстояния от каждой точки до каждого центра
        distances = cdist(centers, X)

        # Инициализируем матрицу принадлежности
        U = np.zeros((n_clusters, n_samples))

        # Заполняем матрицу принадлежности по формуле FCM
        for i in range(n_clusters):
            for j in range(n_samples):
                if distances[i, j] == 0:
                    # Если точка совпадает с центром кластера, принадлежит ему на 100%
                    U[:, j] = 0
                    U[i, j] = 1
                    break
                else:
                    # Стандартный расчет при ненулевом расстоянии
                    denominator = sum((distances[i, j] / distances[k, j]) ** (2 / (m - 1)) for k in range(n_clusters) if
                                      distances[k, j] != 0)
                    U[i, j] = 1 / denominator

        return U


    def cmeans_factory(self):

        data = self.train_features_set_scaled

        clasters_number = int(input("Enter clusters number: "))
        print("Clasters number:        ", clasters_number)

        # u - Степени принадлежности каждого объекта к каждому кластеру
        cntr, u = self.cmeans_clustering(data, clasters_number)

        self.plot_pca(data, u, cntr, show_indexes=False, show_ages=False)

        labels = np.argmax(u, axis=0)
        indexes = self.clusters_patient_indexes(labels)
        clusters_bio_age = self.clusters_bio_age_c_means(self.train_ages, indexes, u)

        print(indexes)
        print(clusters_bio_age)

    def clusters_bio_age_c_means(self, train_ages_dataframe, indexes_of_persons_in_clusters, u):

        """Mean ariphmetic by each cluster bio age """

        clusters_bio_age = {}

        for cluster_number in indexes_of_persons_in_clusters.keys():

            summ = 0

            persons_indexes = indexes_of_persons_in_clusters[cluster_number]

            for person_index in persons_indexes:
                summ += train_ages_dataframe['Age'].values[person_index] * u[cluster_number][person_index]

            summ = summ / np.sum(u[cluster_number])

            clusters_bio_age[cluster_number] = summ

        return clusters_bio_age

    def cmeans_clustering(self, data, clasters_number):


        
        x = [4, 5, 10, 4, 3, 11, 14 , 6, 10, 12]
        y = [21, 19, 24, 17, 16, 25, 24, 22, 21, 21]



        #data = list(zip(x, y))

        
        
        print(data)
        
        data = np.array(data)

        # Пример использования
        #data = np.random.rand(100, 2)  # Данные

        m = 3  # Параметр "размытия"

        # Initializing centers matrix by k-means++ method
        centers = self.initialize_centers_kmeans_pp(data, clasters_number)
        membership_matrix = self.calculate_initial_membership_matrix(data, centers, m)
        print(centers)
        # C-means clustering
        # m - fuzziness parameter
        cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(
        np.transpose(data), c=clasters_number, m=3, error=0.005, maxiter=1000, init=membership_matrix)
        


        # Assign pacients to clusters based on maximum membership,
        # Result: len(clusters) == pacients count, element at index in "clusters" == cluster number
        # All works correctly
        

        #print(clusters)
      
        # Plot assigned clusters

        """
        for j in range(classes_number):
             
            # : (двоеточие) — означает, что мы берем все строки (или весь диапазон данных по первой оси).
            plt.plot(data[:, 0][clusters == j], data[:, 1][clusters == j], 'o', label=f'cluster{j}')

        plt.legend()
        plt.show()
        """
        return cntr, u
        #plt.scatter(self.data['MCH'], self.data['MCHC'], c=kmeans.labels_)
        #plt.show()


    def minimal_spanning_tree_clustering(self):

        import seaborn as sns; sns.set()

        # matplotlib 1.4 + numpy 1.10 produces warnings; we'll filter these
        import warnings; warnings.filterwarnings('ignore', message='elementwise')

        def plot_mst(model, cmap='rainbow'):
           
            """Utility code to visualize a minimum spanning tree"""
            X = model.X_fit_
            fig, ax = plt.subplots(1, 2, figsize=(16, 6), sharex=True, sharey=True)
            for axi, full_graph, colors in zip(ax, [True, False], ['lightblue', model.labels_]):
                segments = model.get_graph_segments(full_graph=full_graph)
                print(segments)
                axi.plot(segments[0], segments[1], '-k', zorder=1, lw=1)
                axi.scatter(X[:, 0], X[:, 1], c=colors, cmap=cmap, zorder=2)
                axi.axis('tight')
                
            
            ax[0].set_title('Full Minimum Spanning Tree', size=16)
            ax[1].set_title('Trimmed Minimum Spanning Tree', size=16);
            plt.show()

        from sklearn.datasets import make_blobs
        
        #X, y = make_blobs(200, centers=4, random_state=42)
        #X, y = make_blobs(n_samples=200, centers=4, n_features=16 ,
        #          random_state=42)
        #self.plot_pca(0, [0])
        
        
        #plt.scatter(X[:, 0], X[:, 1], c='lightblue');
        #plt.show()

        from mst_clustering import MSTClustering
        model = MSTClustering(cutoff_scale=7, approximate=False)
        #labels = model.fit_predict(X)
        labels = model.fit_predict(self.train_features_set_scaled)
        
        #plt.scatter(X[:, 0], X[:, 1], c=labels, cmap='rainbow');
        #plt.show()

        #plot_mst(model)

        #print(labels)
        #self.plot_pca(len(np.unique(labels)), labels)
        #print(model.get_graph_segments(True))

        segments = model.get_graph_segments(True)
        
        def segments_from_features_space_to_pca (segments):
            
            start_points_list = []
            end_points_list = []
           
    
            for i in range(len(segments)):
                start_points_list.append(segments[i][0])
                end_points_list.append(segments[i][1])

            
            start_points = np.column_stack(start_points_list)  # Начальные точки рёбер
            end_points = np.column_stack(end_points_list)      # Конечные точки рёбер

            # Объединяем начало и конец рёбер для общей проекции
            all_points = np.vstack([start_points, end_points])  # Все точки для PCA

            # Применяем PCA для проекции из 16D в 3D
            pca = PCA(n_components=3)
            all_points_pca = pca.fit_transform(all_points)

            # Разделяем обратно на начальные и конечные точки рёбер в новом 3D-пространстве
            start_points_pca = all_points_pca[:len(start_points)]
            end_points_pca = all_points_pca[len(start_points):]

            return start_points_pca, end_points_pca

        start_points_pca, end_points_pca = segments_from_features_space_to_pca(segments)



        
      
        # Создаем 3D-график
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Проходим по всем сегментам и рисуем линии в 3D-пространстве PCA
        for i in range(len(start_points_pca)):
            x_start, y_start, z_start = start_points_pca[i]
            x_end, y_end, z_end = end_points_pca[i]
            
            # Рисуем ребро между начальной и конечной точкой сегмента
            ax.plot([x_start, x_end], [y_start, y_end], [z_start, z_end], 'k-', lw=1)

        # Добавляем точки для визуализации вершин
        ax.scatter(start_points_pca[:, 0], start_points_pca[:, 1], start_points_pca[:, 2], c='r', s=50)
        ax.scatter(end_points_pca[:, 0], end_points_pca[:, 1], end_points_pca[:, 2], c='b', s=50)

        # Настраиваем оси
        ax.set_xlabel('PCA Component 1')
        ax.set_ylabel('PCA Component 2')
        ax.set_zlabel('PCA Component 3')

        plt.show()

      

        
        # create some data with four clusters
        X, y = make_blobs(200, centers=4, random_state=42)
        
        # predict the labels with the MST algorithm
        model = MSTClustering(cutoff_scale=2)
        labels = model.fit_predict(X)
        print(labels)
        
        # plot the results
        plt.scatter(X[:, 0], X[:, 1], c=labels, cmap='rainbow')
        plt.show()
        
    def minimal_spanning_tree_clustering2(self):

        
        import seaborn as sns; sns.set()

        # matplotlib 1.4 + numpy 1.10 produces warnings; we'll filter these
        import warnings; warnings.filterwarnings('ignore', message='elementwise')

        """
        def plot_mst(model, cmap='rainbow'):
               
            #Utility code to visualize a minimum spanning tree
            X = model.X_fit_

             # Применяем PCA для проекции в пространство трех главных компонент
            pca = PCA(n_components=3)
            X_pca = pca.fit_transform(X)

             # Создаем 3D-график
            fig = plt.figure(figsize=(16, 8))
            ax1 = fig.add_subplot(121, projection='3d' )
            ax2 = fig.add_subplot(122, projection='3d')
    
            #fig, ax = plt.subplots(1, 2, figsize=(16, 6), sharex=True, sharey=True)
            for axi, full_graph, colors in zip([ax1, ax2], [True, False], ['lightblue', model.labels_]):
                segments = model.get_graph_segments(full_graph=full_graph)
                print(segments)
                #axi.plot(segments[0], segments[1], '-k', zorder=1, lw=1)
                #axi.scatter(X[:, 0], X[:, 1], c=colors, cmap=cmap, zorder=2)
                #axi.axis('tight')
                 # Для каждого сегмента рисуем линию в пространстве PCA
                for seg in segments:
                    p1 = X_pca[seg[0]]
                    p2 = X_pca[seg[1]]
                    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], '-k', zorder=1, lw=1)
        
                # Рисуем точки
                scatter = ax.scatter(X_pca[:, 0], X_pca[:, 1], X_pca[:, 2], c=colors, cmap=cmap, zorder=2)
                ax.set_title('Full MST' if full_graph else 'Trimmed MST', size=16)
                    
                #ax[0].set_title('Full Minimum Spanning Tree', size=16)
                #ax[1].set_title('Trimmed Minimum Spanning Tree', size=16);
            plt.show()
        """
        from sklearn.datasets import make_blobs
        
        #X, y = make_blobs(200, centers=4, random_state=42)

        #self.plot_pca(0, [0])
        
        
        #plt.scatter(X[:, 0], X[:, 1], c='lightblue');
        #plt.show()

        from mst_clustering import MSTClustering
        model = MSTClustering(cutoff_scale=2, approximate=False)
        #labels = model.fit_predict(X)
        labels = model.fit_predict(self.train_features_set_scaled)
        #plt.scatter(X[:, 0], X[:, 1], c=labels, cmap='rainbow');
        #plt.show()

        #plot_mst(model)

        #print(labels)
        #print(model.get_graph_segments(True))
        #self.plot_pca(len(np.unique(labels)), labels)

        # Допустим, segments содержит две строки — начало и конец рёбер в 16D пространстве:
        # segments[0] — это координаты начала рёбер, segments[1] — координаты конца рёбер
        start_points_list = []
        end_points_list = []
        segments = model.model.get_graph_segments(True)
        print(len(segments))
        for i in len(segments):
            start_points_list.append(segments[i][0])
            end_points_list.append(segments[i][1])

        
        start_points = np.column_stack(start_points_list)  # Начальные точки рёбер
        end_points = np.column_stack(end_points_list)      # Конечные точки рёбер

        # Объединяем начало и конец рёбер для общей проекции
        all_points = np.vstack([start_points, end_points])  # Все точки для PCA

        # Применяем PCA для проекции из 16D в 3D
        pca = PCA(n_components=3)
        all_points_pca = pca.fit_transform(all_points)

        # Разделяем обратно на начальные и конечные точки рёбер в новом 3D-пространстве
        start_points_pca = all_points_pca[:len(start_points)]
        end_points_pca = all_points_pca[len(start_points):]



        # Создаем 3D-график
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Проходим по всем сегментам и рисуем линии в 3D-пространстве PCA
        for i in range(len(start_points_pca)):
            x_start, y_start, z_start = start_points_pca[i]
            x_end, y_end, z_end = end_points_pca[i]
            
            # Рисуем ребро между начальной и конечной точкой сегмента
            ax.plot([x_start, x_end], [y_start, y_end], [z_start, z_end], 'k-', lw=1)

        # Добавляем точки для визуализации вершин
        ax.scatter(start_points_pca[:, 0], start_points_pca[:, 1], start_points_pca[:, 2], c='r', s=50)
        ax.scatter(end_points_pca[:, 0], end_points_pca[:, 1], end_points_pca[:, 2], c='b', s=50)

        # Настраиваем оси
        ax.set_xlabel('PCA Component 1')
        ax.set_ylabel('PCA Component 2')
        ax.set_zlabel('PCA Component 3')

        plt.show()
            
    
if __name__ == '__main__':
    """
    import matplotlib.pyplot as plt

    x = [4, 5, 10, 4, 3, 11, 14 , 6, 10, 12]
    y = [21, 19, 24, 17, 16, 25, 24, 22, 21, 21]

    plt.scatter(x, y)
    plt.show()

    

    data = list(zip(x, y))
    inertias = []

    for i in range(1,11):
        kmeans = KMeans(n_clusters=i)
        kmeans.fit(data)
        inertias.append(kmeans.inertia_)

    plt.plot(range(1,11), inertias, marker='o')
    plt.title('Elbow method')
    plt.xlabel('Number of clusters')
    plt.ylabel('Inertia')
    plt.show()
    """
    

    ClAnalysis = ClusterAnalysis(r'datasets/gemogramma_filled_empty_by_polynomial_method_3.xlsx', 'Male')
    ClAnalysis.ages_distribution()
  
    ClAnalysis.scale()
    ClAnalysis.plot_pca(ClAnalysis.train_features_set_scaled)
    #ClAnalysis.elbow()
    ClAnalysis.kmeans_clustering_factory()
    ClAnalysis.cmeans_factory()



    #print(ClAnalysis.train_features_set_scaled)
    ClAnalysis.minimal_spanning_tree_clustering()
  
    #ClAnalysis.kmeans_clustering()
    
    #ClAnalysis.biological_age((24.1, 391, 78, 9.7, 14.4, 15.7, 0.45, 149, 66.4,	5.13, 8, 29.9, 3.7, 0.218, 226, 5))









    
"""from sklearn import datasets
wine_data = datasets.load_wine(as_frame=True)"""
#

"""
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"

# load dataset into Pandas DataFrame
df = pd.read_csv(url, names=['sepal length','sepal width','petal length','petal width','target'])"""

#Dataset





 












"""
df = wine_data.data
print(df)

print(df.shape)
print(df.info())


X = np.array([[0,0],
              [1,1],
              [2,2],
              [3,3],
              [4,4]])





print(std_scaler.mean_)
print(std_scaler.transform(X))

print(scaled_df)
"""

