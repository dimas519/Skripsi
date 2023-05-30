
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
                  <input type="text" class="form-control" id="email" aria-describedby="emailHelp" value="{{Session::get('username')}}" name="username" disabled>
                  
                </div>
                <div class="form-group mt-2">
                  <label >Old Password</label>
                  <input type="password" class="form-control" id="old_password" placeholder="Old Password" name="old_password">
                </div>

                <div class="form-group mt-2">
                    <label >New Password</label>
                    <input type="password" class="form-control" id="new_password" placeholder="New Password" name="new_password">
                  </div>
                <button type="submit" class="btn btn-primary mt-3 ">Change Password</button>
              </form>

        </div>
      </div>



</div>





@include("footer")