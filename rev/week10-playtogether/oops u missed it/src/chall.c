#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int kolsodwsd() {
    return rand() % 4096;
}

void ayamsadocisa() {
    int i, j, k;
    int a, b, c;
    int attempts = 13;

    i = kolsodwsd();
    j = kolsodwsd();
    k = kolsodwsd();

    while (attempts > 0) {
        if (scanf("%d %d %d", &a, &b, &c) != 3) {
            fflush(stdin); // Clear the input buffer
            continue;
        }

        if (a == i && b == j && c == k) {
            FILE *flagFile = fopen("/app/flag.txt", "r");
            if (flagFile) {
                char buffer[1024]; // A buffer to hold the content
                while (fgets(buffer, sizeof(buffer), flagFile) != NULL) {
                    printf("%s\n", buffer);
                }
                fclose(flagFile);
            } else {
                printf("Error opening /app/flag.txt\n");
            }
            break;
        } else {
            printf("%c %c %c\n", (a < i) ? 'd' : ((a > i) ? 'k' : 'l'),
                                  (b < j) ? 'v' : ((b > j) ? 'g' : 'q'),
                                  (c < k) ? 'n' : ((c > k) ? 'l' : 'w'));
            attempts--;
        }
    }

    if (attempts == 0) {
        printf("You've used all your chances. Game over.\n");
    }
}

int main() {
	setbuf(stdin, NULL);
	setbuf(stdout, NULL);
	setbuf(stderr, NULL);
    srand(time(NULL)); // Initialize random number generator

    ayamsadocisa();

    return 0;
}
