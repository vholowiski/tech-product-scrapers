<?php
/*
	getProductCategories.php
	returns product categories as json, queried from mongodb

	TODO: Move appropriate stuff in to classes.
	TODO: Figure out how to handle multiple results. Probably just return an array of mongoids?
		anyway, mostly i'll be searching by id. but sometimes name.
*/

require_once("../shared/mongoConfig.php");
#TODO: error checking! robust!
$m = new MongoClient("mongodb://".MONGO_SERVER_IP.":".MONGO_SERVER_PORT);
$db = $m->{MONGO_DATABASE};
$collectionCategory = $db->{MONGO_TABLE_TD_CATEGORY};

#for now, just find one. set up to accept params
$document = $collectionCategory->findOne(array('_id' => new MongoId('55281a158a1d5769fea76945')));
var_dump( $document );

?>
