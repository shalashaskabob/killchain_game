import random

kill_chain_questions = [
    # Reconnaissance
    {"scenario": "An attacker uses the harvester tool to gather employee email addresses from a company's public website.", "stage": "Reconnaissance", "actor": "Generic Cybercriminal"},
    {"scenario": "A threat actor scans a target's network for open SSH ports using Nmap.", "stage": "Reconnaissance", "actor": "APT28 (Fancy Bear)"},
    {"scenario": "Hackers analyze job postings on LinkedIn to identify key personnel and technologies used by a target organization.", "stage": "Reconnaissance", "actor": "Lazarus Group"},
    {"scenario": "An attacker uses Shodan.io to search for unpatched and vulnerable web servers within a specific IP range.", "stage": "Reconnaissance", "actor": "Sandworm Team"},
    {"scenario": "A group purchases a list of a company's executive home addresses from a dark web marketplace.", "stage": "Reconnaissance", "actor": "FIN7"},
    {"scenario": "A threat actor uses Google dorking to find sensitive documents accidentally exposed on a target's website.", "stage": "Reconnaissance", "actor": "Turla"},
    {"scenario": "An attacker physically observes a target building to identify security camera locations and employee entry patterns.", "stage": "Reconnaissance", "actor": "Red Team Pentester"},

    # Weaponization
    {"scenario": "An attacker embeds a malicious macro into a Microsoft Word document that promises 'updated salary information'.", "stage": "Weaponization", "actor": "Emotet Gang"},
    {"scenario": "APT29 creates a custom backdoor and bundles it with a legitimate software installer for a popular VPN client.", "stage": "Weaponization", "actor": "APT29 (Cozy Bear)"},
    {"scenario": "A hacker crafts a PDF file that exploits a known vulnerability in Adobe Reader (CVE-2018-4990) to execute code.", "stage": "Weaponization", "actor": "Generic Malware Author"},
    {"scenario": "A state-sponsored group develops a zero-day exploit for a popular web browser and integrates it into an exploit kit.", "stage": "Weaponization", "actor": "Equation Group"},
    {"scenario": "An attacker uses a packer to obfuscate a known malware sample, creating a new binary with a unique hash to evade signature-based antivirus.", "stage": "Weaponization", "actor": "Malware Packager"},
    {"scenario": "A malicious actor uses a known exploit framework like Metasploit to package a reverse shell payload.", "stage": "Weaponization", "actor": "Script Kiddie"},
    {"scenario": "A threat group creates a polyglot file that appears as a harmless image but also contains malicious JavaScript.", "stage": "Weaponization", "actor": "Steganography Specialist"},

    # Delivery
    {"scenario": "A phishing email with a malicious attachment disguised as an invoice is sent to the accounting department.", "stage": "Delivery", "actor": "FIN7"},
    {"scenario": "An attacker leaves several infected USB drives labeled 'Q3 Layoff Plans' in the cafeteria of a target company, hoping an employee will plug one in.", "stage": "Delivery", "actor": "Social Engineer"},
    {"scenario": "A watering hole attack is set up on a popular industry news website frequently visited by the target's employees.", "stage": "Delivery", "actor": "Lazarus Group"},
    {"scenario": "An attacker sends a spear-phishing email to a high-level executive, appearing to be from the company's CEO.", "stage": "Delivery", "actor": "Whaling Attackers"},
    {"scenario": "A malicious link to a weaponized document is shared via a direct message on a professional networking site.", "stage": "Delivery", "actor": "Social Engineer"},
    {"scenario": "A hacker compromises a legitimate software update server to distribute their malware instead of the real update.", "stage": "Delivery", "actor": "Sandworm Team"},
    {"scenario": "An attacker uses a compromised social media account to send a malicious link to the victim's friends.", "stage": "Delivery", "actor": "Generic Phisher"},

    # Exploitation
    {"scenario": "A user opens a malicious Word document, and the embedded macro script executes, exploiting a vulnerability in the macro engine.", "stage": "Exploitation", "actor": "Dridex Operators"},
    {"scenario": "A victim visits a compromised website, and an exploit kit silently executes code in their browser by leveraging a Flash Player vulnerability.", "stage": "Exploitation", "actor": "Angler Exploit Kit"},
    {"scenario": "The EternalBlue exploit is used to gain remote code execution on a server that has not been patched for SMB vulnerabilities.", "stage": "Exploitation", "actor": "WannaCry Ransomware"},
    {"scenario": "A Java deserialization vulnerability (e.g., in Apache Struts) is triggered, allowing an attacker to execute arbitrary code on the server.", "stage": "Exploitation", "actor": "Equifax Breach Actor"},
    {"scenario": "A buffer overflow vulnerability in a web application is triggered by a specially crafted HTTP request, allowing the attacker to run their own commands.", "stage": "Exploitation", "actor": "Web App Attacker"},
    {"scenario": "A zero-day exploit in a PDF reader is triggered when the victim opens a booby-trapped document.", "stage": "Exploitation", "actor": "APT29 (Cozy Bear)"},
    {"scenario": "An SQL injection attack successfully bypasses login authentication on a web server.", "stage": "Exploitation", "actor": "Anonymous"},

    # Installation
    {"scenario": "After successful exploitation, a PowerShell script downloads and installs a persistent backdoor service on the victim's machine.", "stage": "Installation", "actor": "PowerShell Mafia"},
    {"scenario": "The Cobalt Strike Beacon is installed on a compromised system, and its configuration is stored in the Windows Registry to ensure it runs on startup.", "stage": "Installation", "actor": "Many APTs"},
    {"scenario": "Malware modifies a system's scheduled tasks to run a malicious script every hour, ensuring its persistence.", "stage": "Installation", "actor": "Generic Malware"},
    {"scenario": "A rootkit is installed on a compromised Linux server, hiding its files and processes from the system administrator.", "stage": "Installation", "actor": "Turla"},
    {"scenario": "The attacker drops a remote access trojan (RAT) into the Temp directory and creates a new service pointing to it.", "stage": "Installation", "actor": "Poison Ivy RAT"},
    {"scenario": "A fileless malware variant injects itself directly into the memory of a legitimate process like `explorer.exe` to avoid detection.", "stage": "Installation", "actor": "Kovter"},
    {"scenario": "Malware installs itself as a Browser Helper Object (BHO) in Internet Explorer to monitor user activity.", "stage": "Installation", "actor": "Adware Author"},

    # Command & Control
    {"scenario": "A compromised machine begins sending periodic 'heartbeat' signals to an attacker-controlled server via DNS queries.", "stage": "Command & Control", "actor": "DNS-Tunneling Actors"},
    {"scenario": "The Emotet trojan uses a list of hardcoded IP addresses for its C2 servers and communicates over a non-standard port.", "stage": "Command & Control", "actor": "Emotet"},
    {"scenario": "Malware on an infected host communicates with its operator by posting and reading encrypted comments on a specific social media page.", "stage": "Command & Control", "actor": "Stealthy Persuasion"},
    {"scenario": "An attacker uses the Tor network to anonymize their C2 communications, making them difficult to trace.", "stage": "Command & Control", "actor": "Anonymity Seekers"},
    {"scenario": "A backdoor on a corporate workstation receives commands hidden within standard-looking HTTPS traffic to a public cloud service.", "stage": "Command & Control", "actor": "Cloud-Native C2"},
    {"scenario": "Malware on a compromised host establishes an encrypted reverse connection to a server, waiting for commands from the attacker.", "stage": "Command & Control", "actor": "Gh0st RAT"},
    {"scenario": "An attacker uses a legitimate cloud storage service like Dropbox to send commands to and exfiltrate data from a compromised host.", "stage": "Command & Control", "actor": "Cloud-based C2"},

    # Actions on Objectives
    {"scenario": "An attacker uses their access to encrypt all files on a company's shared network drive and displays a ransom note.", "stage": "Actions on Objectives", "actor": "Ryuk Ransomware"},
    {"scenario": "The Lazarus Group uses their foothold in a bank's network to issue fraudulent SWIFT transactions, stealing millions of dollars.", "stage": "Actions on Objectives", "actor": "Lazarus Group"},
    {"scenario": "A hacktivist group defaces a government website with political messages after gaining access to the web server.", "stage": "Actions on Objectives", "actor": "Anonymous"},
    {"scenario": "An insider threat copies sensitive intellectual property, including product blueprints, to an external hard drive.", "stage": "Actions on Objectives", "actor": "Disgruntled Employee"},
    {"scenario": "An attacker exfiltrates a compressed archive containing thousands of customer credit card numbers to a server they control.", "stage": "Actions on Objectives", "actor": "FIN7"},
    {"scenario": "A state-sponsored actor uses their access to disrupt a power grid by sending malicious commands to industrial control systems.", "stage": "Actions on Objectives", "actor": "Sandworm Team"},
    {"scenario": "An attacker who has compromised an email server begins to read and forward all emails belonging to the company's CEO.", "stage": "Actions on Objectives", "actor": "Business Email Compromise"},
    {"scenario": "A threat actor uses stolen credentials to access a cloud environment and deploys a cryptocurrency mining script on multiple servers.", "stage": "Actions on Objectives", "actor": "Cryptojacking Group"}
] 