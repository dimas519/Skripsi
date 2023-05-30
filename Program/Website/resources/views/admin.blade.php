<link rel="stylesheet" href="{{'css/location.css'}}">
<script src="{{asset('js/mainAdmin.js')}}" defer></script>


<div class="container" id="workSheet">
  
  {{-- bagian update Config --}}
  <a class="btn btn-primary" data-toggle="collapse" data-target="#multiCollapseExample1" role="button" aria-expanded="false" aria-controls="multiCollapseExample1">Toggle first element</a>
  
  @include('adminItem/updateInterval')
 
<div style="height:5px; background-color:red;"></div>

 @include('adminItem/insertKota')


<div style="height:5px; background-color:red;"></div>

@include('adminItem/newSensor')


  <div style="height:5px; background-color:red;"></div>

</div>