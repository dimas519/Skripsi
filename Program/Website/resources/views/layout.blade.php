


@if (Session::has('token'))
@include('header',['menu'=> $menu ])
@include("navigation",['location'=>$location])
    <div class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
        @include($page)
    </div>
@include("footer")
@else
    @if (!Route::is('/login') || !Route::is('/'))
    <script>
       window.location.href ="{{url('login')}}"
    </script>
    @endif

@endif



