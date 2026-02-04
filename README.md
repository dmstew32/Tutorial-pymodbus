\# Tutorial-pymodbus



Modbus RTU Server/Client implementation using pymodbus.



\## Setup

1\. Create virtual environment: `python -m venv venv`

2\. Activate: `venv\\\\Scripts\\\\activate`

3\. Install dependencies: `pip install -r requirements.txt`



\## Register Map

Server supports Read Holding Registers (0x03) for:

\- 0x0000

\- 0x0005-0x0008

\- 0x0010-0x0012

\- 0x001A-0x001F

\- 0x0020-0x0022

\- 0x002A-0x002F

\- 0x01F4-0x01F9

