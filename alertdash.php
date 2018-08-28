<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta http-equiv="refresh" content="60">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>DFSI SRS Hardware Status</title>
<meta name="description" content="console for SRS hardware alert status">
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">
<style>
.borderlesshdr th {
  border: none;
}
th.rotate {
  /* Something you can count on */
  height: 145px;
  white-space: nowrap;
}

th.rotate > div {
  transform: 
    /* Magic Numbers */
    translate(5px, 100px)
    /* 45 is really 360 - 45 */
    rotate(315deg);
  width: 10px;
}
th.rotate > div > span {
  border-bottom: 1px solid #ccc;
  padding: 1px 1px;
}
</style>
</head>
<body>
<div class="container">
<div class="row">
<div class="col-md-12">
<table class='table borderlesshdr'>
<tr>
<th class="rotate"><div><span>Time Stamp</span></div></th>
<th class="rotate"><div><span>SRS</span></div></th>
<th class="rotate"><div><span>Conference Mic</span></div></th>
<th class="rotate"><div><span>Conference Speaker</span></div></th>
<th class="rotate"><div><span>Default Speaker</span></div></th>
<th class="rotate"><div><span>Camera</span></div></th>
<th class="rotate"><div><span>Display</span></div></th>
<th class="rotate"><div><span>Motion Detector</span></div></th>
<th class="rotate"><div><span>HDMI Ingress</span></div></th>
<th class="rotate"><div><span>Network</span></div></th>
<th class="rotate"><div><span>Exchange</span></div></th>
<th class="rotate"><div><span>Sign In</span></div></th>
</tr>
<?php
$hostname="localhost";
$username="peter";
$password="ay2M7lE5YKqZ2kAb";
$dbname = "dfsioms";

// Create connection
$conn = new mysqli($hostname, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$sql = "SELECT hw.datetime, hw.computer, hw.confmic, hw.confspeaker, hw.defaultspeaker, hw.camera, hw.display, hw.motion, hw.hdmi, sw.network, sw.exchange, sw.signin, ( hw.confmic + hw.confspeaker + hw.defaultspeaker + hw.camera + hw.display + hw.motion + hw.hdmi ) AS hwalerttotal, ( sw.network + sw.exchange + sw.signin ) AS swalerttotal FROM `alertstate` hw LEFT JOIN swalertstate sw ON hw.computer = sw.computer ORDER BY `hwalerttotal` DESC, `swalerttotal` DESC, `datetime` DESC";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    // output data of each row
    while($row = $result->fetch_assoc()) {
        $localdt = new DateTime($row['datetime'], new DateTimeZone('UTC'));
        $localdt->setTimeZone(new DateTimeZone('Australia/Sydney'));
        if($row['hwalerttotal'] > 0 OR $row['swalerttotal'] > 0) {
            echo '<tr class="danger">';
        } else {
            echo '<tr class="success">';
        }
        echo "<td>" . $localdt->format('m-d H:i:s') . "</td>";
        echo "<td>" . $row['computer'] . "</td>";
        echo "<td>" . $row['confmic'] . "</td>";
        echo "<td>" . $row['confspeaker'] . "</td>";
        echo "<td>" . $row['defaultspeaker'] . "</td>";
        echo "<td>" . $row['camera'] . "</td>";
        echo "<td>" . $row['display'] . "</td>";
        echo "<td>" . $row['motion'] . "</td>";
        echo "<td>" . $row['hdmi'] . "</td>";
        echo "<td>" . $row['network'] . "</td>";
        echo "<td>" . $row['exchange'] . "</td>";
        echo "<td>" . $row['signin'] . "</td>";
        echo "</tr>"; 
    }
} else {
    echo "0 results";
}
$conn->close();
?>
</table>
</div>
</div>
</div>
</body>
</html>
