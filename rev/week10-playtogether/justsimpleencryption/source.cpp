#include <iostream>
#include <string>
#include <bitset>   
#include <cstdbool>
#include <vector>
#include <sstream> 

using namespace std;

const int BLOCK_SIZE = 128;
const int BYTE_COUNT = BLOCK_SIZE / 8;
const int NIBBLE_SIZE = 4;
const int NIBBLE_COUNT = BLOCK_SIZE / NIBBLE_SIZE;
const int ROUND_NUMBER = 10;

bitset<4> roundKeys[ROUND_NUMBER][NIBBLE_COUNT];
bitset<4> buffer[NIBBLE_COUNT];

int mod(int a, int b){
    return (b + (a % b)) % b;
}

void chrstouint4s(string charArray, bitset<4> *uint4Array, int arraySize) {
    for (int i = 0; i < arraySize; ++i) {
        for (int j = 0; j < 2; ++j) {
            uint4Array[i * 2 + j] = bitset<4>((charArray[i] >> (8 - (j + 1) * 4)) & 0x0F);
        }
    }
}

void stringXor(bitset<4> *buffer, bitset<4> *k) {
    for (int i = 0; i < NIBBLE_COUNT; i++) {
        buffer[i] ^= k[i];
    }
}

void indexShiftAdd(bitset<4> *buffer, int shiftNum, bool inverse) {
    bitset<4> temp[NIBBLE_COUNT];
    bitset<4> temp2[NIBBLE_COUNT];
    shiftNum = shiftNum % 2 ? shiftNum : shiftNum + 1;
    if(!inverse){
        for (int i = 0; i < NIBBLE_COUNT; i++) {
            if(i % 2 == 0)
                temp[i] = (buffer[i].to_ulong() + buffer[(i + shiftNum) % NIBBLE_COUNT].to_ulong()) % 16;
            else
                temp[i] = buffer[i].to_ulong() ^ buffer[(i + shiftNum) % NIBBLE_COUNT].to_ulong();
        }
        temp[shiftNum] = buffer[shiftNum];
        temp2[0] = temp[0];
        for (int i = 1; i < NIBBLE_COUNT; i++) {
            temp2[i] = temp[i] ^ temp[i - 1];
        }
    } else {
        temp[0] = buffer[0];
        for (int i = 1; i < NIBBLE_COUNT; i++) {
            temp[i] = buffer[i] ^ temp[i - 1];
        }
        temp2[shiftNum] = temp[shiftNum];
        for (int i = 0; i < NIBBLE_COUNT-1; i++) {
            if(i % 2 == 0)
                temp2[mod(shiftNum * (-i), NIBBLE_COUNT)] = (temp[mod(shiftNum * (-i), NIBBLE_COUNT)].to_ulong() - temp2[mod(shiftNum * (-i+1), NIBBLE_COUNT)].to_ulong()) % 16;
            else
                temp2[mod(shiftNum * (-i), NIBBLE_COUNT)] = temp[mod(shiftNum * (-i), NIBBLE_COUNT)].to_ulong() ^ temp2[mod(shiftNum * (-i+1), NIBBLE_COUNT)].to_ulong();
        }
    }
    for (int i = 0; i < NIBBLE_COUNT; i++) {
        buffer[i] = temp2[i];
    }
}

void indexShiftTrans(bitset<4> *buffer, int shiftNum, bool inverse) {
    bitset<4> temp[NIBBLE_COUNT];
    if (!inverse) {
        for (int i = 0; i < NIBBLE_COUNT; i++) {
            temp[i] = buffer[(i + shiftNum) % NIBBLE_COUNT];
        }
    } else {
        for (int i = 0; i < NIBBLE_COUNT; i++) {
            temp[(i + shiftNum) % NIBBLE_COUNT] = buffer[i];
        }
    }
    
    for (int i = 0; i < NIBBLE_COUNT; i++) {
        buffer[i] = temp[i];
    }
}

int calcSum(bitset<4> *nibbles) {
    int sum = 0;
    for (int i = 0; i < NIBBLE_COUNT; i++) {
        sum += nibbles[i].to_ulong();
    }
    return sum % NIBBLE_COUNT;
}

string pkcs7Padding(string plain) {
    int padLen = BYTE_COUNT - (plain.length() % BYTE_COUNT);
    plain.append(padLen, static_cast<char>(padLen));
    return plain;
}

string removePkcs7Padding(string padded) {
    int padLen = static_cast<int>(padded.back());
    return padded.substr(0, padded.length() - padLen);
}

