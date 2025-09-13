import requests
import random
import string
import time
from colorama import Fore, init
from dataclasses import dataclass

@dataclass
class UserAgentComponents:
    device: str
    os: str
    os_version: str
    webkit_version: str
    safari_version: str
    mobile_component: str = ""
    is_mobile: bool = True

@dataclass
class InstagramComponents:
    version: str
    device: str
    android_version: str
    dpi: str
    resolution: str
    device_id: str
    build_id: str
    session_id: str
    phone_id: str
    language: str
    locale: str

class UserAgentGenerator:
    def __init__(self):
        self.devices = {
            'apple_mobile': [
                'iPhone', 'iPhone SE', 'iPhone 8', 'iPhone 8 Plus', 'iPhone X', 
                'iPhone 11', 'iPhone 12', 'iPhone 13', 'iPhone 14', 'iPhone 15',
                'iPod Touch'
            ],
            'apple_tablet': [
                'iPad', 'iPad Air', 'iPad Pro', 'iPad Mini'
            ],
            'apple_desktop': [
                'Macintosh'
            ],
            'android_mobile': [
                'Samsung Galaxy S8', 'Samsung Galaxy S9', 'Samsung Galaxy S10',
                'Samsung Galaxy S20', 'Samsung Galaxy S21', 'Samsung Galaxy S22',
                'Samsung Galaxy S23', 'Google Pixel 3', 'Google Pixel 4',
                'Google Pixel 5', 'Google Pixel 6', 'Google Pixel 7',
                'OnePlus 8', 'OnePlus 9', 'OnePlus 10', 'OnePlus Nord',
                'Xiaomi Mi 10', 'Xiaomi Mi 11', 'Xiaomi Redmi Note 10',
                'Huawei P30', 'Huawei P40', 'Huawei Mate 40'
            ],
            'android_tablet': [
                'Samsung Galaxy Tab S6', 'Samsung Galaxy Tab S7',
                'Samsung Galaxy Tab S8', 'Amazon Kindle Fire',
                'Amazon Fire HD 8', 'Amazon Fire HD 10'
            ],
            'windows_desktop': [
                'Windows NT 10.0', 'Windows NT 6.3', 'Windows NT 6.2'
            ],
            'linux_desktop': [
                'X11; Linux x86_64', 'X11; Ubuntu; Linux x86_64',
                'X11; Fedora; Linux x86_64'
            ]
        }

        self.os_versions = {
            'ios': [(f"{major}_{minor}" if minor != 0 else f"{major}") 
                   for major in range(14, 18) 
                   for minor in range(0, 5)],
            'macos': ['10_15', '11_0', '12_0', '12_1', '12_2', '12_3', '12_4', 
                     '13_0', '13_1', '13_2', '13_3', '13_4', '14_0'],
            'android': [f"{major}.{minor}" 
                        for major in range(9, 14) 
                        for minor in range(0, 5)],
            'windows': ['10.0', '6.3', '6.2'],
            'linux': ['', 'Ubuntu', 'Fedora']
        }

        self.webkit_versions = {
            'apple': ['605.1.15', '606.1.36', '607.1.40', '608.1.38'],
            'android': ['537.36'],
            'desktop': ['537.36', '605.1.15']
        }

        self.safari_versions = {
            'mobile': ['16.0', '16.1', '16.2', '16.3', '16.4', '16.5', '16.6',
                      '17.0', '17.1', '17.2', '17.3'],
            'desktop': ['15.6', '16.0', '16.1', '16.2', '16.3', '16.4', '16.5',
                        '17.0', '17.1', '17.2']
        }

    def _select_platform(self):
        return random.choices(
            ['mobile', 'tablet', 'desktop'],
            weights=[60, 20, 20],
            k=1
        )[0]

    def _generate_apple_components(self, device_type):
        if device_type == 'mobile':
            device = random.choice(self.devices['apple_mobile'])
            os = 'iPhone OS'
            os_version = random.choice(self.os_versions['ios'])
            mobile = f"Mobile/{random.choice(['15E148', '15E216', '15E302'])}"
        elif device_type == 'tablet':
            device = random.choice(self.devices['apple_tablet'])
            os = 'CPU OS'
            os_version = random.choice(self.os_versions['ios'])
            mobile = f"Mobile/{random.choice(['15E148', '15E216'])}"
        else:
            device = random.choice(self.devices['apple_desktop'])
            os = 'Macintosh'
            os_version = random.choice(self.os_versions['macos'])
            mobile = ""

        return UserAgentComponents(
            device=device,
            os=os,
            os_version=os_version,
            webkit_version=random.choice(self.webkit_versions['apple']),
            safari_version=random.choice(self.safari_versions['mobile' if device_type != 'desktop' else 'desktop']),
            mobile_component=mobile,
            is_mobile=(device_type != 'desktop')
        )

    def _generate_android_components(self, device_type):
        if device_type == 'mobile':
            device = random.choice(self.devices['android_mobile'])
            mobile = "Mobile"
        else:
            device = random.choice(self.devices['android_tablet'])
            mobile = ""

        return UserAgentComponents(
            device=device,
            os='Android',
            os_version=random.choice(self.os_versions['android']),
            webkit_version=random.choice(self.webkit_versions['android']),
            safari_version='',
            mobile_component=mobile,
            is_mobile=True
        )

    def _generate_desktop_components(self, os_type):
        if os_type == 'windows':
            device = random.choice(self.devices['windows_desktop'])
            os = 'Windows NT'
            os_version = random.choice(self.os_versions['windows'])
        else:
            device = random.choice(self.devices['linux_desktop'])
            os = 'X11'
            os_version = random.choice(self.os_versions['linux'])

        return UserAgentComponents(
            device=device,
            os=os,
            os_version=os_version,
            webkit_version=random.choice(self.webkit_versions['desktop']),
            safari_version=random.choice(self.safari_versions['desktop']),
            mobile_component="",
            is_mobile=False
        )

    def _generate_instagram_android_components(self):
        instagram_versions = [
            "357.1.0.52.100", "356.0.0.30.115", "355.0.0.22.110", 
            "354.0.0.16.97", "353.0.0.12.98", "352.0.0.14.100", 
            "351.0.0.22.108", "350.0.0.18.92", "349.0.0.20.104", 
            "348.0.0.11.76", "347.0.0.21.120", "346.0.0.25.118",
            "345.0.0.19.113", "344.0.0.17.105", "343.0.0.15.99"
        ]
        
        android_devices = [
            "Pixel 5", "Pixel 6", "Pixel 7", "Pixel 8",
            "Samsung Galaxy S21", "Samsung Galaxy S22", "Samsung Galaxy S23",
            "Samsung Galaxy S20", "Samsung Galaxy Note 20",
            "iPhone 12", "iPhone 13", "iPhone 14", "iPhone 15",
            "OnePlus 9", "OnePlus 10", "OnePlus 11",
            "Xiaomi Mi 11", "Xiaomi Mi 12", "Xiaomi 13",
            "Huawei P30", "Huawei P40", "Huawei P50",
            "Motorola Edge 30", "Motorola Edge 40",
            "Oppo Find X3", "Oppo Find X5", "Oppo Find X6",
            "Vivo X80", "Vivo X90",
            "Realme GT 2", "Realme GT 3"
        ]
        
        android_versions = [
            ("28", "9"), ("29", "10"), ("30", "11"), 
            ("31", "12"), ("32", "12L"), ("33", "13"),
            ("34", "14")
        ]
        
        dpis = ["320", "360", "420", "480", "560", "640"]
        resolutions = [
            "720x1280", "1080x1920", "1080x2160", 
            "1440x2560", "1440x3120", "900x1600"
        ]
        
        languages = ["en", "es", "fr", "de", "it", "pt", "ru", "ja", "zh"]
        locales = {
            "en": ["US", "GB", "AU", "CA", "IN"],
            "es": ["ES", "MX", "AR"],
            "fr": ["FR", "CA"],
            "de": ["DE", "AT"],
            "pt": ["PT", "BR"],
        }
        
        version = random.choice(instagram_versions)
        device = random.choice(android_devices)
        android_ver, sdk_ver = random.choice(android_versions)
        dpi = random.choice(dpis)
        resolution = random.choice(resolutions)
        
        language = random.choice(languages)
        locale_options = locales.get(language, ["US"])
        locale = random.choice(locale_options)
        
        def generate_id(length=16):
            return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
        
        device_id = generate_id()
        build_id = generate_id()
        session_id = generate_id()
        phone_id = generate_id()
        
        return InstagramComponents(
            version=version,
            device=device,
            android_version=f"{android_ver}/{sdk_ver}",
            dpi=dpi,
            resolution=resolution,
            device_id=device_id,
            build_id=build_id,
            session_id=session_id,
            phone_id=phone_id,
            language=language,
            locale=locale
        )

    def generate(self):
        platform = self._select_platform()

        if platform in ['mobile', 'tablet']:
            if random.random() < 0.7:
                components = self._generate_apple_components(platform)
            else:
                components = self._generate_android_components(platform)
        else:
            if random.random() < 0.6:
                components = self._generate_desktop_components('windows')
            else:
                components = self._generate_desktop_components('linux')

        if components.os in ['iPhone OS', 'CPU OS']:
            return (f"Mozilla/5.0 ({components.device}; {components.os} {components.os_version} "
                    f"like Mac OS X) AppleWebKit/{components.webkit_version} "
                    f"(KHTML, like Gecko) Version/{components.safari_version.split('.')[0]}.0 "
                    f"{components.mobile_component} Safari/{components.webkit_version}")
        elif components.os == 'Android':
            if components.mobile_component:
                return (f"Mozilla/5.0 (Linux; Android {components.os_version}; "
                        f"{components.device}) AppleWebKit/{components.webkit_version} "
                        f"(KHTML, like Gecko) Chrome/{random.randint(90, 115)}.0.0.0 "
                        f"{components.mobile_component} Safari/{components.webkit_version}")
            else:
                return (f"Mozilla/5.0 (Linux; Android {components.os_version}; "
                        f"{components.device}) AppleWebKit/{components.webkit_version} "
                        f"(KHTML, like Gecko) Safari/{components.webkit_version}")
        else:
            if components.os == 'Macintosh':
                return (f"Mozilla/5.0 (Macintosh; Intel Mac OS X {components.os_version}) "
                        f"AppleWebKit/{components.webkit_version} (KHTML, like Gecko) "
                        f"Version/{components.safari_version} Safari/{components.webkit_version}")
            elif components.os == 'Windows NT':
                return (f"Mozilla/5.0 (Windows; {components.device}) "
                        f"AppleWebKit/{components.webkit_version} (KHTML, like Gecko) "
                        f"Chrome/{random.randint(90, 115)}.0.0.0 Safari/{components.webkit_version}")
            else:
                return (f"Mozilla/5.0 ({components.device}) "
                        f"AppleWebKit/{components.webkit_version} (KHTML, like Gecko) "
                        f"Chrome/{random.randint(90, 115)}.0.0.0 Safari/{components.webkit_version}")

    def generate_instagram_android(self):
        components = self._generate_instagram_android_components()
        
        return (
            f"Instagram {components.version} Android "
            f"({components.android_version}; {components.dpi}dpi; {components.resolution}; "
            f"{components.device}/{components.device_id}/{components.build_id}; "
            f"{components.session_id}; {components.phone_id}; "
            f"{components.language}_{components.locale};)"
        )
