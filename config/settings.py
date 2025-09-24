from typing import Mapping, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import date, datetime
from zoneinfo import ZoneInfo
import os, hashlib

class ConfigError(ValueError):
    """
    This class will only serve some user-friendly messages when been called 
    """
    pass

    
# Difine the seedmode as enum
class SeedMode(Enum): 
    TODAY = "today"
    FIXED = "fixed"

# Define a dataclass for our env varibales using @dataclass
@dataclass
class Settings:
    feed_urls: list[str] # means it'll be a list of string
    max_items: int
    timezone: str
    seed_mode: SeedMode # This will be whatever elements in the enum (just one of them)
    fixed_seed: Optional[int] 

# Functions to parse the env file variables 
# These functions will read a specific environment variable, validate its content, and convert it into the correct Python type.
# Note: env: Mapping[str, str]) -> list[str] means 
# that it's a type hint. It's not executable code but a way of documenting what the function expects and what it returns.
def parse_feed_urls(env: Mapping[str, str]) -> list[str]:
    """
    Parses a comma-separated string of URLs from a given environment mapping.
    Raises ConfigError if the key is missing or the value is invalid.
    """
    # 1. Read the key
    feed_urls_key = "FEED_URLS" # The value MUST MATCH the var name u have i ur env file
    url_value = env.get(feed_urls_key)

    # 2. Handle the missing key
    if not url_value:
        raise ConfigError(f"Missing required environment variable: '{feed_urls_key}'")
    
    # 3. In case there are multiple urls, split them the trim teh whitespaces
    urls = [u.strip() for u in url_value.split(",") if u.strip()]
    if not urls:
        raise ConfigError("FEED_URLS is required (comma-separated) and cannot be empty.")
    
    # 4. Validate each url that is actually a url
    for url in urls:
        if not (url.startswith("http://") or url.startswith("https://")):
            raise ConfigError(f"Invalid URL format for '{feed_urls_key}': '{url_value}'")
    
    # 4. Return the list
    return urls

# This function will check for the max items
def parse_max_items(env: Mapping[str, str]) -> int:
    """
    Parses a max item string from a given environment mapping.
    Raises ConfigError if the key is missing or the value is invalid.
    """
    # 1. Read the key
    max_items_key = "MAX_ITEMS"
    max_item_value = env.get(max_items_key)

    # 2. Validate the value
    if max_item_value is None or str(max_item_value).strip() == "":
        max_item_value = "25"
    
    # 3. Parse and return
    try:
        value = int(max_item_value)
    except(TypeError, ValueError):
            raise ConfigError(f"MAX_ITEMS must be a positive integer but got {value}.")
    
    if value <= 0:
        raise ConfigError(f"MAX_ITEMS must be a positive integer (got: '{value}').")
    
     # 4. Return the int
    return value

# Function to check the timezone
def parse_timezone(env: Mapping[str, str]) -> str:
    """
    Parses timezone string from a given environment mapping.
    Raises ConfigError if the key is missing or the value is invalid.
    """

    # 1. Read the key
    timezone_key = "TIMEZONE"
    timezone_value = env.get(timezone_key)
    
    # 2. Validate the value 
    if not timezone_value or str(timezone_value).strip() == "":
        raise ConfigError("TIMEZONE is required.")
    
    try:
        ZoneInfo(timezone_value)
    except Exception:
        raise ConfigError("TIMEZONE must be a valid IANA name (e.g., 'Asia/Bahrain').")
    
    # 3. Return the variable
    return timezone_value

# Create a function for seed mode 
def parse_seed_mode(env: Mapping[str, str]) -> SeedMode:
    """
    Parses seed mode enum from a given environment mapping.
    Raises ConfigError if the key is missing or the value is invalid.
    """

    # Read the variable
    seed_mode_key = "RANDOM_SEED_MODE"
    seed_mode_value = env.get(seed_mode_key)    
    # Below code will 
    # 1. Convert the value to a string 
    # 2. Trim any whitespaces
    # 3. Convert to lowercase
    # 4. check after all these operations, if the mode is empty
    mode = str(seed_mode_value).strip().lower() if seed_mode_value is not None else "today"

    # Check the seed mode 
    if mode == "TODAY":
        return SeedMode.TODAY

    if mode == "FIXED":
        return SeedMode.FIXED
    
    raise ConfigError(f"RANDOM_SEED_MODE must be 'today' or 'fixed' (got: '{mode}').")

def parse_fixed_seed(env: Mapping[str, str], mode: SeedMode) -> Optional[int]:
    """
    Parses fixed seed enum from a given environment mapping.
    Raises ConfigError if the key is missing or the value is invalid.
    """

    # Validate the variable
    if mode == SeedMode.TODAY:
        return None
    else:
        # Read the vars
        fixed_seed_key = "FIXED_RANDOM_SEED"
        fixed_seed_value = int(env.get(fixed_seed_key))
        if fixed_seed_value is None or str(fixed_seed_value).strip() == "":
            raise ConfigError("FIXED_RANDOM_SEED is required when RANDOM_SEED_MODE=fixed.")
    try:
        return int(fixed_seed_value)
    except (TypeError, ValueError):
        raise ConfigError(f"FIXED_RANDOM_SEED must be an integer (got: '{fixed_seed_value}').")