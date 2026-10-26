# Plain text protocol
* Run plain text server
```bash
uv run plain_text_server.py
```

* Connect with telnet
```bash
telnet localhost 65432
```

# Simple HTTP web server 
**Note:** This is just a partial implementation of the HTTP protocol which supports only GET method.
* Run simple http server
```bash
uv run simple_http.py
```

* Open browser
http://localhost:8080

# Binary Protocol
* Run plain text server
```bash
uv binary_server.py
```

* Send binary data
```bash
echo -ne "\x00\x00\x00\x0e\x01\x48\x65\x6c\x6c\x6f\x2c\x20\x73\x65\x72\x76\x65\x72\x21" | nc 127.0.0.1 65432
```