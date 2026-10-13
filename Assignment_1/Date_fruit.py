import numpy
import plotly.express as px
import pandas

# Fetching Dataset and making the dataframe
Date_dataset_main = pandas.read_excel("Assignment_1/Date_fruit_dataset/Date_Fruit_Datasets/Date_Fruit_Datasets.xlsx")
Date_dataset = Date_dataset_main.iloc[:, lambda Date_dataset: [0,1,2,-1]]

# Converting to numpy array
Date_features = Date_dataset.iloc[:,:3].to_numpy()
Labels, Date_class = pandas.factorize(Date_dataset.iloc[:, 3])
Dataset = numpy.column_stack((Date_features, Labels.reshape(-1, 1)))
Date_class = list(Date_class)

# 2D Plot
Figure_2D = px.scatter(Date_dataset,
                       x = "AREA",
                       y = "PERIMETER",
                       color = "Class",
                       symbol = "Class")
Figure_2D.show()

# 3D Plot
Figure_3D = px.scatter_3d(Date_dataset,
                          x = "AREA",
                          y = "PERIMETER",
                          z = "MAJOR_AXIS",
                          color = "Class",
                          symbol = "Class")
Figure_3D.show()

# Getting mean values for each class of dates
Mean_data_list = []
for Class in Date_class:
    Queried_dataset = Date_dataset.query("Class == @Class")
    Mean_data_list.append({
        "AREA": Queried_dataset["AREA"].mean(),
        "PERIMETER": Queried_dataset["PERIMETER"].mean(),
        "MAJOR_AXIS": Queried_dataset["MAJOR_AXIS"].mean(),
        "Class": Class
    })
Mean_dataset = pandas.DataFrame(data = Mean_data_list)


# Making the 2D mean plot and adding its traces to the original 2D plot
Figure_2D_mean_plot = px.scatter(Mean_dataset,
                                 x = "AREA",
                                 y = "PERIMETER",
                                 color = "Class",
                                 symbol = "Class",
                                 )
Figure_2D_mean_plot.update_traces(marker=dict(size=20))

for trace in Figure_2D_mean_plot.data:
    Figure_2D.add_trace(trace)

Figure_2D.show()

# Making the 3D mean plot and adding its traces to the original 3D plot
Figure_3D_mean_plot = px.scatter_3d(Mean_dataset,
                                    x = "AREA",
                                    y = "PERIMETER",
                                    z = "MAJOR_AXIS",
                                    color = "Class",
                                    symbol = "Class",
                                    )
Figure_3D_mean_plot.update_traces(marker=dict(size=20))

for trace in Figure_3D_mean_plot.data:
    Figure_3D.add_trace(trace)

Figure_3D.show()

# Histogram plots for each dimention
for column in ["AREA", "PERIMETER", "MAJOR_AXIS"]:
    Figure_histogram = px.histogram(
        Date_dataset, 
        x = column, 
        title = f"Histogram for {column}"
    )
    Figure_histogram.show()

# Vectorized calculation using linear algebra (Formula: sqrt(sum((x - mean)^2) / (N - 1)))
N = Date_features.shape[0]
Date_features_mean_vector = numpy.mean(Date_features, axis = 0)
Standard_deviation = numpy.sqrt(numpy.sum((Date_features - Date_features_mean_vector) ** 2, axis=0) / (N - 1))
print(Standard_deviation)

# Normalizing the first three dimensions before box plotting otherwise AREA skews the result immensly
Date_dataset_normalized = Date_dataset.copy()
for column in ["AREA", "PERIMETER", "MAJOR_AXIS"]:
    min_val = Date_dataset_normalized[column].min()
    max_val = Date_dataset_normalized[column].max()
    Date_dataset_normalized[column] = (Date_dataset_normalized[column] - min_val) / (max_val - min_val)

# Melting the dataset, turing it into 5 columns [Class, Dimension(AREA/PERIMETER/MAJOR_AXIS), Value(Dimension)]
Date_dataset_melted = pandas.melt(
    Date_dataset_normalized, 
    id_vars = ["Class"], 
    value_vars = ["AREA", "PERIMETER", "MAJOR_AXIS"], 
    var_name = "Dimension", 
    value_name = "Normalized_Value"
)

# Creating the box plot, with x axis as the Dimension(AREA/PERIMETER/MAJOR_AXIS), and y axis as their values
Figure_Box_All = px.box(
    Date_dataset_melted, 
    x = "Dimension", 
    y = "Normalized_Value", 
    title = "Box Plots for First Three Dimensions"
)
Figure_Box_All.show()

# Creating the box plot for each of the Dimensions over Classes of Date
for column in ["AREA", "PERIMETER", "MAJOR_AXIS"]:
    Figure_Box_Class = px.box(
        Date_dataset,
        x = "Class",
        y = column,
        color = "Class",
        title = f"Box Plots for {column} Across Classes"
    )
    Figure_Box_Class.show()



# Date_dataset used, 3 value columns with color and symbol depending on Class
Figure_Matrix = px.scatter_matrix(
    Date_dataset,
    dimensions = ["AREA", "PERIMETER", "MAJOR_AXIS"],
    color = "Class",
    symbol = "Class",
    title="3x3 Scatter Matrix for First Three Dimensions (Unnormalized)"
)
Figure_Matrix.show()

# Creating the 7D date dataset
Date_dataset_7D = Date_dataset_main.iloc[:, lambda Date_dataset: [0,1,2,3,4,5,6,7,-1]]
Column_names = list(Date_dataset_7D.columns)

# Normalizing the dimensions before plotting otherwise AREA skews the result immensly
Date_dataset_normalized_7D = Date_dataset_7D.copy()
for column in Column_names[0:8]:
    min_val = Date_dataset_normalized_7D[column].min()
    max_val = Date_dataset_normalized_7D[column].max()
    Date_dataset_normalized_7D[column] = (Date_dataset_normalized_7D[column] - min_val) / (max_val - min_val)

# Melting the dataset
Date_dataset_melted_7D = pandas.melt(
    Date_dataset_normalized_7D, 
    id_vars = ["Class"], 
    value_vars = Column_names[0:8],
    var_name = "Dimension", 
    value_name = "Value"
)

# Circular segment plot
Figure_Polar = px.scatter_polar(
    Date_dataset_melted_7D,
    r = "Value",
    theta = "Dimension",
    color = "Class",
    symbol = "Class",
    title = "Circle Segment Representation"
)
Figure_Polar.show()

# Parallel Figure
Date_dataset_normalized_7D["Class_numeric"], unique_classes = pandas.factorize(Date_dataset_normalized_7D["Class"])
Figure_parallel = px.parallel_coordinates(
    Date_dataset_normalized_7D,
    dimensions = Column_names,
    color = "Class_numeric",
)
Figure_parallel.show()