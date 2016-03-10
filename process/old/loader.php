<?php
require_once("config/config.php");
#var_dump(JSONBASEDIR);
#echo("Done loading loader.php\n");

//should be converted to a lazy loader!
require_once(CLASSPATH.'/jsonObject.class.php');

//load tigerdirect classes
require_once(CLASSPATH.'/tigerdirect/tdIdentifyObject.class.php');
?>
