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
	//var_dump($filename);
	$arryFilename = explode('.', $filename);
	//var_dump($arryFilename);

	if ( isJsonFile($filename) ) {
		//if (!SILENT) {  echo("Processing file: $filename | Size: ".filesize($filename)."\n"); }
		$fileContents = loadFile($filename);
		//var_dump($fileContents);
		if ( !($fileContents === false) ) {
			if (!SILENT && DEBUG ) { echo("Loading JSON\n"); }
			$json = processJSON($fileContents);
			//var_dump($json);
			$manArray = getAllManufacturers($json);
			echo ("Found ".count($manArray)." manufacturers.\n");
			$manJSON = json_encode($manArray);
			var_dump($arryFilename[0]);
			//var_dump(JSONSOURCEDIR."/$file"."_manufacturers.json");
			//file_put_contents(JSONSOURCEDIR."/$filename_manufacturers.json", $manJSON);

			$catArray = getCategories($json);
			echo ("Found ".count($catArray)." categories.\n");
			$catJSON = json_encode($catArray);

		}
	}

	
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

function getAllManufacturers($json) {
	$manArray = array();

	foreach ($json as $element) {
		if ($element["type"] = "category") {

			//get unique manufacturers
			if ( isset( $element["manufacturers"] ) ) {
				$a = getCategoryManufacturers($element["manufacturers"]);
				//var_dump($a);
				//var_dump($manArray);
				$manArray = $manArray + $a;

				/*$manufacturers = $element["manufacturers"];
				foreach ( $manufacturers as $mfg ) {
					//var_dump($key);
					//var_dump($value);
					$manArray[$mfg['mfgID']] = $mfg['name'];
					//echo ("Key: ".$mfg['name']." | Value: ".$mfg['mfgID']."\n");
				}*/
			}
			//get unique categories

		}
	}
	if ( count($manArray) > 0 ) {
		return $manArray;
	} else {
		return false;
	}
}

function getCategoryManufacturers($manufacturers) {
	$return = array();
	foreach ( $manufacturers as $mfg ) {
		//var_dump($key);
		//var_dump($value);
		$return[$mfg['mfgID']] = $mfg['name'];
		//echo ("Key: ".$mfg['name']." | Value: ".$mfg['mfgID']."\n");
	}
	return $return;
}

function getCategories($json) {
	$catArray = array();
	
	foreach ($json as $element) {
		if ( ($element["type"] == "category") && ( !isset($element["hierarchy"]) && ( isset($element["id"]) ) ) ) {
			//var_dump($element);
			//sleep(10);
			$category = array();
			if (isset($category['name'])) { $category['name'] = $element['name']; }
			if ( isset( $element["manufacturers"] ) ) {
				$manufacturers = getCategoryManufacturers($element["manufacturers"]);
				$category['manufacturers'] = $manufacturers;
			}
			//var_dump($category);
			$catArray[$element["id"]] = $category;
		}
	}
	//var_dump($catArray);
	return $catArray;

}
