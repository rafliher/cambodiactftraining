import hashlib

# Hashes from your hashDB
hashes = [
    "f3f0c6e992b7562598d9865b6fe8b3a6", 
    "aa8c41330509455ee5679d04ed41535d280d9a89",
    "ecb53f367b3541da3a14236d9a091f9bcc7a9903953f36577c2664fdd2a68a55",
    "67f2a835697e7c9c2c5146c76eca6038", 
    "91a8c384094a60c4e38e2741bb1462e2a3233c13",
    "f5d95c4771c4b0dc095c3cbb3a21396aaafd39d96eb0b55ff5077ccc050273f2",
    "afa8b5df937facadbba529e500e69a6e", 
    "2d231af11f9498ed68b39d752c4ac434c2e93ecd",
]

# Paste your full word list as a triple-quoted string
word_string = """apple banana cloud stream hacker wire stone crystal gate iron matrix signal flame radar stealth vault dragon quantum circuit glitch phantom shadow mask echo spear agent frost spike neon hunter binary pulse venom cipher lock storm pixel fusion silent rogue blast freeze data swarm scale flare ninja brute wave flare vector orbit prism core shield strike blaze byte ghost sneak energy decrypt flux phase acid scan trace decode spark delta nova stealthy bug zero thunder shell ghostly token pirate stealthier crack digital stealthest poison scar crypt hash encoder spider malware traceback beast chaos beam signaler bruteify infect rage vapor glitchy botnet seed overflow bypass tracey bytecode jumper mutator stealthbot crawler inject intrude spam injecter crawl force strength relay stealthmode overclock tunnel firewall trap cloak burn gravity trapper silencer scanner breaker sentry snare snarebot disrupt confuse jammer rupture invade steal fake silentrun tracker sleuth decoy smoke worm crawlbot sniff sneakbot cyber leak breach capture nether trick lurker lockbot cloner parasite patch hackerbot signalbot detonate shift enigma roguewave spikeball deflect vortex drone clash warp server spoof cloaked silence defuse cracked crackedbot ignite splinter obfuscate crash corruption stealthcode zerobot bitmask decodebot keygen exfil replicate spread scramble cyberpath maskify invader cracker cloneware fuzz honeypot hook infector reroute failover fusebox mainframe cycler encryptor disabler armor seeker disguise buzz camo cloakify breakerbot trapdoor override nullbyte overrun gridlock byteforce bugbot sniffer control rampage erratic hijack backdoor codebreak reboot swarmbot fade desync loader demux gatekeeper shatter bytebomb doser"""

words = word_string.split()

# Hash function by position
hash_funcs = [
    lambda b: hashlib.md5(b).hexdigest(),
    lambda b: hashlib.sha1(b).hexdigest(),
    lambda b: hashlib.sha256(b).hexdigest(),
    lambda b: hashlib.md5(b).hexdigest(),
    lambda b: hashlib.sha1(b).hexdigest(),
    lambda b: hashlib.sha256(b).hexdigest(),
    lambda b: hashlib.md5(b).hexdigest(),
    lambda b: hashlib.sha1(b).hexdigest(),
]

# Find matches
matches = []
for i, target_hash in enumerate(hashes):
    for word in words:
        if hash_funcs[i](word.encode()) == target_hash:
            print(f"Match found for index {i}: {word}")
            matches.append(word)
            break
    else:
        print(f"No match found for index {i}")
        matches.append(None)

# Construct and print the flag
if all(matches):
    flag = "CNCC{" + "_".join(matches) + "}"
    print("✅ Final Flag:", flag)
else:
    print("❌ Could not resolve all parts of the flag.")
