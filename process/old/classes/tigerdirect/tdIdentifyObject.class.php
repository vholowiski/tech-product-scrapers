<?php

class tdIdentifyObject {
	private $silent = false;
	private $debug 	= false;

	private $productKey = "product";
	private $categoryKey = "category";

	function __construct($silent = false, $debug = false) {
		//set up initial stuff
		$this->setSilent($silent);
		$this->setDebug($debug);
	}

	public function findType($item) {
		$itemType = false;

		if ( $this->isProduct($item) ) 	{ $itemType = $this->getProductKey(); }
		if ( $this->isCategory($item) ) { $itemType = $this->getCategoryKey(); }

		return $itemType;
	}

	private function isProduct($item) {
		$isProduct = false;

		if ( isset($item["type"]) ) {
			if ( $item["type"] == ( $this->getProductKey() ) ) {
				$isProduct = true;
			}
		}

		return $isProduct;
	}

	private function isCategory($item) {
		$isCategory = false;

		if ( isset($item["type"]) ) {
			if ( $item["type"] == ( $this->getCategoryKey() ) ) {
				$isCategory = true;
			}
		}

		return $isCategory;
	}

	//setters and getters
	private function setSilent( $silent )			{ $this->silent = $silent;	}
	private function setDebug( $debug ) 			{ $this->debug = $debug;	}

	private function getSilent()					{ return $this->silent;		}
	private function getDebug() 					{ return $this->debug;		}
	
	//public getters/setters
	public function getProductKey()					{ return $this->productKey;	}
	public function getCategoryKey()				{ return $this->categoryKey; }
}
?>