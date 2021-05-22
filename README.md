# Introduction
This folder contains the implementation of connectors form Smart Museum Management System project.

## Run the connectors
1.  Before running connectors, homeCat should be running first. See README.md under homeCat folder.
2.  Go to connector root directory:
    ```
    $ cd connector
    ```
3.  Run laserConnector with:
    ```
    $ python laserConnector.py
    
    # Then will ask to enter laser connector configurations:
    ./configs/laserConfig.json
    
    # Then you can choose the working mode
    
    # If you choose replay mode, you will be asked for record file:
    ./record/laserRecord.json
    
    ```
4.  To run other connectors, use the similar command as step 2
5.  The ImageManger should run in a independent terminal together with cameraConnector to achieve full function of cameraConnector.

## Communication Data Format
* Data send to message borker(publisher)
  1. Laser sensors
   <br>Topic:   /museumId/floorNum/gateNum/laser
   <br>Message: ```{"laserId":"laser0","timestamp":"","enter":0, "leaving":0} ```
   <br>Note: numbers could be positive integer or 0
   <br/>

    2. Infraed camera
    <br>Topic:  /museumId/entranceId
	<br>Message:```{"cameraId":"camera0","timestamp":"","sequenceNum":0, "temperature":36.5} ```
	<br>Note:   "secquenceNum" should be double type, "temperature" should be float
    <br/>    

* Data receive form message borker(subscriber)
    1. Motor controller
    <br>Topic:  Not set yet
	<br>Message:```{"motroControlerId":"motor0","timestamp":"", "targetStatus":"open"}```
	<br>Note:   value of "targetStatus" could be "open"/"close"
    
    2. Light controller
    <br>Topic:  Not set yet
	<br>Message:```{"lightControllerId":"light0","timestamp":"","brightness":0}```
	<br>Note:   value of "brightness" could be in range [0,100], means(0% to 100%)

## Registration Data Format
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
    "leavingZone":"zone2",
    "currentStatus":"close"}
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
