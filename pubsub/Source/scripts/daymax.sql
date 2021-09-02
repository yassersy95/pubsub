select deviceid, max(temperature) from weather_trans where FROM_UNIXTIME(time,'%d') = @d  and FROM_UNIXTIME(time,'%m') = @m group by deviceid;
