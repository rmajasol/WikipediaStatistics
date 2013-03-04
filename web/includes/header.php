<!DOCTYPE html>
<html lang ="es">
<head>
    <?php
    require_once 'config.php';
    require_once 'functions.php';
    ?>

    <meta charset="utf-8">
    <title>
        Wikipedia Statistics
    </title>

    <!--
        CSS
    -->
    <link rel="stylesheet" href="css/normalize.css"/>
    <link rel="stylesheet" href="http://code.jquery.com/ui/1.10.1/themes/base/jquery-ui.css" />

    <link rel="stylesheet" href="css/styles.css"/>


    <!--
        JS
    -->
    <script src="js/prefixfree.min.js"></script>
    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.min.js"></script>
    <script src="http://code.jquery.com/ui/1.10.1/jquery-ui.js"></script>
    <script src="vendor/js/jquery.caret.js"></script>
    <script src="vendor/js/jquery.hotkeys.js"></script>
    <script src="vendor/js/shortcut.js"></script>
    <script src="https://www.google.com/jsapi"></script>

    <!-- Con el '?n=1' evitamos tener que limpiar la caché del navegador
    cada vez que hagamos cambios en este archivo -->
    <script src="js/codiguito.js?n=1"></script>

</head>
<body>