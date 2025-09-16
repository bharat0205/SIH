# utils/data_loader.py

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_dummy_data(num_records=500): # Increased record count
    """
    Generates a Pandas DataFrame with dummy compliance data to simulate the AI backend.
    """
    platforms = ["Amazon.in", "Flipkart", "Myntra", "Ajio", "Meesho", "Tata CLiQ"]
    violation_types = [
        "MRP Declaration Missing",
        "Country of Origin Missing",
        "Incorrect Net Quantity",
        "Manufacturer Details Missing",
        "No Customer Care Info",
        "Compliant"
    ]
    products = {
        "Electronics": ["Smartphone", "Laptop", "Headphones", "Smartwatch"],
        "Apparel": ["T-Shirt", "Jeans", "Jacket", "Sneakers"],
        "Groceries": ["Organic Honey", "Basmati Rice", "Olive Oil", "Almonds"]
    }
    brands = ["BrandA", "BrandB", "BrandC", "BrandD", "BrandE"]

    data = []
    for i in range(num_records):
        category = np.random.choice(list(products.keys()))
        product_name = np.random.choice(products[category])
        platform = np.random.choice(platforms)
        violation = np.random.choice(violation_types, p=[0.2, 0.2, 0.15, 0.15, 0.1, 0.2])
        
        data.append({
            "id": 1000 + i,
            "product_name": f"{product_name} ({category})",
            "brand": np.random.choice(brands),
            "platform": platform,
            # Generate data over a wider time range for the trend chart
            "timestamp": datetime.now() - timedelta(days=np.random.randint(0, 30), hours=np.random.randint(0, 24)),
            "violation_type": violation if violation != "Compliant" else None,
            "is_compliant": violation == "Compliant",
            "severity": "Critical" if violation in ["MRP Declaration Missing", "Country of Origin Missing"] else "High" if violation is not None else "None",
            "product_url": f"https://www.{platform.lower().split('.')[0]}.com/product/{1000+i}",
            "image_url": f"https://picsum.photos/seed/{1000+i}/400/200"
        })
    return pd.DataFrame(data).sort_values(by="timestamp", ascending=False)
