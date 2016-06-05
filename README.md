# CAN-Translator
## Toyota Prius CAN message translator
 
 The Toyota Prius is currently the most popular hybrid automobile on the market. Its hybrid system relies on the vehicles many sensors to operate at highest efficiency, and the car relays data to the user in the form of mileage and energy consumption charts. This project aims to validate data broadcast on the CAN bus and determine how some UI data presented to the user is calculated. A VSI-2534 with DLM2 software was used to connect to the vehicle, and a VBox was used to validate vehicle speed using its GPS. Wheel speed CAN IDs were found along with an ID that appears to calculate speed through averaging the wheel speeds. It was found that mileage data was not broadcast directly on the bus so fuel economy was determined through use of speed and fuel injector CAN data. A python program was used to generate plots from different CAN log files generated.
 
 Example data, charts, and data translators are included in folders.
