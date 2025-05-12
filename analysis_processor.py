import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import os


def process_file(file_path, output_dir):
    try:
        # Load the dataset
        df = pd.read_csv(file_path, sep="\t", comment="!", low_memory=False)
        print("Dataset loaded successfully!")
    except Exception as e:
        raise Exception(f"Error loading dataset: {e}")

    # Drop missing values and duplicates
    df = df.dropna()
    df = df.drop_duplicates()

    # Select only numeric columns
    numeric_columns = df.select_dtypes(include=["float64", "int64"]).columns

    # Standardize numeric columns
    scaler = StandardScaler()
    df[numeric_columns] = scaler.fit_transform(df[numeric_columns])

    # Perform PCA
    pca = PCA(n_components=2)
    principal_components = pca.fit_transform(df[numeric_columns])
    pca_df = pd.DataFrame(data=principal_components, columns=["PC1", "PC2"])

    # Save a scatter plot of PCA results
    plot_path = os.path.join(output_dir, "pca_scatter.png")
    plt.figure(figsize=(10, 7))
    sns.scatterplot(x="PC1", y="PC2", data=pca_df, alpha=0.7)
    plt.title("PCA Visualization (Top 2 Principal Components)")
    plt.xlabel("Principal Component 1")
    plt.ylabel("Principal Component 2")
    plt.savefig(plot_path)
    plt.close()

    # Save cleaned dataset
    processed_file_path = os.path.join(output_dir, "processed_dataset.csv")
    df.to_csv(processed_file_path, index=False)

    return numeric_columns, pca_df, plot_path, processed_file_path
