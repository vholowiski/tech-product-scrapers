<?php

class mongoCategories {
	const MONGO_TABLE_TD_CATEGORY = "td_category";

	const MONGO_ITEM_TYPE_FIELD = "itemType";
	const MONGO_CATEGORY_FIELD = "category";
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
       echo "Destroying mongoCategories\n";
   }

	public function getCategoryByMongoID($mongoID) {
		/*Gets a single category, by it's mongoID
		Expects a data type MongoID
		Returns an associative array which is the category object*/

		$mongoDBConn = $this->getMongoDB();
		$mongoCat = $mongoDBConn->MONGO_TABLE_TD_CATEGORY;
		#$mongoID = new MongoID($mongoID);
		$document = $mongoCat->findOne(array('_id' => $mongoID));

		return $document;

	}

	public function getCategories($query = false) {
		$mongoDBConn = $this->getMongoDB();
		$mongoCat = $mongoDBConn->td_category;

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
	}

}

?>