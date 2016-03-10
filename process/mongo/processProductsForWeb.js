//connect to the database
var defaultDB = "techProducts_development";

if (typeof database !== 'undefined') {
	defaultDB = database;
}
db = connect("127.0.0.1:27017/"+defaultDB);

//loop through products, add most recent price

db.td_product.find().forEach(function(data) {
	//for each data, get the most recent price
	price = 
}