<?php
require_once('/home/dholowiski/development/tech-product-scrapers/api/shared/mongoConfig.php');

?>
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <title>Search for Storage</title>

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
            <li class="active"><a href="/custom/storage/index.php">Filter Storage</a></li>
            <li ><a href="/custom/storage/ssd.php">SSD</a></li>
            <li><a href="#contact">Contact</a></li>
          </ul>
        </div><!--/.nav-collapse -->
      </div>
    </nav>

<div class="container">

  <div class="starter-template">
    <h1>Find Storage</h1>
    <p class="lead">Currently searching TigerDirect, hard drives</p>
  </div>

</div>

<div class="container-fluid">
  <div class="row" id="filterOptions">
    <!-- <div class="col-md-4">
      .col-md-4
    </div> -->
    <div class="col-md-12">
    <table class="table">
    <tr class="success">
    <td>itemNo</td>
    <td>Model</td>
    <td>Capacity</td>
    <td>finalPrice</td>
    <td>Price Per GB</td>
    </tr>
    
      <?php
      $productList = array();
      //grab the SSD Drives
      #var_dump(MONGO_SERVER_IP);
      #var_dump(MONGO_SERVER_PORT);
      #var_dump(MONGO_DATABASE);
      #var_dump(MONGO_TABLE_TD_PRODUCT);
      $conn = new MongoClient("mongodb://".MONGO_SERVER_IP.":".MONGO_SERVER_PORT);
      #var_dump($conn);
      $dbName = MONGO_DATABASE;
      #$db = $conn->$dbName;
      $db = $conn->techProducts_development;
      #var_dump($db);
      $collName = MONGO_TABLE_TD_MANUFACTURER;
      #$collection = $db->collName;
      $collection = $db->td_product;
      #var_dump($collection);
      #'specifications.driveMedium': 'ssd'
      $query = array("specifications.driveMedium" => "ssd");
      $cursor = $collection->find($query);
      #var_dump($cursor);
      foreach ($cursor as $document) {
        
        $capacityBytes = $document['specifications']['driveBytesCapacity'];
        $capacityGB = $capacityBytes / 1000000000;
        $itemNo = $document['itemNo'];
        $conn2 = new MongoClient("mongodb://".MONGO_SERVER_IP.":".MONGO_SERVER_PORT);
        $db2 = $conn2->techProducts_development;
        $collection2 = $db2->td_price;

        #db.getCollection('td_price').find().sort({"seenAt":-1}).limit(1)
        #$query2 = array('itemID' => $itemNo);
        $query2 = array('itemID' => $itemNo);

        $cursor2 = $collection2->find($query2)->sort(array('seenAt' => -1))->limit(1);
        
        #$itemNo = $document['itemNo'];
        $modelNo = $document['modelNo'];
        #$finalPrice = $document2['finalPrice'];
        $purchaseURL = $document2['purchaseURL'];
  
        #echo("itemNo: ".$document['itemNo']." Model: ".$document['modelNo']." - Capacity: ".$capacityGB." gb \n");        
        foreach ($cursor2 as $document2) {
          echo('$');
          $finalPrice = $document2['finalPrice'];
          $purchaseURL = $document2['purchaseURL'];
          #echo("FinalPrice: <a href=\"".$document2['purchaseURL']."\">".$document2['finalPrice']."</a>\n");
          #echo("<pre>\n");
          #var_dump($document2);
          #echo("</pre>\n");
        }
        $pricePerGB = $capacityGB / $finalPrice;
        $product = array();
        $product['itemNo'] = $itemNo;
        $product['modelNo'] = $modelNo;
        $product['capacityGB'] = $capacityGB;
        $product['finalPrice'] = $finalPrice;
        $product['purchaseURL'] = $purchaseURL;
        $product['pricePerGB'] = $capacityGB / $finalPrice;
        array_push($productList, $product);
	#var_dump($document);
      }
      $price = array();
      foreach ($productList as $key => $row)
      {
          $price[$key] = $row['pricePerGB'];
      }
      array_multisort($price, SORT_ASC, $productList);

      foreach ($productList as $product) {
        echo("<tr>\n");
        echo("<td>".$product['itemNo']."</td>\n");
        echo("<td>".$product['modelNo']."</td>\n");
        echo("<td>".$product['capacityGB']."</td>\n");
        echo("<td><a href=\"".$product['purchaseURL']."\">".$product['finalPrice']."</a></td>\n");
        echo("<td>".$product['pricePerGB']."</td>\n");
        echo("</tr>\n");        
      }
      ?>
    </table>
    </div>
    <!-- <div class="col-md-4">.col-md-4</div> -->
  </div>
</div>
    <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    <script src="/js/jquery.min.js"></script>
    <!-- Include all compiled plugins (below), or include individual files as needed -->
    <script src="/bootstrap/js/bootstrap.min.js"></script>
  </body>
</html>
