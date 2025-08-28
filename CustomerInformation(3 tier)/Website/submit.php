<?php
// Get form input
$name  = $_POST['name'];
$email = $_POST['email'];
$phone = $_POST['phone'];

// Connect to MySQL (RDS endpoint, username, password, database)
$mysqli = new mysqli(
    'capstoneprod.cxy6m4cca3fo.us-east-2.rds.amazonaws.com', // RDS endpoint
    'webappuser',   // DB username
    'john1234',  // DB password
    'mywebapp'      // Database name
);

// Check connection
if ($mysqli->connect_errno) {
    die('Failed to connect to MySQL: ' . $mysqli->connect_error);
}

// Insert query
$query = "INSERT INTO customers (name, email, phone) VALUES ('$name', '$email', '$phone')";

// Execute query
if (!$result = $mysqli->query($query)) {
    die('Error executing query: ' . $mysqli->error);
}

// Close connection
$mysqli->close();

echo 'Customer information saved successfully!';
?>
