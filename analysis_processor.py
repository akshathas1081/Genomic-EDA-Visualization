import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import os


def process_file(file_path, output_dir):
    try:
        df = pd.read_csv(file_path, sep="\t", comment="!", low_memory=False)
        print("Dataset loaded successfully!")
    except Exception as e:
        raise Exception(f"Error loading dataset: {e}")

    # Drop missing and duplicate rows
    df = df.dropna()
    df = df.drop_duplicates()

    # Select numeric columns
    numeric_columns = df.select_dtypes(include=["float64", "int64"]).columns
    df_numeric = df[numeric_columns]

    # Standardize
    scaler = StandardScaler()
    df_scaled = pd.DataFrame(scaler.fit_transform(df_numeric), columns=numeric_columns)

    # PCA
    pca = PCA(n_components=2)
    principal_components = pca.fit_transform(df_scaled)
    pca_df = pd.DataFrame(principal_components, columns=["PC1", "PC2"])

    # PCA Scatter Plot
    pca_plot_path = os.path.join(output_dir, "pca_scatter.png")
    plt.figure(figsize=(10, 7))
    sns.scatterplot(x="PC1", y="PC2", data=pca_df, alpha=0.7)
    plt.title("PCA Visualization (Top 2 Principal Components)")
    plt.xlabel("Principal Component 1")
    plt.ylabel("Principal Component 2")
    plt.savefig(pca_plot_path)
    plt.close()

    # Correlation Heatmap
    heatmap_path = os.path.join(output_dir, "correlation_heatmap.png")
    plt.figure(figsize=(12, 10))
    sns.heatmap(df_numeric.corr(), annot=False, cmap="coolwarm")
    plt.title("Correlation Heatmap of Numeric Features")
    plt.tight_layout()
    plt.savefig(heatmap_path)
    plt.close()

    # Numeric Summary
    summary_df = df_numeric.describe().transpose()
    summary_html = summary_df.to_html(classes="table table-sm table-bordered", border=0)

    # Save processed CSV
    processed_file_path = os.path.join(output_dir, "processed_dataset.csv")
    df.to_csv(processed_file_path, index=False)

    return (
        numeric_columns,
        pca_df,
        summary_html,
        pca_plot_path,
        heatmap_path,
        processed_file_path,
    )
