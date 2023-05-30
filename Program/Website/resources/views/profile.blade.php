


@include('layout',['menu'=> false ])
@include("navigation",['location'=>false])



@if (!Session::has('key'))

<div class="col-md-9 ms-sm-auto col-lg-10 px-md-4">

    <div class="container" >
        <form action="#">
            <label for="username">Username</label>
            <input type="text" name="username" value="dimasTest" value="{{Session::get('username')}}"  readonly>
        
            <label for="email">Email</label>
            <input type="text" name="email" value="dimasTest"  readonly>
        
            <label for="email">Old password</label>
            <input type="password" name="oldPass" value="dimasTest@email"  >
        
            <label for="email">New password</label>
            <input type="password" name="newPass" value="dimasTest@email"  >
        
            <button type="submit">Change Password</button>
        </form>
        
    </div>

</div>
@endif
@include("footer")



