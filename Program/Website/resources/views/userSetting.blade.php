
<link rel="stylesheet" href="{{'css/login.css'}}">


<div class="d-flex justify-content-start" style="margin: 30px 0px 00px 10px;">



    <div class="card" style="width: 80vw;">
        <div class="card-body">
            <div class="text-center">
                <img class="text-center" src="assets/img/logo.png" width="100px" alt="logo app">
            </div>
            <form class="form-signin" action="/ganti" method="post">
                <div class="form-group">
                  <label>Username</label>
                  <input type="text" class="form-control" id="email" aria-describedby="emailHelp" value="{{session('username')}}" name="username" disabled>
                  
                  <label>Role</label>
                  <input type="text" class="form-control" id="email" aria-describedby="emailHelp" value="{{session('role')==0?"User":"Admin"}}" name="username" disabled>
              </form>

        </div>
      </div>



</div>





@include("footer")