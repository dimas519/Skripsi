@include('layout',['menu'=> true ])
@include("navigation")


@if (!Session::has('key'))

<main class="col-md-9 ms-sm-auto col-lg-10 px-md-4">

    @include('graphSelection')

    @include('graph')




</main>
@endif







@include("footer")
