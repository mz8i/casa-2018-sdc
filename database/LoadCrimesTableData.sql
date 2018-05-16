load data local infile '/home/maciek/Documents/DropboxLargeFiles/Studia/UCL/SDC/Crimes_-_2001_to_present.csv'
into table Crimes
fields terminated by ','
optionally enclosed by '"'
lines terminated by '\n'
ignore 1 lines
(ID, CaseNumber, @Date, Block, IUCR, PrimaryType, Description, 
LocationDescription, @Arrest, @Domestic, Beat, District, Ward,
CommunityArea, FBICode, XCoordinate, YCoordinate, Year,
@UpdatedOn, Latitude, Longitude, Location)
SET Date := str_to_date(@Date, '%m/%d/%Y %I:%i:%S %p'),
Arrest := @Arrest = 'true',
Domestic := @Domestic = 'true',
UpdatedOn := str_to_date(@UpdatedOn, '%m/%d/%Y %I:%i:%S %p');