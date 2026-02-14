import unittest
from g4f.providers.base_provider import RaiseErrorMixin
from g4f.errors import MissingAuthError, PaymentRequiredError, RateLimitError, ResponseError


class TestRaiseError(unittest.TestCase):
    """Test the RaiseErrorMixin.raise_error method"""

    def test_status_401_with_title_detail(self):
        """Test that status 401 in response body raises MissingAuthError"""
        data = {
            "status": 401,
            "title": "Unauthorized",
            "detail": "Authentication failed"
        }
        with self.assertRaises(MissingAuthError) as cm:
            RaiseErrorMixin.raise_error(data)
        self.assertIn("401", str(cm.exception))
        self.assertIn("Unauthorized", str(cm.exception))
        self.assertIn("Authentication failed", str(cm.exception))

    def test_status_402_with_title_detail(self):
        """Test that status 402 in response body raises PaymentRequiredError"""
        data = {
            "status": 402,
            "title": "Payment Required",
            "detail": "Insufficient credits"
        }
        with self.assertRaises(PaymentRequiredError) as cm:
            RaiseErrorMixin.raise_error(data)
        self.assertIn("402", str(cm.exception))

    def test_status_429_with_title_detail(self):
        """Test that status 429 in response body raises RateLimitError"""
        data = {
            "status": 429,
            "title": "Too Many Requests",
            "detail": "Rate limit exceeded"
        }
        with self.assertRaises(RateLimitError) as cm:
            RaiseErrorMixin.raise_error(data)
        self.assertIn("429", str(cm.exception))

    def test_status_500_with_title_detail(self):
        """Test that status 500 in response body raises ResponseError"""
        data = {
            "status": 500,
            "title": "Internal Server Error",
            "detail": "Something went wrong"
        }
        with self.assertRaises(ResponseError) as cm:
            RaiseErrorMixin.raise_error(data)
        self.assertIn("500", str(cm.exception))

    def test_status_200_does_not_raise(self):
        """Test that status 200 in response body does not raise an error"""
        data = {
            "status": 200,
            "title": "OK",
            "detail": "Success"
        }
        # Should not raise any exception
        RaiseErrorMixin.raise_error(data)

    def test_error_field_still_works(self):
        """Test that the original 'error' field still works"""
        data = {"error": "Some error message"}
        with self.assertRaises(ResponseError) as cm:
            RaiseErrorMixin.raise_error(data)
        self.assertIn("Some error message", str(cm.exception))

    def test_error_message_field_still_works(self):
        """Test that the original 'error_message' field still works"""
        data = {"error_message": "Some error message"}
        with self.assertRaises(ResponseError) as cm:
            RaiseErrorMixin.raise_error(data)
        self.assertIn("Some error message", str(cm.exception))

    def test_status_without_title_detail(self):
        """Test that status field without title/detail still raises error"""
        data = {"status": 401}
        with self.assertRaises(MissingAuthError) as cm:
            RaiseErrorMixin.raise_error(data)
        self.assertIn("401", str(cm.exception))


if __name__ == '__main__':
    unittest.main()
