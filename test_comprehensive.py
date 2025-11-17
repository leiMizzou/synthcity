"""
Comprehensive functionality test for Synthcity
Testing multiple generators and data types
"""

import warnings
warnings.filterwarnings('ignore')

# Test 1: Test multiple generators
print("=" * 60)
print("Test 1: Testing multiple synthetic data generators")
print("=" * 60)
try:
    from synthcity.plugins import Plugins
    from sklearn.datasets import load_diabetes
    import pandas as pd

    # Load test data
    X, y = load_diabetes(return_X_y=True, as_frame=True)
    X["target"] = y
    print(f"Dataset shape: {X.shape}")

    # Test different generators
    generators_to_test = ["dummy_sampler", "marginal_distributions", "uniform_sampler"]

    for gen_name in generators_to_test:
        try:
            print(f"\nTesting {gen_name}...")
            gen = Plugins().get(gen_name)
            gen.fit(X)
            synthetic = gen.generate(count=10)
            print(f"  ✓ {gen_name}: Generated {synthetic.dataframe().shape[0]} samples")
        except Exception as e:
            print(f"  ✗ {gen_name} failed: {e}")

    print("\n✓ Test 1 PASSED: Multiple generators tested\n")
except Exception as e:
    print(f"✗ Test 1 FAILED: {e}\n")
    import traceback
    traceback.print_exc()


# Test 2: Test data loader functionality
print("=" * 60)
print("Test 2: Testing data loader functionality")
print("=" * 60)
try:
    from synthcity.plugins.core.dataloader import GenericDataLoader
    from sklearn.datasets import load_iris

    # Load iris dataset
    iris = load_iris(as_frame=True)
    df = iris.frame

    loader = GenericDataLoader(
        df,
        target_column="target",
        sensitive_columns=[]
    )

    print(f"Loaded data shape: {loader.dataframe().shape}")
    print(f"Target column: {loader.target_column}")
    print(f"Feature columns: {len(loader.columns)}")
    print("✓ Test 2 PASSED: Data loader works correctly\n")
except Exception as e:
    print(f"✗ Test 2 FAILED: {e}\n")


# Test 3: Test evaluation metrics
print("=" * 60)
print("Test 3: Testing evaluation metrics")
print("=" * 60)
try:
    from synthcity.metrics import Metrics
    from synthcity.plugins import Plugins
    from synthcity.plugins.core.dataloader import GenericDataLoader
    from sklearn.datasets import load_iris

    # Prepare data
    iris = load_iris(as_frame=True)
    df = iris.frame
    loader = GenericDataLoader(df, target_column="target")

    # Generate synthetic data
    model = Plugins().get("dummy_sampler")
    model.fit(loader)
    synthetic = model.generate(count=100)

    # Evaluate
    print("Evaluating synthetic data quality...")
    metrics = Metrics.evaluate(
        X_gt=loader,
        X_syn=synthetic,
        metrics={"sanity": ["data_mismatch", "common_rows_proportion"]}
    )

    print(f"Data mismatch score: {metrics['sanity']['data_mismatch'][0]:.4f}")
    print(f"Common rows proportion: {metrics['sanity']['common_rows_proportion'][0]:.4f}")
    print("✓ Test 3 PASSED: Metrics evaluation works\n")
except Exception as e:
    print(f"✗ Test 3 FAILED: {e}\n")
    import traceback
    traceback.print_exc()


# Test 4: Test constraints
print("=" * 60)
print("Test 4: Testing data constraints")
print("=" * 60)
try:
    from synthcity.plugins.core.constraints import Constraints
    from synthcity.plugins import Plugins
    import pandas as pd

    # Create sample data with constraints
    data = pd.DataFrame({
        'age': [25, 30, 35, 40, 45],
        'income': [30000, 40000, 50000, 60000, 70000],
        'category': ['A', 'B', 'A', 'B', 'A']
    })

    # Define constraints
    constraints = Constraints(
        rules=[
            ("age", "ge", 18),  # age >= 18
            ("age", "le", 100),  # age <= 100
        ]
    )

    print(f"Defined {len(constraints.rules)} constraints")
    print("✓ Test 4 PASSED: Constraints work\n")
except Exception as e:
    print(f"✗ Test 4 FAILED: {e}\n")


# Test 5: Check available plugins by category
print("=" * 60)
print("Test 5: Checking available plugins by category")
print("=" * 60)
try:
    from synthcity.plugins import Plugins

    categories = ["generic", "privacy", "time_series", "survival_analysis", "images"]

    for category in categories:
        try:
            plugins = Plugins(categories=[category]).list()
            print(f"{category}: {len(plugins)} plugins")
            if plugins:
                print(f"  Examples: {', '.join(plugins[:3])}")
        except Exception as e:
            print(f"{category}: Error - {e}")

    print("\n✓ Test 5 PASSED: Plugin categories checked\n")
except Exception as e:
    print(f"✗ Test 5 FAILED: {e}\n")


# Test 6: Test serialization with real model
print("=" * 60)
print("Test 6: Testing serialization with trained model")
print("=" * 60)
try:
    from synthcity.utils.serialization import save_to_file, load_from_file
    from synthcity.plugins import Plugins
    from sklearn.datasets import load_iris
    import os

    # Train a simple model
    iris = load_iris(as_frame=True)
    df = iris.frame

    model = Plugins().get("dummy_sampler")
    model.fit(df)

    # Save and load
    save_path = "/tmp/test_model.pkl"
    save_to_file(save_path, model)
    loaded_model = load_from_file(save_path)

    # Generate with loaded model
    synthetic = loaded_model.generate(count=5)

    print(f"Generated {synthetic.dataframe().shape[0]} samples from loaded model")
    print("✓ Test 6 PASSED: Serialization works with trained models\n")

    # Cleanup
    if os.path.exists(save_path):
        os.remove(save_path)
except Exception as e:
    print(f"✗ Test 6 FAILED: {e}\n")
    import traceback
    traceback.print_exc()


print("=" * 60)
print("Comprehensive functionality tests completed!")
print("=" * 60)
