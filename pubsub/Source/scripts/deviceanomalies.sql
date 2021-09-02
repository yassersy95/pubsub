select deviceid, temperature from weather_trans where isanomal = 1 and UNIX_TIMESTAMP() - time < 1800 order by deviceid;
