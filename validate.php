<?php
    $user = $_POST['uname'];
    $pass = $_POST['psw'];
    if($user == 'admin' && $pass == 'pass123')
    {
    header("Location:Scanpage.html");
    }
?>