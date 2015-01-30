<?php

/*
	This is the first step of processing. 
	Seperates the single gigantic crawl file in to seperate files
	One for each object type
	Like - category, item, manufacturer etc
*/

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

//create a tiger direct identifier
$tdID = new tdIdentifyObject();

$directory_iterator = new RecursiveDirectoryIterator(JSONBASEDIR);

foreach (new RecursiveIteratorIterator($directory_iterator) as $filename => $file) {
	
	//TODO handle . and .. or in general non-json files

	$js = new jsonObject($filename, false, true);
	if ( $js->getFileIsJSON() ) {
		//parse the file in to json
		if (!SILENT ) { echo("Loading JSON... "); }
		$json = $js->getjsonOBJ();
		if (!SILENT ) { echo(count($json)." objects loaded.\n"); }

		//initialize counters:
		$productCount = 0;
		$categoryCount = 0;

		//loop through it
		if ( (count($json) > 0) ) {
			foreach ( $json as $item ) {
				$itemType = $tdID->findType($item);
				//var_dump($itemType);
				if ($itemType == ( $tdID->getProductKey() ) ) { $productCount++; }
				if ($itemType == ( $tdID->getCategoryKey() ) ) { $categoryCount++; }

			}
		}
		if (!SILENT ) { echo("Done processing. Found: $productCount products.\n"); }
		if (!SILENT ) { echo("Done processing. Found: $categoryCount categories.\n"); }

	} else {
		//if (!SILENT && DEBUG ) { echo("Skipping - not a JSON file $filename\n"); }
	}
	

	//now, line by line, identify what the object is
	//and put ti in the right place


	/*if ( isJsonFile($filename) ) {
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


