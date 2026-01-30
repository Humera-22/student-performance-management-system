"""
import requests
from app.exceptions import AppException

class HttpClient:

    @staticmethod
    def get(url, timeout=5):
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            raise AppException("External API timeout", 504)
        except requests.exceptions.RequestException:
            raise AppException("External API failed", 502)
"""
# app/http_client.py
import requests
from app.exceptions import AppException

class HttpClient:
    """Utility to call external HTTP APIs"""

    @staticmethod
    def get(url: str, timeout: int = 5):
        """Send GET request and handle exceptions"""
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            raise AppException("External API timeout", 504)
        except requests.exceptions.RequestException as e:
            raise AppException(f"External API failed: {str(e)}", 502)
