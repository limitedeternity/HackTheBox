// gcc -Wall -pie -fPIE -fstack-protector-all -D_FORTIFY_SOURCE=2 -Wl,-z,now -Wl,-z,relro note_server.c -o note_server

#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#define BUFFER_SIZE 1024

void handle_client(int sock) {
    char note[BUFFER_SIZE];
    uint16_t index = 0;
    uint8_t cmd;
    // copy var
    uint8_t buf_size;
    uint16_t offset;
    uint8_t copy_size;

    while (1) {

        // get command ID
        if (read(sock, &cmd, 1) != 1) {
            exit(1);
        }

        switch(cmd) {
            // write note
            case 1:
                if (read(sock, &buf_size, 1) != 1) {
                    exit(1);
                }

                // prevent user to write over the buffer
                if (index + buf_size > BUFFER_SIZE) {
                    exit(1);
                }

                // write note
                if (read(sock, &note[index], buf_size) != buf_size) {
                    exit(1);
                }

                index += buf_size;
                

            break;

            // copy part of note to the end of the note
            case 2:
                // get offset from user want to copy
                if (read(sock, &offset, 2) != 2) {
                    exit(1);
                }

                // sanity check: offset must be > 0 and < index
                if (offset < 0 || offset > index) {
                    exit(1);
                }

                // get the size of the buffer we want to copy
                if (read(sock, &copy_size, 1) != 1) {
                    exit(1);
                }

                // prevent user to write over the buffer's note
                if (index > BUFFER_SIZE) {
                    exit(1);
                }

                // copy part of the buffer to the end 
                memcpy(&note[index], &note[offset], copy_size);

                index += copy_size;
            break;

            // show note
            case 3:
                write(sock, note, index);
            return;

        }
    }


}



int main( int argc, char *argv[] ) {
    int sockfd, newsockfd, portno;
    unsigned int clilen;
    struct sockaddr_in serv_addr, cli_addr;
    int pid;

    /* ignore SIGCHLD, prevent zombies */
    struct sigaction sigchld_action = {
        .sa_handler = SIG_DFL,
        .sa_flags = SA_NOCLDWAIT
    };
    sigaction(SIGCHLD, &sigchld_action, NULL);

    /* First call to socket() function */
    sockfd = socket(AF_INET, SOCK_STREAM, 0);

    if (sockfd < 0) {
        perror("ERROR opening socket");
        exit(1);
    }
    if (setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &(int){ 1 }, sizeof(int)) < 0)
        perror("setsockopt(SO_REUSEADDR) failed");

    /* Initialize socket structure */ 
    bzero((char *) &serv_addr, sizeof(serv_addr));
    portno = 5001;

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = inet_addr("127.0.0.1");
    serv_addr.sin_port = htons(portno);

    /* Now bind the host address using bind() call.*/
    if (bind(sockfd, (struct sockaddr *) &serv_addr, sizeof(serv_addr)) < 0) {
        perror("ERROR on binding");
        exit(1);
    }

    listen(sockfd,5);
    clilen = sizeof(cli_addr);

    while (1) {
        newsockfd = accept(sockfd, (struct sockaddr *) &cli_addr, &clilen);

        if (newsockfd < 0) {
            perror("ERROR on accept");
            exit(1);
        }

        /* Create child process */
        pid = fork();

        if (pid < 0) {
            perror("ERROR on fork");
            exit(1);
        }

        if (pid == 0) {
            /* This is the client process */
            close(sockfd);
            handle_client(newsockfd);
            exit(0);
        }
        else {
            close(newsockfd);
        }

    } /* end of while */
}