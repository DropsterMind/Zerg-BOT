from aiohttp import (
    ClientResponseError,
    ClientSession,
    ClientTimeout,
    BasicAuth
)
from aiohttp_socks import ProxyConnector
from http.cookies import SimpleCookie
from base58 import b58encode, b58decode
from nacl.signing import SigningKey
from datetime import datetime
from colorama import *
import asyncio, random, uuid, sys, re, os

class Zerg:
    def __init__(self) -> None:
        self.BASE_API = "https://api-prod.zerg.app"
        self.REF_CODE = "EYZW12I9JU"

        self.USE_PROXY = False
        self.ROTATE_PROXY = False

        self.proxies = []
        self.proxy_index = 0
        self.account_proxies = {}
        self.accounts = {}
        
        self.USER_AGENTS = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1 Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64; rv:133.0) Gecko/20100101 Firefox/133.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 OPR/117.0.0.0"
        ]

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def log(self, message):
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(
            f"{Fore.BLACK + Style.BRIGHT}[{Style.RESET_ALL}"
            f"{Fore.CYAN + Style.BRIGHT}{timestamp}{Style.RESET_ALL}"
            f"{Fore.BLACK + Style.BRIGHT}]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} › {Style.RESET_ALL}{message}",
            flush=True
        )

    def log_success(self, label, value):
        """Log baris dengan label dan nilai sukses"""
        print(
            f"  {Fore.BLACK + Style.BRIGHT}│{Style.RESET_ALL}"
            f"  {Fore.WHITE + Style.BRIGHT}{label:<10}{Style.RESET_ALL}"
            f"{Fore.BLACK + Style.BRIGHT}: {Style.RESET_ALL}"
            f"{Fore.GREEN + Style.BRIGHT}{value}{Style.RESET_ALL}",
            flush=True
        )

    def log_info(self, label, value):
        """Log baris dengan label dan nilai info"""
        print(
            f"  {Fore.BLACK + Style.BRIGHT}│{Style.RESET_ALL}"
            f"  {Fore.WHITE + Style.BRIGHT}{label:<10}{Style.RESET_ALL}"
            f"{Fore.BLACK + Style.BRIGHT}: {Style.RESET_ALL}"
            f"{Fore.CYAN + Style.BRIGHT}{value}{Style.RESET_ALL}",
            flush=True
        )

    def log_warn(self, label, value):
        """Log baris dengan label dan nilai warning"""
        print(
            f"  {Fore.BLACK + Style.BRIGHT}│{Style.RESET_ALL}"
            f"  {Fore.WHITE + Style.BRIGHT}{label:<10}{Style.RESET_ALL}"
            f"{Fore.BLACK + Style.BRIGHT}: {Style.RESET_ALL}"
            f"{Fore.YELLOW + Style.BRIGHT}{value}{Style.RESET_ALL}",
            flush=True
        )

    def log_error(self, label, value):
        """Log baris dengan label dan nilai error"""
        print(
            f"  {Fore.BLACK + Style.BRIGHT}│{Style.RESET_ALL}"
            f"  {Fore.WHITE + Style.BRIGHT}{label:<10}{Style.RESET_ALL}"
            f"{Fore.BLACK + Style.BRIGHT}: {Style.RESET_ALL}"
            f"{Fore.RED + Style.BRIGHT}{value}{Style.RESET_ALL}",
            flush=True
        )

    def log_divider(self, idx=None, total=None):
        """Divider antar akun dengan nomor opsional"""
        line = "─" * 50
        if idx and total:
            label = f" Account {idx}/{total} "
            pad = (50 - len(label)) // 2
            bar = "─" * pad + label + "─" * (50 - pad - len(label))
            print(f"\n{Fore.BLUE + Style.BRIGHT}  ┌{bar}┐{Style.RESET_ALL}")
        else:
            print(f"{Fore.BLUE + Style.BRIGHT}  └{line}┘{Style.RESET_ALL}\n")

    def welcome(self):
        banner = f"""
{Fore.BLUE + Style.BRIGHT}  ╔══════════════════════════════════════════════════╗
  ║                                                  ║
  ║   {Fore.CYAN}███████╗███████╗██████╗  ██████╗              {Fore.BLUE}║
  ║   {Fore.CYAN}╚══███╔╝██╔════╝██╔══██╗██╔════╝              {Fore.BLUE}║
  ║   {Fore.CYAN}  ███╔╝ █████╗  ██████╔╝██║  ███╗             {Fore.BLUE}║
  ║   {Fore.CYAN} ███╔╝  ██╔══╝  ██╔══██╗██║   ██║             {Fore.BLUE}║
  ║   {Fore.CYAN}███████╗███████╗██║  ██║╚██████╔╝             {Fore.BLUE}║
  ║   {Fore.CYAN}╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝              {Fore.BLUE}║
  ║                                                  ║
  ║   {Fore.WHITE}Auto BOT {Fore.YELLOW}v1.0{Fore.BLUE}     {Fore.MAGENTA}by DropsterMind{Fore.BLUE}           ║
  ║   {Fore.BLACK + Style.BRIGHT}═══════════════════════════════════════════{Fore.BLUE}║
  ║   {Fore.WHITE + Style.DIM}Automated farming tool for Zerg App{Fore.BLUE}          ║
  ╚══════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
        print(banner)

    def format_seconds(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
    
    def load_accounts(self):
        filename = "accounts.txt"
        try:
            with open(filename, 'r') as file:
                accounts = [line.strip() for line in file if line.strip()]
            return accounts
        except Exception as e:
            print(f"{Fore.RED + Style.BRIGHT}  ✗ Failed To Load Accounts: {e}{Style.RESET_ALL}")
            return None

    def load_proxies(self):
        filename = "proxy.txt"
        try:
            if not os.path.exists(filename):
                self.log(f"{Fore.RED + Style.BRIGHT}✗ File {filename} Not Found.{Style.RESET_ALL}")
                return
            with open(filename, 'r') as f:
                self.proxies = [line.strip() for line in f.read().splitlines() if line.strip()]
            
            if not self.proxies:
                self.log(f"{Fore.RED + Style.BRIGHT}✗ No Proxies Found.{Style.RESET_ALL}")
                return

            self.log(
                f"{Fore.GREEN + Style.BRIGHT}✓ Loaded {Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT}{len(self.proxies)}{Style.RESET_ALL}"
                f"{Fore.GREEN + Style.BRIGHT} proxies{Style.RESET_ALL}"
            )
        
        except Exception as e:
            self.log(f"{Fore.RED + Style.BRIGHT}✗ Failed To Load Proxies: {e}{Style.RESET_ALL}")
            self.proxies = []

    def check_proxy_schemes(self, proxies):
        schemes = ["http://", "https://", "socks4://", "socks5://"]
        if any(proxies.startswith(scheme) for scheme in schemes):
            return proxies
        return f"http://{proxies}"
    
    def get_next_proxy_for_account(self, account):
        if account not in self.account_proxies:
            if not self.proxies:
                return None
            proxy = self.check_proxy_schemes(self.proxies[self.proxy_index])
            self.account_proxies[account] = proxy
            self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return self.account_proxies[account]

    def rotate_proxy_for_account(self, account):
        if not self.proxies:
            return None
        proxy = self.check_proxy_schemes(self.proxies[self.proxy_index])
        self.account_proxies[account] = proxy
        self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return proxy
    
    def build_proxy_config(self, proxy=None):
        if not proxy:
            return None, None, None
        if proxy.startswith("socks"):
            connector = ProxyConnector.from_url(proxy)
            return connector, None, None
        elif proxy.startswith("http"):
            match = re.match(r"http://(.*?):(.*?)@(.*)", proxy)
            if match:
                username, password, host_port = match.groups()
                clean_url = f"http://{host_port}"
                auth = BasicAuth(username, password)
                return None, clean_url, auth
            else:
                return None, proxy, None
        raise Exception("Unsupported Proxy Type.")
    
    def display_proxy(self, proxy_url=None):
        if not proxy_url: return "No Proxy"
        proxy_url = re.sub(r"^(http|https|socks4|socks5)://", "", proxy_url)
        if "@" in proxy_url:
            proxy_url = proxy_url.split("@", 1)[1]
        return proxy_url
    
    def initialize_headers(self, address: str):
        headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cache-Control": "no-cache",
            "Origin": "https://welcome.zerg.app",
            "Pragma": "no-cache",
            "Referer": "https://welcome.zerg.app/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": self.accounts[address]["user_agent"],
            "X-Frontend-key": "Zerg-Frontend/1.0"
        }
        return headers.copy()
        
    def generate_signing_key(self, private_key: str):
        try:
            decode_account = b58decode(private_key)
            signing_key = SigningKey(decode_account[:32])
            return signing_key
        except Exception as e:
            self.log_error("Key", f"Failed to Generate Signing Key — {str(e)}")
            return None
        
    def generate_address(self, signing_key: bytes):
        try:
            verify_key = signing_key.verify_key
            address = b58encode(verify_key.encode()).decode()
            return address
        except Exception as e:
            self.log_error("Address", f"Failed to Generate Sol Address — {str(e)}")
            return None
        
    def generate_payload(self, signing_key: bytes, address: str, nonce_data: dict):
        try:
            nonce = nonce_data.get("data", {}).get("nonce")
            message = nonce_data.get("data", {}).get("message")
            message_bytes = message.encode("utf-8")
            signed = signing_key.sign(message_bytes)
            signature = b58encode(signed.signature).decode()
            payload = {
                "walletAddress": address,
                "nonce": nonce,
                "signature": signature,
                "message": message,
                "referredByCode": self.REF_CODE
            }
            return payload
        except Exception as e:
            raise Exception(f"Generate Req Payload Failed: {str(e)}")
        
    def extract_cookies(self, address: str, response):
        jar = SimpleCookie()
        existing_cookie = self.accounts[address].get("cookie")
        if existing_cookie:
            jar.load(existing_cookie)
        set_cookies = response.headers.getall("Set-Cookie", [])
        for raw_cookie in set_cookies:
            jar.load(raw_cookie)
        cookie_string = "; ".join(
            f"{key}={morsel.value}" for key, morsel in jar.items()
        )
        self.accounts[address]["cookie"] = cookie_string
        return cookie_string

    def mask_account(self, account):
        try:
            return account[:6] + '••••••' + account[-6:]
        except Exception:
            return None

    def print_question(self):
        print(f"\n{Fore.BLUE + Style.BRIGHT}  ┌─────────────── Proxy Setup ───────────────┐{Style.RESET_ALL}")
        while True:
            try:
                print(f"{Fore.BLUE + Style.BRIGHT}  │{Style.RESET_ALL}  {Fore.WHITE}1.{Style.RESET_ALL} Run With Proxy")
                print(f"{Fore.BLUE + Style.BRIGHT}  │{Style.RESET_ALL}  {Fore.WHITE}2.{Style.RESET_ALL} Run Without Proxy")
                proxy_choice = int(input(f"{Fore.BLUE + Style.BRIGHT}  └─▶ {Style.RESET_ALL}{Fore.YELLOW}Choose [1/2]: {Style.RESET_ALL}").strip())
                if proxy_choice in [1, 2]:
                    proxy_type = "With Proxy" if proxy_choice == 1 else "Without Proxy"
                    print(f"  {Fore.GREEN + Style.BRIGHT}✓ Selected: {proxy_type}{Style.RESET_ALL}\n")
                    self.USE_PROXY = proxy_choice == 1
                    break
                else:
                    print(f"  {Fore.RED + Style.BRIGHT}✗ Please enter 1 or 2.{Style.RESET_ALL}")
            except ValueError:
                print(f"  {Fore.RED + Style.BRIGHT}✗ Invalid input. Enter a number.{Style.RESET_ALL}")

        if self.USE_PROXY:
            while True:
                rotate_proxy = input(f"  {Fore.YELLOW}Rotate Invalid Proxy? [y/n]: {Style.RESET_ALL}").strip()
                if rotate_proxy in ["y", "n"]:
                    self.ROTATE_PROXY = rotate_proxy == "y"
                    status = "Enabled" if self.ROTATE_PROXY else "Disabled"
                    print(f"  {Fore.GREEN + Style.BRIGHT}✓ Proxy Rotation: {status}{Style.RESET_ALL}\n")
                    break
                else:
                    print(f"  {Fore.RED + Style.BRIGHT}✗ Invalid input. Enter 'y' or 'n'.{Style.RESET_ALL}")
    
    async def ensure_ok(self, response):
        if response.status >= 400:
            error_text = await response.text()
            raise Exception(f"HTTP {response.status}: {error_text}")
    
    async def check_connection(self, proxy_url=None):
        url = "https://api.ipify.org?format=json"
        connector, proxy, proxy_auth = self.build_proxy_config(proxy_url)
        try:
            async with ClientSession(connector=connector, timeout=ClientTimeout(total=30)) as session:
                async with session.get(url=url, proxy=proxy, proxy_auth=proxy_auth) as response:
                    await self.ensure_ok(response)
                    return True
        except (Exception, ClientResponseError) as e:
            self.log_error("Network", f"Connection failed — {str(e)}")
        return None
    
    async def auth_nonce(self, address: str, proxy_url=None, retries=5):
        url = f"{self.BASE_API}/api/v1/auth/nonce"
        for attempt in range(retries):
            connector, proxy, proxy_auth = self.build_proxy_config(proxy_url)
            try:
                headers = self.initialize_headers(address)
                headers["Content-Type"] = "application/json"
                payload = {"walletAddress": address}
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.post(url=url, headers=headers, json=payload, proxy=proxy, proxy_auth=proxy_auth) as response:
                        await self.ensure_ok(response)
                        self.extract_cookies(address, response)
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.log_error("Login", f"Failed to Fetch Auth Nonce — {str(e)}")
        return None
    
    async def auth_verify(self, signing_key: str, address: str, nonce_data: dict, proxy_url=None, retries=5):
        url = f"{self.BASE_API}/api/v1/auth/verify"
        for attempt in range(retries):
            connector, proxy, proxy_auth = self.build_proxy_config(proxy_url)
            try:
                headers = self.initialize_headers(address)
                headers["Content-Type"] = "application/json"
                headers["X-Idempotency-Key"] = str(uuid.uuid4())
                payload = self.generate_payload(signing_key, address, nonce_data)
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.post(url=url, headers=headers, json=payload, proxy=proxy, proxy_auth=proxy_auth) as response:
                        await self.ensure_ok(response)
                        self.extract_cookies(address, response)
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.log_error("Login", f"Failed to Fetch Auth Token — {str(e)}")
        return None
    
    async def users_xp(self, address: str, proxy_url=None, retries=5):
        url = f"{self.BASE_API}/api/v1/users/me/xp"
        for attempt in range(retries):
            connector, proxy, proxy_auth = self.build_proxy_config(proxy_url)
            try:
                headers = self.initialize_headers(address)
                headers["Cookie"] = self.accounts[address]["cookie"]
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.get(url=url, headers=headers, proxy=proxy, proxy_auth=proxy_auth) as response:
                        await self.ensure_ok(response)
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.log_error("Points", f"Failed to Fetch XP — {str(e)}")
        return None
    
    async def gumball_status(self, address: str, proxy_url=None, retries=5):
        url = f"{self.BASE_API}/api/v1/gumball/status"
        for attempt in range(retries):
            connector, proxy, proxy_auth = self.build_proxy_config(proxy_url)
            try:
                headers = self.initialize_headers(address)
                headers["Cookie"] = self.accounts[address]["cookie"]
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.get(url=url, headers=headers, proxy=proxy, proxy_auth=proxy_auth) as response:
                        await self.ensure_ok(response)
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.log_error("Gumball", f"Failed to Fetch Status — {str(e)}")
        return None
    
    async def gumball_play(self, address: str, proxy_url=None, retries=5):
        url = f"{self.BASE_API}/api/v1/gumball/play"
        for attempt in range(retries):
            connector, proxy, proxy_auth = self.build_proxy_config(proxy_url)
            try:
                headers = self.initialize_headers(address)
                headers["Cookie"] = self.accounts[address]["cookie"]
                headers["X-Idempotency-Key"] = str(uuid.uuid4())
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.post(url=url, headers=headers, proxy=proxy, proxy_auth=proxy_auth) as response:
                        await self.ensure_ok(response)
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.log_error("Gumball", f"Failed to Play — {str(e)}")
        return None

    async def process_check_connection(self, address: str, proxy_url=None):
        while True:
            if self.USE_PROXY:
                proxy_url = self.get_next_proxy_for_account(address)

            self.log_info("Proxy", self.display_proxy(proxy_url))

            is_valid = await self.check_connection(proxy_url)
            if is_valid: return True

            if self.ROTATE_PROXY:
                proxy_url = self.rotate_proxy_for_account(address)
                await asyncio.sleep(1)
                continue

            return False
    
    async def process_user_login(self, signing_key: str, address: str, proxy_url=None):
        is_valid = await self.process_check_connection(address, proxy_url)
        if not is_valid: return False

        if self.USE_PROXY:
            proxy_url = self.get_next_proxy_for_account(address)

        nonce = await self.auth_nonce(address, proxy_url)
        if not nonce: return False

        verify = await self.auth_verify(signing_key, address, nonce, proxy_url)
        if not verify: return False

        self.log_success("Auth", "Login successful ✓")
        return True

    async def process_accounts(self, signing_key: str, address: str, proxy_url=None):
        logined = await self.process_user_login(signing_key, address, proxy_url)
        if not logined: return False

        if self.USE_PROXY:
            proxy_url = self.get_next_proxy_for_account(address)

        xp = await self.users_xp(address, proxy_url)
        if xp:
            total_xp = xp.get("data", {}).get("totalXpEarned")
            rank = xp.get("data", {}).get("rank")
            self.log_info("XP", f"{total_xp} XP")
            self.log_info("Rank", f"#{rank}")

        gumball = await self.gumball_status(address, proxy_url)
        if gumball:
            remaining = gumball.get("data", {}).get("playsRemaining")

            if remaining > 0:
                self.log_info("Gumball", f"{remaining} play(s) remaining")

                for i in range(remaining):
                    # Progress bar mini
                    filled = "█" * (i + 1)
                    empty = "░" * (remaining - i - 1)
                    pct = int(((i + 1) / remaining) * 100)
                    print(
                        f"  {Fore.BLUE + Style.BRIGHT}│{Style.RESET_ALL}"
                        f"  {Fore.YELLOW}Playing {i+1}/{remaining} {Style.RESET_ALL}"
                        f"{Fore.GREEN}[{filled}{empty}]{Style.RESET_ALL}"
                        f"{Fore.WHITE} {pct}%{Style.RESET_ALL}",
                        flush=True
                    )

                    play = await self.gumball_play(address, proxy_url)
                    if play:
                        rarity = play.get("data", {}).get("rarity")
                        reward = play.get("data", {}).get("xpAmount")

                        rarity_color = {
                            "legendary": Fore.YELLOW,
                            "epic": Fore.MAGENTA,
                            "rare": Fore.BLUE,
                            "uncommon": Fore.CYAN,
                            "common": Fore.WHITE
                        }.get(str(rarity).lower(), Fore.WHITE)

                        print(
                            f"  {Fore.BLUE + Style.BRIGHT}│{Style.RESET_ALL}"
                            f"  {Fore.WHITE}  ╰─ Rarity: {rarity_color + Style.BRIGHT}{rarity}{Style.RESET_ALL}"
                            f"  {Fore.WHITE}Reward: {Fore.GREEN + Style.BRIGHT}+{reward} XP{Style.RESET_ALL}",
                            flush=True
                        )
                    await asyncio.sleep(1)

            else:
                self.log_warn("Gumball", "No plays remaining")

    async def main(self):
        try:
            accounts = self.load_accounts()
            if not accounts:
                print(f"{Fore.RED+Style.BRIGHT}  ✗ No Accounts Loaded.{Style.RESET_ALL}") 
                return

            self.print_question()

            while True:
                self.clear_terminal()
                self.welcome()

                self.log(
                    f"{Fore.WHITE + Style.BRIGHT}Accounts loaded: {Style.RESET_ALL}"
                    f"{Fore.CYAN + Style.BRIGHT}{len(accounts)}{Style.RESET_ALL}"
                )

                if self.USE_PROXY: self.load_proxies()

                print()
                for idx, private_key in enumerate(accounts, start=1):
                    self.log_divider(idx, len(accounts))

                    signing_key = self.generate_signing_key(private_key)
                    if not signing_key: continue

                    address = self.generate_address(signing_key)
                    if not address: continue

                    if address not in self.accounts:
                        self.accounts[address] = {
                            "user_agent": random.choice(self.USER_AGENTS)
                        }

                    self.log_info("Address", self.mask_account(address))
                        
                    await self.process_accounts(signing_key, address)
                    self.log_divider()
                    await asyncio.sleep(random.uniform(2.0, 3.0))

                # Countdown
                delay = 24 * 60 * 60
                print(f"\n{Fore.BLUE + Style.BRIGHT}  ╔══════════ All Accounts Processed ══════════╗{Style.RESET_ALL}")
                while delay > 0:
                    formatted_time = self.format_seconds(delay)
                    print(
                        f"{Fore.BLUE + Style.BRIGHT}  ║{Style.RESET_ALL}"
                        f"  {Fore.WHITE}Next cycle in: {Fore.CYAN + Style.BRIGHT}{formatted_time}{Style.RESET_ALL}"
                        f"                    "
                        f"{Fore.BLUE + Style.BRIGHT}║{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    await asyncio.sleep(1)
                    delay -= 1
                print(f"\n{Fore.BLUE + Style.BRIGHT}  ╚════════════════════════════════════════════╝{Style.RESET_ALL}\n")

        except Exception as e:
            self.log(f"{Fore.RED+Style.BRIGHT}✗ Fatal Error: {e}{Style.RESET_ALL}")
            raise e

if __name__ == "__main__":
    try:
        bot = Zerg()
        asyncio.run(bot.main())
    except KeyboardInterrupt:
        print(
            f"\n{Fore.BLUE + Style.BRIGHT}  ╔══════════════════════════════╗{Style.RESET_ALL}\n"
            f"{Fore.BLUE + Style.BRIGHT}  ║{Style.RESET_ALL}  {Fore.RED + Style.BRIGHT}Bot stopped by user  ✗{Style.RESET_ALL}        {Fore.BLUE + Style.BRIGHT}║{Style.RESET_ALL}\n"
            f"{Fore.BLUE + Style.BRIGHT}  ║{Style.RESET_ALL}  {Fore.MAGENTA}by DropsterMind{Style.RESET_ALL}               {Fore.BLUE + Style.BRIGHT}║{Style.RESET_ALL}\n"
            f"{Fore.BLUE + Style.BRIGHT}  ╚══════════════════════════════╝{Style.RESET_ALL}\n"
        )
        sys.exit(0)
