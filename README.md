# An IoT based Smart Home System using HTTP
This is a brief description of An IoT based Smart Home System using HTTP.
## 1. Entities and Corresponding Files

### i) main.py  
Implements the functionalities of core features of the system: Monitoring room temperature and room light intensity.  
Implements the functionality of Wi-Fi connectivity.  
Implements the functionality of HTTP POST operation.  

### ii) lcd1502.py  
The library of external LCD 1602

### iii) esp8266.py  
This is a class for access ESP8266 using AT commands.

### iv) httpParser.py  
This is a class for parse HTTP response.

## 2. Runtime Environment  
In order to implement the system successfully, you need to install the following softwares or visiting following websites.

### i) Python Interpreter: 

[Welcome to Python.org](https://python.org/)

### ii) Thonny IDE: 

[Thonny, Python IDE for beginners](https://thonny.org/)

### iii) ThingsBoard Cloud: 

[ThinsBoard Cloud](https://thingsboard.cloud/)

### iv) Reliable Internet Connectivity. :)

## 3. Implementing the System

### i) Configure the Wi-Fi AP's SSID and password in main.py

`wifi_ssid = "***********" # Configure the ssid of wifi ap`

`wifi_pswd = "***********" # Configure the password of wifi ap`  

### ii) Connect the microcontroller to the USB port of the computer while pressing the "BOOTSEL" button on the board

This will clean the flash memory of the board.  

### iii) Install the firmware of MicroPython  

### iv) Load all the .py files to the microcontroller  

### v) Run the main.py file
