for a in `ls -rt ~/Maildir/new`
do
 subject=`~/.local/bin/mailparser -f ~/Maildir/new/$a -u`

 flag=`echo $subject|awk '{print match($0,"SRS - Alert Hardware Fault")}'`;
 if [ $flag -gt 0 ];then
  ~/.local/bin/mailparser -f ~/Maildir/new/$a -b >> ~/dfsioms/omshwfile.txt
  rm ~/Maildir/new/$a
 fi

 flag=`echo $subject|awk '{print match($0,"SRS - Alert Software Fault")}'`;
 if [ $flag -gt 0 ];then
  ~/.local/bin/mailparser -f ~/Maildir/new/$a -b >> ~/dfsioms/omsswfile.txt
  rm ~/Maildir/new/$a
 fi
done
/usr/bin/python3 ~/dfsioms/oms2alert_hw.py
/usr/bin/python3 ~/dfsioms/oms2alert_sw.py

