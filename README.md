# SAM-Kahuna9600-TallyMonitor
Very basic interface to monitor sources tallied by a SAM Kahuna 9600

![image](https://github.com/user-attachments/assets/3f8a000a-38c3-4c33-8f8f-3e980ef43a5a)


## Control Bytes

Kahuna appears to use different control bytes to signify the tally level of the source selected. <br>
The unit being used here has two switchers. I am not sure how the control bytes are assigned at this stage but;


0x0 = source not curently in use<br>
0xA0 = PGM source (Swicher 1)<br>
0x90 = PGM source (switcher 2)<br>
0xC0 = PVW Source (Swicther 1)<br>



## Nodejs and Python

There are two versions of the script;<br>
<br>
1. Python Flask webserver (app.py) <br>
2. Nodejs script (KahunaTally.js)<br>
<br>
<br>
Two two verisons of the script work independently of each other. The idea was original written out as a Nodejs script, but worked into a python function for the web app. <br>
The Nodejs version has a debug mode;<br>

## Using Flask app;

```bash
python app.py -i KAHUNA-IP -p KAHUNA-PORT
```

## Using Nodejs Script;

```bash
node KahunaTally.js -h KAHUNA-IP -p KAHUNA-PORT --debug
```
<br>
Output of the Nodejs script with debug option will offer up all the raw sources and their reqpective control bytes. This can be used to taylor the web app. <br>
<br>
It will give you something that looks like this;

```bash
=======================================
Raw source: DVE1 OP1F
In ignore list?: false
Control byte: 0x0
=======================================
=======================================
Raw source: DVE1 OP1K
In ignore list?: false
Control byte: 0x0
=======================================
=======================================
Raw source: CCU 1
In ignore list?: false
Control byte: 0xA0
=======================================
=======================================
Raw source: CCU 2
In ignore list?: false
Control byte: 0x0
=======================================
=======================================
Raw source: CCU 3
In ignore list?: false
Control byte: 0x0
=======================================
```
