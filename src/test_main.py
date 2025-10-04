import unittest
import pandas as pd
from main import generate_dummy_data, perform_segmentation

class TestCustomerSegmentation(unittest.TestCase):

    def test_generate_dummy_data(self):
        df = generate_dummy_data(num_samples=10)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 10)
        self.assertIn("CustomerID", df.columns)
        self.assertIn("Age", df.columns)
        self.assertIn("AnnualIncome (k$)", df.columns)
        self.assertIn("SpendingScore (1-100)", df.columns)

    def test_perform_segmentation(self):
        df = generate_dummy_data(num_samples=50)
        segmented_df = perform_segmentation(df.copy())
        self.assertIsInstance(segmented_df, pd.DataFrame)
        self.assertIn("Cluster", segmented_df.columns)
        self.assertEqual(len(segmented_df), 50)
        # Check if the cluster column has values (i.e., segmentation was performed)
        self.assertTrue(segmented_df["Cluster"].nunique() > 0)

if __name__ == "__main__":
    unittest.main()

