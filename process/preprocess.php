<?php

if ( count($argv) > 2 ) {
 $filename = $argv[1];
} else {
 exit(1);
}

if ( !file_exists($filename) ) {
 echo("Error: file not found\n");
 exit(1);
}

?>
