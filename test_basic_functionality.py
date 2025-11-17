"""
Basic functionality test for Synthcity
Testing the core features as shown in the README
"""

# Test 1: List available generators
print("=" * 60)
print("Test 1: Listing available generators")
print("=" * 60)
from synthcity.plugins import Plugins

try:
    plugins_list = Plugins(categories=["generic", "privacy"]).list()
    print(f"Available plugins: {plugins_list}")
    print("✓ Test 1 PASSED: Successfully listed generators\n")
except Exception as e:
    print(f"✗ Test 1 FAILED: {e}\n")

# Test 2: Load and train a simple model
print("=" * 60)
print("Test 2: Training a simple synthetic data generator")
print("=" * 60)
try:
    from sklearn.datasets import load_diabetes

    X, y = load_diabetes(return_X_y=True, as_frame=True)
    X["target"] = y

    print(f"Dataset shape: {X.shape}")
    print(f"Dataset columns: {list(X.columns)}")

    # Use a simple generator with minimal training
    syn_model = Plugins().get("dummy_sampler")
    print(f"Using generator: {syn_model.name()}")

    syn_model.fit(X)
    print("✓ Model training completed")

    # Generate synthetic data
    synthetic_data = syn_model.generate(count=10)
    print(f"Generated synthetic data shape: {synthetic_data.dataframe().shape}")
    print("✓ Test 2 PASSED: Successfully trained and generated data\n")
except Exception as e:
    print(f"✗ Test 2 FAILED: {e}\n")
    import traceback
    traceback.print_exc()

# Test 3: Test serialization
print("=" * 60)
print("Test 3: Testing model serialization")
print("=" * 60)
try:
    from synthcity.utils.serialization import save, load

    syn_model = Plugins().get("dummy_sampler")

    buff = save(syn_model)
    reloaded = load(buff)

    assert syn_model.name() == reloaded.name()
    print(f"Original model: {syn_model.name()}")
    print(f"Reloaded model: {reloaded.name()}")
    print("✓ Test 3 PASSED: Serialization works correctly\n")
except Exception as e:
    print(f"✗ Test 3 FAILED: {e}\n")

print("=" * 60)
print("Basic functionality tests completed!")
print("=" * 60)
