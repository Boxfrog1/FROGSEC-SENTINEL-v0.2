import os
import time
import ctypes
import random
import subprocess
import math
import argparse
import logging
from collections import defaultdict
from datetime import datetime

# Logging setup
logging.basicConfig(
    filename='sentinel.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ANSI Colors
RESET = '\033[0m'
BOLD  = '\033[1m'
CYAN, GREEN, MAGENTA, YELLOW, RED, BLUE = '\033[96m','\033[92m','\033[95m','\033[93m','\033[91m','\033[94m'

class EntropyVector:
    """Measures environmental chaos vs order - your anti-heuristic entropy signature"""
    def __init__(self):
        self.vector = defaultdict(float)

    def add_sample(self, data: str):
        """Calculate Shannon entropy of a string or data sample"""
        if not data:
            return 0.0
        freq = defaultdict(int)
        for char in data:
            freq[char] += 1
        length = len(data)
        entropy = -sum((count / length) * math.log2(count / length) for count in freq.values())
        return entropy

    def get_vector(self):
        """Return current entropy vector components"""
        return {
            "syscall_entropy": self.add_sample(str(os.getpid()) + str(random.random())),  # fake some syscall-like noise
            "proc_entropy": self.add_sample(str(len(os.listdir("/proc"))) if os.path.exists("/proc") else "0"),
            "timing_jitter": random.uniform(0.0, 2.5),   # your CPU sleep style
        }


class NucleusBinding:
    """Full FrogSec Nucleus Binding with Entropy Vectors"""
    def __init__(self):
        self.signals = defaultdict(float)
        self.bindings = {}
        self.entropy = EntropyVector()
        self.determinant = -42.0

    def add_signal(self, name: str, value: float):
        self.signals[name] = float(value)

    def cooperative_bind(self, name: str, *signal_names, interaction=0.45):
        total = sum(self.signals.get(s, 0.0) for s in signal_names)
        self.bindings[name] = (total * 1.18) + (total ** 1.25) * interaction

    def integrate_entropy(self):
        """Add entropy vector as a first-class signal"""
        vec = self.entropy.get_vector()
        self.add_signal("entropy_syscall", vec["syscall_entropy"])
        self.add_signal("entropy_proc", vec["proc_entropy"])
        self.add_signal("entropy_timing", vec["timing_jitter"])

        # Bind entropy cooperatively with other signals
        self.cooperative_bind("entropy_layer", "entropy_syscall", "entropy_proc", "entropy_timing")
        self.cooperative_bind("full_chaos", "entropy_layer", "seccomp_strict", "rssi_drop")

    def compute_affinity(self):
        raw = sum(self.bindings.values())
        biased = raw + (self.determinant * 0.12)
        noise = (biased % 13) * 0.08          # biological noise
        return biased + noise

    def get_status(self):
        affinity = self.compute_affinity()
        if affinity > 950: return "CRITICAL"
        if affinity > 750: return "HIGH"
        if affinity > 500: return "MEDIUM"
        if affinity > 300: return "LOW"
        return "CLEAN"


class FrogSecSentinel:
    """Complete FrogSec Sentinel with Nucleus + Entropy Vectors"""
    def __init__(self, mode='real'):
        self.nucleus = NucleusBinding()
        self.running = True
        self.scan_interval = 8
        self.mode = mode
        self.api_available = False
        self._check_termux_api()

    def _check_termux_api(self):
        try:
            result = subprocess.getoutput("termux-wifi-connectioninfo")
            if "rssi" in result.lower() or "wifi" in result.lower():
                self.api_available = True
            else:
                logger.warning("Termux:API not responding. Install with: pkg install termux-api and grant permission in Android settings.")
        except Exception as e:
            logger.warning(f"Termux:API check failed: {e}. --real mode requires Termux:API for full RSSI data.")

    def sample_environment(self):
        if self.mode == 'demo':
            # Safe demo mode - no risky system calls
            self.nucleus.add_signal("seccomp_strict", 0.8)
            self.nucleus.add_signal("selinux_enforce", 1)
            self.nucleus.add_signal("apparmor", 0.5)
            self.nucleus.add_signal("ebpf", 0.3)
            self.nucleus.add_signal("falco", 0.4)
            self.nucleus.add_signal("rssi_drop", 5.0)
        else:
            # Real mode with specific exception handling
            try:
                libc = ctypes.CDLL(None)
                blocked = libc.syscall(0) == -1 and ctypes.get_errno() in (1, 13)
                self.nucleus.add_signal("seccomp_strict", 1.0 if blocked else 0.3)
            except (OSError, AttributeError) as e:
                logger.warning(f"seccomp_strict check failed: {e}")
                self.nucleus.add_signal("seccomp_strict", 0.4)

            try:
                with open("/sys/fs/selinux/enforce", "r") as f:
                    self.nucleus.add_signal("selinux_enforce", int(f.read().strip()))
            except (FileNotFoundError, PermissionError, OSError) as e:
                logger.warning(f"SELinux check failed: {e}")
                self.nucleus.add_signal("selinux_enforce", 0.8)

            try:
                self.nucleus.add_signal("apparmor", 1.0 if os.path.exists("/sys/kernel/security/apparmor") else 0.2)
            except Exception as e:
                logger.warning(f"AppArmor check failed: {e}")
                self.nucleus.add_signal("apparmor", 0.2)

            try:
                self.nucleus.add_signal("ebpf", 1.0 if os.path.exists("/sys/fs/bpf") else 0.2)
            except Exception as e:
                logger.warning(f"eBPF check failed: {e}")
                self.nucleus.add_signal("ebpf", 0.2)

            try:
                self.nucleus.add_signal("falco", 1.0 if os.path.exists("/usr/bin/falco") else 0.25)
            except Exception as e:
                logger.warning(f"Falco check failed: {e}")
                self.nucleus.add_signal("falco", 0.25)

            # Network / signal interference
            try:
                rssi_out = subprocess.getoutput("termux-wifi-connectioninfo")
                if "rssi" in rssi_out.lower():
                    rssi = int([line for line in rssi_out.splitlines() if "rssi" in line.lower()][0].split(":")[-1].strip().replace(",", ""))
                    self.nucleus.add_signal("rssi_drop", max(0, -65 - rssi))
                else:
                    if not self.api_available:
                        logger.warning("No RSSI data. Ensure Termux:API is installed and permission granted.")
                    self.nucleus.add_signal("rssi_drop", 0.0)
            except Exception as e:
                logger.warning(f"RSSI check failed: {e}")
                self.nucleus.add_signal("rssi_drop", 0.0)

        # Always integrate entropy
        self.nucleus.integrate_entropy()

    def run(self):
        print(f"{BOLD}FrogSec Sentinel v0.2 — Mode: {self.mode.upper()}{RESET}")
        print("We watch from the gray. We shield in silence.\n")
        if self.mode == 'real' and not self.api_available:
            print(f"{YELLOW}Warning: Termux:API not detected. Some signals will use safe defaults.{RESET}\n")

        try:
            while self.running:
                self.sample_environment()
                affinity = self.nucleus.compute_affinity()
                status = self.nucleus.get_status()

                os.system('clear')
                print(f"{BOLD}╔════════════════════════════════════╗{RESET}")
                print(f"{BOLD}║        FROGSEC SENTINEL v0.2       ║{RESET}")
                print(f"{BOLD}╠════════════════════════════════════╣{RESET}")
                print(f"{CYAN}║ Seccomp       : {RESET}{'STRICT' if self.nucleus.signals['seccomp_strict'] > 0.7 else 'normal'}")
                print(f"{GREEN}║ SELinux       : {RESET}{'ENFORCING' if self.nucleus.signals['selinux_enforce'] == 1 else 'permissive'}")
                print(f"{YELLOW}║ Entropy       : {RESET}{self.nucleus.signals['entropy_timing']:.2f} (jitter)")
                print(f"{BLUE}║ Affinity      : {affinity:.1f}{RESET}")
                color = RED if status != "CLEAN" else GREEN
                print(f"{color}║ Status        : {status}{RESET}")
                print(f"{BOLD}╚════════════════════════════════════╝{RESET}")
                print(f"\n{BLUE}Operating where signal meets noise.{RESET}")

                logger.info(f"Affinity: {affinity:.1f} | Status: {status} | Mode: {self.mode}")

                time.sleep(self.scan_interval)
        except KeyboardInterrupt:
            print(f"\n\n{BLUE}Sentinel offline.{RESET}")
            logger.info("Sentinel stopped by user")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="FrogSec Sentinel v0.2 - Android Security Monitor")
    parser.add_argument('--mode', choices=['demo', 'real'], default='real', 
                        help='demo: safe mode with no risky calls; real: attempt device checks (requires Termux:API for full features)')
    args = parser.parse_args()
    sentinel = FrogSecSentinel(mode=args.mode)
    sentinel.run()