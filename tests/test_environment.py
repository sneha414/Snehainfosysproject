"""
============================================================================
ENVIRONMENT TEST SUITE
============================================================================
This file tests that Dask and Ray are installed and working correctly.
It verifies your development environment is set up properly.

What gets tested:
1. Can we import Dask and Ray?
2. Can we read our YAML schema files?
3. Can Dask process data?
4. Can Ray monitor data?
5. Can they work together?
"""

import pytest # pyright: ignore[reportMissingImports]
import sys
import os

# ----------------------------------------------------------------------------
# TEST 1: DASK IMPORT
# ----------------------------------------------------------------------------
def test_dask_import():
    """
    TEST: Can we import Dask?
    PURPOSE: Verifies Dask is installed correctly
    SUCCESS: Prints Dask version number
    FAILURE: Shows error message if Dask is missing
    """
    try:
        # Try to import Dask and its dataframe module
        import dask
        import dask.dataframe as dd
        
        # If import succeeds, print version
        print(f"✓ Dask version: {dask.__version__}")
        
        # Test passes
        assert True
        
    except ImportError as e:
        # If import fails, test fails with error message
        pytest.fail(f"❌ Failed to import Dask: {e}")


# ----------------------------------------------------------------------------
# TEST 2: RAY IMPORT
# ----------------------------------------------------------------------------
def test_ray_import():
    """
    TEST: Can we import Ray?
    PURPOSE: Verifies Ray is installed correctly
    SUCCESS: Prints Ray version number
    FAILURE: Shows error if Ray is missing
    """
    try:
        # Try to import Ray
        import ray # pyright: ignore[reportMissingImports]
        
        # If successful, print version
        print(f"✓ Ray version: {ray.__version__}")
        
        # Test passes
        assert True
        
    except ImportError as e:
        # If fails, show error
        pytest.fail(f"❌ Failed to import Ray: {e}")


# ----------------------------------------------------------------------------
# TEST 3: YAML IMPORT
# ----------------------------------------------------------------------------
def test_yaml_import():
    """
    TEST: Can we import PyYAML?
    PURPOSE: We need this to read our schema files
    SUCCESS: Confirms PyYAML is installed
    FAILURE: Shows error if missing
    """
    try:
        # Try to import yaml module
        import yaml
        
        print(f"✓ PyYAML is installed")
        
        # Test passes
        assert True
        
    except ImportError as e:
        pytest.fail(f"❌ Failed to import PyYAML: {e}")


# ----------------------------------------------------------------------------
# TEST 4: READ LOG SCHEMA
# ----------------------------------------------------------------------------
def test_read_log_schema():
    """
    TEST: Can we read our log schema file?
    PURPOSE: Verifies the YAML file is valid and properly formatted
    CHECKS:
      1. File exists
      2. Valid YAML syntax
      3. Has required structure (log_entry → fields)
      4. Has at least 4 required fields
    """
    try:
        import yaml
        
        # Read the log schema file
        # 'r' means read mode, not write mode
        with open('schemas/log_schema.yaml', 'r') as file:
            schema = yaml.safe_load(file)  # Parse YAML into Python dict
        
        # Check structure
        # Assert means "this must be true or test fails"
        assert 'log_entry' in schema, "Schema must have 'log_entry' section"
        assert 'fields' in schema['log_entry'], "Schema must define fields"
        
        # Count how many fields are required
        # This loops through all fields and counts ones where required = 'yes'
        required_fields = [
            field for field in schema['log_entry']['fields'] 
            if field.get('required') == 'yes'
        ]
        
        # Print result
        print(f"✓ Log schema loaded: {len(required_fields)} required fields")
        
        # Verify we have at least 4 required fields
        # (timestamp, level, service, message)
        assert len(required_fields) >= 4, "Should have at least 4 required fields"
        
    except FileNotFoundError:
        # If file doesn't exist
        pytest.fail("❌ schemas/log_schema.yaml not found. Did you create it?")
        
    except yaml.YAMLError as e:
        # If YAML syntax is invalid
        pytest.fail(f"❌ Invalid YAML syntax: {e}")
        
    except Exception as e:
        # Any other error
        pytest.fail(f"❌ Error reading log schema: {e}")


