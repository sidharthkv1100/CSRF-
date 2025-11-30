import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def find_forms(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.find_all("form")

def has_csrf_token(form):
    hidden_inputs = form.find_all("input", {"type": "hidden"})
    for hi in hidden_inputs:
        if "csrf" in hi.get("name", "").lower():
            return True
    return False

def analyze_page(url):
    print(f"\nScanning: {url}")
    forms = find_forms(url)
    print(f"Found {len(forms)} forms")

    for index, form in enumerate(forms, start=1):
        action = form.get("action")
        method = form.get("method", "GET").upper()
        print(f"\nForm #{index}:")
        print(f"Action: {action}")
        print(f"Method: {method}")

        if method in ["POST", "PUT", "DELETE"]:
            if has_csrf_token(form):
                print("✓ CSRF token found")
            else:
                print("✗ Missing CSRF token — Potential CSRF vulnerability")
        else:
            print("GET method — typically not vulnerable")

if __name__ == "__main__":
    target = "http://example.com"
    analyze_page(target)

