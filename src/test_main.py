import unittest
import pandas as pd
import numpy as np
import os
import tempfile
from pathlib import Path
from main import generate_dummy_data, perform_segmentation

class TestCustomerSegmentation(unittest.TestCase):

    def test_generate_dummy_data(self):
        """Test that dummy data is generated correctly."""
        df = generate_dummy_data(num_samples=10)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 10)
        self.assertIn("CustomerID", df.columns)
        self.assertIn("Age", df.columns)
        self.assertIn("AnnualIncome (k$)", df.columns)
        self.assertIn("SpendingScore (1-100)", df.columns)
        
    def test_generate_dummy_data_ranges(self):
        """Test that generated data is within expected ranges."""
        df = generate_dummy_data(num_samples=100)
        # Check Age range
        self.assertTrue(df['Age'].min() >= 18)
        self.assertTrue(df['Age'].max() <= 70)
        # Check Income range
        self.assertTrue(df['AnnualIncome (k$)'].min() >= 15)
        self.assertTrue(df['AnnualIncome (k$)'].max() <= 120)
        # Check SpendingScore range
        self.assertTrue(df['SpendingScore (1-100)'].min() >= 1)
        self.assertTrue(df['SpendingScore (1-100)'].max() <= 100)
        # Check CustomerID is sequential
        self.assertEqual(list(df['CustomerID']), list(range(1, 101)))

    def test_perform_segmentation(self):
        """Test that segmentation is performed correctly."""
        # Use temporary directory for test outputs
        with tempfile.TemporaryDirectory() as tmpdir:
            df = generate_dummy_data(num_samples=50)
            segmented_df = perform_segmentation(df.copy(), output_dir=tmpdir)
            
            self.assertIsInstance(segmented_df, pd.DataFrame)
            self.assertIn("Cluster", segmented_df.columns)
            self.assertEqual(len(segmented_df), 50)
            # Check if the cluster column has values (i.e., segmentation was performed)
            self.assertTrue(segmented_df["Cluster"].nunique() > 0)
            # Check that cluster labels are in expected range (0-4 for 5 clusters)
            self.assertTrue(segmented_df["Cluster"].min() >= 0)
            self.assertTrue(segmented_df["Cluster"].max() <= 4)
            
            # Check that plots were created
            elbow_plot = Path(tmpdir) / "elbow_method.png"
            segments_plot = Path(tmpdir) / "customer_segments.png"
            self.assertTrue(elbow_plot.exists(), "Elbow method plot should be created")
            self.assertTrue(segments_plot.exists(), "Customer segments plot should be created")
    
    def test_perform_segmentation_output_consistency(self):
        """Test that segmentation produces consistent results with same random state."""
        np.random.seed(42)
        df1 = generate_dummy_data(num_samples=50)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            segmented_df1 = perform_segmentation(df1.copy(), output_dir=tmpdir)
            
            # Reset seed and regenerate with same data
            np.random.seed(42)
            df2 = generate_dummy_data(num_samples=50)
            segmented_df2 = perform_segmentation(df2.copy(), output_dir=tmpdir)
            
            # Results should be identical
            pd.testing.assert_frame_equal(segmented_df1, segmented_df2)

if __name__ == "__main__":
    unittest.main()

