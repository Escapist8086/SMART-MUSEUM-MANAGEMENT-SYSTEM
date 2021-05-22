# Introduction
This folder contains the implementation of homeCat for Smart Museum Management System project. Home Catalog works as service and device registry system, it will use REST api for communication.

## Running HomeCat
To run homeCat with:
```
$ cd homeCat
$ python homeCat.py
```

## Museum Configuration
Before running homeCat, you should first define the general setting of the museum in the file configuration.json, with the format as below:
```
{
  "museumId": "museum123",
  "museumName": "Palazzo Reale",
  "floors": ["1","2","3"],
  "zones": ["zone1","zone2","zone3"],
  "entrances": ["Entrance1","Entrance2"]
}
```

## Registration
* **Devices** (Using PUT, data write in the body in json format)
    1. Laser
    ```
    {
    "registerType":"device",
    "id":"laser0",
    "type":"laser",
    "topic":"/museumeId/...",
    "attribute":{
        "floor":"1",
        "enterZone":"zone1",
        "leavingZone":"zone2"}
    }
    ```
    2. Camera
    ```
    {
    "registerType":"device",
    "id":"camera0",
    "type":"camera",
    "topic":"/museumId/...",
    "attribute":{
        "entranceId":"Entrance1",
        "motroControllerId":"motor123",
        "RESTaddr":"https://192.168.123.1:8090"}
    }
    ```
    3. Motor
    ```
    {
    "registerType":"device",
    "id":"motor0",
    "type":"motorController",
    "topic":"/museumId/...",
    "attribute":{
        "floor":"1",
        "enterZone":"zone1",
        "leavingZone":"zone2"}
    }
    ```
    4. Light
    ```
    {
    "registerType":"device",
    "id":"light0",
    "type":"lightController",
    "topic":"/museumId/...",
    "attribute":{
        "floor":"1",
        "controlZone":"zone1",
        "currentSataus":"open",
        "currentBrightness":50}
    }
    ```
    * Return (in body):
	<br>Format: 
	```
    {"status":"success","errorType":"error type","setting":""}
    ```
	Note1:  "setting" is the general configuration of the entire museum, or general setting
    <br>Note2:  "status" could be : success or fail

<br>Note:gate in main entrance should integrate with infraed camera, the corresponding controllerId will be placed in the attribute of camera in register.But the gate inside the museum for each zone can without camera.

* **Services** (Using PUT, data write in the body in json format)
	1. Telegram
	```
	{
    "registerType":"service",
    "Id":"serviceId",
    "type":"crowControl",
    "attribute":{...}
    }
    ```
    2. Crow Management
    ```
	{
    "registerType":"service",
    "Id":"serviceId",
    "type":"crowControl",
    "attribute":{...}
    }
    ```
    3. Health Management
    ```
    {
    "registerType":"service",
    "Id":"serviceId",
    "type":"crowControl",
    "attribute":{...}
    }
    ```
    * Return (in body):
	```
	{"registerStatus":"Success","errorType":"None"}
    ```
	

## Resource acquire:
Use GET, and specifiy the target resource with parameters
eg,
```
172.0.0.1:8080/devices/type?floor=2&enterZone=zone1  ==> acquire all lasers in the second floor
```
<br>Note1:type is defined in uri
<br>Note2:attributes are defined in param

Return data in body:
```
{status:"success","failType":"None",data:[{"deviceId":"","type":"","topic":"","attribute":{}},.......]}
```

## Delete Device in homeCat
Device/Service log out: (Using DELETE),using:	
```
172.0.0.1:8080/type/id
```    
type: device,service
* body is not allow in DELETE
* no return value
