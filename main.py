from HideMe import HideME as proxy

if __name__ == '__main__':
    """
    page - Page count INT
    ================================
    max_time - Speed ms INT
    ================================
    types: STR
    h - HTTP: regular proxies that support HTTP requests. You can use them to view websites and download files over HTTP.
    s - HTTPS: Also called SSL-enabled proxy servers. Allow you to view HTTPS sites. Using specialized programs, they can be used for any protocol, like SOCKS proxy servers.
    4 - Socks 4: Proxies that support the SOCKS protocol version 4. They can be used to connect over TCP / IP protocol to any address and port.
    5 - Socks 5: Includes all the features of version 4. Additional features include use of the UDP Protocol, the ability to make DNS requests through a proxy, and use of the BIND method to open the port for incoming connections.
    ================================
    anon: INT
    1 - No anonymity: The remote server knows your IP address and knows that you are using a proxy.
    2 - Low anonymity: The remote server does not know your IP, but knows that you are using a proxy.
    3 - Average anonymity: The remote server knows that you are using a proxy and thinks that it knows your IP, but it is not yours (these are usually multi-network proxies that show the remote server the incoming interface as REMOTE_ADDR).
    4 - High anonymity: The remote server does not know your IP, and it has no direct evidence that you are using a proxy. These are anonymous proxies.
    ================================
    """
    proxy(url='/proxy-list/', max_time=500, types='s')
