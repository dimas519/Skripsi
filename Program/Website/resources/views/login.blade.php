@include('layout',['menu'=> false ])
<link rel="stylesheet" href="{{'css/login.css'}}">


<div class="d-flex justify-content-end" style="margin: 30px 50px 0px 0px">



    <div class="card login" style="width: 18rem;">
        <div class="card-body">
            <div class="text-center">
                <img class="text-center" src="assets/img/logo.png" width="75px" alt="logo app">
            </div>
            <h3>LOGIN</h3>
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
                <div class="form-check mt-2">
                  <input type="checkbox" class="form-check-input" id="exampleCheck1" name="signIn">
                  <label class="form-check-label" for="exampleCheck1">Keep Sign in</label>
                </div>
                <div>
                  Dont have account? <a href="/signUP">Create one</a>
                </div>
                <button type="submit" class="btn btn-primary mt-3 ">Submit</button>
              </form>

        </div>
      </div>



</div>





@include("footer")