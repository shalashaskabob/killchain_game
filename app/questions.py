import random

QUESTIONS = [
    # Reconnaissance
    {"description": "An attacker uses the harvester tool to gather employee email addresses from a company's public website.", "answer": "Reconnaissance", "apt": "Generic Cybercriminal"},
    {"description": "A threat actor scans a target's network for open SSH ports using Nmap.", "answer": "Reconnaissance", "apt": "APT28 (Fancy Bear)"},
    {"description": "Hackers analyze job postings on LinkedIn to identify key personnel and technologies used by a target organization.", "answer": "Reconnaissance", "apt": "Lazarus Group"},
    {"description": "An attacker uses Shodan.io to search for unpatched and vulnerable web servers within a specific IP range.", "answer": "Reconnaissance", "apt": "Sandworm Team"},
    {"description": "A group purchases a list of a company's executive home addresses from a dark web marketplace.", "answer": "Reconnaissance", "apt": "FIN7"},
    {"description": "A threat actor uses Google dorking to find sensitive documents accidentally exposed on a target's website.", "answer": "Reconnaissance", "apt": "Turla"},
    {"description": "An attacker physically observes a target building to identify security camera locations and employee entry patterns.", "answer": "Reconnaissance", "apt": "Red Team Pentester"},

    # Weaponization
    {"description": "An attacker embeds a malicious macro into a Microsoft Word document that promises 'updated salary information'.", "answer": "Weaponization", "apt": "Emotet Gang"},
    {"description": "APT29 creates a custom backdoor and bundles it with a legitimate software installer for a popular VPN client.", "answer": "Weaponization", "apt": "APT29 (Cozy Bear)"},
    {"description": "A hacker crafts a PDF file that exploits a known vulnerability in Adobe Reader (CVE-2018-4990) to execute code.", "answer": "Weaponization", "apt": "Generic Malware Author"},
    {"description": "A state-sponsored group develops a zero-day exploit for a popular web browser and integrates it into an exploit kit.", "answer": "Weaponization", "apt": "Equation Group"},
    {"description": "An attacker sets up a command and control server with a domain name that closely mimics the target company's actual domain.", "answer": "Weaponization", "apt": "APT28 (Fancy Bear)"},
    {"description": "A malicious actor uses a known exploit framework like Metasploit to package a reverse shell payload.", "answer": "Weaponization", "apt": "Script Kiddie"},
    {"description": "A threat group creates a polyglot file that appears as a harmless image but also contains malicious JavaScript.", "answer": "Weaponization", "apt": "Steganography Specialist"},

    # Delivery
    {"description": "A phishing email with a malicious attachment disguised as an invoice is sent to the accounting department.", "answer": "Delivery", "apt": "FIN7"},
    {"description": "An employee is tricked into plugging in a USB drive found in the company parking lot, which then executes a malicious payload.", "answer": "Delivery", "apt": "Stuxnet"},
    {"description": "A watering hole attack is set up on a popular industry news website frequently visited by the target's employees.", "answer": "Delivery", "apt": "Lazarus Group"},
    {"description": "An attacker sends a spear-phishing email to a high-level executive, appearing to be from the company's CEO.", "answer": "Delivery", "apt": "Whaling Attackers"},
    {"description": "A malicious link to a weaponized document is shared via a direct message on a professional networking site.", "answer": "Delivery", "apt": "Social Engineer"},
    {"description": "A hacker compromises a legitimate software update server to distribute their malware instead of the real update.", "answer": "Delivery", "apt": "Sandworm Team"},
    {"description": "An attacker uses a compromised social media account to send a malicious link to the victim's friends.", "answer": "Delivery", "apt": "Generic Phisher"},

    # Exploitation
    {"description": "A user opens a malicious Word document, and the embedded macro script executes, exploiting a vulnerability in the macro engine.", "answer": "Exploitation", "apt": "Dridex Operators"},
    {"description": "A victim visits a compromised website, and an exploit kit silently executes code in their browser by leveraging a Flash Player vulnerability.", "answer": "Exploitation", "apt": "Angler Exploit Kit"},
    {"description": "The EternalBlue exploit is used to gain remote code execution on a server that has not been patched for SMB vulnerabilities.", "answer": "Exploitation", "apt": "WannaCry Ransomware"},
    {"description": "A user is convinced to enter their credentials on a fake login page that looks identical to their corporate portal.", "answer": "Exploitation", "apt": "Credential Harvester"},
    {"description": "A buffer overflow vulnerability in a web application is triggered by a specially crafted HTTP request, allowing the attacker to run their own commands.", "answer": "Exploitation", "apt": "Web App Attacker"},
    {"description": "A zero-day exploit in a PDF reader is triggered when the victim opens a booby-trapped document.", "answer": "Exploitation", "apt": "APT29 (Cozy Bear)"},
    {"description": "An SQL injection attack successfully bypasses login authentication on a web server.", "answer": "Exploitation", "apt": "Anonymous"},

    # Installation
    {"description": "After successful exploitation, a PowerShell script downloads and installs a persistent backdoor service on the victim's machine.", "answer": "Installation", "apt": "PowerShell Mafia"},
    {"description": "The Cobalt Strike Beacon is installed on a compromised system, and its configuration is stored in the Windows Registry to ensure it runs on startup.", "answer": "Installation", "apt": "Many APTs"},
    {"description": "Malware modifies a system's scheduled tasks to run a malicious script every hour, ensuring its persistence.", "answer": "Installation", "apt": "Generic Malware"},
    {"description": "A rootkit is installed on a compromised Linux server, hiding its files and processes from the system administrator.", "answer": "Installation", "apt": "Turla"},
    {"description": "The attacker drops a remote access trojan (RAT) into the Temp directory and creates a new service pointing to it.", "answer": "Installation", "apt": "Poison Ivy RAT"},
    {"description": "A fileless malware variant injects itself directly into the memory of a legitimate process like `explorer.exe` to avoid detection.", "answer": "Installation", "apt": "Kovter"},
    {"description": "Malware installs itself as a Browser Helper Object (BHO) in Internet Explorer to monitor user activity.", "answer": "Installation", "apt": "Adware Author"},

    # Command & Control (C2)
    {"description": "A compromised machine begins sending periodic 'heartbeat' signals to an attacker-controlled server via DNS queries.", "answer": "Command & Control", "apt": "DNS-Tunneling Actors"},
    {"description": "The Emotet trojan uses a list of hardcoded IP addresses for its C2 servers and communicates over a non-standard port.", "answer": "Command & Control", "apt": "Emotet"},
    {"description": "Malware on an infected host communicates with its operator by posting and reading encrypted comments on a specific social media page.", "answer": "Command & Control", "apt": "Stealthy Persuasion"},
    {"description": "An attacker uses the Tor network to anonymize their C2 communications, making them difficult to trace.", "answer": "Command & Control", "apt": "Anonymity Seekers"},
    {"description": "A backdoor on a corporate workstation receives commands hidden within standard-looking HTTPS traffic to a public cloud service.", "answer": "Command & Control", "apt": "Cloud-Native C2"},
    {"description": "A remote access trojan establishes a reverse shell back to the attacker's machine, giving them full control.", "answer": "Command & Control", "apt": "Gh0st RAT"},
    {"description": "An attacker uses a legitimate cloud storage service like Dropbox to send commands to and exfiltrate data from a compromised host.", "answer": "Command & Control", "apt": "Cloud-based C2"},

    # Actions on Objectives
    {"description": "An attacker uses their access to encrypt all files on a company's shared network drive and displays a ransom note.", "answer": "Actions on Objectives", "apt": "Ryuk Ransomware"},
    {"description": "The Lazarus Group uses their foothold in a bank's network to issue fraudulent SWIFT transactions, stealing millions of dollars.", "answer": "Actions on Objectives", "apt": "Lazarus Group"},
    {"description": "A hacktivist group defaces a government website with political messages after gaining access to the web server.", "answer": "Actions on Objectives", "apt": "Anonymous"},
    {"description": "An insider threat copies sensitive intellectual property, including product blueprints, to an external hard drive.", "answer": "Actions on Objectives", "apt": "Disgruntled Employee"},
    {"description": "An attacker exfiltrates a compressed archive containing thousands of customer credit card numbers to a server they control.", "answer": "Actions on Objectives", "apt": "FIN7"},
    {"description": "A state-sponsored actor uses their access to disrupt a power grid by sending malicious commands to industrial control systems.", "answer": "Actions on Objectives", "apt": "Sandworm Team"},
    {"description": "An attacker who has compromised an email server begins to read and forward all emails belonging to the company's CEO.", "answer": "Actions on Objectives", "apt": "Business Email Compromise"},
    {"description": "A threat actor uses stolen credentials to access a cloud environment and deploys a cryptocurrency mining script on multiple servers.", "answer": "Actions on Objectives", "apt": "Cryptojacking Group"}
]

def get_shuffled_questions():
    """Returns a shuffled copy of the questions list."""
    shuffled_list = QUESTIONS.copy()
    random.shuffle(shuffled_list)
    return shuffled_list 