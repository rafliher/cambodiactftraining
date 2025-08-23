fn encrypt(flag: &str, key: &str) -> Vec<u8> {
    let mut encrypted = Vec::new();
    
    // Convert the flag to bytes
    let bytes = flag.as_bytes();
    
    // Convert the key to bytes
    let key_bytes = key.as_bytes();
    let key_len = key_bytes.len();
    
    for (i, &byte) in bytes.iter().enumerate() {
        // Get the key byte, cycling through the key if it's shorter than the flag
        let key_byte = key_bytes[i % key_len];
        
        let mut encrypted_byte = byte;
        
        match i % 4 {
            0 => {
                // i % 4 == 0: Add the key byte to the flag byte
                encrypted_byte = byte.wrapping_add(key_byte);
            }
            1 => {
                // i % 4 == 1: XOR the flag byte with the key byte
                encrypted_byte = byte ^ key_byte;
            }
            2 => {
                // i % 4 == 2: Right shift the flag byte by 1
                encrypted_byte = byte >> 1;
            }
            3 => {
                // i % 4 == 3: Combination of addition and XOR
                encrypted_byte = (byte.wrapping_add(key_byte)) ^ key_byte;
            }
            _ => {}
        }
        
        encrypted.push(encrypted_byte);
    }
    
    encrypted
}

fn main() {
    let flag = "CNCC{REDACTED}";
    let key = "rustkey";  // You can change this to any word you'd like as the key

    let encrypted_flag = encrypt(flag, key);
    
    // Print encrypted flag as bytes
    println!("Encrypted flag (bytes): {:?}", encrypted_flag);
    
    // Optionally, print the encrypted flag as a readable string (characters)
    let encrypted_str: String = encrypted_flag.iter().map(|&b| b as char).collect();
    println!("Encrypted flag (string): {}", encrypted_str);
}
