# Github Username Checker

A powerful application for checking Github username availability with multiple checking modes and proxy support.

## Features

### 🔍 Multiple Check Modes
- **File Mode**: Check usernames from a text file
- **Random Mode**: Generate and check random usernames of specified length
- **Specific Mode**: Check a single specific username
- **Semi-Pattern Mode**: Generate usernames with mixed patterns

### 🌐 Proxy Support
- **No Proxy**: Direct connection
- **Paid Proxies**: Load from file with multiple format support
- **Free Proxies**: Automatically fetch from public proxy sources

### 📊 Real-time Statistics
- Live counter for checked, available, unavailable, and deleted usernames
- Progress bar with target-based completion
- Color-coded results for easy reading

### 💾 Data Management
- Save available usernames automatically to `available_Github.txt`
- Export full results to custom files
- Session persistence

## Installation

1. **Clone the repository**:
```bash
git clone https://github.com/9rfm/github-username-checker.git
cd Github-username-checker
```

2. **Install required dependencies**:
```bash
pip install -r requirements.txt
```

## Required Dependencies
```text
tkinter
requests
colorama
```

2. Select your preferred check mode
3. Configure proxy settings (if needed)
4. Set your target number of available usernames
5. Click "Start Checking"

### Proxy Configuration

#### Paid Proxies
Supported proxy formats:
- `HTTP (ip:port)`
- `SOCKS4`
- `SOCKS5`
- `user:pass@host:port`
- `host:port:user:pass`
- `ip:port:user:pass`
- `user:pass:host:port`

#### Free Proxies
The application automatically fetches free proxies from:
- ProxyScraper GitHub repository
- ProxyScrape API
- TheSpeedX PROXY-List
- monosans proxy list

### Check Modes Explained

#### 1. File Mode
- Load usernames from a text file (one username per line)
- Ideal for checking specific username lists

#### 2. Random Mode
- Generate random alphanumeric usernames
- Specify length and quantity
- Great for finding available short usernames

#### 3. Specific Mode
- Check availability of a single username
- Quick verification for specific usernames

#### 4. Semi-Pattern Mode
- Generate mixed-pattern usernames
- Combines different character types
- Higher chance of finding available names

## Output Files

- `available_Github.txt`: Automatically saves all available usernames
- `res.txt`: Raw API responses for debugging purposes
- Custom export: Save full results via the "Save Results" button


## Response Handling

The application interprets these status codes:
- **OK**: Username is available (green)
- **TAKEN**: Username is already taken (gray)
- **DELETED**: Username was previously used (yellow)
- **UNKNOWN**: Unexpected response (requires investigation)

## Error Handling

- Automatic proxy rotation on connection failures
- Retry mechanism with exponential backoff
- Comprehensive error logging
- Graceful recovery from network issues

## Performance Tips

1. **Use Proxies**: Avoid rate limiting with proxy rotation
2. **Adjust Delay**: Built-in delay between requests (1.5-3.0 seconds)
3. **Target Setting**: Set realistic targets to avoid unnecessary checks
4. **Proxy Quality**: Use reliable proxies for better performance

## Support

If you encounter issues:
1. Check the `res.txt` file for API responses
2. Verify your proxy configurations
3. Ensure you have stable internet connection
4. Check for application updates



## Version

Current version: 1.0.0

