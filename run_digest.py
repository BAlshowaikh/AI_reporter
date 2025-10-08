# run_digest.py

# Ensures type hints are interpreted using postponed evaluation, a modern practice 
# that allows for cleaner use of types (e.g., class referencing itself).
from __future__ import annotations 

import sys # Module used for system-level operations, specifically to exit the program.
from typing import Sequence # Used for type hinting, indicating that 'urls' can be any sequence (like a list).

# Imports required configuration functions and a custom exception from your 'config.settings' module.
from config.settings import (
    load_settings,    # Function to load configuration data (e.g., from .env, environment variables).
    effective_seed,  # Function to calculate or resolve a random seed based on settings.
    ConfigError,     # A custom exception for handling expected configuration problems.
)


def _preview_urls(urls: Sequence[str], n: int = 3) -> list[str]:
    """
    A private helper function (indicated by the leading underscore _) 
    to take a sequence of URLs and return a small, fixed-size slice for display.
    
    urls[: max(0, n)]: 
    - Slices the list to return the first 'n' elements.
    - 'max(0, n)' ensures the slice index is never negative, preventing potential errors.
    """
    return list(urls[: max(0, n)])


def main() -> int:
    """
    The main execution function for the script.
    It returns an integer exit code for the operating system (0 for success).
    """
    print("Reached this!")

    try:
        # Attempt to load all application configuration settings.
        settings = load_settings()
        
        # Calculate the random seed based on the loaded settings.
        seed = effective_seed(settings)
        
    except ConfigError as e:
        # --- Specific Error Handling (Expected Configuration Failure) ---
        # Catches anticipated issues like invalid values or missing variables.
        print(f"Config error: {e}")
        # Returns 2: This non-zero code signals a configuration problem to external tools.
        return 2
        
    except Exception as e:
        # --- General Error Handling (Unexpected Runtime Failure) ---
        # Catches any other unforeseen error (e.g., file permissions, unexpected bug).
        
        # Unexpected error: show a short message but nonzero exit
        # Prints the class name of the error for easier identification.
        print(f"Unexpected error: {e.__class__.__name__}: {e}")
        # Returns 1: This is the standard generic non-zero code for failure.
        return 1

    # --- Configuration Summary (Execution proceeds only if settings loaded successfully) ---
    
    # Get the first 3 URLs for a clean summary display.
    preview = _preview_urls(settings.feed_urls, 3)

    print("AI_reporter config")
    print("------------------")
    
    # Report the total number of URLs and the number being shown in the preview.
    print(f"FEED_URLS: {len(settings.feed_urls)} (showing {len(preview)})")
    
    # Print the previewed URLs with proper indentation.
    for u in preview:
        print(f"  - {u}")
        
    # Print the rest of the key resolved configuration values.
    print(f"MAX_ITEMS: {settings.max_items}")
    print(f"TIMEZONE: {settings.timezone}")
    print(f"RANDOM_SEED_MODE: {settings.seed_mode.value}")
    print(f"RESOLVED_SEED: {seed}")

    # Returns 0: Indicates that the program completed successfully.
    return 0


if __name__ == "__main__":
    # Standard entry point for a Python script.
    # The code inside here runs only when the file is executed directly.
    
    # sys.exit(main()): Calls the 'main' function. The integer return value (0, 1, or 2) 
    # is then passed to sys.exit(), which immediately terminates the process and sets the 
    # program's exit status code for the operating system.
    # sys.exit(main())
    main()
