# usage: crackencfs.sh /path/to/encrypted/folder /path/to/mountpoint /path/to/wordlist
counter=1

while [ true ]; do
   echo "$(head -n $counter $3 | tail -n 1)" | encfs $1 $2 --stdinpass 
    if [ $? -eq 0 ]; then
        echo Key recovered - the password is: 
        echo "$(head -n $counter $3 | tail -n 1)"
        exit
    fi
    counter=$(($counter + 1))
done
