from slowapi import Limiter
from slowapi.util import get_remote_address

""" Rate Limiter Configuration
This module sets up a rate limiter for the application using SlowAPI.
It uses the client's IP address as the key for rate limiting.
"""
limiter = Limiter(key_func=get_remote_address)