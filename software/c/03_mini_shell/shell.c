/* Minimal POSIX shell: builtins (cd, exit), external commands, single pipe. */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>

#define MAX_LINE 1024
#define MAX_ARGS 64

static char **tokenize(char *line) {
    char **argv = malloc(sizeof(char *) * MAX_ARGS);
    if (!argv) {
        fprintf(stderr, "malloc failed\n");
        exit(1);
    }
    int argc = 0;
    char *token = strtok(line, " \t\n");
    while (token && argc < MAX_ARGS - 1) {
        argv[argc++] = token;
        token = strtok(NULL, " \t\n");
    }
    argv[argc] = NULL;
    return argv;
}

static void run_external(char **argv) {
    pid_t pid = fork();
    if (pid < 0) {
        perror("fork");
        return;
    }
    if (pid == 0) {
        execvp(argv[0], argv);
        perror("execvp");
        exit(1);
    } else {
        int status;
        waitpid(pid, &status, 0);
    }
}

static void run_pipeline(char **left_argv, char **right_argv) {
    int fd[2];
    if (pipe(fd) < 0) {
        perror("pipe");
        return;
    }

    pid_t left_pid = fork();
    if (left_pid == 0) {
        dup2(fd[1], STDOUT_FILENO);
        close(fd[0]);
        close(fd[1]);
        execvp(left_argv[0], left_argv);
        perror("execvp");
        exit(1);
    }

    pid_t right_pid = fork();
    if (right_pid == 0) {
        dup2(fd[0], STDIN_FILENO);
        close(fd[0]);
        close(fd[1]);
        execvp(right_argv[0], right_argv);
        perror("execvp");
        exit(1);
    }

    close(fd[0]);
    close(fd[1]);
    waitpid(left_pid, NULL, 0);
    waitpid(right_pid, NULL, 0);
}

int main(void) {
    char line[MAX_LINE];

    while (1) {
        printf("mini_shell> ");
        fflush(stdout);

        if (!fgets(line, sizeof(line), stdin)) {
            printf("\n");
            break; /* EOF (Ctrl-D) */
        }
        if (line[0] == '\n') {
            continue;
        }

        char *pipe_pos = strchr(line, '|');
        if (pipe_pos) {
            *pipe_pos = '\0';
            char *left_str = line;
            char *right_str = pipe_pos + 1;

            char **left_argv = tokenize(left_str);
            char **right_argv = tokenize(right_str);

            if (left_argv[0] && right_argv[0]) {
                run_pipeline(left_argv, right_argv);
            }
            free(left_argv);
            free(right_argv);
            continue;
        }

        char **argv = tokenize(line);
        if (!argv[0]) {
            free(argv);
            continue;
        }

        if (strcmp(argv[0], "exit") == 0) {
            free(argv);
            break;
        }
        if (strcmp(argv[0], "cd") == 0) {
            const char *target = argv[1] ? argv[1] : getenv("HOME");
            if (target && chdir(target) != 0) {
                perror("cd");
            }
            free(argv);
            continue;
        }

        run_external(argv);
        free(argv);
    }

    return 0;
}
