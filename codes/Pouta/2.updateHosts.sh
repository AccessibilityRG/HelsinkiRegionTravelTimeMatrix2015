# Get local IP
LocalIP="$(ifconfig eth0 | grep 'inet addr' | cut -d: -f2 | cut -d ' ' -f1)" 

# Change local IP to hosts
command="/.novalocal/s/127.0.0.1/$LocalIP/g"
sed -i.bkp -e $command /etc/hosts 
