#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_FLAG_LENGTH 1024

// Finite-State-Automata states
typedef enum {
    STATE_0,
    STATE_1,
    STATE_2,
    STATE_3,
    NUM_STATES
} State;

// Transition table for FSA
State transition[NUM_STATES][2] = {
    {STATE_1, STATE_2},
    {STATE_2, STATE_3},
    {STATE_3, STATE_0},
    {STATE_0, STATE_1}
};

// Function to read binary flag from file
char* read_flag(const char* filename) {
    FILE* file = fopen(filename, "r");
    if (file == NULL) {
        perror("Failed to open flag file");
        exit(EXIT_FAILURE);
    }

    char* flag = (char*)malloc(MAX_FLAG_LENGTH);
    if (flag == NULL) {
        perror("Failed to allocate memory");
        exit(EXIT_FAILURE);
    }

    if (fgets(flag, MAX_FLAG_LENGTH, file) == NULL) {
        perror("Failed to read flag");
        exit(EXIT_FAILURE);
    }

    fclose(file);
    return flag;
}

// Function to shuffle the flag using FSA
void shuffle_flag(char* flag) {
    State current_state = STATE_0;
    size_t len = strlen(flag);
    for (size_t i = 0; i < len; ++i) {
        int bit = flag[i] - '0';
        if (bit != 0 && bit != 1) {
            fprintf(stderr, "Invalid character in flag: %c\n", flag[i]);
            exit(EXIT_FAILURE);
        }
        current_state = transition[current_state][bit];
        flag[i] = '0' + current_state;
    }
}

// Main function
int main(int argc, char* argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <flagfile>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    char* flag = read_flag(argv[1]);
    shuffle_flag(flag);
    printf("Shuffled flag: %s\n", flag);
    free(flag);

    return 0;
}
