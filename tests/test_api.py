import requests
import sys
from pathlib import Path

API_BASE = "http://localhost:8000"

def test_health():
    """Test health endpoint."""
    print("Testing /health...")
    response = requests.get(f"{API_BASE}/health")
    assert response.status_code == 200
    data = response.json()
    print(f"✅ Health check passed: {data}")
    return True

def test_pdf_upload():
    """Test PDF upload."""
    print("\nTesting PDF upload...")
    
    # Create a dummy PDF for testing
    dummy_pdf = Path("test_document.pdf")
    if not dummy_pdf.exists():
        print("⚠️  No test PDF found. Skipping upload test.")
        return False  # Fail CI if test file missing
    
    with open(dummy_pdf, "rb") as f:
        response = requests.post(
            f"{API_BASE}/pdf/upload",
            files={"file": f}
        )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ PDF upload passed: {data}")
        return True
    else:
        print(f"❌ PDF upload failed: {response.text}")
        return False

def test_pdf_search():
    """Test PDF search."""
    print("\nTesting PDF search...")
    response = requests.post(
        f"{API_BASE}/pdf/search",
        json={"input": "test query"}
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ PDF search passed: {len(data.get('results', []))} results")
        return True
    else:
        print(f"❌ PDF search failed: {response.text}")
        return False

def test_web_scrape():
    """Test web scraping."""
    print("\nTesting web scraping...")
    response = requests.post(
        f"{API_BASE}/web/scrape",
        json={"url": "https://example.com"}
    )
    
    if response.status_code in (200, 202):
        print(f"✅ Web scrape passed")
        return True
    else:
        print(f"❌ Web scrape failed: {response.text}")
        return False

def test_agent_chat():
    """Test agent chat."""
    print("\nTesting agent chat...")
    response = requests.post(
        f"{API_BASE}/agent/chat",
        json={"input": "Hello, what can you do?"}
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Agent chat passed")
        print(f"   Response: {data.get('output', '')[:100]}...")
        return True
    else:
        print(f"❌ Agent chat failed: {response.text}")
        return False

def main():
    """Run all tests."""
    print("=" * 50)
    print("OmniKnow API Test Suite")
    print("=" * 50)
    
    tests = [
        test_health,
        test_pdf_upload,
        test_pdf_search,
        test_web_scrape,
        test_agent_chat
    ]
    
    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print(f"Results: {sum(results)}/{len(results)} tests passed")
    print("=" * 50)
    
    if all(results):
        print("✅ All tests passed!")
        sys.exit(0)
    else:
        print("❌ Some tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()