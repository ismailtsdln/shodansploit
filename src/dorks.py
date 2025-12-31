"""
Shodan Dorks - A collection of popular Shodan search queries.
These dorks help find various vulnerable or interesting devices on the internet.
"""

DORKS = {
    "Webcams & Cameras": [
        {"name": "Webcams", "query": "title:\"webcamXP 5\""},
        {"name": "IP Cameras", "query": "Server: SQ-WEBCAM"},
        {"name": "Axis Network Cameras", "query": "Server: AXIS"},
        {"name": "Hikvision Cameras", "query": "Server: App-webs"},
        {"name": "DVR Devices", "query": "port:554 has_screenshot:true"},
    ],
    
    "Industrial Control Systems (ICS/SCADA)": [
        {"name": "Siemens S7 PLCs", "query": "port:102"},
        {"name": "Modbus Devices", "query": "port:502"},
        {"name": "SCADA Systems", "query": "SCADA"},
        {"name": "Niagara Fox", "query": "port:1911,4911 product:Niagara"},
        {"name": "BACnet Building Automation", "query": "port:47808"},
    ],
    
    "Databases": [
        {"name": "MongoDB", "query": "product:MongoDB"},
        {"name": "MySQL", "query": "product:MySQL"},
        {"name": "PostgreSQL", "query": "product:PostgreSQL"},
        {"name": "Elasticsearch", "query": "port:9200 product:Elasticsearch"},
        {"name": "Redis", "query": "product:Redis"},
    ],
    
    "Default Credentials": [
        {"name": "Default Passwords", "query": "default password"},
        {"name": "Admin Login", "query": "title:\"admin login\""},
        {"name": "Login Pages", "query": "http.title:\"login\""},
        {"name": "Router Login", "query": "title:\"router login\""},
    ],
    
    "Remote Access": [
        {"name": "VNC Servers", "query": "port:5900 has_screenshot:true"},
        {"name": "RDP Services", "query": "port:3389"},
        {"name": "TeamViewer", "query": "port:5938"},
        {"name": "SSH Servers", "query": "port:22"},
        {"name": "Telnet", "query": "port:23"},
    ],
    
    "Web Services": [
        {"name": "Apache Servers", "query": "product:Apache"},
        {"name": "Nginx Servers", "query": "product:nginx"},
        {"name": "Jenkins CI", "query": "product:Jenkins"},
        {"name": "Docker APIs", "query": "product:Docker"},
        {"name": "Kubernetes", "query": "product:Kubernetes"},
    ],
    
    "IoT Devices": [
        {"name": "Smart TVs", "query": "device:tv"},
        {"name": "Printers", "query": "device:printer"},
        {"name": "Smart Home Devices", "query": "home automation"},
        {"name": "Raspberry Pi", "query": "device:pi"},
    ],
    
    "Vulnerable Services": [
        {"name": "Heartbleed Vulnerable", "query": "vuln:CVE-2014-0160"},
        {"name": "Eternal Blue Vulnerable", "query": "vuln:ms17-010"},
        {"name": "Anonymous FTP", "query": "port:21 Anonymous user logged in"},
        {"name": "Open DNS Resolvers", "query": "port:53"},
    ],
}

def get_all_dorks():
    """Returns all dorks as a flat list."""
    all_dorks = []
    for category, dorks_list in DORKS.items():
        for dork in dorks_list:
            dork['category'] = category
            all_dorks.append(dork)
    return all_dorks

def get_dorks_by_category(category):
    """Returns dorks for a specific category."""
    return DORKS.get(category, [])

def get_categories():
    """Returns list of all categories."""
    return list(DORKS.keys())

def search_dorks(keyword):
    """Search for dorks by keyword."""
    results = []
    keyword = keyword.lower()
    for category, dorks_list in DORKS.items():
        for dork in dorks_list:
            if keyword in dork['name'].lower() or keyword in dork['query'].lower():
                results.append({**dork, 'category': category})
    return results
