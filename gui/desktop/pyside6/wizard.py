from PySide6.QtWidgets import (QWizard, QWizardPage, QVBoxLayout, QGridLayout, QLabel, QLineEdit, 
                               QTextEdit, QFrame, QComboBox, QCheckBox, QWidget, QPushButton, 
                               QHBoxLayout, QDialog)
from PySide6.QtCore import Qt, QThread, Signal, QObject
from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
import dns.resolver
import re
import requests
import sys
from io import StringIO


class DNSHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Define formats for different DNS record types
        self.highlighting_rules = []
        
        # A record - blue
        a_format = QTextCharFormat()
        a_format.setForeground(QColor(0, 0, 255))
        a_format.setFontWeight(QFont.Weight.Bold)
        self.highlighting_rules.append((re.compile(r'\bA\s+'), a_format))
        
        # AAAA record - cyan
        aaaa_format = QTextCharFormat()
        aaaa_format.setForeground(QColor(0, 150, 200))
        aaaa_format.setFontWeight(QFont.Weight.Bold)
        self.highlighting_rules.append((re.compile(r'\bAAAA\s+'), aaaa_format))
        
        # MX record - green
        mx_format = QTextCharFormat()
        mx_format.setForeground(QColor(0, 150, 0))
        mx_format.setFontWeight(QFont.Weight.Bold)
        self.highlighting_rules.append((re.compile(r'\bMX\s+'), mx_format))
        
        # TXT record - orange
        txt_format = QTextCharFormat()
        txt_format.setForeground(QColor(255, 140, 0))
        txt_format.setFontWeight(QFont.Weight.Bold)
        self.highlighting_rules.append((re.compile(r'\bTXT\s+'), txt_format))
        
        # NS record - purple
        ns_format = QTextCharFormat()
        ns_format.setForeground(QColor(150, 0, 200))
        ns_format.setFontWeight(QFont.Weight.Bold)
        self.highlighting_rules.append((re.compile(r'\bNS\s+'), ns_format))
        
        # IP addresses - gray
        ip_format = QTextCharFormat()
        ip_format.setForeground(QColor(100, 100, 100))
        ipv4_pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
        ipv6_pattern = re.compile(r'\b(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\b')
        self.highlighting_rules.append((ipv4_pattern, ip_format))
        self.highlighting_rules.append((ipv6_pattern, ip_format))
        
        # Domain names - dark blue
        domain_format = QTextCharFormat()
        domain_format.setForeground(QColor(0, 100, 200))
        domain_pattern = re.compile(r'\b[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*\b')
        self.highlighting_rules.append((domain_pattern, domain_format))
    
    def highlightBlock(self, text):
        for pattern, format in self.highlighting_rules:
            for match in pattern.finditer(text):
                start, end = match.span()
                self.setFormat(start, end - start, format)


