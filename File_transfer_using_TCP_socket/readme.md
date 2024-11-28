# File_transfer_using_TCP_socket

The client.c file contains the code for the client-side, which read the text file and sends it to the server and the server.c file receives the data from the client and saves it in a text file

- Server

```
dat@ubuntu:/ds2025/File_transfer_using_TCP_socket$ gcc server.c -o server
dat@ubuntu:/ds2025/File_transfer_using_TCP_socket$ ./server
[+] Socket of server connected
[+] bind successfully
[+] Listening for connections...
```

- Client

```
dat@ubuntu:/ds2025/File_transfer_using_TCP_socket$ gcc client.c -o client
dat@ubuntu:/ds2025/File_transfer_using_TCP_socket$ ./client
[+] Socket of server connected
[+] connect to server successfully
[+] Data sent successfully to server
```

- Now in Server

```
[+] Data received and written to 'test2.txt' successfully
```

### open_clientfd.c

Reference : https://www.cse.psu.edu/~deh25/cmpsc311/Lectures/Sockets/open_clientfd.c
```c
/*
 * open_clientfd - open connection to server at <hostname, port> 
 *   and return a socket descriptor ready for reading and writing.
 *   Returns -1 and sets errno on Unix error. 
 *   Returns -2 and sets h_errno on DNS (gethostbyname) error.
 */

typedef struct sockaddr SA;

int open_clientfd(char *hostname, int port) 
{
  int clientfd;
  struct hostent *hp;
  struct sockaddr_in serveraddr;

  if ((clientfd = socket(AF_INET, SOCK_STREAM, 0)) < 0)
    return -1; /* check errno for cause of error */

  /* Fill in the server's IP address and port */
  if ((hp = gethostbyname(hostname)) == NULL)
    return -2; /* check h_errno for cause of error */

  bzero((char *) &serveraddr, sizeof(serveraddr));
  serveraddr.sin_family = AF_INET;
  bcopy((char *) hp->h_addr_list[0], 
        (char *) &serveraddr.sin_addr.s_addr,
        hp->h_length);
  serveraddr.sin_port = htons(port);

  /* Establish a connection with the server */
  if (connect(clientfd, (SA *) &serveraddr, sizeof(serveraddr)) < 0)
    return -1;

  return clientfd;
}
```

### open_listenfd.c

Reference : https://www.cse.psu.edu/~deh25/cmpsc311/Lectures/Sockets/open_listenfd.c
```c    
/*  
 * open_listenfd - open and return a listening socket on port
 *     Returns -1 and sets errno on Unix error.
 */

typedef struct sockaddr SA;

int open_listenfd(int port) 
{
  int listenfd, optval=1;
  struct sockaddr_in serveraddr;
  
  /* Create a socket descriptor */
  if ((listenfd = socket(AF_INET, SOCK_STREAM, 0)) < 0)
    return -1;
 
  /* Eliminates "Address already in use" error from bind. */
  if (setsockopt(listenfd, SOL_SOCKET, SO_REUSEADDR, 
                 (const void *)&optval , sizeof(int)) < 0)
    return -1;

  /* Listenfd will be an endpoint for all requests to port
     on any IP address for this host */
  bzero((char *) &serveraddr, sizeof(serveraddr));
  serveraddr.sin_family = AF_INET; 
  serveraddr.sin_addr.s_addr = htonl(INADDR_ANY); 
  serveraddr.sin_port = htons((unsigned short) port); 

  if (bind(listenfd, (SA *) &serveraddr, sizeof(serveraddr)) < 0)
    return -1;

  /* Make it a listening socket ready to accept connection requests */
  if (listen(listenfd, LISTENQ) < 0)
    return -1;

  return listenfd;
}

Explain
```