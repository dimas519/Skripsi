<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-GLhlTQ8iRABdZLl6O3oVMWSktQOp6b7In1Zl3/Jr59b6EGGoI1aFkw7cmDA6j6gD" crossorigin="anonymous">
    <script defer src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>




    <link rel="icon" href="assets/img/logo.png" type="image/icon">
    <link rel="stylesheet" href="{{'css/layout.css'}}">



    <title>Sensor Vision</title>
    

</head>
<body>
 


            <div class="d-flex flex-row menuAtas">

                    @php
                    if($menu){
                        echo "<button type='button'  class='btn btn-link mx-2' >
                                <img src='assets/img/menu.png' height='30px' />
                            </button>";
                    }
                    @endphp
                
                <img  id="logo"src="assets/img/logo.png" width="80px" alt="logo app">
                <span id="title" class= "align-self-center" >Sensor Vision</span>



                {{-- <div style=" margin-top: 20px;">
                    <ul>
                        <li><a href="../index.html">Home</a></li>
                        <li><a href="mainWeather.php" class="active">Weather</a></li>
                        <li><a href="mainPrediction.php">Prediction</a></li>
                    </ul>
                </div> --}}
            </div>
