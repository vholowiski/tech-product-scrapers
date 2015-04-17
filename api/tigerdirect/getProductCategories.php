<?php
/*
	getProductCategories.php
	returns product categories as json, queried from mongodb

	TODO: Move appropriate stuff in to classes.
	TODO: Figure out how to handle multiple results. Probably just return an array of mongoids?
		anyway, mostly i'll be searching by id. but sometimes name.
*/


require_once("../shared/mongoConfig.php");
require_once(__DIR__."/classes/database/mongoCategories.php");

#TODO: error checking! robust!
//$m = new MongoClient("mongodb://".MONGO_SERVER_IP.":".MONGO_SERVER_PORT);
//$db = $m->{MONGO_DATABASE};
//$collectionCategory = $db->{MONGO_TABLE_TD_CATEGORY};

#for now, just find one. set up to accept params

//$query = array(MONGO_ITEM_TYPE_FIELD=>MONGO_CATEGORY_FIELD);

//$document = $collectionCategory->findOne($query);
//$document = $collectionCategory->findOne(array('_id' => new MongoId('5527d83c4184797db0b15cde')));
//var_dump( $document );

$abc = new mongoCategories(MONGO_SERVER_IP, MONGO_SERVER_PORT, MONGO_DATABASE);
$mongoID = new MongoId('5527d83c4184797db0b15cde');

var_dump($abc->getCategoryByMongoID($mongoID));

?>
