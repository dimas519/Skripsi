
@php
    use Illuminate\Support\Facades\Session;
@endphp



@include('header',['menu'=> $menu ])
@include("navigation")


@if (Route::is('/login')  ||  Route::is('/signup') )
    
@else  
    @if (!session()->has('token'))
    <script>
        //  redirect tidak dilakukan langsung di dalam file Blade karena Blade hanya bertanggung jawab untuk merender tampilan
        window.location.href = "{{ url('/login') }}"; 
    </script>
    @endif


    <div class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
        @include($page)
        {{-- @include('live')
    --}}
    </div>
    @include("footer")



@endif



