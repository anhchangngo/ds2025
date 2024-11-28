#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <netdb.h> // For gethostbyname()

#define PORT 8080
#define SIZE 1024

int open_clientfd(char *hostname, int port) {
    int clientfd;           // File descriptor of the client
    struct hostent *hp;     // store information about the host
    struct sockaddr_in serveraddr;

    if ((clientfd = socket(AF_INET, SOCK_STREAM, 0)) < 0) {     // AF_INET : IPv4, SOCK_STREAM : TCP
        perror("[-] Socket creation failed");
        return -1;
    }

    // TCP connection through DNS (resolve hostname)
    if ((hp = gethostbyname(hostname)) == NULL) {  // gethostbyname() to resolve the hostname into an IP address.
        perror("[-] DNS resolution failed");
        return -1;
    }

    bzero((char *)&serveraddr, sizeof(serveraddr));     // Clear serveraddr - Sets all bytes of the serveraddr structure to 0.
    serveraddr.sin_family = AF_INET;
    bcopy((char *)hp->h_addr_list[0], (char *)&serveraddr.sin_addr.s_addr, hp->h_length);
    serveraddr.sin_port = htons(port);      // host-to-network byte order

    if (connect(clientfd, (struct sockaddr *)&serveraddr, sizeof(serveraddr)) < 0) {
        perror("[-] Connection failed");
        return -1;
    }

    return clientfd;
}

int main() {
    char *hostname = "127.0.0.1"; // You can change domain name
    char buffer[SIZE];
    FILE *file;
    int clientfd;

    clientfd = open_clientfd(hostname, PORT);
    if (clientfd < 0) {
        return 1; // Exit if connection fails
    }
    printf("[+] Connected to server successfully\n");

    file = fopen("test.txt", "r");
    if (file == NULL) {
        perror("[-] Error opening file");
        close(clientfd);
        return 1;
    }

    ssize_t bytes_read, bytes_sent;
    while ((bytes_read = fread(buffer, 1, SIZE, file)) > 0) {
        bytes_sent = send(clientfd, buffer, bytes_read, 0); // Using send()
        if (bytes_sent < 0) {
            perror("[-] Error sending data");
            fclose(file);
            close(clientfd);
            return 1;
        }
    }

    printf("[+] File sent successfully\n");

    fclose(file);
    close(clientfd);
    return 0;
}
