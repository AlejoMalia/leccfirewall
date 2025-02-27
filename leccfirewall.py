# -*- coding: utf-8 -*-
import sys
import os
import time
import threading

# Ensure the current directory is in the module search path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from lecc import LECCCore, GenericModule, protocol_configs

print("\033[1mLeccFirewall - Dynamic Communication Firewall\033[0m")

class LeccFirewall(LECCCore):
    def __init__(self):
        super().__init__()
        # Define priority rules for protocol fallback
        self.priority_rules = {
            "critical": ["HTTP", "UDP", "TCP", "BLUETOOTH"],  # High-priority systems
            "secondary": ["TCP", "UDP", "BLUETOOTH"]          # Lower-priority systems
        }
        self.device_roles = {}
        self.action_protocol = {}

    def assign_roles(self):
        """Assign roles to protocols based on their criticality"""
        # User-configurable: Adjust according to your system's needs
        self.device_roles = {
            "http": "critical",      # E.g., payment terminals
            "udp": "secondary",      # Local network backup
            "tcp": "secondary",      # Internal server
            "bluetooth": "secondary" # Mobile device backup
        }
        print("[LeccFirewall] Roles assigned: {}".format(self.device_roles))

    def scan_system(self):
        """Scan all modules to track availability"""
        print("[LeccFirewall] Scanning system...")
        available = {p: m for p, m in self.modules.items() if m.available}
        for protocol in self.modules:
            status = "Available" if protocol in available else "Unavailable"
            emulated = self.modules[protocol].emulated
            print("  {}: {} - Emulated: {}".format(protocol, status, emulated))
        return available

    def create_action_protocol(self, available_modules):
        """Create a dynamic action protocol based on availability and priorities"""
        print("[LeccFirewall] Creating action protocol...")
        self.action_protocol.clear()

        for protocol, role in self.device_roles.items():
            if protocol in available_modules and available_modules[protocol].available:
                self.action_protocol[protocol] = protocol
                print("    Using {} directly".format(protocol))
            else:
                for fallback_proto in self.priority_rules[role]:
                    if fallback_proto.lower() in available_modules and available_modules[fallback_proto.lower()].available:
                        self.action_protocol[protocol] = "{} (fallback)".format(fallback_proto.lower())
                        print("    Using {} as fallback for {}".format(fallback_proto.lower(), protocol))
                        break
                else:
                    self.action_protocol[protocol] = "Offline"
                    print("    {} offline, no fallbacks available".format(protocol))

        print("  Current protocol: {}".format(self.action_protocol))
        return self.action_protocol

    def monitor_and_adapt(self):
        """Monitor the system and adapt the protocol in real-time"""
        while self.running:
            time.sleep(5)  # Check every 5 seconds; adjust based on your needs
            print("[LeccFirewall] Monitoring changes...")
            available = self.scan_system()
            self.create_action_protocol(available)
            self.route_messages_with_protocol()

    def route_messages_with_protocol(self):
        """Route messages using the current action protocol"""
        for protocol, target_proto in self.action_protocol.items():
            if target_proto != "Offline" and not self.modules[protocol].failed_message_queue.empty():
                msg = self.modules[protocol].failed_message_queue.get()
                target_protocol = target_proto.split()[0]
                print("[LeccFirewall] Routing message from {} via {}".format(protocol, target_proto))
                self.route_message(msg, target_protocol)

def main():
    # Initialize the firewall
    firewall = LeccFirewall()

    # Register protocols relevant to your system (customize as needed)
    used_protocols = {
        "http": protocol_configs["http"],        # E.g., payment terminals
        "udp": protocol_configs["udp"],          # Local network backup
        "tcp": protocol_configs["tcp"],          # Internal server
        "bluetooth": protocol_configs["bluetooth"]  # Mobile device backup
    }
    for protocol, config in used_protocols.items():
        firewall.register_module(protocol, GenericModule(protocol, config))

    print("\033[1mInitializing LeccFirewall...\033[0m")
    time.sleep(10)  # Wait for modules to initialize; adjust if needed

    # Assign roles and start with initial protocol
    firewall.assign_roles()
    available = firewall.scan_system()
    firewall.create_action_protocol(available)

    # Start real-time monitoring in a separate thread
    monitor_thread = threading.Thread(target=firewall.monitor_and_adapt, daemon=True)
    monitor_thread.start()

    # Keep the program running until manually stopped
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[LeccFirewall] Shutting down...")
        firewall.running = False
        for module in firewall.modules.values():
            module.running = False

if __name__ == "__main__":
    main()