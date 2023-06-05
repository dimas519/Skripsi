
@php
    use Illuminate\Support\Facades\Session;
@endphp



@include('header',['menu'=> $menu ])
@include("navigation")


{{-- @if (!Route::is('/login') )
    @if (session()->has('token'))
    window.location.href ="{{url('login')}}"
    @endif
@else   --}}



    <div class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
        @include($page)
        {{-- @include('live') --}}
   
    </div>
    @include("footer")



{{-- @endif --}}



