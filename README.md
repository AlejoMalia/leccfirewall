LECCFirewall
========================
![HEADER](docs/banner01.png)

A dynamic communication firewall built on the *LECC framework* to ensure uninterrupted connectivity. **LeccFirewall** is an advanced communication management system that leverages the [LECC framework](https://github.com/AlejoMalia/lecc) to maintain connectivity in critical scenarios. It dynamically scans available protocols, prioritizes them based on user-defined roles, and reroutes data through fallback options when primary connections fail.

![Python](https://img.shields.io/badge/Python-3.7+-blue) ![License](https://img.shields.io/badge/License-MIT-yellow)

Features
--------

*   🌐 **Multi-Protocol Support:** Works with HTTP, TCP, UDP, MQTT, UART, Bluetooth, and more.
*   🧩 **Dynamic Adaptation:** Automatically switches to available protocols during failures.
*   🚀 **Priority-Based Routing:** Ensures critical systems (e.g., payment terminals) stay online.
*   📺 **Real-Time Monitoring:** Continuously checks and updates connection status.

Installation
------------

1.  Clone the repository:
    
        git clone https://github.com/AlejoMalia/LeccFirewall.git
        cd LeccFirewall
    
2.  Install dependencies:
    
        pip install -r requirements.txt
    
3.  Run the firewall:
    
        python leccfirewall.py
    

Use Cases
---------

### 1\. Hospital Critical Systems

⚠️ **Problem:** Internet cuts interrupt patient monitors.

🧪 **Solution:** LeccFirewall switches MQTT sensor data to UART or TCP over a local network, keeping doctors informed.

💎 **Outcome:** Continuous patient monitoring despite network issues.

### 2\. Smart City Traffic Management

⚠️ **Problem:** Network failure stops traffic light coordination.

🧪 **Solution:** LeccFirewall uses UDP or Ethernet backups to maintain local control until the main network recovers.

💎 **Outcome:** Traffic flows smoothly during outages.

Configuration
-------------

Edit `leccfirewall.py` to define your system's roles and priorities:

    self.device_roles = {
        "http": "critical",  # Payment terminals
        "udp": "secondary",  # Local network backup
        "tcp": "secondary"   # Server
    }
    self.priority_rules = {
        "critical": ["HTTP", "UDP", "TCP"],
        "secondary": ["TCP", "UDP"]
    }

Dependencies
------------

Listed in `requirements.txt`:

    requests
    paho-mqtt
    smbus2
    flask

Contributing
------------

Feel free to fork this repository, submit pull requests, or open issues for suggestions!

License
-------

This project is open-source under the MIT License.

Credits
-------

|                                                                                    | Name        | Role         | GitHub                                         |
| ---------------------------------------------------------------------------------- | ----------- | ------------ | ---------------------------------------------- |
| ![Alejo](https://github.com/alejomalia.png?size=72) | Alejo |   Author & Development   | [@alejomalia](https://github.com/alejomalia) |

[![Twitter](https://img.shields.io/badge/Twitter-black?style=for-the-badge&logo=twitter&logoColor=white)](https://twitter.com/alejomalia_) [![Instagram](https://img.shields.io/badge/Instagram-black?style=for-the-badge&logo=instagram&logoColor=white)](https://www.instagram.com/alejomalia/)

<small>*Developed with assistance from Grok3, created by xAI.*</small>