# ----------------------------------------------------------------------------
# TEST 5: READ ANOMALY SCHEMA
# ----------------------------------------------------------------------------
def test_read_anomaly_schema():
    """
    TEST: Can we read our anomaly detection rules?
    PURPOSE: Verifies the anomaly schema is valid
    CHECKS:
      1. File exists
      2. Valid YAML
      3. Has 'anomalies' section
      4. Has at least 5 anomaly types defined
    """
    try:
        import yaml
        
        # Read the anomaly schema file
        with open('schemas/anomaly_schema.yaml', 'r') as file:
            schema = yaml.safe_load(file)
        
        # Check that it has anomaly definitions
        assert 'anomalies' in schema, "Schema must have 'anomalies' section"
        
        # Count how many anomalies are defined
        anomaly_count = len(schema['anomalies'])
        
        print(f"✓ Anomaly schema loaded: {anomaly_count} anomaly types defined")
        
        # Verify we have at least 5 anomaly types
        assert anomaly_count >= 5, "Should have at least 5 anomaly types"
        
    except FileNotFoundError:
        pytest.fail("❌ schemas/anomaly_schema.yaml not found. Did you create it?")
        
    except Exception as e:
        pytest.fail(f"❌ Error reading anomaly schema: {e}")


# ----------------------------------------------------------------------------
# TEST 6: DASK BASIC OPERATION
# ----------------------------------------------------------------------------
def test_dask_basic_operation():
    """
    TEST: Can Dask process data?
    PURPOSE: Simulates processing log data with Dask
    PROCESS:
      1. Create sample log data (3 logs)
      2. Convert to Dask dataframe
      3. Count total logs
      4. Filter for errors only
      5. Count errors
    """
    import dask.dataframe as dd
    import pandas as pd
    
    # STEP 1: Create sample log data
    # In real system, this would be millions of logs from files/database
    sample_logs = pd.DataFrame({
        'timestamp': [
            '2024-02-13 10:00:00',
            '2024-02-13 10:01:00',
            '2024-02-13 10:02:00'
        ],
        'level': ['INFO', 'ERROR', 'WARNING'],
        'service': ['auth-service', 'payment-service', 'database-service'],
        'message': ['User login', 'Payment failed', 'Slow query']
    })
    
    # STEP 2: Convert to Dask dataframe
    # npartitions=1 means don't split the data (it's small)
    # In production, you'd use more partitions for parallel processing
    ddf = dd.from_pandas(sample_logs, npartitions=1)
    
    # STEP 3: Count total logs
    total_logs = len(ddf)
    print(f"✓ Dask processed {total_logs} sample logs")
    assert total_logs == 3, "Should have 3 logs"
    
    # STEP 4: Filter for errors
    # This is like SQL: SELECT * FROM logs WHERE level = 'ERROR'
    errors = ddf[ddf['level'] == 'ERROR']
    
    # STEP 5: Count errors
    error_count = len(errors)
    print(f"✓ Dask found {error_count} ERROR logs")
    assert error_count == 1, "Should have 1 error"


# ----------------------------------------------------------------------------
# TEST 7: RAY BASIC OPERATION
# ----------------------------------------------------------------------------
def test_ray_basic_operation():
    """
    TEST: Can Ray monitor data in real-time?
    PURPOSE: Simulates anomaly detection with Ray
    PROCESS:
      1. Start Ray
      2. Define a remote function (runs in parallel)
      3. Count errors in sample logs
      4. Verify count is correct
      5. Shut down Ray
    """
    import ray # pyright: ignore[reportMissingImports]
    
    # STEP 1: Initialize Ray
    # This starts the Ray runtime
    # ignore_reinit_error=True: Don't error if Ray already running
    # num_cpus=1: Use 1 CPU core (for testing)
    ray.init(ignore_reinit_error=True, num_cpus=1)
    
    # STEP 2: Define a remote function
    # @ray.remote decorator makes this function run in parallel
    @ray.remote
    def count_errors(logs):
        """
        Count how many error logs we have
        This would be our anomaly detection logic
        """
        return sum(1 for log in logs if 'ERROR' in log)
    
    # STEP 3: Sample logs
    test_logs = [
        'INFO: System started',
        'ERROR: Database connection failed',
        'ERROR: Payment timeout',
        'WARNING: High memory usage'
    ]
    
    # STEP 4: Process with Ray
    # count_errors.remote() runs the function in parallel
    # ray.get() waits for result and returns it
    result = ray.get(count_errors.remote(test_logs))
    
    print(f"✓ Ray counted {result} errors")
    assert result == 2, "Should find 2 errors"
    
    # STEP 5: Cleanup
    # Always shut down Ray after use
    ray.shutdown()


