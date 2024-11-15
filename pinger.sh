#/bin/bash
#IP to ping
IP=1.1.1.1

#local of log file:
log=/tmp/pinger.log

while true
do
	unset result
	unset reply
	result=$(ping -n -W 1 -c 1 $IP|awk 'NR==2 {print $0}')
	#echo $result
	reply=$(echo $result |grep $IP)
	if [ -z "$reply" ]; then
		echo "" >> $log
	else
		echo "$result" >> $log
		#Used 997 instead of 1000 to account for the 0.003 second lost over the sleep command.
		sleeptime=$(echo $result|awk '{print $7}'|sed 's/time=//'|xargs echo "997 -"|bc|xargs -i echo "{} / 1000"|bc -l)
		sleep $sleeptime
	fi
done

