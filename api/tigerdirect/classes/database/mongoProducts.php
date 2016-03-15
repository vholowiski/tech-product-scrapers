<?php

class mongoProducts {
	const MONGO_TABLE_TD_PRODUCT = "td_product";

	const MONGO_ITEM_TYPE_FIELD = "itemType";
	const MONGO_PRODUCT_TYPE_VALUE = "product";
	#define("MONGO_ITEM_TYPE_FIELD", "itemType");
	#define("MONGO_CATEGORY_FIELD", 'category');

	private $serverIP;
	private $serverPort;
	private $database;
	private function setServerIP($ip) { $this->serverIP = $ip; }
	private function getServerIP() { return $this->serverIP; }
	private function setServerPort($port) { $this->serverPort = $port; }
	private function getServerPort() { return $this->serverPort; }
	private function setDatabase($database) { $this->database = $database; }
	private function getDatabase() { return $this->database; }

	private $mongoClient;
	private function setMongoClient($client) { $this->mongoClient = $client; }
	private function getMongoClient() { return $this->mongoClient; }
	private $mongoDb;
	private function setMongoDB($db) { $this->mongoDB = $db; }
	private function getMongoDB() { return $this->mongoDB; }

	public function __construct($serverIP, $serverPort, $database) {
		$this->setServerIP($serverIP);
		$this->setServerPort($serverPort);
		$this->setDatabase($database);

		#should surround in a try/catch
		$conn = new MongoClient("mongodb://".$this->getServerIP().":".$this->getServerPort());
		$db = $conn->{$this->getDatabase()};
		$this->setMongoClient($conn);
		$this->setMongoDB($db);

	}

	function __destruct() {
       
   }

   public function getProductsByCategoryID($tdCatID) {
   	$tdCatID= strval($tdCatID);
   	$mongoDBConn = $this->getMongoDB();
	$mongoCat = $mongoDBConn->td_product;
	
	#fuck. dunno if im getting a string or an int, and if i need to search a string or int!
	#lets try searching as an int first!
	$intTdCatID = (int) $tdCatID;
	#var_dump($intTdCatID);
	$result = $mongoCat->find( array('tdCategoryID'=>$intTdCatID) );
	#var_dump($result->count());
	if ($result->count() == 0) {
		$strTDCatID = (string) $tdCatID;
		#var_dump($strTDCatID);
		$result = $mongoCat->find( array('tdCategoryID'=>$strTDCatID) );
		#var_dump($result->count());
	}
	return $result;
   }

   public function getProductPrice($tditemID) {
   	echo("UNTESTED");
   	$mongoDBConn = $this->getMongoDB();
   	$mongoPrice = $mongoDBConn->td_price;
   	$newestPrice = $mongoPrice->find()->sort(array('crawlTimestamp'=>-1))->limit(1);
   	var_dump($newestPrice);
   	return $newestPrice;
   }

/*	public function getCategoryByMongoID($mongoID) {
		Gets a single category, by it's mongoID
		Expects a data type MongoID
		Returns an associative array which is the category object

		$mongoDBConn = $this->getMongoDB();
		$mongoCat = $mongoDBConn->MONGO_TABLE_td_product;
		#$mongoID = new MongoID($mongoID);
		$document = $mongoCat->findOne(array('_id' => $mongoID));

		return $document;

	}

	public function getOneCategoryByID($tdCatID) {
		$mongoDBConn = $this->getMongoDB();
		$mongoCat = $mongoDBConn->td_product;
		$result = $mongoCat->findOne(array('tdCategoryID'=>$tdCatID));
		return $result;
	}

	public function getAllParentCategories() {
		$mongoDBConn = $this->getMongoDB();
		$mongoCat = $mongoDBConn->td_product;
		$result = $mongoCat->find(array('tdCategoryLevel'=>1));
		return $result;		
	}

	public function getChildCategories($parentID) {
		$mongoDBConn = $this->getMongoDB();
		$mongoCat = $mongoDBConn->td_product;
		$result = $mongoCat->find(array('tdCategoryParent'=>$parentID));
		//var_dump($parentID);
		//var_dump($result->count());
		return $result;
	}

	public function getCategories($query = false) {
		$mongoDBConn = $this->getMongoDB();
		$mongoCat = $mongoDBConn->td_product;

		//$mongoCat = $this->getMongoDB();
		if (!$query) {
			//the default query
			$result = $mongoCat->find();
		}
		//print_r($result->count());
		return $result;
	}

	public function buildQuery($stuff, $things) {
		$query = array();

		return $query;
	}*/

}

?>