"""Quick test to make sure everything works"""

def test_config():
    from config.settings import DashboardConfig
    assert DashboardConfig.VERSION == "2.2.1"
    assert DashboardConfig.FEATURES.EXECUTIVE_MODE is True
    print("✅ Config working")

def test_data_loading():
    from data.loaders import load_historical_data
    data = load_historical_data()
    assert len(data) > 0
    print("✅ Data loading working")

def test_helpers():
    from utils.helpers import clean_filename, safe_execute
    filename = clean_filename("Test File 📊")
    assert filename == "test_file"
    
    result = safe_execute(lambda: "success", show_error=False)
    assert result == "success"
    print("✅ Helpers working")

if __name__ == "__main__":
    test_config()
    test_data_loading() 
    test_helpers()
    print("🎉 All basic tests passed!")