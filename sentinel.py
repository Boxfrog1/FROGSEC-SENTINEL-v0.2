import os
import time
import ctypes
import random
import subprocess
import math
from collections import defaultdict

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
    def __init__(self):
        self.nucleus = NucleusBinding()
        self.running = True
        self.scan_interval = 8

    def sample_environment(self):
        # Core signals
        try:
            libc = ctypes.CDLL(None)
            blocked = libc.syscall(0) == -1 and ctypes.get_errno() in (1, 13)
            self.nucleus.add_signal("seccomp_strict", 1.0 if blocked else 0.3)
        except:
            self.nucleus.add_signal("seccomp_strict", 0.4)

        try:
            with open("/sys/fs/selinux/enforce", "r") as f:
                self.nucleus.add_signal("selinux_enforce", int(f.read().strip()))
        except:
            self.nucleus.add_signal("selinux_enforce", 0.8)

        self.nucleus.add_signal("apparmor", 1.0 if os.path.exists("/sys/kernel/security/apparmor") else 0.2)
        self.nucleus.add_signal("ebpf", 1.0 if os.path.exists("/sys/fs/bpf") else 0.2)
        self.nucleus.add_signal("falco", 1.0 if os.path.exists("/usr/bin/falco") else 0.25)

        # Network / signal interference
        try:
            rssi_out = subprocess.getoutput("termux-wifi-connectioninfo")
            if "rssi" in rssi_out.lower():
                rssi = int([line for line in rssi_out.splitlines() if "rssi" in line.lower()][0].split(":")[-1].strip().replace(",", ""))
                self.nucleus.add_signal("rssi_drop", max(0, -65 - rssi))
        except:
            self.nucleus.add_signal("rssi_drop", 0.0)

        # Integrate Entropy Vectors
        self.nucleus.integrate_entropy()

    def run(self):
        print(f"{BOLD}FrogSec Sentinel — Nucleus + Entropy Vector Active{RESET}")
        print("We watch from the gray. We shield in silence.\n")

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

                time.sleep(self.scan_interval)
        except KeyboardInterrupt:
            print(f"\n\n{BLUE}Sentinel offline.{RESET}")

if __name__ == "__main__":
    sentinel = FrogSecSentinel()
    sentinel.run()