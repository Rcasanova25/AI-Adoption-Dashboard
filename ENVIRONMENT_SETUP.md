# Environment Setup Guide

This guide explains how to configure environment variables for the AI Adoption Dashboard.

## Quick Start

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file to set your resources path:
   ```bash
   # For Windows (WSL):
   AI_ADOPTION_RESOURCES_PATH=/mnt/c/Users/YOUR_USERNAME/path/to/AI adoption resources

   # For Linux:
   AI_ADOPTION_RESOURCES_PATH=/home/YOUR_USERNAME/path/to/AI adoption resources

   # For macOS:
   AI_ADOPTION_RESOURCES_PATH=/Users/YOUR_USERNAME/path/to/AI adoption resources
   ```

3. Install python-dotenv (if not already installed):
   ```bash
   pip install python-dotenv
   ```

## Environment Variables

### Required Variables

- **AI_ADOPTION_RESOURCES_PATH**: Path to the directory containing AI adoption resource files
  - This should point to your "AI adoption resources" directory
  - The path should be absolute, not relative
  - On Windows using WSL, use `/mnt/c/` format instead of `C:\`

### Optional Variables

- **CACHE_MEMORY_SIZE**: Maximum items in memory cache (default: 200)
- **CACHE_MEMORY_TTL**: Time-to-live for memory cache in seconds (default: 600)
- **CACHE_DISK_SIZE**: Maximum disk cache size in bytes (default: 2GB)
- **MAX_WORKERS**: Maximum concurrent workers for parallel loading (default: 4)
- **LOG_LEVEL**: Logging level (default: INFO)
- **DEBUG**: Enable debug mode (default: False)

## Testing Your Configuration

Run the test script to verify your settings:

```bash
python3 test_settings.py
```

This will show:
- Current configuration values
- Whether the resources path exists
- Whether the DataManager can initialize properly

## Troubleshooting

### Resources Path Not Found

If you get an error about the resources path not existing:

1. Check that the path in your `.env` file is correct
2. Ensure the path uses forward slashes (`/`) not backslashes (`\`)
3. For WSL users, remember to use `/mnt/c/` instead of `C:\`
4. Make sure the "AI adoption resources" directory exists at the specified location

### Missing python-dotenv

If you get an import error for dotenv:

```bash
pip install python-dotenv
```

### Permission Issues

If you encounter permission issues:

1. Check that you have read access to the resources directory
2. On Linux/macOS, you may need to adjust file permissions:
   ```bash
   chmod -R 755 "/path/to/AI adoption resources"
   ```

## Cross-Platform Compatibility

The configuration system is designed to work across:
- Windows (using WSL)
- Linux (native)
- macOS

Just ensure you use the appropriate path format for your system in the `.env` file.