init(autoreset=True)

class GithubChecker:
    def __init__(self):
        self.checked = 0
        self.user = ""
        self.available = 0
        self.unavailable = 0
        self.deleted = 0
        self.run = True
        self.target_available = 1005
        self.proxies = None
        self.proxymod = None
        self.proxy_type = None
        self.P = []
        
        print(f"{Fore.CYAN}===== Github Username Checker =====")
        
        self.proxymod = input("Use proxies? (p)aid/(f)ree/(n)o: ").strip().lower()
        if self.proxymod == "p":
            self.proxy_type = input("Proxy type:\n1. http ip:port\n2. socks4\n3. socks5\n4. user:pass@host:port\n5. host:port:user:pass\n6. ip:port:user:pass\n7. user:pass:host:port\nEnter choice (1-7): ").strip()
            proxy_file = input("Enter proxy file path: ").strip()
            try:
                with open(proxy_file, 'r') as file:
                    self.P = [line.strip() for line in file if line.strip()]
                    if not self.P:
                        print(f"{Fore.RED}No valid proxies found in file. Continuing without proxy.")
                        self.proxymod = "n"
                    else:
                        print(f"{Fore.GREEN}Loaded {len(self.P)} proxies.")
            except FileNotFoundError:
                print(f"{Fore.RED}Proxy file not found. Continuing without proxy.")
                self.proxymod = "n"
            except Exception as e:
                print(f"{Fore.RED}Error loading proxy: {str(e)}. Continuing without proxy.")
                self.proxymod = "n"
        elif self.proxymod == "f":
            print(f"{Fore.GREEN}Will use free proxies from public sources.")
        else:
            print(f"{Fore.YELLOW}Continuing without proxy.")
            self.proxymod = "n"
        
        self.mode = input(f"Choose mode:\n1. Check from file\n2. Check random usernames\n3. Check specific username\n4. Check with semi-username patterns\nEnter choice (1-4): ").strip()
        
        if self.mode == "1":
            self.file_path = input("Enter file path containing usernames: ").strip()
            self.usernames = self.load_usernames()
        elif self.mode == "2":
            self.length = int(input("Enter username length: ").strip())
            self.count = int(input("Enter number of usernames to check (or press Enter for unlimited until 1005 available): ").strip() or 0)
        elif self.mode == "3":
            self.username = input("Enter username to check: ").strip()
        elif self.mode == "4":
            self.count = int(input("Enter number of usernames to check (or press Enter for unlimited until 1005 available): ").strip() or 0)
        else:
            print(f"{Fore.RED}Invalid choice. Exiting.")
            exit()
            
        self.start()
    
    def load_usernames(self):
        try:
            with open(self.file_path, 'r') as file:
                return [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            print(f"{Fore.RED}File not found. Exiting.")
            exit()
    
    def generate_random_username(self):
        return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(self.length))
    
    def generate_semi_usernames(self):
        chars = string.ascii_lowercase + string.digits
        patterns = [
            lambda: f"{random.choice(chars)}_{random.choice(chars)}{random.choice(chars)}",
            lambda: f"{random.choice(chars)}-{random.choice(chars)}{random.choice(chars)}",
            lambda: f"{random.choice(chars)}_{random.choice(chars)}",
            lambda: f"{random.choice(chars)}-{random.choice(chars)}"
        ]
        return random.choice(patterns)()
    
    def proxynew(self):
        if self.proxymod == "p":
            self.mode = "Paid Proxy"
            if not self.P:
                print(f"{Fore.RED} No proxies available in the list")
                return None
                
            self.proxy = random.choice(self.P)
            if self.proxy_type == '1':
                self.proxymode = "http ip:port"
                return {
                    'http': f'http://{self.proxy}',
                    'https': f'http://{self.proxy}'
                }
            elif self.proxy_type == '2':
                self.proxymode = "socks4"
                return {
                    'http': f'socks4://{self.proxy}',
                    'https': f'socks4://{self.proxy}'
                }
            elif self.proxy_type == '3':
                self.proxymode = "socks5"
                return {
                    'http': f'socks5://{self.proxy}',
                    'https': f'socks5://{self.proxy}'
                }
            elif self.proxy_type == '4':
                self.proxymode = "user:pass@host:port"
                return {
                    'http': f'http://{self.proxy}',
                    'https': f'http://{self.proxy}'
                }
            elif self.proxy_type == '5':
                self.proxymode = "host:port:user:pass"
                host_port, user_pass = self.proxy.split(':', 1)
                user, password = user_pass.split(':', 1)
                return {
                    'http': f'http://{user}:{password}@{host_port}',
                    'https': f'http://{user}:{password}@{host_port}'
                }
            elif self.proxy_type == '6':
                self.proxymode = "ip:port:user:pass"
                ip_port, user_pass = self.proxy.split(':', 1)
                user, password = user_pass.split(':', 1)
                return {
                    'http': f'http://{user}:{password}@{ip_port}',
                    'https': f'http://{user}:{password}@{ip_port}'
                }
            elif self.proxy_type == '7':
                self.proxymode = "user:pass:host:port"
                user_pass, host_port = self.proxy.split(':', 1)
                user, password = user_pass.split(':', 1)
                return {
                    'http': f'http://{user}:{password}@{host_port}',
                    'https': f'http://{user}:{password}@{host_port}'
                }
        elif self.proxymod == "f":
            self.mode = "Free proxy"
            proxy = self.get_free_proxy()
            if proxy:
                return {'http': f'http://{proxy}', 'https': f'http://{proxy}'}
        return None
    
    def get_free_proxy(self):
        sources = [
            "https://raw.githubusercontent.com/ProxyScraper/ProxyScraper/main/http.txt",
            "https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&protocol=http&proxy_format=protocolipport&format=text&timeout=20000",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
            "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt"
        ]
        
        for source in sources:
            try:
                response = requests.get(source, timeout=10)
                if response.status_code == 200:
                    proxies = [p.strip() for p in response.text.splitlines() if ":" in p]
                    if "api.proxyscrape.com" in source:
                        proxies = [p.replace("http://", "") for p in proxies if p.startswith("http://")]
                    if proxies:
                        return random.choice(proxies)
            except:
                continue
        return None
    
    def check_username(self, username):
        max_retries = 3
        retry_delay = 2
        
        if self.proxymod in ["p", "f"]:
            self.proxies = self.proxynew()
        
        for attempt in range(max_retries):
            try:
                self.user = username
                url='https://github.com/signup_check/username'
                params={'value': self.user}
                headers={'Host': 'github.com','Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126"','Accept-Language': 'en-US','Sec-Ch-Ua-Mobile': '?0','User-Agent': UserAgentGenerator().generate(),'Sec-Ch-Ua-Platform': '"Windows"','Accept': '*/*','Sec-Fetch-Site': 'same-origin','Sec-Fetch-Mode': 'cors','Sec-Fetch-Dest': 'empty','Referer': 'https://github.com/signup','Priority': 'u=1, i',}
                
                response = requests.get(url,params=params, headers=headers, proxies=self.proxies)
                with open("ress.txt", "a", encoding="utf-8") as file:
                    file.write(f"[{self.user}] {response.text}\n")

                if f'{self.user} is available' in response.text:
                    self.available += 1
                    with open("available_Github.txt", "a", encoding="utf-8") as file:
                        file.write(f"{self.user}\n")
                elif f'Username {self.user} is not available' in response.text:
                    self.unavailable += 1
                else:
                    self.unavailable += 1
                
                self.checked += 1
                break  
                
            except Exception as e:
                if self.proxymod in ["p", "f"] and attempt < max_retries - 1:
                    print(f"{Fore.YELLOW}[RETRY] {username}: {str(e)}. Switching proxy...")
                    self.proxies = self.proxynew()
                    time.sleep(1) 
                elif attempt < max_retries - 1:
                    print(f"{Fore.YELLOW}[RETRY] {username}: {str(e)}. Retrying in {retry_delay}s...")
                    time.sleep(retry_delay)
                    retry_delay *= 2 
                else:
                    print(f"{Fore.YELLOW}[ERROR] {username}: {str(e)} after {max_retries} attempts")
    
    def print_status(self):
        print(f"\r{Fore.CYAN}Checked: {self.checked} | {Fore.GREEN}Available: {self.available} | {Fore.RED}Unavailable: {self.unavailable} | {Fore.YELLOW}Deleted: {self.deleted} | {Fore.MAGENTA} username :{self.user}", end='', flush=True)
    
    def start(self):
        print(f"{Fore.CYAN}Starting username checker...")
        
        try:
            if self.mode == "1":
                for username in self.usernames:
                    if not self.run or self.available >= self.target_available:
                        break
                    self.check_username(username)
                    self.print_status()
                    time.sleep(random.uniform(1.5, 3.0))
                print(f"\n{Fore.YELLOW}All usernames checked from file.")
                
            elif self.mode == "2":
                checked = 0
                while (self.count == 0 or checked < self.count) and self.run and self.available < self.target_available:
                    username = self.generate_random_username()
                    self.check_username(username)
                    checked += 1
                    self.print_status()
                    time.sleep(random.uniform(1.5, 3.0))
                if self.count > 0:
                    print(f"\n{Fore.YELLOW}Completed checking {self.count} random usernames.")
                else:
                    print(f"\n{Fore.GREEN}Target of {self.target_available} available usernames reached!")
                    
            elif self.mode == "3":
                self.check_username(self.username)
                self.print_status()
                print("\nUsername check completed.")
                
            elif self.mode == "4":
                checked = 0
                while (self.count == 0 or checked < self.count) and self.run and self.available < self.target_available:
                    username = self.generate_semi_usernames()
                    self.check_username(username)
                    checked += 1
                    self.print_status()
                    time.sleep(random.uniform(1.5, 3.0)) 
                
                if self.count > 0:
                    print(f"\n{Fore.YELLOW}Completed checking {self.count} random usernames.")
                else:
                    print(f"\n{Fore.GREEN}Target of {self.target_available} available usernames reached!")
                
        except KeyboardInterrupt:
            self.run = False
            print(f"\n{Fore.YELLOW}Interrupted by user. Stopping...")
        
        print(f"\n{Fore.CYAN}Final Results:")
        print(f"{Fore.CYAN}Checked: {self.checked} | {Fore.GREEN}Available: {self.available} | {Fore.RED}Unavailable: {self.unavailable} | {Fore.YELLOW}Deleted: {self.deleted}")
        
        if self.available > 0:
            print(f"{Fore.GREEN}Available usernames saved in available_Github.txt")

if __name__ == "__main__":
    GithubChecker()