void prepareRoundKeys(string key) {
    if (key.length() < BYTE_COUNT) {
        key.append(BYTE_COUNT - key.length(), 'F');
    }
    chrstouint4s(key, roundKeys[0], BYTE_COUNT);

    for (int i = 0; i < NIBBLE_COUNT; i++) {
        roundKeys[1][i] = roundKeys[0][NIBBLE_COUNT - i - 1];
    }
    for (int i = 2; i < ROUND_NUMBER; i++) {
        for (int j = 0; j < NIBBLE_COUNT; j++) {
            roundKeys[i][j] = roundKeys[i - 1][(j + 1) % BYTE_COUNT] ^ roundKeys[i - 2][(j + 2) % BYTE_COUNT];
        }
    }
}

string encryptBlock(string plainBlock) {
    chrstouint4s(plainBlock, buffer, BYTE_COUNT);

    for (int k = 0; k < ROUND_NUMBER; k++) {
        stringXor(buffer, roundKeys[k]);
        indexShiftAdd(buffer, calcSum(roundKeys[k]), false);
        indexShiftTrans(buffer, calcSum(buffer), false);
    }

    string encrypted;
    encrypted.reserve(NIBBLE_COUNT / 2);
    for (int i = 0; i < NIBBLE_COUNT; i+=2) {
        encrypted += static_cast<char>((buffer[i].to_ulong() << 4) | buffer[i + 1].to_ulong());
    }
    return encrypted;
}

string decryptBlock(string cipherBlock) {
    chrstouint4s(cipherBlock, buffer, BYTE_COUNT);

    for (int k = ROUND_NUMBER-1; k >= 0; k--) {
        indexShiftTrans(buffer, calcSum(buffer), true);
        indexShiftAdd(buffer, calcSum(roundKeys[k]), true);
        stringXor(buffer, roundKeys[k]);
    }

    string decrypted;
    decrypted.reserve(NIBBLE_COUNT / 2);
    for (int i = 0; i < NIBBLE_COUNT; i+=2) {
        decrypted += static_cast<char>((buffer[i].to_ulong() << 4) | buffer[i + 1].to_ulong());
    }
    return decrypted;
}

string encrypt(string plain, string key) {
    plain = pkcs7Padding(plain);
    prepareRoundKeys(key);

    string encrypted;
    for (size_t i = 0; i < plain.length(); i += BYTE_COUNT) {
        encrypted += encryptBlock(plain.substr(i, BYTE_COUNT));
    }
    return encrypted;
}

string decrypt(string cipher, string key) {
    prepareRoundKeys(key);

    string decrypted;
    for (size_t i = 0; i < cipher.length(); i += BYTE_COUNT) {
        decrypted += decryptBlock(cipher.substr(i, BYTE_COUNT));
    }
    return removePkcs7Padding(decrypted);
}

string hexValuesToString(const vector<string>& hexValues) {
    string result;
    result.reserve(hexValues.size()); // Reserve space to avoid multiple allocations

    for (const auto& hexValue : hexValues) {
        // Convert the hex string to an integer
        unsigned int charValue;
        stringstream ss;
        ss << hex << hexValue;
        ss >> charValue;

        // Append the character to the result string
        result += static_cast<char>(charValue);
    }

    return result;
}

int main() {
    string plain = "CNCC{justaverysimplesymetricencryptionwithoutsboxorpbox}"; // Example plaintext
    string key = ".;D,AWo,asdfnpwe";

    cout << "Plain: " << plain << endl;
    cout << "Key: " << key << endl;

    string encrypted = encrypt(plain, key);

    cout << "Encrypted: ";
    for (char c : encrypted) {
        cout << hex << (int)(unsigned char)c << " ";
    }
    cout << endl;

    string decrypted = decrypt(encrypted, key);
    cout << "Decrypted: " << decrypted << endl;


    vector<string> hexValues = {
        "b2", "5b", "80", "53", "89", "b5", "aa", "5f", "2b", "af", "4a", "85", "7", "13", "d2", "63", "90", "6b", "fc", "4f", "b2", "52", "56", "40", "8d", "6a", "74", "7f", "5a", "ee", "97", "ce", "24", "3b", "2d", "40", "9d", "53", "73", "c9", "7a", "27", "1", "36", "84", "4f", "a1", "7", "67", "95", "e9", "2c", "d2", "a8", "3b", "f4", "5e", "ab", "68", "e5", "f1", "3", "b6", "61"
    };

    string result = hexValuesToString(hexValues);
    
    // Print the result
    cout << "Resulting string: " << result << endl;

    decrypted = decrypt(result, key);
    cout << "Decrypted: " << decrypted << endl;
    return 0;
}