class CloudflareAPIThread(QThread):
    finished = Signal(list)
    error = Signal(str)
    
    def __init__(self, token):
        super().__init__()
        self.token = token
    
    def run(self):
        print(f"[Cloudflare API] Fetching domains with token...")
        domains = []
        
        try:
            # Clean and validate token
            token = self.token.strip()
            if not token:
                self.error.emit("Token is empty")
                return
            
            # Check if token looks like an API key (contains @) vs API token
            # API tokens are typically longer and don't contain @
            # For now, we'll assume it's an API token and use Bearer format
            # If it fails, we can try API key format
            
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            print(f"[Cloudflare API] Using Authorization header format: Bearer <token>")
            
            # Fetch zones (domains) from Cloudflare API
            url = "https://api.cloudflare.com/client/v4/zones"
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    zones = data.get("result", [])
                    domains = [zone.get("name", "") for zone in zones if zone.get("name")]
                    print(f"[Cloudflare API] Found {len(domains)} domain(s)")
                    for domain in domains:
                        print(f"[Cloudflare API] Domain: {domain}")
                else:
                    error_msg = data.get("errors", [{}])[0].get("message", "Unknown error")
                    print(f"[Cloudflare API] API error: {error_msg}")
                    self.error.emit(error_msg)
            elif response.status_code == 400:
                # Try to parse error details
                try:
                    error_data = response.json()
                    errors = error_data.get("errors", [])
                    if errors:
                        error_code = errors[0].get("code", "")
                        error_msg = errors[0].get("message", "Unknown error")
                        print(f"[Cloudflare API] Error {error_code}: {error_msg}")
                        
                        # If it's an authorization header format error, provide helpful message
                        if error_code == 6111 or "Authorization header" in error_msg:
                            self.error.emit("Invalid token format. Please ensure you're using a Cloudflare API Token (not API Key). Token should start with the token value directly.")
                        else:
                            self.error.emit(f"API error: {error_msg}")
                    else:
                        self.error.emit(f"HTTP error {response.status_code}: {response.text}")
                except:
                    self.error.emit(f"HTTP error {response.status_code}: {response.text}")
            elif response.status_code == 401:
                print(f"[Cloudflare API] Authentication failed - invalid token")
                self.error.emit("Invalid token - authentication failed. Please check your API token.")
            else:
                print(f"[Cloudflare API] HTTP error {response.status_code}: {response.text}")
                self.error.emit(f"HTTP error {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"[Cloudflare API] Request error: {e}")
            self.error.emit(f"Request error: {str(e)}")
        except Exception as e:
            print(f"[Cloudflare API] Error: {e}")
            self.error.emit(f"Error: {str(e)}")
        
        self.finished.emit(domains)


class CloudflareZoneDataThread(QThread):
    finished = Signal(dict)
    error = Signal(str)
    
    def __init__(self, token, domain):
        super().__init__()
        self.token = token
        self.domain = domain
    
    def run(self):
        print(f"[Cloudflare Zone] Fetching zone data for {self.domain}...")
        result = {
            "dns_records": [],
            "email_routing": {},
            "email_routing_addresses": [],
            "email_routing_rules": [],
            "email_routing_destinations": [],
            "dmarc_record": {},
            "health_checks": [],
            "zone_settings": {},
            "ssl_settings": {},
            "logs": []
        }
        
        try:
            # Clean and validate token
            token = self.token.strip()
            if not token:
                self.error.emit("Token is empty")
                return
            
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            # Get zone ID first
            zones_url = "https://api.cloudflare.com/client/v4/zones"
            zones_response = requests.get(zones_url, headers=headers, params={"name": self.domain}, timeout=10)
            
            if zones_response.status_code != 200:
                self.error.emit(f"Failed to get zone ID: HTTP {zones_response.status_code}")
                return
            
            zones_data = zones_response.json()
            if not zones_data.get("success") or not zones_data.get("result"):
                self.error.emit("Zone not found")
                return
            
            zone_id = zones_data["result"][0]["id"]
            print(f"[Cloudflare Zone] Zone ID: {zone_id}")
            
            # 1. Fetch DNS records
            print(f"[Cloudflare Zone] Fetching DNS records...")
            try:
                dns_url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"
                dns_response = requests.get(dns_url, headers=headers, timeout=10)
                if dns_response.status_code == 200:
                    dns_data = dns_response.json()
                    if dns_data.get("success"):
                        result["dns_records"] = dns_data.get("result", [])
                        print(f"[Cloudflare Zone] Found {len(result['dns_records'])} DNS record(s)")
            except Exception as e:
                print(f"[Cloudflare Zone] Error fetching DNS records: {e}")
            
            # 2. Fetch Email Routing settings
            print(f"[Cloudflare Zone] Fetching Email Routing settings...")
            try:
                # Email Routing configuration
                email_url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/email/routing"
                email_response = requests.get(email_url, headers=headers, timeout=10)
                if email_response.status_code == 200:
                    email_data = email_response.json()
                    if email_data.get("success"):
                        result["email_routing"] = email_data.get("result", {})
                        print(f"[Cloudflare Zone] Email Routing: {result['email_routing']}")
                
                # Email Routing addresses
                addresses_url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/email/routing/addresses"
                addresses_response = requests.get(addresses_url, headers=headers, timeout=10)
                if addresses_response.status_code == 200:
                    addresses_data = addresses_response.json()
                    if addresses_data.get("success"):
                        result["email_routing_addresses"] = addresses_data.get("result", [])
                        print(f"[Cloudflare Zone] Found {len(result['email_routing_addresses'])} email routing address(es)")
                
                # Email Routing rules
                rules_url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/email/routing/rules"
                rules_response = requests.get(rules_url, headers=headers, timeout=10)
                if rules_response.status_code == 200:
                    rules_data = rules_response.json()
                    if rules_data.get("success"):
                        result["email_routing_rules"] = rules_data.get("result", [])
                        print(f"[Cloudflare Zone] Found {len(result['email_routing_rules'])} email routing rule(s)")
                
                # Email Routing destinations
                destinations_url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/email/routing/destinations"
                destinations_response = requests.get(destinations_url, headers=headers, timeout=10)
                if destinations_response.status_code == 200:
                    destinations_data = destinations_response.json()
                    if destinations_data.get("success"):
                        result["email_routing_destinations"] = destinations_data.get("result", [])
                        print(f"[Cloudflare Zone] Found {len(result['email_routing_destinations'])} email routing destination(s)")
            except Exception as e:
                print(f"[Cloudflare Zone] Error fetching Email Routing: {e}")
            
            # 2.5. Fetch DMARC record from DNS
            print(f"[Cloudflare Zone] Fetching DMARC record...")
            try:
                import dns.resolver
                dmarc_domain = f"_dmarc.{self.domain}"
                txt_records = dns.resolver.resolve(dmarc_domain, 'TXT')
                for rdata in txt_records:
                    txt_parts = []
                    for part in rdata.strings:
                        if isinstance(part, bytes):
                            txt_parts.append(part.decode('utf-8', errors='ignore'))
                        else:
                            txt_parts.append(str(part))
                    txt_value = ''.join(txt_parts)
                    if txt_value.startswith('v=DMARC1'):
                        # Parse DMARC record
                        dmarc_parts = txt_value.split(';')
                        dmarc_data = {}
                        for part in dmarc_parts:
                            part = part.strip()
                            if '=' in part:
                                key, value = part.split('=', 1)
                                dmarc_data[key.strip()] = value.strip()
                        result["dmarc_record"] = {
                            "raw": txt_value,
                            "parsed": dmarc_data
                        }
                        print(f"[Cloudflare Zone] DMARC record found: {txt_value}")
                        break
            except Exception as e:
                print(f"[Cloudflare Zone] No DMARC record found or error: {e}")
            
            # 3. Fetch Health Checks
            print(f"[Cloudflare Zone] Fetching Health Checks...")
            try:
                health_url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/healthchecks"
                health_response = requests.get(health_url, headers=headers, timeout=10)
                if health_response.status_code == 200:
                    health_data = health_response.json()
                    if health_data.get("success"):
                        result["health_checks"] = health_data.get("result", [])
                        print(f"[Cloudflare Zone] Found {len(result['health_checks'])} health check(s)")
            except Exception as e:
                print(f"[Cloudflare Zone] Error fetching Health Checks: {e}")
            
            # 4. Fetch Zone Settings
            print(f"[Cloudflare Zone] Fetching Zone Settings...")
            try:
                settings_url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/settings"
                settings_response = requests.get(settings_url, headers=headers, timeout=10)
                if settings_response.status_code == 200:
                    settings_data = settings_response.json()
                    if settings_data.get("success"):
                        result["zone_settings"] = settings_data.get("result", [])
                        print(f"[Cloudflare Zone] Found {len(result['zone_settings'])} zone setting(s)")
            except Exception as e:
                print(f"[Cloudflare Zone] Error fetching Zone Settings: {e}")
            
            # 5. Fetch SSL/TLS Settings
            print(f"[Cloudflare Zone] Fetching SSL/TLS Settings...")
            try:
                ssl_url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/ssl/universal/settings"
                ssl_response = requests.get(ssl_url, headers=headers, timeout=10)
                if ssl_response.status_code == 200:
                    ssl_data = ssl_response.json()
                    if ssl_data.get("success"):
                        result["ssl_settings"] = ssl_data.get("result", {})
                        print(f"[Cloudflare Zone] SSL Settings: {result['ssl_settings']}")
            except Exception as e:
                print(f"[Cloudflare Zone] Error fetching SSL Settings: {e}")
            
            # 6. Fetch Zone Logs (recent logs)
            print(f"[Cloudflare Zone] Fetching Zone Logs...")
            try:
                # Note: Logs API might require different endpoint or authentication
                logs_url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/logs/received"
                logs_response = requests.get(logs_url, headers=headers, timeout=10)
                if logs_response.status_code == 200:
                    logs_data = logs_response.json()
                    if logs_data.get("success"):
                        result["logs"] = logs_data.get("result", [])
                        print(f"[Cloudflare Zone] Found {len(result['logs'])} log entry(ies)")
            except Exception as e:
                print(f"[Cloudflare Zone] Error fetching Logs: {e}")
            
            print(f"[Cloudflare Zone] Zone data fetch completed for {self.domain}")
            self.finished.emit(result)
            
        except requests.exceptions.RequestException as e:
            print(f"[Cloudflare Zone] Request error: {e}")
            self.error.emit(f"Request error: {str(e)}")
        except Exception as e:
            print(f"[Cloudflare Zone] Error: {e}")
            self.error.emit(f"Error: {str(e)}")


class DNSLookupThread(QThread):
    finished = Signal(dict)
    
    def __init__(self, domain, token=None):
        super().__init__()
        self.domain = domain
        self.token = token
    
    def run(self):
        print(f"[DNS Lookup] Starting lookup for domain: {self.domain}")
        result = {
            "ns1": "",
            "ns2": "",
            "ipv4": "",
            "dns_records": ""
        }
        
        try:
            # Fetch nameservers
            print(f"[DNS Lookup] Fetching nameservers (NS) for {self.domain}...")
            try:
                ns_records = dns.resolver.resolve(self.domain, 'NS')
                ns_list = [str(ns).rstrip('.') for ns in ns_records]
                print(f"[DNS Lookup] Found {len(ns_list)} nameserver(s)")
                if len(ns_list) >= 1:
                    result["ns1"] = ns_list[0]
                    print(f"[DNS Lookup] NS1: {result['ns1']}")
                if len(ns_list) >= 2:
                    result["ns2"] = ns_list[1]
                    print(f"[DNS Lookup] NS2: {result['ns2']}")
            except Exception as e:
                print(f"[DNS Lookup] Error fetching nameservers: {e}")
            
            # Fetch common DNS records
            dns_lines = []
            
            # A record
            print(f"[DNS Lookup] Fetching A records for {self.domain}...")
            try:
                a_records = dns.resolver.resolve(self.domain, 'A')
                print(f"[DNS Lookup] Found {len(a_records)} A record(s)")
                for idx, rdata in enumerate(a_records):
                    dns_lines.append(f"A    {rdata}")
                    print(f"[DNS Lookup] A record: {rdata}")
                    # Store first A record as IPv4
                    if idx == 0:
                        result["ipv4"] = str(rdata)
            except Exception as e:
                print(f"[DNS Lookup] No A records found: {e}")
            
            # AAAA record
            print(f"[DNS Lookup] Fetching AAAA records for {self.domain}...")
            try:
                aaaa_records = dns.resolver.resolve(self.domain, 'AAAA')
                print(f"[DNS Lookup] Found {len(aaaa_records)} AAAA record(s)")
                for rdata in aaaa_records:
                    dns_lines.append(f"AAAA {rdata}")
                    print(f"[DNS Lookup] AAAA record: {rdata}")
            except Exception as e:
                print(f"[DNS Lookup] No AAAA records found: {e}")
            
            # MX record
            print(f"[DNS Lookup] Fetching MX records for {self.domain}...")
            try:
                mx_records = dns.resolver.resolve(self.domain, 'MX')
                print(f"[DNS Lookup] Found {len(mx_records)} MX record(s)")
                for rdata in mx_records:
                    dns_lines.append(f"MX   {rdata.preference} {rdata.exchange}")
                    print(f"[DNS Lookup] MX record: {rdata.preference} {rdata.exchange}")
            except Exception as e:
                print(f"[DNS Lookup] No MX records found: {e}")
            
            # TXT record
            print(f"[DNS Lookup] Fetching TXT records for {self.domain}...")
            try:
                txt_records = dns.resolver.resolve(self.domain, 'TXT')
                print(f"[DNS Lookup] Found {len(txt_records)} TXT record(s)")
                for rdata in txt_records:
                    # Handle both bytes and strings in TXT records
                    txt_parts = []
                    for part in rdata.strings:
                        if isinstance(part, bytes):
                            txt_parts.append(part.decode('utf-8', errors='ignore'))
                        else:
                            txt_parts.append(str(part))
                    txt_value = ''.join(txt_parts)
                    dns_lines.append(f"TXT  {txt_value}")
                    print(f"[DNS Lookup] TXT record: {txt_value}")
            except Exception as e:
                print(f"[DNS Lookup] No TXT records found: {e}")
            
            result["dns_records"] = "\n".join(dns_lines) if dns_lines else ""
            print(f"[DNS Lookup] Total DNS records collected: {len(dns_lines)}")
            print(f"[DNS Lookup] Lookup completed successfully for {self.domain}")
            
        except Exception as e:
            result["error"] = str(e)
            print(f"[DNS Lookup] Error during lookup: {e}")
        
        self.finished.emit(result)


class ConsoleOutputHandler(QObject):
    """Custom stdout handler that emits signals for console output"""
    text_written = Signal(str)
    
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget
        self.original_stdout = sys.stdout
    
    def write(self, text):
        if text.strip():  # Only emit non-empty text
            self.text_written.emit(text)
        self.original_stdout.write(text)  # Also write to original stdout
    
    def flush(self):
        self.original_stdout.flush()


class NullOutputHandler:
    """Null output handler that suppresses all output"""
    def write(self, text):
        pass
    
    def flush(self):
        pass


class ConsoleWidget(QWidget):
    """Widget containing Settings and Console"""
    def __init__(self, parent=None):
        super().__init__(parent)
        
        layout = QVBoxLayout()
        
        # Settings section with checkboxes
        settings_label = QLabel("Settings:")
        layout.addWidget(settings_label)
        
        self.verbose_checkbox = QCheckBox("Verbose")
        self.verbose_checkbox.setChecked(False)
        layout.addWidget(self.verbose_checkbox)
        
        self.autoscroll_checkbox = QCheckBox("AutoScroll")
        self.autoscroll_checkbox.setChecked(True)
        layout.addWidget(self.autoscroll_checkbox)
        
        # Console output area
        layout.addWidget(QLabel("Console:"))
        
        # Create console with matrix-style appearance
        self.console_input = QTextEdit()
        self.console_input.setReadOnly(True)
        self.console_input.setPlaceholderText("Console output will appear here...")
        
        # Set monospace font for console look
        font = QFont("Courier", 10)
        font.setStyleHint(QFont.StyleHint.Monospace)
        self.console_input.setFont(font)
        
        # Set black background with green text (matrix style, no border)
        self.console_input.setStyleSheet("""
            QTextEdit {
                background-color: #000000;
                color: #00ff00;
                border: none;
            }
        """)
        
        layout.addWidget(self.console_input)
        self.setLayout(layout)


class DockableConsoleWidget(QWidget):
    """Dockable widget wrapper for ConsoleWidget that can be detached"""
    def __init__(self, console_widget, parent=None):
        super().__init__(parent)
        self.console_widget = console_widget
        self.detached_window = None
        self.parent_container = None
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Title bar with detach button
        title_bar = QWidget()
        title_bar.setStyleSheet("background-color: #2b2b2b; padding: 4px;")
        title_layout = QHBoxLayout()
        title_layout.setContentsMargins(4, 4, 4, 4)
        
        title_label = QLabel("Console")
        title_label.setStyleSheet("color: #00ff00; font-weight: bold;")
        title_layout.addWidget(title_label)
        
        title_layout.addStretch()
        
        self.detach_button = QPushButton("⊟")
        self.detach_button.setToolTip("Detach/Attach Console")
        self.detach_button.setMaximumWidth(30)
        self.detach_button.clicked.connect(self.toggle_detach)
        title_layout.addWidget(self.detach_button)
        
        title_bar.setLayout(title_layout)
        layout.addWidget(title_bar)
        
        # Add console widget
        layout.addWidget(self.console_widget)
        
        self.setLayout(layout)
    
    def toggle_detach(self):
        """Toggle between attached and detached state"""
        if self.detached_window is None:
            self.detach()
        else:
            self.attach()
    
    def detach(self):
        """Detach the console widget into a separate window"""
        print("[Console] Detaching console window")
        
        # Create detached window
        self.detached_window = QDialog(self)
        self.detached_window.setWindowTitle("Console - Detached")
        self.detached_window.setMinimumSize(600, 400)
        
        # Move console widget to detached window
        layout = self.layout()
        layout.removeWidget(self.console_widget)
        self.console_widget.setParent(self.detached_window)
        
        detached_layout = QVBoxLayout()
        detached_layout.setContentsMargins(0, 0, 0, 0)
        detached_layout.addWidget(self.console_widget)
        self.detached_window.setLayout(detached_layout)
        
        # Update button
        self.detach_button.setText("⊞")
        self.detach_button.setToolTip("Attach Console")
        
        # Show detached window
        self.detached_window.show()
        self.detached_window.finished.connect(self.on_detached_window_closed)
    
    def attach(self):
        """Attach the console widget back to the main window"""
        print("[Console] Attaching console window")
        
        if self.detached_window:
            # Move console widget back
            detached_layout = self.detached_window.layout()
            detached_layout.removeWidget(self.console_widget)
            self.console_widget.setParent(self)
            
            # Add back to main layout (after title bar)
            layout = self.layout()
            layout.addWidget(self.console_widget)
            
            # Close detached window
            self.detached_window.close()
            self.detached_window = None
            
            # Update button
            self.detach_button.setText("⊟")
            self.detach_button.setToolTip("Detach Console")
    
    def on_detached_window_closed(self):
        """Handle when detached window is closed"""
        if self.detached_window:
            self.attach()


class ConsolePage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("Console Wizard")
        self.setSubTitle("Console output and configuration")
        
        # Create widget area for Settings and Console
        layout = QVBoxLayout()
        
        # Create console widget containing Settings and Console
        console_widget = ConsoleWidget()
        
        # Wrap in dockable widget
        self.dockable_console = DockableConsoleWidget(console_widget, self)
        self.console_widget = console_widget  # Keep reference for easy access
        layout.addWidget(self.dockable_console)
        
        # Setup stdout capture
        self.stdout_handler = ConsoleOutputHandler(self.console_widget.console_input)
        self.stdout_handler.text_written.connect(self.append_console_output)
        self.null_handler = NullOutputHandler()
        self.original_stdout = sys.stdout
        sys.stdout = self.stdout_handler  # Default: show output in console
        
        # Connect checkbox signals
        self.console_widget.verbose_checkbox.stateChanged.connect(self.on_verbose_changed)
        self.console_widget.autoscroll_checkbox.stateChanged.connect(self.on_autoscroll_changed)
        
        self.setLayout(layout)
        
        self.registerField("console", self.console_widget.console_input)
        self.registerField("verbose", self.console_widget.verbose_checkbox)
        self.registerField("autoscroll", self.console_widget.autoscroll_checkbox)
    
    def append_console_output(self, text):
        """Append text to console output, ensuring each message starts on a new line"""
        # Get current text to check if we need to add a newline
        current_text = self.console_widget.console_input.toPlainText()
        
        # If console is not empty and doesn't end with newline, add one
        if current_text and not current_text.endswith('\n'):
            text = '\n' + text
        
        # If console is empty, ensure text starts with newline
        elif not current_text and not text.startswith('\n'):
            text = '\n' + text
        
        if self.console_widget.autoscroll_checkbox.isChecked():
            self.console_widget.console_input.moveCursor(self.console_widget.console_input.textCursor().MoveOperation.End)
            self.console_widget.console_input.insertPlainText(text)
            self.console_widget.console_input.moveCursor(self.console_widget.console_input.textCursor().MoveOperation.End)
        else:
            # Insert at current cursor position without auto-scrolling
            self.console_widget.console_input.insertPlainText(text)
    
    def on_autoscroll_changed(self, state):
        """Handle autoscroll checkbox state change"""
        if state == Qt.CheckState.Checked:
            print("[Console Settings] AutoScroll enabled")
        else:
            print("[Console Settings] AutoScroll disabled")
    
    def on_verbose_changed(self, state):
        """Handle verbose checkbox state change"""
        if state == Qt.CheckState.Checked:
            print("[Console Settings] Verbose mode enabled - suppressing stdout")
            sys.stdout = self.null_handler
        else:
            print("[Console Settings] Verbose mode disabled - showing stdout in console")
            sys.stdout = self.stdout_handler
    
    def cleanupPage(self):
        """Restore original stdout when leaving page"""
        sys.stdout = self.original_stdout
    
    def validatePage(self):
        return True


class HostPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("Domain Wizard")
        self.setSubTitle("Enter the domain information")
        
        # Main layout with grid for domain/IP and NS fields
        main_layout = QVBoxLayout()
        
        # Token field at top
        self.token_input = QLineEdit()
        self.token_input.setPlaceholderText("Enter token/password")
        self.token_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.token_input.editingFinished.connect(self.on_token_changed)
        self.token_input.textChanged.connect(self.completeChanged)
        main_layout.addWidget(QLabel("Token:"))
        main_layout.addWidget(self.token_input)
        
        # Separator line
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(separator)
        
        # Grid layout for Domain + IPv4 and NS1 + NS2
        grid_layout = QGridLayout()
        
        # Row 0: Domain and IPv4
        grid_layout.addWidget(QLabel("Domain:"), 0, 0)
        self.domain_input = QComboBox()
        self.domain_input.setEditable(True)
        self.domain_input.lineEdit().setPlaceholderText("Enter or select domain")
        self.domain_input.currentTextChanged.connect(self.on_domain_changed)
        self.domain_input.currentTextChanged.connect(self.completeChanged)
        self.domain_input.lineEdit().editingFinished.connect(self.on_domain_changed)
        self.domain_input.lineEdit().textChanged.connect(self.completeChanged)
        grid_layout.addWidget(self.domain_input, 0, 1)
        
        grid_layout.addWidget(QLabel("IPv4:"), 0, 2)
        self.ipv4_input = QLineEdit()
        self.ipv4_input.setPlaceholderText("IPv4 address")
        self.ipv4_input.setReadOnly(True)
        grid_layout.addWidget(self.ipv4_input, 0, 3)
        
        # Row 1: NS1 and NS2
        grid_layout.addWidget(QLabel("NS1:"), 1, 0)
        self.ns1_input = QLineEdit()
        self.ns1_input.setPlaceholderText("Enter nameserver 1")
        self.ns1_input.setReadOnly(True)
        grid_layout.addWidget(self.ns1_input, 1, 1)
        
        grid_layout.addWidget(QLabel("NS2:"), 1, 2)
        self.ns2_input = QLineEdit()
        self.ns2_input.setPlaceholderText("Enter nameserver 2")
        self.ns2_input.setReadOnly(True)
        grid_layout.addWidget(self.ns2_input, 1, 3)
        
        main_layout.addLayout(grid_layout)
        
        # DNS Record textarea
        self.dns_input = QTextEdit()
        self.dns_input.setPlaceholderText("Enter DNS record")
        self.dns_input.setReadOnly(True)
        self.dns_highlighter = DNSHighlighter(self.dns_input.document())
        main_layout.addWidget(QLabel("DNS Record:"))
        main_layout.addWidget(self.dns_input)
        
        self.setLayout(main_layout)
        self.registerField("domain*", self.domain_input, "currentText")
        self.registerField("token*", self.token_input)
        self.registerField("ipv4", self.ipv4_input)
        self.registerField("ns1", self.ns1_input)
        self.registerField("ns2", self.ns2_input)
        self.registerField("dns", self.dns_input)
        
        self.lookup_thread = None
        self.cloudflare_thread = None
        self.cloudflare_zone_thread = None
        self.cloudflare_zone_data = None
    
    def on_token_changed(self):
        token = self.token_input.text().strip()
        if not token:
            print("[Domain Wizard] Token field is empty, skipping Cloudflare API call")
            return
        
        print(f"[Domain Wizard] Token changed, fetching domains from Cloudflare...")
        self.domain_input.lineEdit().setPlaceholderText("Fetching domains...")
        self.domain_input.setEnabled(False)
        
        # Wait for previous thread to finish if it exists
        if self.cloudflare_thread and self.cloudflare_thread.isRunning():
            self.cloudflare_thread.wait()
        
        # Start Cloudflare API lookup in background thread
        self.cloudflare_thread = CloudflareAPIThread(token)
        self.cloudflare_thread.finished.connect(self.on_cloudflare_finished)
        self.cloudflare_thread.error.connect(self.on_cloudflare_error)
        self.cloudflare_thread.start()
    
    def on_cloudflare_finished(self, domains):
        print(f"[Domain Wizard] Cloudflare API finished, found {len(domains)} domain(s)")
        self.domain_input.clear()
        if domains:
            self.domain_input.addItems(domains)
            print(f"[Domain Wizard] Populated domain dropdown with {len(domains)} domain(s)")
            
            # If only one domain is available, auto-select it
            if len(domains) == 1:
                print(f"[Domain Wizard] Only one domain available, auto-selecting: {domains[0]}")
                self.domain_input.setCurrentIndex(0)
                # Trigger domain changed to fetch DNS info
                self.on_domain_changed()
        else:
            print("[Domain Wizard] No domains found")
        self.domain_input.setEnabled(True)
        self.domain_input.lineEdit().setPlaceholderText("Enter or select domain")
    
    def on_cloudflare_error(self, error_msg):
        print(f"[Domain Wizard] Cloudflare API error: {error_msg}")
        self.domain_input.setEnabled(True)
        self.domain_input.lineEdit().setPlaceholderText(f"Error: {error_msg}")
    
    def on_domain_changed(self):
        domain = self.domain_input.currentText().strip() if isinstance(self.domain_input, QComboBox) else self.domain_input.text().strip()
        if not domain:
            print("[Domain Wizard] Domain field is empty, skipping lookup")
            return
        
        # Prevent duplicate lookups if one is already in progress
        if self.lookup_thread and self.lookup_thread.isRunning():
            print("[Domain Wizard] DNS lookup already in progress, skipping duplicate request")
            return
        
        print(f"[Domain Wizard] Domain changed to: {domain}")
        print("[Domain Wizard] Starting DNS lookup...")
        
        # Wait for previous thread to finish if it exists
        if self.lookup_thread:
            self.lookup_thread.wait()
        
        # Start DNS lookup in background thread
        self.lookup_thread = DNSLookupThread(domain)
        self.lookup_thread.finished.connect(self.on_dns_lookup_finished)
        self.lookup_thread.start()
        
        # Also fetch Cloudflare zone data if token is available
        token = self.token_input.text().strip()
        if token:
            print("[Domain Wizard] Token available, fetching Cloudflare zone data...")
            if self.cloudflare_zone_thread and self.cloudflare_zone_thread.isRunning():
                self.cloudflare_zone_thread.wait()
            
            self.cloudflare_zone_thread = CloudflareZoneDataThread(token, domain)
            self.cloudflare_zone_thread.finished.connect(self.on_cloudflare_zone_finished)
            self.cloudflare_zone_thread.error.connect(self.on_cloudflare_zone_error)
            self.cloudflare_zone_thread.start()
        
        # Show loading state
        self.ipv4_input.setPlaceholderText("Fetching...")
        self.ns1_input.setPlaceholderText("Fetching...")
        self.ns2_input.setPlaceholderText("Fetching...")
        self.dns_input.setPlaceholderText("Fetching DNS records...")
    
    def on_dns_lookup_finished(self, result):
        print("[Domain Wizard] DNS lookup finished, updating fields...")
        
        if result.get("error"):
            print(f"[Domain Wizard] Error in lookup result: {result['error']}")
            self.ipv4_input.setPlaceholderText("Error fetching IPv4")
            self.ns1_input.setPlaceholderText("Error fetching nameservers")
            self.ns2_input.setPlaceholderText("Error fetching nameservers")
            self.dns_input.setPlaceholderText("Error fetching DNS records")
            return
        
        if result.get("ipv4"):
            print(f"[Domain Wizard] Setting IPv4: {result['ipv4']}")
            self.ipv4_input.setText(result["ipv4"])
        if result.get("ns1"):
            print(f"[Domain Wizard] Setting NS1: {result['ns1']}")
            self.ns1_input.setText(result["ns1"])
        if result.get("ns2"):
            print(f"[Domain Wizard] Setting NS2: {result['ns2']}")
            self.ns2_input.setText(result["ns2"])
        if result.get("dns_records"):
            print(f"[Domain Wizard] Setting DNS records ({len(result['dns_records'].split(chr(10)))} lines)")
            self.dns_input.setPlainText(result["dns_records"])
        
        # Reset placeholders
        if not result.get("ipv4"):
            print("[Domain Wizard] No IPv4 found, keeping placeholder")
            self.ipv4_input.setPlaceholderText("IPv4 address")
        if not result.get("ns1"):
            print("[Domain Wizard] No NS1 found, keeping placeholder")
            self.ns1_input.setPlaceholderText("Enter nameserver 1")
        if not result.get("ns2"):
            print("[Domain Wizard] No NS2 found, keeping placeholder")
            self.ns2_input.setPlaceholderText("Enter nameserver 2")
        if not result.get("dns_records"):
            print("[Domain Wizard] No DNS records found, keeping placeholder")
            self.dns_input.setPlaceholderText("Enter DNS record")
        
        print("[Domain Wizard] Fields updated successfully")
        
        # Merge Cloudflare zone data if available
        if self.cloudflare_zone_data:
            self.merge_cloudflare_data()
    
    def on_cloudflare_zone_finished(self, zone_data):
        print("[Domain Wizard] Cloudflare zone data fetched successfully")
        self.cloudflare_zone_data = zone_data
        
        # Merge with existing DNS records if DNS lookup is done
        if not (self.lookup_thread and self.lookup_thread.isRunning()):
            self.merge_cloudflare_data()
    
    def on_cloudflare_zone_error(self, error_msg):
        print(f"[Domain Wizard] Cloudflare zone data error: {error_msg}")
        # Don't block the wizard, just log the error
    
    def merge_cloudflare_data(self):
        """Merge Cloudflare zone data with DNS records display"""
        if not self.cloudflare_zone_data:
            return
        
        current_dns = self.dns_input.toPlainText()
        cloudflare_lines = []
        
        # Add Cloudflare DNS records
        if self.cloudflare_zone_data.get("dns_records"):
            cloudflare_lines.append("\n=== Cloudflare DNS Records ===")
            for record in self.cloudflare_zone_data["dns_records"]:
                record_type = record.get("type", "")
                record_name = record.get("name", "")
                record_content = record.get("content", "")
                record_ttl = record.get("ttl", "")
                cloudflare_lines.append(f"{record_type:6} {record_name:30} {record_content:30} TTL:{record_ttl}")
        
        # Add Email Routing
        if (self.cloudflare_zone_data.get("email_routing") or 
            self.cloudflare_zone_data.get("email_routing_addresses") or
            self.cloudflare_zone_data.get("email_routing_rules") or
            self.cloudflare_zone_data.get("email_routing_destinations")):
            cloudflare_lines.append("\n=== Email Routing ===")
            
            # Email Routing Configuration
            if self.cloudflare_zone_data.get("email_routing"):
                email_routing = self.cloudflare_zone_data["email_routing"]
                cloudflare_lines.append(f"Status: {'Enabled' if email_routing.get('enabled') else 'Disabled'}")
                if email_routing.get("tag"):
                    cloudflare_lines.append(f"Tag: {email_routing.get('tag')}")
                if email_routing.get("name"):
                    cloudflare_lines.append(f"Name: {email_routing.get('name')}")
            
            # Email Routing Addresses
            if self.cloudflare_zone_data.get("email_routing_addresses"):
                cloudflare_lines.append(f"\n  Addresses ({len(self.cloudflare_zone_data['email_routing_addresses'])}):")
                for addr in self.cloudflare_zone_data["email_routing_addresses"]:
                    email = addr.get("email", "N/A")
                    verified = addr.get("verified", False)
                    created = addr.get("created", "N/A")
                    cloudflare_lines.append(f"    - {email} (Verified: {verified}, Created: {created})")
            
            # Email Routing Rules
            if self.cloudflare_zone_data.get("email_routing_rules"):
                cloudflare_lines.append(f"\n  Rules ({len(self.cloudflare_zone_data['email_routing_rules'])}):")
                for rule in self.cloudflare_zone_data["email_routing_rules"]:
                    rule_name = rule.get("name", "Unnamed")
                    rule_tag = rule.get("tag", "N/A")
                    enabled = rule.get("enabled", False)
                    actions = rule.get("actions", [])
                    cloudflare_lines.append(f"    - {rule_name} (Tag: {rule_tag}, Enabled: {enabled})")
                    for action in actions:
                        action_type = action.get("type", "N/A")
                        action_value = action.get("value", [])
                        cloudflare_lines.append(f"      Action: {action_type} -> {action_value}")
            
            # Email Routing Destinations
            if self.cloudflare_zone_data.get("email_routing_destinations"):
                cloudflare_lines.append(f"\n  Destinations ({len(self.cloudflare_zone_data['email_routing_destinations'])}):")
                for dest in self.cloudflare_zone_data["email_routing_destinations"]:
                    dest_email = dest.get("email", "N/A")
                    verified = dest.get("verified", False)
                    created = dest.get("created", "N/A")
                    cloudflare_lines.append(f"    - {dest_email} (Verified: {verified}, Created: {created})")
        
        # Add DMARC Management
        if self.cloudflare_zone_data.get("dmarc_record"):
            cloudflare_lines.append("\n=== DMARC Management ===")
            dmarc = self.cloudflare_zone_data["dmarc_record"]
            cloudflare_lines.append(f"Raw Record: {dmarc.get('raw', 'N/A')}")
            
            if dmarc.get("parsed"):
                parsed = dmarc["parsed"]
                cloudflare_lines.append("\n  Parsed DMARC Policy:")
                
                # Policy (p=)
                policy = parsed.get("p", "none")
                policy_map = {
                    "none": "No action (monitoring only)",
                    "quarantine": "Quarantine messages",
                    "reject": "Reject messages"
                }
                cloudflare_lines.append(f"    Policy: {policy} ({policy_map.get(policy, 'Unknown')})")
                
                # Subdomain Policy (sp=)
                if "sp" in parsed:
                    sp_policy = parsed.get("sp", "none")
                    cloudflare_lines.append(f"    Subdomain Policy: {sp_policy} ({policy_map.get(sp_policy, 'Unknown')})")
                
                # Aggregate Reporting (rua=)
                if "rua" in parsed:
                    rua = parsed.get("rua", "")
                    cloudflare_lines.append(f"    Aggregate Reports: {rua}")
                
                # Forensic Reporting (ruf=)
                if "ruf" in parsed:
                    ruf = parsed.get("ruf", "")
                    cloudflare_lines.append(f"    Forensic Reports: {ruf}")
                
                # Percentage (pct=)
                if "pct" in parsed:
                    pct = parsed.get("pct", "100")
                    cloudflare_lines.append(f"    Percentage: {pct}%")
                
                # Alignment (aspf=, adkim=)
                if "aspf" in parsed:
                    cloudflare_lines.append(f"    SPF Alignment: {parsed.get('aspf', 'r')}")
                if "adkim" in parsed:
                    cloudflare_lines.append(f"    DKIM Alignment: {parsed.get('adkim', 'r')}")
                
                # Failure Options (fo=)
                if "fo" in parsed:
                    cloudflare_lines.append(f"    Failure Options: {parsed.get('fo', '0')}")
                
                # Reporting Interval (ri=)
                if "ri" in parsed:
                    cloudflare_lines.append(f"    Reporting Interval: {parsed.get('ri', '86400')} seconds")
        
        # Add Health Checks
        if self.cloudflare_zone_data.get("health_checks"):
            cloudflare_lines.append("\n=== Health Checks ===")
            for check in self.cloudflare_zone_data["health_checks"]:
                check_name = check.get("name", "Unknown")
                check_status = check.get("status", "Unknown")
                check_address = check.get("address", "N/A")
                cloudflare_lines.append(f"  {check_name}: {check_status} ({check_address})")
        
        # Add Zone Settings
        if self.cloudflare_zone_data.get("zone_settings"):
            cloudflare_lines.append("\n=== Zone Settings ===")
            for setting in self.cloudflare_zone_data["zone_settings"]:
                setting_id = setting.get("id", "Unknown")
                setting_value = setting.get("value", "N/A")
                cloudflare_lines.append(f"  {setting_id}: {setting_value}")
        
        # Add SSL Settings
        if self.cloudflare_zone_data.get("ssl_settings"):
            cloudflare_lines.append("\n=== SSL/TLS Settings ===")
            ssl_settings = self.cloudflare_zone_data["ssl_settings"]
            for key, value in ssl_settings.items():
                cloudflare_lines.append(f"  {key}: {value}")
        
        # Add Logs (limited to last 10)
        if self.cloudflare_zone_data.get("logs"):
            cloudflare_lines.append("\n=== Recent Logs ===")
            logs = self.cloudflare_zone_data["logs"][:10]  # Limit to 10 most recent
            for log in logs:
                cloudflare_lines.append(f"  {log}")
        
        # Combine with existing DNS records
        if current_dns:
            combined = current_dns + "\n" + "\n".join(cloudflare_lines)
        else:
            combined = "\n".join(cloudflare_lines)
        
        self.dns_input.setPlainText(combined)
        print("[Domain Wizard] Cloudflare zone data merged with DNS records")
    
    def cleanupPage(self):
        """Clean up threads when leaving the page"""
        if self.lookup_thread and self.lookup_thread.isRunning():
            print("[Domain Wizard] Waiting for DNS lookup thread to finish...")
            self.lookup_thread.wait(5000)  # Wait up to 5 seconds
        if self.cloudflare_thread and self.cloudflare_thread.isRunning():
            print("[Domain Wizard] Waiting for Cloudflare API thread to finish...")
            self.cloudflare_thread.wait(5000)  # Wait up to 5 seconds
        if self.cloudflare_zone_thread and self.cloudflare_zone_thread.isRunning():
            print("[Domain Wizard] Waiting for Cloudflare zone thread to finish...")
            self.cloudflare_zone_thread.wait(5000)  # Wait up to 5 seconds
    
    def isComplete(self):
        """Override to enable Next button when domain and token are filled"""
        domain = self.domain_input.currentText().strip() if isinstance(self.domain_input, QComboBox) else self.domain_input.text().strip()
        token = self.token_input.text().strip()
        return bool(domain and token)
    
    def validatePage(self):
        """Validate page when Next is clicked"""
        domain = self.domain_input.currentText().strip() if isinstance(self.domain_input, QComboBox) else self.domain_input.text().strip()
        if not domain:
            return False
        if not self.token_input.text().strip():
            return False
        return True


class EmailPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("Email Configuration")
        self.setSubTitle("Select email from Cloudflare Email Routing")
        
        layout = QVBoxLayout()
        
        self.email_input = QComboBox()
        self.email_input.setEditable(True)
        self.email_input.lineEdit().setPlaceholderText("Select or enter email address")
        layout.addWidget(QLabel("Email:"))
        layout.addWidget(self.email_input)
        
        self.setLayout(layout)
        self.registerField("email*", self.email_input, "currentText")
    
    def initializePage(self):
        """Populate email dropdown when page is shown"""
        # Get email routing data from the previous page (HostPage)
        wizard = self.wizard()
        if wizard:
            host_page = wizard.page(1)  # HostPage is the second page (index 1, after ConsolePage)
            if hasattr(host_page, 'cloudflare_zone_data') and host_page.cloudflare_zone_data:
                emails = []
                
                # Get emails from email routing addresses
                if host_page.cloudflare_zone_data.get("email_routing_addresses"):
                    for addr in host_page.cloudflare_zone_data["email_routing_addresses"]:
                        email = addr.get("email", "")
                        if email:
                            verified = addr.get("verified", False)
                            status = "✓" if verified else "✗"
                            emails.append(f"{email} {status}")
                            print(f"[Email Page] Adding email routing address: {email} (Verified: {verified})")
                
                # Get emails from email routing destinations
                if host_page.cloudflare_zone_data.get("email_routing_destinations"):
                    for dest in host_page.cloudflare_zone_data["email_routing_destinations"]:
                        email = dest.get("email", "")
                        if email:
                            verified = dest.get("verified", False)
                            status = "✓" if verified else "✗"
                            emails.append(f"{email} {status}")
                            print(f"[Email Page] Adding email routing destination: {email} (Verified: {verified})")
                
                # Get emails from email routing rules
                if host_page.cloudflare_zone_data.get("email_routing_rules"):
                    for rule in host_page.cloudflare_zone_data["email_routing_rules"]:
                        rule_name = rule.get("name", "Unnamed")
                        
                        # Extract emails from match field (custom addresses - redirect from)
                        match = rule.get("match", {})
                        if match:
                            # Check match.field for email addresses
                            match_field = match.get("field", "")
                            if isinstance(match_field, str) and '@' in match_field:
                                emails.append(f"{match_field} (Custom: {rule_name})")
                                print(f"[Email Page] Adding custom address from rule '{rule_name}': {match_field}")
                            
                            # Check match.value for email addresses
                            match_value = match.get("value", "")
                            if isinstance(match_value, str) and '@' in match_value:
                                emails.append(f"{match_value} (Custom: {rule_name})")
                                print(f"[Email Page] Adding custom address value from rule '{rule_name}': {match_value}")
                            
                            # Check if match is a list or dict with email values
                            if isinstance(match, dict):
                                for key, value in match.items():
                                    if isinstance(value, str) and '@' in value:
                                        emails.append(f"{value} (Custom: {rule_name})")
                                        print(f"[Email Page] Adding custom address from rule '{rule_name}' {key}: {value}")
                                    elif isinstance(value, list):
                                        for item in value:
                                            if isinstance(item, str) and '@' in item:
                                                emails.append(f"{item} (Custom: {rule_name})")
                                                print(f"[Email Page] Adding custom address from rule '{rule_name}' {key}: {item}")
                        
                        # Extract emails from actions (redirect to)
                        actions = rule.get("actions", [])
                        for action in actions:
                            action_type = action.get("type", "")
                            action_value = action.get("value", [])
                            # Extract emails from action values
                            if isinstance(action_value, list):
                                for value in action_value:
                                    if isinstance(value, str) and '@' in value:
                                        # Check if it's an email address
                                        emails.append(f"{value} (Rule: {rule_name})")
                                        print(f"[Email Page] Adding email from rule '{rule_name}': {value}")
                            elif isinstance(action_value, str) and '@' in action_value:
                                emails.append(f"{action_value} (Rule: {rule_name})")
                                print(f"[Email Page] Adding email from rule '{rule_name}': {action_value}")
                
                # Remove duplicates while preserving order
                seen = set()
                unique_emails = []
                for email in emails:
                    # Extract just the email part for comparison
                    email_part = email.split(' ')[0] if ' ' in email else email
                    if email_part not in seen:
                        seen.add(email_part)
                        unique_emails.append(email)
                emails = unique_emails
                
                # Populate the dropdown
                if emails:
                    self.email_input.clear()
                    self.email_input.addItems(emails)
                    print(f"[Email Page] Populated {len(emails)} email(s) from Cloudflare Email Routing")
                else:
                    print("[Email Page] No emails found in Cloudflare Email Routing")
                    self.email_input.lineEdit().setPlaceholderText("No emails found - enter manually")
    
    def validatePage(self):
        email = self.email_input.currentText().strip() if isinstance(self.email_input, QComboBox) else self.email_input.text().strip()
        # Remove status indicators if present
        email = email.split(' ')[0] if ' ' in email else email
        if not email:
            return False
        # Basic email validation
        return '@' in email and '.' in email.split('@')[1] if '@' in email else False


class UserPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("User Configuration")
        self.setSubTitle("Enter the user information")
        
        layout = QGridLayout()
        
        # Row 0: User and Password
        layout.addWidget(QLabel("User:"), 0, 0)
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Enter username")
        layout.addWidget(self.user_input, 0, 1)
        
        layout.addWidget(QLabel("Password:"), 0, 2)
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input, 0, 3)
        
        # Row 1: Email (rules) and Role
        layout.addWidget(QLabel("Email:"), 1, 0)
        self.rule_input = QComboBox()
        self.rule_input.setEditable(True)
        self.rule_input.lineEdit().setPlaceholderText("Select email routing rule")
        layout.addWidget(self.rule_input, 1, 1)
        
        layout.addWidget(QLabel("Role:"), 1, 2)
        self.role_input = QLineEdit()
        self.role_input.setPlaceholderText("Enter role")
        layout.addWidget(self.role_input, 1, 3)
        
        self.setLayout(layout)
        self.registerField("user*", self.user_input)
        self.registerField("password*", self.password_input)
        self.registerField("rule", self.rule_input, "currentText")
        self.registerField("role", self.role_input)
    
    def initializePage(self):
        """Populate email routing rules when page is shown"""
        # Get email routing rules from the HostPage
        wizard = self.wizard()
        if wizard:
            host_page = wizard.page(0)  # HostPage is the first page (index 0)
            if hasattr(host_page, 'cloudflare_zone_data') and host_page.cloudflare_zone_data:
                rules = []
                
                # Get email routing rules
                if host_page.cloudflare_zone_data.get("email_routing_rules"):
                    for rule in host_page.cloudflare_zone_data["email_routing_rules"]:
                        rule_name = rule.get("name", "Unnamed")
                        rule_tag = rule.get("tag", "")
                        enabled = rule.get("enabled", False)
                        status = "✓" if enabled else "✗"
                        
                        # Format rule display
                        rule_display = f"{rule_name}"
                        if rule_tag:
                            rule_display += f" (Tag: {rule_tag})"
                        rule_display += f" {status}"
                        
                        rules.append(rule_display)
                        print(f"[User Page] Adding email routing rule: {rule_name} (Enabled: {enabled})")
                
                # Populate the dropdown
                if rules:
                    self.rule_input.clear()
                    self.rule_input.addItems(rules)
                    print(f"[User Page] Populated {len(rules)} email routing rule(s)")
                else:
                    print("[User Page] No email routing rules found")
                    self.rule_input.lineEdit().setPlaceholderText("No rules found - enter manually")
    
    def validatePage(self):
        return bool(self.user_input.text().strip() and self.password_input.text().strip())


class DataPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("Data Configuration")
        self.setSubTitle("Enter the data information")
        
        layout = QVBoxLayout()
        
        self.data_input = QTextEdit()
        self.data_input.setPlaceholderText("Enter data")
        layout.addWidget(QLabel("Data:"))
        layout.addWidget(self.data_input)
        
        self.setLayout(layout)
        self.registerField("data*", self.data_input)
    
    def validatePage(self):
        return bool(self.data_input.toPlainText().strip())


class Wizard(QWizard):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Space Wizard")
        self.setWizardStyle(QWizard.WizardStyle.ModernStyle)
        
        self.console_page = ConsolePage()
        self.host_page = HostPage()
        self.email_page = EmailPage()
        self.user_page = UserPage()
        self.data_page = DataPage()
        
        self.addPage(self.console_page)
        self.addPage(self.host_page)
        self.addPage(self.email_page)
        self.addPage(self.user_page)
        self.addPage(self.data_page)
    
    def getResults(self):
        return {
            "console": self.field("console"),
            "domain": self.field("domain"),
            "token": self.field("token"),
            "ipv4": self.field("ipv4"),
            "ns1": self.field("ns1"),
            "ns2": self.field("ns2"),
            "dns": self.field("dns"),
            "email": self.field("email"),
            "user": self.field("user"),
            "password": self.field("password"),
            "rule": self.field("rule"),
            "role": self.field("role"),
            "data": self.field("data")
        }

