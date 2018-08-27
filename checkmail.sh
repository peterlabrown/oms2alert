for a in `ls -rt ~/Maildir/$1`
do
 body=`~/.local/bin/mailparser -f ~/Maildir/$1/$a -b`
 echo $a: $body
done

