mitre_attack_questions = [
    # Reconnaissance
    {
        "tactic": "Reconnaissance",
        "scenario": "An adversary gathers information about the target organization by scanning their public-facing websites and looking for employee information on social media.",
        "actor": "APT28 (Fancy Bear)"
    },
    {
        "tactic": "Reconnaissance",
        "scenario": "A threat group actively scans for vulnerabilities in a company's external network infrastructure, such as unpatched VPN servers.",
        "actor": "Lazarus Group"
    },
    {
        "tactic": "Reconnaissance",
        "scenario": "Attackers purchase details about the target's network infrastructure from dark web brokers to plan their intrusion.",
        "actor": "FIN7"
    },
    # Resource Development
    {
        "tactic": "Resource Development",
        "scenario": "An APT group sets up a series of command-and-control servers with domain names that look similar to legitimate services used by the target.",
        "actor": "APT29 (Cozy Bear)"
    },
    {
        "tactic": "Resource Development",
        "scenario": "A threat actor acquires a valid code signing certificate to make their malware appear legitimate and bypass security checks.",
        "actor": "Stuxnet"
    },
    {
        "tactic": "Resource Development",
        "scenario": "Adversaries compromise a third-party software developer's infrastructure to inject malicious code into a legitimate software update.",
        "actor": "APT41 (Barium)"
    },
    # Initial Access
    {
        "tactic": "Initial Access",
        "scenario": "An employee receives a targeted email with a malicious attachment disguised as an invoice, which, when opened, executes malware.",
        "actor": "APT28 (Fancy Bear)"
    },
    {
        "tactic": "Initial Access",
        "scenario": "Attackers exploit a known vulnerability in a public-facing web server to gain a foothold in the network.",
        "actor": "Lazarus Group"
    },
    {
        "tactic": "Initial Access",
        "scenario": "A group uses stolen credentials, purchased from a criminal marketplace, to log into a company's remote access portal.",
        "actor": "FIN6"
    },
    # Execution
    {
        "tactic": "Execution",
        "scenario": "After gaining access, the adversary uses PowerShell to run a series of commands that download additional malicious payloads.",
        "actor": "APT29 (Cozy Bear)"
    },
    {
        "tactic": "Execution",
        "scenario": "Malware is executed on a user's machine when they are tricked into clicking a malicious link delivered via a phishing email.",
        "actor": "Lazarus Group"
    },
    {
        "tactic": "Execution",
        "scenario": "An attacker uses Windows Management Instrumentation (WMI) to execute malicious scripts on a compromised system.",
        "actor": "APT32 (OceanLotus)"
    },
    # Persistence
    {
        "tactic": "Persistence",
        "scenario": "A threat actor creates a new scheduled task on a compromised machine to run their malware each time the system boots up.",
        "actor": "APT28 (Fancy Bear)"
    },
    {
        "tactic": "Persistence",
        "scenario": "Adversaries modify a system's registry to ensure their malicious DLL is loaded by a legitimate process upon startup.",
        "actor": "Turla"
    },
    {
        "tactic": "Persistence",
        "scenario": "A new user account is created on a domain controller to provide the attacker with ongoing access to the network.",
        "actor": "Sandworm Team"
    },
    # Privilege Escalation
    {
        "tactic": "Privilege Escalation",
        "scenario": "An attacker exploits a vulnerability in the operating system's kernel to gain administrator-level privileges on a local machine.",
        "actor": "Equation Group"
    },
    {
        "tactic": "Privilege Escalation",
        "scenario": "Malware uses a token manipulation technique to impersonate a logged-in user with higher privileges.",
        "actor": "APT29 (Cozy Bear)"
    },
    {
        "tactic": "Privilege Escalation",
        "scenario": "Adversaries abuse Sudo caching on a Linux system to run commands with root privileges without re-entering a password.",
        "actor": "Rocke"
    },
    # Defense Evasion
    {
        "tactic": "Defense Evasion",
        "scenario": "Malware is packed and obfuscated to avoid detection by signature-based antivirus solutions.",
        "actor": "FIN7"
    },
    {
        "tactic": "Defense Evasion",
        "scenario": "An attacker clears the event logs on a compromised system to hide their activity from system administrators.",
        "actor": "APT3 (Gothic Panda)"
    },
    {
        "tactic": "Defense Evasion",
        "scenario": "A threat group uses a legitimate, trusted process like `svchost.exe` to inject and hide their malicious code.",
        "actor": "PoisonIvy"
    },
    # Credential Access
    {
        "tactic": "Credential Access",
        "scenario": "A tool like Mimikatz is used on a compromised host to extract plaintext passwords and hashes from memory.",
        "actor": "APT28 (Fancy Bear)"
    },
    {
        "tactic": "Credential Access",
        "scenario": "An adversary installs a keylogger on a victim's machine to capture usernames and passwords as they are typed.",
        "actor": "Lazarus Group"
    },
    {
        "tactic": "Credential Access",
        "scenario": "Attackers perform a brute-force attack against an RDP server to guess the administrator password.",
        "actor": "SamSam"
    },
    # Discovery
    {
        "tactic": "Discovery",
        "scenario": "After gaining access, an attacker runs `ipconfig` and `netstat` to learn about the network configuration of the compromised system.",
        "actor": "APT29 (Cozy Bear)"
    },
    {
        "tactic": "Discovery",
        "scenario": "The `net user /domain` command is used to list all user accounts within the organization's domain.",
        "actor": "APT32 (OceanLotus)"
    },
    {
        "tactic": "Discovery",
        "scenario": "An adversary scans the internal network to find other active hosts and open file shares.",
        "actor": "NotPetya"
    },
    # Lateral Movement
    {
        "tactic": "Lateral Movement",
        "scenario": "An attacker uses stolen administrator credentials with PsExec to run commands on other computers in the network.",
        "actor": "FIN5"
    },
    {
        "tactic": "Lateral Movement",
        "scenario": "The EternalBlue exploit is used to spread malware from one unpatched Windows machine to another within the same network.",
        "actor": "WannaCry"
    },
    {
        "tactic": "Lateral Movement",
        "scenario": "Adversaries use Remote Desktop Protocol (RDP) to log into other servers and systems inside the compromised environment.",
        "actor": "SamSam"
    },
    # Collection
    {
        "tactic": "Collection",
        "scenario": "An attacker searches for and gathers all files with extensions like .docx, .xlsx, and .pdf from a user's documents folder.",
        "actor": "APT28 (Fancy Bear)"
    },
    {
        "tactic": "Collection",
        "scenario": "Sensitive data from a database server is queried and saved to a CSV file in a temporary directory.",
        "actor": "FIN7"
    },
    {
        "tactic": "Collection",
        "scenario": "A threat actor takes screenshots of the victim's desktop to capture sensitive information displayed on the screen.",
        "actor": "Darkhotel"
    },
    # Command and Control
    {
        "tactic": "Command and Control",
        "scenario": "Malware communicates with an external server over HTTPS, disguising its traffic to look like normal web browsing.",
        "actor": "APT29 (Cozy Bear)"
    },
    {
        "tactic": "Command and Control",
        "scenario": "A threat actor uses a popular public service like Twitter or GitHub to send commands to their implants.",
        "actor": "Turla"
    },
    {
        "tactic": "Command and Control",
        "scenario": "An implant uses DNS queries to a domain controlled by the attacker to send and receive instructions.",
        "actor": "Cobalt Strike"
    },
    # Exfiltration
    {
        "tactic": "Exfiltration",
        "scenario": "Sensitive documents are compressed into an encrypted ZIP file and uploaded to a cloud storage service controlled by the attacker.",
        "actor": "APT41 (Barium)"
    },
    {
        "tactic": "Exfiltration",
        "scenario": "Data is slowly leaked out of the network through a series of small, scheduled DNS requests to avoid detection.",
        "actor": "OilRig"
    },
    {
        "tactic": "Exfiltration",
        "scenario": "An attacker uses a tool like `scp` (Secure Copy Protocol) to transfer stolen data from a compromised Linux server to an external machine.",
        "actor": "Rocke"
    },
    # Impact
    {
        "tactic": "Impact",
        "scenario": "Ransomware encrypts all files on a hospital's computer systems, making patient records inaccessible and disrupting services.",
        "actor": "WannaCry"
    },
    {
        "tactic": "Impact",
        "scenario": "A threat actor deletes critical system files and overwrites the Master Boot Record (MBR) of servers, rendering them unbootable.",
        "actor": "NotPetya"
    },
    {
        "tactic": "Impact",
        "scenario": "Adversaries manipulate industrial control systems (ICS) to cause physical damage to equipment in a power plant.",
        "actor": "Stuxnet"
    },
    {
        "tactic": "Reconnaissance",
        "scenario": "A threat actor phishes a target to get credentials for their corporate VPN.",
        "actor": "APT29 (Cozy Bear)"
    },
    {
        "tactic": "Resource Development",
        "scenario": "An attacker develops a custom malware implant designed specifically to target the software used by the target organization.",
        "actor": "Equation Group"
    },
    {
        "tactic": "Initial Access",
        "scenario": "A user unknowingly inserts a malicious USB drive they found into their work computer, leading to a malware infection.",
        "actor": "Stuxnet"
    },
    {
        "tactic": "Execution",
        "scenario": "A user is tricked into running a malicious executable disguised as a legitimate software installer.",
        "actor": "FIN7"
    },
    {
        "tactic": "Persistence",
        "scenario": "Adversaries install a web shell on a public-facing web server to maintain access.",
        "actor": "APT1 (Comment Crew)"
    },
    {
        "tactic": "Privilege Escalation",
        "scenario": "An attacker exploits a misconfigured service that is running with system-level permissions to elevate their own privileges.",
        "actor": "Lazarus Group"
    },
    {
        "tactic": "Defense Evasion",
        "scenario": "A threat actor uses timestomping to modify the timestamps of a malicious file to make it look like a legitimate system file.",
        "actor": "APT28 (Fancy Bear)"
    }
] 