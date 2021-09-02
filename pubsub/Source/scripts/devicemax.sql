use weather;
select deviceid, max(temperature) temp from weather_trans group by deviceid;
