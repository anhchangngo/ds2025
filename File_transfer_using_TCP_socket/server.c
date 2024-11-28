#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <fcntl.h>
#include <strings.h> // For bzero()

#define PORT 8080
#define SIZE 1024
#define LISTENQ 10 // Maximum number of pending connections

typedef struct sockaddr SA;

int open_listenfd(int port) {
    int listenfd, optval = 1;   // listenfd : File descriptor of socket server, optval: Parameter for the SO_REUSEADDR option
    struct sockaddr_in serveraddr;

    if ((listenfd = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        perror("[-] Socket creation failed");
        return -1;
    }

    // SO_REUSEADDR: This option allows a socket to reuse a local socket address that was previously in use.
    if (setsockopt(listenfd, SOL_SOCKET, SO_REUSEADDR, (const void *)&optval, sizeof(int)) < 0) {
        perror("[-] Set socket options failed");
        return -1;
    }

    bzero((char *)&serveraddr, sizeof(serveraddr));
    serveraddr.sin_family = AF_INET;
    serveraddr.sin_addr.s_addr = htonl(INADDR_ANY);
    serveraddr.sin_port = htons((unsigned short)port);

    if (bind(listenfd, (SA *)&serveraddr, sizeof(serveraddr)) < 0) {
        perror("[-] Bind failed");
        return -1;
    }

    if (listen(listenfd, LISTENQ) < 0) {
        perror("[-] Listen failed");
        return -1;
    }

    return listenfd;
}

int main() {
    char buffer[SIZE];
    struct sockaddr_in clientaddr;
    socklen_t clientlen = sizeof(clientaddr);
    int listenfd, connfd, file_fd;  // connfd : File descriptor of the connection has been accepted from the client.
                                    // file_fd: File descriptor of the file to write the data received from the client.

    listenfd = open_listenfd(PORT);     // open_listenfd() : create a socket and start listening for connections on port 8080.
    if (listenfd < 0) {
        return 1; // Exit if setup fails
    }
    printf("[+] Server is listening on port %d\n", PORT);

    connfd = accept(listenfd, (SA *)&clientaddr, &clientlen);   // accept(): Accepts a connection from the client.
    if (connfd < 0) {
        perror("[-] Accept failed");
        close(listenfd);
        return 1;
    }
    printf("[+] Connection accepted\n");

    file_fd = open("test2.txt", O_WRONLY | O_CREAT | O_TRUNC, 0666);
    if (file_fd < 0) {
        perror("[-] Error opening/creating file");
        close(connfd);
        close(listenfd);
        return 1;
    }

    ssize_t bytes_received;
    while ((bytes_received = recv(connfd, buffer, SIZE, 0)) > 0) { // recv(): Receive data from the client
        if (write(file_fd, buffer, bytes_received) != bytes_received) {
            perror("[-] Error writing to file");
            close(file_fd);
            close(connfd);
            close(listenfd);
            return 1;
        }
    }

    if (bytes_received < 0) {
        perror("[-] Error receiving data");
    }

    printf("[+] File received successfully\n");

    close(file_fd);
    close(connfd);
    close(listenfd);
    return 0;
}
