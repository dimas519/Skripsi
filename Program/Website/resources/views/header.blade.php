<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sensor Vision</title>

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-GLhlTQ8iRABdZLl6O3oVMWSktQOp6b7In1Zl3/Jr59b6EGGoI1aFkw7cmDA6j6gD" crossorigin="anonymous">
    <script defer src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>

    <link rel="icon" href="assets/img/logo.png" type="image/icon">
    <link rel="stylesheet" href="{{'css/layout.css'}}">


</head>
<body style="height: 100%">
            <div class="d-flex flex-row menuAtas">
                    @php
                    if($menu){
                        echo "<button type='button'  class='btn btn-link mx-2' data-bs-toggle='collapse' href='#navigation' aria-expanded='false' aria-controls='collapseExample' >
                                <img src='assets/img/menu.png' height='25vh;' />
                            </button>";
                    }
                    @endphp
                
                <img  id="logo"src="assets/img/logo.png" alt="logo app">
                <span id="title" class= "align-self-center" >Sensor Vision</span>
            </div>


   