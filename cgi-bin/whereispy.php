<?php
$output = shell_exec('whereis python');
$output2 = shell_exec('/usr/bin/python -V');
echo "<pre>$output</pre>";
echo "<pre>$output2</pre>";
?>