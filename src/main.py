import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
import os
from pathlib import Path

def generate_dummy_data(num_samples=200):
    """Gera dados fictícios para demonstração."""
    data = {
        'CustomerID': range(1, num_samples + 1),
        'Age': np.random.randint(18, 70, num_samples),
        'AnnualIncome (k$)': np.random.randint(15, 120, num_samples),
        'SpendingScore (1-100)': np.random.randint(1, 100, num_samples)
    }
    return pd.DataFrame(data)

def perform_segmentation(df, output_dir=None):
    """Realiza a segmentação de clientes usando K-Means."""
    # Define output directory for plots
    if output_dir is None:
        # Get the project root directory (parent of src)
        current_dir = Path(__file__).parent
        project_root = current_dir.parent
        output_dir = project_root / 'docs' / 'images'
    else:
        output_dir = Path(output_dir)
    
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    
    X = df[['AnnualIncome (k$)', 'SpendingScore (1-100)']]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    wcss = []
    for i in range(1, 11):
        kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42, n_init=10)
        kmeans.fit(X_scaled)
        wcss.append(kmeans.inertia_)

    plt.figure(figsize=(10, 6))
    plt.plot(range(1, 11), wcss, marker='o', linestyle='--')
    plt.title('Elbow Method for K-Means')
    plt.xlabel('Number of Clusters')
    plt.ylabel('WCSS')
    plt.savefig(output_dir / "elbow_method.png")
    plt.close()

    n_clusters = 5
    kmeans = KMeans(n_clusters=n_clusters, init='k-means++', random_state=42, n_init=10)
    df['Cluster'] = kmeans.fit_predict(X_scaled)

    plt.figure(figsize=(10, 8))
    sns.scatterplot(x='AnnualIncome (k$)', y='SpendingScore (1-100)', hue='Cluster', data=df, palette='viridis', s=100, alpha=0.8)
    plt.title('Customer Segmentation by Annual Income and Spending Score')
    plt.xlabel("Annual Income (k$)")
    plt.ylabel("Spending Score (1-100)")
    plt.legend(title="Cluster")
    plt.savefig(output_dir / "customer_segments.png")
    plt.close()
    return df

if __name__ == "__main__":
    # Get the project root directory
    current_dir = Path(__file__).parent
    project_root = current_dir.parent
    data_dir = project_root / 'data'
    
    # Ensure data directory exists
    data_dir.mkdir(parents=True, exist_ok=True)
    
    print("Generating dummy data...")
    customer_data = generate_dummy_data(200)
    customer_data.to_csv(data_dir / 'customer_data.csv', index=False)
    print(f"Dummy data generated and saved to {data_dir / 'customer_data.csv'}")

    print("Performing customer segmentation...")
    segmented_customers = perform_segmentation(customer_data.copy())
    segmented_customers.to_csv(data_dir / 'segmented_customer_data.csv', index=False)
    print(f"Segmentation complete and results saved to {data_dir / 'segmented_customer_data.csv'}")
    print("Plots saved to docs/images/elbow_method.png and docs/images/customer_segments.png")

    print("\nFirst 5 rows of segmented data:")
    print(segmented_customers.head())

