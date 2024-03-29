@include('header',['menu'=> false ])
<link rel="stylesheet" href="{{'css/login.css'}}">


<div class="d-flex justify-content-end" style="margin: 30px 50px 0px 0px">

  <img src="{{'assets/img/Cloud_blue_graf.png'}}" id="gambar" alt="">

    <div class="card login" style="width: 18rem;">
        <div class="card-body">
            <div class="text-center">
                <img class="text-center" src="assets/img/logo.png" width="75px" alt="logo app">
            </div>
            <h3>MASUK</h3>
            <form class="form-signin" action="/masuk" method="post">
              @csrf 
              {{-- frame work laravel yang membantu mengenerate token --}}
                <div class="form-group">
                  <label>Username</label>
                  <input type="text" class="form-control" id="email" aria-describedby="emailHelp" placeholder="Enter username" name="username">
                  
                </div>
                <div class="form-group mt-2">
                  <label >Password</label>
                  <input type="password" class="form-control" id="password" placeholder="Password" name="password">
                </div>
                <div>
                Tidak punya akun? <a href="/signUP">Buat akun</a>
                </div>
                @if (app('request')->has('wrong')==1)
                <br>
                <div class="alert alert-danger" role="alert">
                  Username dan password salah
                </div>
                @endif


                <button type="submit" class="btn btn-primary mt-3 ">Masuk</button>
              </form>

        </div>
      </div>
</div>
@include("footer")