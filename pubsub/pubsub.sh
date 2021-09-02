while true; do
        a=`ps -ef | grep 'python Sensor.py' | wc -l`
        if [ $a -lt 2 ]; then
          sudo echo "launching Sensor"
          `python $HOME/pubsub/source/Sensor.py &`
        fi
		
		a=`ps -ef | grep 'python checkanomal.py' | wc -l`
        if [ $a -lt 2 ]; then
          sudo echo "launching detector"
          `python $HOME/pubsub/source/checkanomal.py &`
        fi

        a=`ps -ef | grep 'pub.py pubsub-weather weather_topic' | wc -l`
        if [ $a -lt 2 ]; then
          sudo echo "launching pub"
          `python $HOME/pubsub/source/pub.py $PROJECT weather_topic &`
        fi

        a=`ps -ef | grep 'sub.py pubsub-weather weather_sub' | wc -l`
        if [ $a -lt 2 ]; then
          sudo echo "launching sub"
          `nohup python $HOME/pubsub/source/sub.py $PROJECT weather_sub &`
        fi
		
		a=`ps -ef | grep 'api.py' | wc -l`
        if [ $a -lt 2 ]; then
          sudo echo "launching sub"
          `nohup python $HOME/pubsub/source/api/api.py&`
        fi
		
        sleep 10;
done
