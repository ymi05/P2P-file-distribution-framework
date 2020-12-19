# P2P-file-distribution-framework
The following code represents a basic Peer-to-Peer file distribution framework
## How to run

1. You must run the tracker.py file
The tracker file listens to incoming incoming connections TCP/UDP and behaves accordingly 
```bash
python tracker.py
```
2. Run Peer.py and make sure to change the name and port of each peer 
Note: 
- You can run as many peers as you want.
- Peers hold chunks of files that are not found at the tracker
```python
def Main():
    peer = Peer({peer name} , portNumber={port Number})
    peer.start()    
```
```bash
python peer.py
```
3. run app.py where you can request the files you want from the tracker. 
```bash
python app.py
```

## By
- [Adam Helal](https://github.com/AdamHelal)
- [Youssef Itani](https://github.com/ymi05)

