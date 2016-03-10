<?php

class productUtils {

	public function shortenProductName($productName, $length = 50) {
		if (strlen($productName) >= $length) {
			$return = substr($productName, 0, $length). "...";
		}
			else {
			$return = $productName;
		}
		return $return;
	}

}
