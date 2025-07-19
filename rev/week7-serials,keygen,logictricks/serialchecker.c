#include <stdio.h>
#include <string.h>

int main() {
    char serial[64];
    printf("Enter serial (8 chars): ");
    fgets(serial, sizeof(serial), stdin);
    serial[strcspn(serial, "\n")] = 0;

    if (strlen(serial) != 8) {
        printf("Invalid length.\n");
        return 1;
    }

    if (serial[0] * serial[1] != 5250) {
        printf("Char multiplication failed.\n");
        return 1;
    }

    int digit_sum = 0;
    for (int i = 2; i <= 5; i++) {
        if (serial[i] < '0' || serial[i] > '9') {
            printf("Non-digit found.\n");
            return 1;
        }
        digit_sum += serial[i] - '0';
    }
    if (digit_sum != 17) {
        printf("Digit sum failed.\n");
        return 1;
    }

    unsigned int chksum = 0, x = 0;
    for (int i = 0; i < 6; i++) {
        chksum += serial[i];
        
        x ^= serial[i];
    }
    unsigned char expected_chk = (chksum % 94) + 33;
    unsigned char expected_xor = (x % 94) + 33;

    if ((unsigned char)serial[6] != expected_chk) {
        printf("Checksum mismatch.\n");
        return 1;
    }

    if ((unsigned char)serial[7] != expected_xor) {
        printf("XOR mismatch.\n");
        return 1;
    }

    printf("Serial is valid! Access granted.\n");
    return 0;
}