# ----------------------------------------------------------------------------
# TEST 8: DASK AND RAY INTEGRATION
# ----------------------------------------------------------------------------
def test_dask_ray_integration():
    """
    TEST: Can Dask and Ray work together?
    PURPOSE: This is the real test - both tools working as a team
    
    WORKFLOW:
      1. Dask processes large log files (batch processing)
      2. Ray monitors the results for anomalies (real-time monitoring)
      3. If anomaly detected, trigger alert
    
    SCENARIO:
      We have 100 logs with 40 errors (unusually high)
      Normal is 5-10 errors
      This should trigger our "error_spike" anomaly
    """
    import dask.dataframe as dd
    import pandas as pd
    import ray # pyright: ignore[reportMissingImports]
    
    # Initialize Ray
    ray.init(ignore_reinit_error=True, num_cpus=1)
    
    # STEP 1: Create sample log data
    # Simulating 100 logs over 100 minutes
    # 50 INFO, 40 ERROR (too many!), 10 WARNING
    logs_df = pd.DataFrame({
        'timestamp': pd.date_range('2024-02-13 10:00:00', periods=100, freq='1min'),
        'level': ['INFO'] * 50 + ['ERROR'] * 40 + ['WARNING'] * 10,
        'service': ['payment-service'] * 100,
        'message': ['Transaction processed'] * 50 + ['Payment failed'] * 40 + ['Slow response'] * 10
    })
    
    # STEP 2: Process with Dask
    # Convert to Dask dataframe with 4 partitions (parallel processing)
    ddf = dd.from_pandas(logs_df, npartitions=4)
    
    # Count errors
    # This is like: SELECT COUNT(*) FROM logs WHERE level = 'ERROR'
    error_count = len(ddf[ddf['level'] == 'ERROR'])
    
    print(f"✓ Dask processed 100 logs and found {error_count} errors")
    
    # STEP 3: Monitor with Ray
    # Define anomaly detection function
    @ray.remote
    def check_for_anomaly(error_count, threshold=30):
        """
        Check if error count exceeds threshold
        This simulates our anomaly_schema.yaml rules
        
        Args:
            error_count: Number of errors found
            threshold: Maximum acceptable errors (default 30)
        
        Returns:
            Dictionary with anomaly detection results
        """
        if error_count > threshold:
            return {
                'anomaly_detected': True,
                'type': 'error_spike',
                'severity': 'HIGH',
                'action': 'Alert team',
                'details': f'{error_count} errors exceeds threshold of {threshold}'
            }
        return {
            'anomaly_detected': False,
            'message': 'Error count within normal range'
        }
    
    # STEP 4: Run anomaly check
    # Ray runs this in parallel (in real system, it would run continuously)
    result = ray.get(check_for_anomaly.remote(error_count))
    
    # STEP 5: Print results
    print(f"✓ Ray detected anomaly: {result['anomaly_detected']}")
    if result['anomaly_detected']:
        print(f"  - Type: {result['type']}")
        print(f"  - Severity: {result['severity']}")
        print(f"  - Action: {result['action']}")
        print(f"  - Details: {result['details']}")
    
    # STEP 6: Verify the test
    assert error_count == 40, "Should have counted 40 errors"
    assert result['anomaly_detected'] == True, "Should have detected anomaly"
    assert result['type'] == 'error_spike', "Should be error_spike type"
    
    # STEP 7: Cleanup
    ray.shutdown()
    
    print("✓ Integration test passed! Dask and Ray are working together!")


# ----------------------------------------------------------------------------
# MAIN EXECUTION
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    """
    This runs when you execute: python tests/test_environment.py
    It runs all tests in sequence and reports results
    """
    print("=" * 70)
    print("RUNNING ENVIRONMENT TESTS")
    print("=" * 70)
    print()
    
    # Track if any test fails
    all_passed = True
    
    # Run each test
    tests = [
        ("Dask Import", test_dask_import),
        ("Ray Import", test_ray_import),
        ("YAML Import", test_yaml_import),
        ("Log Schema", test_read_log_schema),
        ("Anomaly Schema", test_read_anomaly_schema),
        ("Dask Operations", test_dask_basic_operation),
        ("Ray Operations", test_ray_basic_operation),
        ("Dask + Ray Integration", test_dask_ray_integration),
    ]
    
    for test_name, test_func in tests:
        try:
            print(f"Running: {test_name}...")
            test_func()
            print(f"✓ {test_name} passed\n")
        except Exception as e:
            print(f"❌ {test_name} FAILED")
            print(f"   Error: {e}\n")
            all_passed = False
    
    print("=" * 70)
    if all_passed:
        print("✓ ALL TESTS PASSED!")
        print("=" * 70)
        print()
        print("Your environment is set up correctly!")
        print("You can now proceed to build the log monitoring system.")
    else:
        print("❌ SOME TESTS FAILED")
        print("=" * 70)
        print()
        print("Please fix the errors above and run tests again.")
        sys.exit(1)