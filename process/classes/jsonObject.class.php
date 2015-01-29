<?php

class jsonObject {
	private $silent = false;
	private $debug 	= false;

	private $strPath 		= false;
	private $strFileName 	= false;
	private $strFileExtension = false;

	private $jsonOBJ = array();

	function __construct($filename, $silent = false, $debug = false) {
		//set up initial stuff
		$this->setSilent($silent);
		$this->setDebug($debug);

		$this->parseFileNameAndPath($filename);
		$strFileContents = $this->loadFile($filename);
		$jsonFileContents = $this->parseJSON($strFileContents);

		$this->setjsonOBJ($jsonFileContents);
	}

	private function loadFile($filename) {
		$fileContents = false; //initialize the variable - in case the function fails

		//try {
			if (!SILENT) {  echo("Processing file: $filename | Size: ".filesize($filename)."\n"); }
			$fileContents = file_get_contents($filename);
		//} catch ( Exception $e ) {
		//	if (!SILENT) { var_dump( $e ); }
		//}
		return $fileContents;
	}

	/*private function isJsonFile($filename) {
		$jsonExtension = "json";

		$arryFilename = explode('.', $filename);
		if ( end($arryFilename) == $jsonExtension ) { return true; } else { return false; }
	}*/

	private function parseJSON($string, $returnArray = true) {
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

	private function parseFileNameAndPath($filename) {
		//TODO handle escaped slashes \\ !
		$arryPath = explode('/', $filename);	//first, seperate along the slashes
		if ( $this->getDebug() ) { 
			echo("-----------arryPath----------\n"); 
			var_dump($arryPath);
			echo("-----------arryPath----------\n"); 
		}
		$strFile = array_pop($arryPath);			//the last element is the file name
		if ( $this->getDebug() ) { 
			echo("-----------strFile----------\n"); 
			var_dump($strFile);
			echo("-----------strFile----------\n"); 
		}

		$this->setPath( $this->arrayToPath($arryPath) );
		
		$arryFilename = $this->splitFilename($strFile);
		$this->setFileName($arryFilename[0]);
		$this->setFileExtension($arryFilename[1]);

	}

	private function arrayToPath($array) {
		$strPath = rtrim( implode('/',$array), '/' );

		if ( $this->getDebug() ) { 
			echo("-----------strPath----------\n"); 
			var_dump($strPath);
			echo("-----------strPath----------\n"); 
		}

		return $strPath;
	}
	private function splitFilename($filename) {
		$arryFilename = explode( '.', $filename );
		if ( $this->getDebug() ) { 
			echo("-----------arryFilename----------\n"); 
			var_dump($arryFilename);
			echo("-----------arryFilename----------\n"); 
		}
		return $arryFilename;
	}

	//setters and getters
	private function setSilent( $silent )			{ $this->silent = $silent;	}
	private function setDebug( $debug ) 			{ $this->debug = $debug;	}
	private function setPath( $strPath ) 			{ $this->strPath = $strPath;}
	private function setFileName( $strFileName )	{ $this->strFileName = $strFileName; }
	private function setFileExtension( $strFileExtension ) { $this->strFileExtension = $strFileExtension; }
	private function setjsonOBJ($jsonOBJ)			{ $this->jsonOBJ = $jsonOBJ;}

	private function getSilent()				{ return $this->silent;		}
	private function getDebug() 				{ return $this->debug;		}
	private function getPath() 					{ return $this->strPath;	}
	private function getFileName() 				{ return $this->strFileName;	}
	private function getFileExtension() 		{ return $this->strFileExtension;	}
	
	//public getter
	public function getjsonOBJ()				{ return $this->jsonOBJ;	}
}
?>