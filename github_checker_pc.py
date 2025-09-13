import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
import threading
import requests
import random
import sys
import ctypes
import string
import time
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
def hidecmd():
    if sys.platform == "win32":
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

class GithubCheckerGUI:
    def __init__(self, root):
        hidecmd()
        self.root = root
        self.root.title("Github Username Checker")
        self.root.geometry("800x600")
        self.root.configure(bg="#2c3e50")
        try:
            self.root.iconbitmap("shadow.ico")
        except Exception:
            pass
        
        self.bg_color = "#2c3e50" 
        self.fg_color = "#2c3e50"  
        self.accent_color = "#3498db"  
        self.success_color = "#2ecc71"  
        self.error_color = "#e74c3c"  
        self.warning_color = "#f39c12"  
        
        self.checked = 0
        self.available = 0
        self.unavailable = 0
        self.deleted = 0
        self.run = False
        self.target_available = 1005
        self.proxies = None
        self.proxymod = "n"
        self.proxy_type = None
        self.P = []
        self.mode = "1"
        self.usernames = []
        self.count = 0
        self.length = 5
        self.username = ""
        
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        self.settings_tab = ttk.Frame(self.notebook)
        self.results_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.settings_tab, text="Settings")
        self.notebook.add(self.results_tab, text="Results")
        
        self.setup_settings_tab()
        
        self.setup_results_tab()
        
        self.status_bar = tk.Label(root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    
    def setup_settings_tab(self):
        proxy_frame = ttk.LabelFrame(self.settings_tab, text="Proxy Settings")
        proxy_frame.pack(fill=tk.X, padx=10, pady=5)
        
        mode_frame = ttk.LabelFrame(self.settings_tab, text="Check Mode")
        mode_frame.pack(fill=tk.X, padx=10, pady=5)
        
        options_frame = ttk.LabelFrame(self.settings_tab, text="Options")
        options_frame.pack(fill=tk.X, padx=10, pady=5)
        
        buttons_frame = ttk.Frame(self.settings_tab)
        buttons_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.proxy_var = tk.StringVar(value="n")
        ttk.Label(proxy_frame, text="Use proxies:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Radiobutton(proxy_frame, text="No", variable=self.proxy_var, value="n", command=self.toggle_proxy_options).grid(row=0, column=1, padx=5, pady=5)
        ttk.Radiobutton(proxy_frame, text="Paid", variable=self.proxy_var, value="p", command=self.toggle_proxy_options).grid(row=0, column=2, padx=5, pady=5)
        ttk.Radiobutton(proxy_frame, text="Free", variable=self.proxy_var, value="f", command=self.toggle_proxy_options).grid(row=0, column=3, padx=5, pady=5)
        
        self.proxy_type_frame = ttk.Frame(proxy_frame)
        self.proxy_type_frame.grid(row=1, column=0, columnspan=4, sticky=tk.W+tk.E, padx=5, pady=5)
        self.proxy_type_frame.grid_remove()
        
        self.proxy_type_var = tk.StringVar(value="1")
        ttk.Label(self.proxy_type_frame, text="Proxy type:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Radiobutton(self.proxy_type_frame, text="HTTP (ip:port)", variable=self.proxy_type_var, value="1").grid(row=0, column=1, padx=5, pady=5)
        ttk.Radiobutton(self.proxy_type_frame, text="SOCKS4", variable=self.proxy_type_var, value="2").grid(row=0, column=2, padx=5, pady=5)
        ttk.Radiobutton(self.proxy_type_frame, text="SOCKS5", variable=self.proxy_type_var, value="3").grid(row=0, column=3, padx=5, pady=5)
        ttk.Radiobutton(self.proxy_type_frame, text="user:pass@host:port", variable=self.proxy_type_var, value="4").grid(row=1, column=0, padx=5, pady=5)
        ttk.Radiobutton(self.proxy_type_frame, text="host:port:user:pass", variable=self.proxy_type_var, value="5").grid(row=1, column=1, padx=5, pady=5)
        ttk.Radiobutton(self.proxy_type_frame, text="ip:port:user:pass", variable=self.proxy_type_var, value="6").grid(row=1, column=2, padx=5, pady=5)
        ttk.Radiobutton(self.proxy_type_frame, text="user:pass:host:port", variable=self.proxy_type_var, value="7").grid(row=1, column=3, padx=5, pady=5)
        
        self.proxy_file_frame = ttk.Frame(proxy_frame)
        self.proxy_file_frame.grid(row=2, column=0, columnspan=4, sticky=tk.W+tk.E, padx=5, pady=5)
        self.proxy_file_frame.grid_remove()
        
        ttk.Label(self.proxy_file_frame, text="Proxy file:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.proxy_file_var = tk.StringVar()
        ttk.Entry(self.proxy_file_frame, textvariable=self.proxy_file_var, width=50).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(self.proxy_file_frame, text="Browse", command=self.browse_proxy_file).grid(row=0, column=2, padx=5, pady=5)
        
        self.mode_var = tk.StringVar(value="1")
        ttk.Label(mode_frame, text="Check mode:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Radiobutton(mode_frame, text="Check from file", variable=self.mode_var, value="1", command=self.toggle_mode_options).grid(row=0, column=1, padx=5, pady=5)
        ttk.Radiobutton(mode_frame, text="Check random usernames", variable=self.mode_var, value="2", command=self.toggle_mode_options).grid(row=0, column=2, padx=5, pady=5)
        ttk.Radiobutton(mode_frame, text="Check specific username", variable=self.mode_var, value="3", command=self.toggle_mode_options).grid(row=1, column=1, padx=5, pady=5)
        ttk.Radiobutton(mode_frame, text="Check with semi-username patterns", variable=self.mode_var, value="4", command=self.toggle_mode_options).grid(row=1, column=2, padx=5, pady=5)
        
        self.file_frame = ttk.Frame(mode_frame)
        self.file_frame.grid(row=2, column=0, columnspan=3, sticky=tk.W+tk.E, padx=5, pady=5)
        
        ttk.Label(self.file_frame, text="Username file:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.file_path_var = tk.StringVar()
        ttk.Entry(self.file_frame, textvariable=self.file_path_var, width=50).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(self.file_frame, text="Browse", command=self.browse_username_file).grid(row=0, column=2, padx=5, pady=5)
        
        self.random_frame = ttk.Frame(mode_frame)
        self.random_frame.grid(row=2, column=0, columnspan=3, sticky=tk.W+tk.E, padx=5, pady=5)
        self.random_frame.grid_remove()
        
        ttk.Label(self.random_frame, text="Username length:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.length_var = tk.StringVar(value="5")
        ttk.Entry(self.random_frame, textvariable=self.length_var, width=10).grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(self.random_frame, text="Number to check (0 for unlimited):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.count_var = tk.StringVar(value="100")
        ttk.Entry(self.random_frame, textvariable=self.count_var, width=10).grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        self.specific_frame = ttk.Frame(mode_frame)
        self.specific_frame.grid(row=2, column=0, columnspan=3, sticky=tk.W+tk.E, padx=5, pady=5)
        self.specific_frame.grid_remove()
        
        ttk.Label(self.specific_frame, text="Username to check:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.username_var = tk.StringVar()
        ttk.Entry(self.specific_frame, textvariable=self.username_var, width=30).grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        self.semi_frame = ttk.Frame(mode_frame)
        self.semi_frame.grid(row=2, column=0, columnspan=3, sticky=tk.W+tk.E, padx=5, pady=5)
        self.semi_frame.grid_remove()
        
        ttk.Label(self.semi_frame, text="Number to check (0 for unlimited):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.semi_count_var = tk.StringVar(value="100")
        ttk.Entry(self.semi_frame, textvariable=self.semi_count_var, width=10).grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(options_frame, text="Target available usernames:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.target_var = tk.StringVar(value="1005")
        ttk.Entry(options_frame, textvariable=self.target_var, width=10).grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        self.start_button = ttk.Button(buttons_frame, text="Start Checking", command=self.start_checking)
        self.start_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.stop_button = ttk.Button(buttons_frame, text="Stop", command=self.stop_checking, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.save_button = ttk.Button(buttons_frame, text="Save Results", command=self.save_results)
        self.save_button.pack(side=tk.LEFT, padx=5, pady=5)
    
    def setup_results_tab(self):
        stats_frame = ttk.Frame(self.results_tab)
        stats_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(stats_frame, text="Checked:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.checked_label = ttk.Label(stats_frame, text="0")
        self.checked_label.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(stats_frame, text="Available:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.available_label = ttk.Label(stats_frame, text="0")
        self.available_label.grid(row=0, column=3, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(stats_frame, text="Unavailable:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.unavailable_label = ttk.Label(stats_frame, text="0")
        self.unavailable_label.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(stats_frame, text="Deleted:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
        self.deleted_label = ttk.Label(stats_frame, text="0")
        self.deleted_label.grid(row=1, column=3, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(stats_frame, text="Progress:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(stats_frame, variable=self.progress_var, length=400)
        self.progress_bar.grid(row=2, column=1, columnspan=3, sticky=tk.W+tk.E, padx=5, pady=5)
        
        ttk.Label(self.results_tab, text="Results:").pack(anchor=tk.W, padx=10, pady=5)
        self.results_text = scrolledtext.ScrolledText(self.results_tab, width=80, height=20)
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        available_frame = ttk.LabelFrame(self.results_tab, text="Available Usernames")
        available_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.available_text = scrolledtext.ScrolledText(available_frame, width=80, height=10)
        self.available_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def toggle_proxy_options(self):
        if self.proxy_var.get() == "p":
            self.proxy_type_frame.grid()
            self.proxy_file_frame.grid()
        elif self.proxy_var.get() == "f":
            self.proxy_type_frame.grid_remove()
            self.proxy_file_frame.grid_remove()
        else: 
            self.proxy_type_frame.grid_remove()
            self.proxy_file_frame.grid_remove()
    
    def toggle_mode_options(self):
        self.file_frame.grid_remove()
        self.random_frame.grid_remove()
        self.specific_frame.grid_remove()
        self.semi_frame.grid_remove()
        
        mode = self.mode_var.get()
        if mode == "1":
            self.file_frame.grid()
        elif mode == "2":
            self.random_frame.grid()
        elif mode == "3":
            self.specific_frame.grid()
        elif mode == "4":
            self.semi_frame.grid()
    
    def browse_proxy_file(self):
        filename = filedialog.askopenfilename(title="Select Proxy File", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if filename:
            self.proxy_file_var.set(filename)
    
    def browse_username_file(self):
        filename = filedialog.askopenfilename(title="Select Username File", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if filename:
            self.file_path_var.set(filename)
    
    def load_usernames(self, file_path):
        try:
            with open(file_path, 'r') as file:
                return [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            self.log_message(f"File not found: {file_path}", "error")
            return []
        except Exception as e:
            self.log_message(f"Error loading file: {str(e)}", "error")
            return []
    
    def generate_random_username(self, length):
        return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))
    
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
            if not self.P:
                self.log_message("No proxies available in the list", "error")
                return None
                
            proxy = random.choice(self.P)
            
            if self.proxy_type == '1':
                return {
                    'http': f'http://{proxy}',
                    'https': f'http://{proxy}'
                }
            elif self.proxy_type == '2':
                return {
                    'http': f'socks4://{proxy}',
                    'https': f'socks4://{proxy}'
                }
            elif self.proxy_type == '3':
                return {
                    'http': f'socks5://{proxy}',
                    'https': f'socks5://{proxy}'
                }
            elif self.proxy_type == '4':
                return {
                    'http': f'http://{proxy}',
                    'https': f'http://{proxy}'
                }
            elif self.proxy_type == '5':
                host_port, user_pass = proxy.split(':', 1)
                user, password = user_pass.split(':', 1)
                return {
                    'http': f'http://{user}:{password}@{host_port}',
                    'https': f'http://{user}:{password}@{host_port}'
                }
            elif self.proxy_type == '6':
                ip_port, user_pass = proxy.split(':', 1)
                user, password = user_pass.split(':', 1)
                return {
                    'http': f'http://{user}:{password}@{ip_port}',
                    'https': f'http://{user}:{password}@{ip_port}'
                }
            elif self.proxy_type == '7':
                user_pass, host_port = proxy.split(':', 1)
                user, password = user_pass.split(':', 1)
                return {
                    'http': f'http://{user}:{password}@{host_port}',
                    'https': f'http://{user}:{password}@{host_port}'
                }
        elif self.proxymod == "f":
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
                    self.log_message(f"[AVAILABLE] {username}", "success")
                    self.available_text.insert(tk.END, f"{username}\n")
                    self.available_text.see(tk.END)
                elif f'Username {self.user} is not available' in response.text:
                    self.unavailable += 1
                    self.log_message(f"[TAKEN] {username}", "unavailable")
                else:
                    self.unavailable += 1
                    self.log_message(f"[UNKNOWN] {username}: {response.text}", "unavailable")
                
                self.checked += 1
                self.update_stats()
                break  
                
            except Exception as e:
                if self.proxymod in ["p", "f"] and attempt < max_retries - 1:
                    self.log_message(f"[RETRY] {username}: {str(e)}. Switching proxy...", "warning")
                    self.proxies = self.proxynew()
                    time.sleep(1)  
                elif attempt < max_retries - 1:
                    self.log_message(f"[RETRY] {username}: {str(e)}. Retrying in {retry_delay}s...", "warning")
                    time.sleep(retry_delay)
                    retry_delay *= 2 
                else:
                    self.log_message(f"[ERROR] {username}: {str(e)} after {max_retries} attempts", "error")
    
    def update_stats(self):
        self.checked_label.config(text=str(self.checked))
        self.available_label.config(text=str(self.available))
        self.unavailable_label.config(text=str(self.unavailable))
        self.deleted_label.config(text=str(self.deleted))
        
        if self.count > 0:
            progress = min(100, (self.checked / self.count) * 100)
            self.progress_var.set(progress)
        elif self.target_available > 0:
            progress = min(100, (self.available / self.target_available) * 100)
            self.progress_var.set(progress)
        
        self.status_bar.config(text=f"Checked: {self.checked} | Available: {self.available} | Unavailable: {self.unavailable} | Deleted: {self.deleted} | Current: {self.user}")
        
        self.root.update_idletasks()
    
    def log_message(self, message, level="info"):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        
        if level == "error":
            tag = "error"
            color = "#e74c3c" 
        elif level == "warning":
            tag = "warning"
            color = "#f39c12"  
        elif level == "success":
            tag = "success"
            color = "#2ecc71"  
        elif level == "unavailable":
            tag = "unavailable"
            color = "#95a5a6"  
        elif level == "deleted":
            tag = "deleted"
            color = "#f1c40f"
        else:
            tag = "info"
            color = "#3498db" 
        
        self.results_text.insert(tk.END, log_message)
        self.results_text.tag_add(tag, f"end-{len(log_message)+1}c", "end-1c")
        self.results_text.tag_config(tag, foreground=color)
        
        self.results_text.see(tk.END)
    
    def start_checking(self):
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        
        self.checked = 0
        self.available = 0
        self.unavailable = 0
        self.deleted = 0
        self.run = True
        
        self.results_text.delete(1.0, tk.END)
        self.available_text.delete(1.0, tk.END)
        
        for tag, color in [("error", "#e74c3c"), ("warning", "#f39c12"), ("success", "#2ecc71"), 
                          ("info", "#3498db"), ("unavailable", "#95a5a6"), ("deleted", "#f1c40f")]:
            self.results_text.tag_config(tag, foreground=color)
        
        self.proxymod = self.proxy_var.get()
        self.proxy_type = self.proxy_type_var.get() if self.proxymod == "p" else None
        self.mode = self.mode_var.get()
        self.target_available = int(self.target_var.get())
        
        if self.proxymod == "p":
            proxy_file = self.proxy_file_var.get()
            try:
                with open(proxy_file, 'r') as file:
                    self.P = [line.strip() for line in file if line.strip()]
                    if not self.P:
                        self.log_message("No valid proxies found in file. Continuing without proxy.", "error")
                        self.proxymod = "n"
                    else:
                        self.log_message(f"Loaded {len(self.P)} proxies.", "info")
            except FileNotFoundError:
                self.log_message("Proxy file not found. Continuing without proxy.", "error")
                self.proxymod = "n"
            except Exception as e:
                self.log_message(f"Error loading proxy: {str(e)}. Continuing without proxy.", "error")
                self.proxymod = "n"
        
        self.check_thread = threading.Thread(target=self.check_thread_function)
        self.check_thread.daemon = True
        self.check_thread.start()
    
    def check_thread_function(self):
        try:
            self.log_message("Starting username checker...", "info")
            
            if self.mode == "1":
                file_path = self.file_path_var.get()
                self.usernames = self.load_usernames(file_path)
                if not self.usernames:
                    self.log_message("No usernames loaded from file.", "error")
                    self.stop_checking()
                    return
                
                self.log_message(f"Loaded {len(self.usernames)} usernames from file.", "info")
                for username in self.usernames:
                    if not self.run or self.available >= self.target_available:
                        break
                    self.check_username(username)
                    time.sleep(random.uniform(1.5, 3.0))  
                self.log_message("All usernames checked from file.", "info")
                
            elif self.mode == "2":  
                self.length = int(self.length_var.get())
                self.count = int(self.count_var.get())
                checked = 0
                
                while (self.count == 0 or checked < self.count) and self.run and self.available < self.target_available:
                    username = self.generate_random_username(self.length)
                    self.check_username(username)
                    checked += 1
                    time.sleep(random.uniform(1.5, 3.0))  
                
                if self.count > 0:
                    self.log_message(f"Completed checking {self.count} random usernames.", "info")
                else:
                    self.log_message(f"Target of {self.target_available} available usernames reached!", "success")
                    
            elif self.mode == "3":  
                username = self.username_var.get()
                if not username:
                    self.log_message("No username specified.", "error")
                    self.stop_checking()
                    return
                
                self.check_username(username)
                self.log_message("Username check completed.", "info")
                
            elif self.mode == "4":
                self.count = int(self.semi_count_var.get())
                checked = 0
                
                while (self.count == 0 or checked < self.count) and self.run and self.available < self.target_available:
                    username = self.generate_semi_usernames()
                    self.check_username(username)
                    checked += 1
                    time.sleep(random.uniform(1.5, 3.0)) 
                
                if self.count > 0:
                    self.log_message(f"Completed checking {self.count} semi-pattern usernames.", "info")
                else:
                    self.log_message(f"Target of {self.target_available} available usernames reached!", "success")
            
            self.log_message("\nFinal Results:", "info")
            self.log_message(f"Checked: {self.checked} | Available: {self.available} | Unavailable: {self.unavailable} | Deleted: {self.deleted}", "info")
            
            if self.available > 0:
                self.log_message("Available usernames saved in available_Github.txt", "success")
        
        except Exception as e:
            self.log_message(f"Error in check thread: {str(e)}", "error")
        finally:
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
    
    def stop_checking(self):
        self.run = False
        self.log_message("Stopping checker...", "warning")
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
    
    def save_results(self):
        filename = filedialog.asksaveasfilename(title="Save Results", defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if filename:
            try:
                with open(filename, 'w', encoding="utf-8") as file:
                    file.write(self.results_text.get(1.0, tk.END))
                self.log_message(f"Results saved to {filename}", "success")
            except Exception as e:
                self.log_message(f"Error saving results: {str(e)}", "error")

if __name__ == "__main__":
    root = tk.Tk()
    app = GithubCheckerGUI(root)
    root.mainloop()