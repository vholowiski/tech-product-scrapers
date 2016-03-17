var defaultDB = "techProducts_development2"; //default database
var silent = false; //should we print additional info, or just csv?

//see if we want to be silent
if (typeof setSilent !== 'undefined') {
  silent = true;
  //let's remember not to print anything except for the CSV data
} else {
	//silent not turned on so let's give some directions
	print("---------------");
	print("To pass start & end dates from the command line, add the following:");
 	print("--eval \"var variable='value', variable2='value2'\"");
 	print("Available options:");
 	print("setSilent='true'  | Silent. if setPrintCSV=true, csv prints anyway.	Default: false");
 	print("setDatabase='dbName' | Set the mongo database.		Default: bllt");
 	print("setDBHost='ip:port' 	| Set the mongo server/port.	Default: localhost:27017");
 	print("---------------");
}

var mongoHost = 'localhost:27017';
if (typeof setDBHost !== 'undefined') {
	//database name. Defaults to bllt
	mongoHost = setDBHost;
}

//set any command line options we've gotten
if (typeof setDatabase !== 'undefined') {
	//database name. Defaults to bllt
	defaultDB = database;
}

db = connect(mongoHost+"/"+defaultDB);

//loop through the products
db.td_product.find().forEach(
		function(product){
			//for each product, find it's price
			if (product['itemNo']) {
				var itemNo = product['itemNo'];
				var productPriceCursor = db.td_price.find({'itemID': itemNo}).sort({'crawlTimestamp':-1}).limit(1);
				if (productPriceCursor.hasNext()) {
					productPriceOBJ = productPriceCursor.next(); //there can be only one
					if (productPriceOBJ['finalPrice']) {
						//productPrice = productPriceOBJ['finalPrice'];
						product['td_price'] = productPriceOBJ;
						db.td_product.update(product);
						//print(productPrice);
					} else {
						print("**************");
						print("Final Price not found for for:");
						print(product['_id']);							
					}
				} else {
					print("**************");
					print("Price not found for for:");
					print(product['_id']);					
				}
				//print(productPrice);
			} else {
				print("**************");
				print("No itemNo for:");
				print(product['_id']);
			}
		}
	);