for a in `ls -rt ~/Maildir/$1`
do
 subject=`~/.local/bin/mailparser -f ~/Maildir/$1/$a -u`
 body=`~/.local/bin/mailparser -f ~/Maildir/$1/$a -b`
# echo $a: $body
 echo $a: $subject
done

