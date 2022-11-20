#ifndef _STDAFX_H
#define _STDAFX_H

#ifdef _WIN32

//Windows specific includes
#define WINVER 0x501
#define _CRT_SECURE_NO_WARNINGS
#define _WINSOCK_DEPRECATED_NO_WARNINGS
#include <WinSock2.h>
#include <WS2tcpip.h>
#include <stdio.h>
#include <time.h>
#include <stdint.h>

#else //#ifdef _WIN32

//other OS includes and some tricks to fake Win32 API
#include <pthread.h>
#include <sys/socket.h> 
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
#include <stdint.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>
#include <time.h>
typedef int SOCKET;
#define SOCKET_ERROR (-1)
#define closesocket(hSock) close(hSock)
#define WSAGetLastError() errno
#define CRITICAL_SECTION pthread_mutex_t
#define InitializeCriticalSection(criticalSection) pthread_mutex_init(criticalSection, NULL)
#define EnterCriticalSection(criticalSection) pthread_mutex_lock(criticalSection)
#define LeaveCriticalSection(criticalSection) pthread_mutex_unlock(criticalSection)

#endif //#ifdef _WIN32

#endif //#ifndef _STDAFX_H
