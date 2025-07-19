#include <stdio.h>

int main() {
    char serial[9]; // 8 chars + null terminator
    serial[8] = '\0';

    for (char a = 'A'; a <= 'Z'; a++) {
        for (char b = 'A'; b <= 'Z'; b++) {
            if (a * b != 5250) continue;

            serial[0] = a;
            serial[1] = b;

            for (int d1 = '0'; d1 <= '9'; d1++) {
                for (int d2 = '0'; d2 <= '9'; d2++) {
                    for (int d3 = '0'; d3 <= '9'; d3++) {
                        for (int d4 = '0'; d4 <= '9'; d4++) {
                            int sum = (d1 - '0') + (d2 - '0') + (d3 - '0') + (d4 - '0');
                            if (sum != 17) continue;

                            serial[2] = d1;
                            serial[3] = d2;
                            serial[4] = d3;
                            serial[5] = d4;

                            unsigned int chksum = 0;
                            unsigned int xor = 0;
                            for (int i = 0; i < 6; i++) {
                                chksum += serial[i];
                                xor ^= serial[i];
                            }

                            serial[6] = (chksum % 94) + 33;
                            serial[7] = (xor % 94) + 33;

                            printf("Generated serial: %s\n", serial);
                            return 0;
                        }
                    }
                }
            }
        }
    }

    printf("No valid serial found.\n");
    return 1;
}
