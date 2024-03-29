<?php
require_once("../../api/shared/mongoConfig.php");
require_once(__DIR__."/../../api/tigerdirect/classes/database/mongoCategories.php");
require_once(__DIR__."/../../api/tigerdirect/classes/database/mongoProducts.php");
require_once(__DIR__."/../../api/shared/products/productUtils.class.php");
?>
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <title>Showing Products in Category</title>

    <!-- Bootstrap -->
    <link href="/bootstrap/css/bootstrap.min.css" rel="stylesheet">

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
  <style>
  body {
  padding-top: 50px;
}
.starter-template {
  padding: 40px 15px;
  text-align: center;
}
</style>
  </head>
  <body>
    <nav class="navbar navbar-inverse navbar-fixed-top">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="#">Project name</a>
        </div>
        <div id="navbar" class="collapse navbar-collapse">
          <ul class="nav navbar-nav">
            <li><a href="/">Home</a></li>
            <li><a href="/custom/storage/index.php">Filter Storage</a></li>
            <li class="active"><a href="/categories/index.php">Categories</a></li>
          </ul>
        </div><!--/.nav-collapse -->
      </div>
    </nav>

<div class="container">

      <div class="starter-template">
        <h1>Bootstrap starter template</h1>
<?php 
        //get the categories
        $productsOBJ = new mongoProducts(MONGO_SERVER_IP, MONGO_SERVER_PORT, MONGO_DATABASE);
        if ( (isset($_REQUEST)) && (isset($_REQUEST['tdCatID'])) ) {
          $catID = (int) $_REQUEST['tdCatID'];
          //var_dump($catID);
          $productCursor = $productsOBJ->getProductsByCategoryID($catID);
          #var_dump($productCursor->count());
          #var_dump($parentCat);
        } 

        if ($productCursor) {
?>
        <table class="table table-striped">
          <thead>
            <tr>
<?php
  if ( (isset($parentCat)) && ($parentCat) ) {
echo("              <th>".$parentCat['categoryName']."</th>\n");
  } else {
echo("              <th></th>\n");    
  }
?>
            <th>Price</th>
            </tr>
            
          </thead>
          <tbody>
<?php
        //create a productUtils objetct
        $putil = new productUtils();

          foreach ($productCursor as $doc) {
            //var_dump($doc);
	$row = "";
	$row = $row."<tr>\n";
	$row = $row."  <th id = \"".$doc['_id']."\" tdItemNo=\"".$doc['tdItemNo']."\">";
	$row = $row."<a href=\"/products/show.php?productMongoID=".$doc['_id']."\">";
  $row = $row.$putil->shortenProductName($doc['productName']);
  $row = $row."</a>";
	$row = $row."</th>";
  $row = $row."<th>priceHere</th>\n";
	$row = $row."</tr>\n";
	echo("$row");
	
          }  
?>
          </tbody>
        </table>
<?php   }?>
      </div>
    </div>
    <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    <script src="/js/jquery.min.js"></script>
    <!-- Include all compiled plugins (below), or include individual files as needed -->
    <script src="/bootstrap/js/bootstrap.min.js"></script>
  </body>
</html>
