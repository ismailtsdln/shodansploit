# shodansploit

<p align="center">
<img src="https://github.com/shodansploit/shodansploit/blob/master/img/shodansploit-logo.png">
<img src="https://cdn.rawgit.com/sindresorhus/awesome/d7305f38d29fed78fa85652e3a63e154dd8e8829/media/badge.svg"> <img src="https://img.shields.io/github/stars/shodansploit/shodansploit?style=social"> <img src="https://img.shields.io/github/forks/shodansploit/shodansploit?style=social"> <img src="https://img.shields.io/badge/security-shodansploit-red"> <img src="https://img.shields.io/github/repo-size/shodansploit/shodansploit"> <img src="https://img.shields.io/github/license/shodansploit/shodansploit">
</p>

## 📖 About

**shodansploit** is a powerful CLI tool for interacting with the Shodan API. It provides both an interactive menu-driven interface and robust command-line capabilities for security researchers, penetration testers, and DevOps professionals.

Shodan is the world's first search engine for Internet-connected devices. With shodansploit, you can:

- 🔍 Search for vulnerable hosts and services
- 🛡️ Discover exposed devices (cameras, databases, industrial systems)
- 💾 Export results for reporting and analysis
- 📚 Use pre-built search queries (Dorks) for common vulnerabilities
- ⚡ Integrate into automated security workflows

## ✨ Features

### Core Features

- **Interactive Menu Mode**: User-friendly terminal UI with rich formatting
- **CLI Mode**: Script-friendly command-line interface
- **Comprehensive API Coverage**: Access all Shodan API endpoints
  - Host information & search
  - Exploit database queries
  - DNS operations
  - Account & tools

### Advanced Features (v2.0)

- **🎯 Shodan Dorks Library**: Pre-configured queries for finding:
  - Vulnerable webcams & IP cameras
  - Exposed databases (MongoDB, MySQL, Elasticsearch)
  - Industrial Control Systems (ICS/SCADA)
  - Default credentials & admin panels
  - Remote access services (VNC, RDP, SSH)
  
- **💾 Data Export**: Save results in multiple formats
  - JSON (structured data)
  - CSV (spreadsheet-compatible)
  - TXT (human-readable)

- **📝 Search History**: Track your queries automatically
  - View recent searches
  - Search history by keyword
  - Persistent storage

- **🎨 Rich UI**: Enhanced terminal experience with syntax highlighting and formatted output

## 🚀 Installation

### Prerequisites

