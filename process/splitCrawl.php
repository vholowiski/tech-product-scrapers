<?php
require_once("loader.php");

define('SILENT', false);
define('DEBUG', true);
/*
define('BASEDIR', "/home/dholowiski/scraper/tech-product-scrapers");
define('CONFIGDIR', "/home/dholowiski/scraper/tech-product-scrapers/process/config");

define('JSONBASEDIR', "/home/dholowiski/tech-product-scrapers/json/crawled");
define('JSONSOURCEDIR', "/home/dholowiski/tech-product-scrapers/json/preprocessed");
define('JSONMFGDIR', "/home/dholowiski/tech-product-scrapers/json/manufacturers");
*/
#var_dump(JSONBASEDIR);
#echo("starting getManufacturers.php\n");



$directory_iterator = new RecursiveDirectoryIterator(JSONBASEDIR);

foreach (new RecursiveIteratorIterator($directory_iterator) as $filename => $file) {
	
	//TODO handle . and .. or in general non-json files

	$js = new jsonObject($filename, false, true);
	$json = $js->getjsonOBJ();
	//var_dump($json);
	
	//var_dump($filename);
	/*$arryFilename = explode('.', $filename);
	//var_dump($arryFilename);

	if ( isJsonFile($filename) ) {
		//if (!SILENT) {  echo("Processing file: $filename | Size: ".filesize($filename)."\n"); }
		$fileContents = loadFile($filename);
		//var_dump($fileContents);
		if ( !($fileContents === false) ) {
			if (!SILENT && DEBUG ) { echo("Loading JSON\n"); }
			$json = processJSON($fileContents);
			//var_dump($json);
			

		}
	}*/

	
}


function loadFile($filename) {
	$fileContents = false; //initialize the variable - in case the function fails

	try {
		if (!SILENT) {  echo("Processing file: $filename | Size: ".filesize($filename)."\n"); }
		$fileContents = file_get_contents($filename);
	} catch ( Exception $e ) {
		if (!SILENT) { var_dump( $e ); }
	}
	return $fileContents;
}

function isJsonFile($filename) {
	$jsonExtension = "json";

	$arryFilename = explode('.', $filename);
	if ( end($arryFilename) == $jsonExtension ) { return true; } else { return false; }
}

function processJSON($string, $returnArray = true) {
	$json = false; //initialize the variable - in case the function fails'
	
	//var_dump($json);
	try {
		$json = json_decode( $string, $returnArray );
	} catch ( Exception $e ) {
		if (!SILENT) { var_dump( $e ); }
	}
	//var_dump($json);
	return $json;
}