- Python 3.6+
- Shodan API Key ([Get one free](https://account.shodan.io/register))

### Install Dependencies

```bash
git clone https://github.com/ismailtasdelen/shodansploit.git
cd shodansploit
pip install -r requirements.txt
```

### Docker Installation

Build the Docker image:

```bash
docker build -t shodansploit -f .Dockerfile .
```

Run with Docker:

```bash
docker run --rm -it shodansploit
```

## 📚 Usage

### Interactive Mode

Simply run the script without arguments:

```bash
python shodansploit.py
```

On first run, you'll be prompted to enter your Shodan API key. The key is stored in `api.txt` for future use.

You can also set the API key via environment variable:

```bash
export SHODAN_API_KEY="your_api_key_here"
python shodansploit.py
```

### CLI Mode

The tool supports command-line arguments for automation and scripting:

#### Basic Examples

```bash
# Get information about a specific host
python shodansploit.py --host 8.8.8.8

# Search for hosts
python shodansploit.py --search "port:22 country:US"

# Count search results
python shodansploit.py --count "apache"

# Get your public IP
python shodansploit.py --myip

# View account profile
python shodansploit.py --profile
```

#### Exploit Database

```bash
# Search exploits by CVE
python shodansploit.py --exploit-cve CVE-2021-44228

# Search exploits by author
python shodansploit.py --exploit-author "metasploit"
```

#### DNS Operations

```bash
# Resolve hostnames to IPs
python shodansploit.py --dns-resolve "google.com,github.com"

# Reverse DNS lookup
python shodansploit.py --dns-reverse "8.8.8.8,1.1.1.1"
```

#### Shodan Dorks

```bash
# Use a pre-configured dork
python shodansploit.py --dork webcam
python shodansploit.py --dork mongodb
```

#### Export Results

```bash
# Export to JSON (default)
python shodansploit.py --search "nginx" --output results.json

# Export to CSV
python shodansploit.py --search "port:3306" --output mysql_hosts.csv --format csv

# Export to TXT
python shodansploit.py --host 1.1.1.1 --output cloudflare.txt --format txt
```

#### Help

```bash
python shodansploit.py --help
```

## 📂 Project Structure

```
shodansploit/
├── shodansploit.py       # Main entry point
├── requirements.txt      # Python dependencies
├── api.txt              # Your Shodan API key (auto-generated)
├── .Dockerfile          # Docker configuration
├── src/                 # Source modules
│   ├── __init__.py
│   ├── api.py           # Shodan API wrapper
│   ├── config.py        # Configuration management
│   ├── ui.py            # User interface
│   ├── export.py        # Data export functionality
│   ├── dorks.py         # Shodan dorks library
│   └── history.py       # Search history tracking
└── results/             # Exported results (auto-created)
```

## 🎯 Shodan Dorks Categories

The tool includes a curated library of Shodan search queries organized by category:

- **Webcams & Cameras**: Find exposed surveillance systems
- **Industrial Control Systems**: Discover ICS/SCADA devices
- **Databases**: Locate exposed database servers
- **Default Credentials**: Find systems with default passwords
- **Remote Access**: Identify RDP, VNC, SSH services
- **Web Services**: Locate web servers and frameworks
- **IoT Devices**: Find smart home and IoT systems
- **Vulnerable Services**: Search for known CVEs

## 🔧 API Key Setup

### Method 1: Interactive Prompt

On first run, the tool will prompt you for your API key:

```
[*] Please enter a valid Shodan.io API Key: YOUR_KEY_HERE
```

### Method 2: Environment Variable

```bash
export SHODAN_API_KEY="YOUR_KEY_HERE"
```

### Method 3: Manual File

Create `api.txt` in the project directory:

```bash
echo "YOUR_KEY_HERE" > api.txt
```

## 📊 Menu Options

| Option | Description |
|--------|-------------|
| 1-5 | Host operations (info, count, search, tokens, ports) |
| 6-16 | Exploit database queries |
| 17-19 | DNS & Labs operations |
| 20-23 | Account & tools |
| 24 | Exit |
| 25 | Shodan Dorks Library |
| 26 | View Search History |

## 🛡️ Security & Privacy

- API keys are stored locally in `api.txt`
- Search history is saved in `.shodansploit_history` (local only)
- No telemetry or external data transmission beyond Shodan API calls
- Results are stored locally in the `results/` directory

## 📖 API Documentation

For detailed information about the Shodan API:

- [REST API Documentation](https://developer.shodan.io/api)
- [Exploits API Documentation](https://developer.shodan.io/api/exploits/rest)
- [Banner Specification](https://developer.shodan.io/api/banner-specification)
- [Exploit Specification](https://developer.shodan.io/api/exploit-specification)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Code Style

- Follow PEP 8 guidelines
- Add docstrings to functions
- Keep code modular and maintainable

## 📝 Changelog

### Version 2.0.0 (2026-01-01)

- ✨ Complete refactor to modular architecture
- 🎯 Added Shodan Dorks library
- 💾 Added export functionality (JSON, CSV, TXT)
- 📝 Added search history tracking
- ⚡ Added CLI mode with argparse
- 🎨 Enhanced UI with Rich library
- 🐳 Updated Docker support
- 🔧 Environment variable support for API key

### Version 1.2.0 (Previous)

- Initial release with basic functionality

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Ismail Tasdelen**

- 📧 Email: <ismailtasdelen@protonmail.com>
- 💼 LinkedIn: [linkedin.com/in/ismailtasdelen](https://www.linkedin.com/in/ismailtasdelen/)
- 🐙 GitHub: [github.com/ismailtasdelen](https://github.com/ismailtasdelen/)


## 💖 Support

If you find this tool useful, consider supporting the development:

**PayPal**: [paypal.me/ismailtsdln](https://paypal.me/ismailtsdln)

**LiberaPay**: <a href="https://liberapay.com/ismailtasdelen/donate"><img alt="Donate using Liberapay" src="https://liberapay.com/assets/widgets/donate.svg"></a>

## ⚠️ Disclaimer

This tool is intended for security research and ethical hacking purposes only. Always obtain proper authorization before scanning or testing systems you don't own. The authors are not responsible for misuse or damage caused by this tool.

## 🌟 Star History

If you find this project useful, please consider giving it a ⭐!
