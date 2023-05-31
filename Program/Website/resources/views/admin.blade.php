<link rel="stylesheet" href="{{'css/location.css'}}">
<link rel="stylesheet" href="{{'css/admin.css'}}">
<script src="{{asset('js/mainAdmin.js')}}" defer></script>


<div class="container" id="workSheet">
  
  {{-- bagian update Config --}}
  <a class="btn btn-primary" data-bs-toggle="collapse" href="#updateInterval" role="button" aria-expanded="false" aria-controls="collapseExample">
    Update Interval
  </a>  
  <a class="btn btn-primary" data-bs-toggle="collapse" href="#tambahKota" role="button" aria-expanded="false" aria-controls="collapseExample">
    Tambah Kota
  </a>  
  <a class="btn btn-primary" data-bs-toggle="collapse" href="#tambahSensor" role="button" aria-expanded="false" aria-controls="collapseExample">
    Tambah WSN
  </a>  
  
  @include('adminItem/updateInterval')


 @include('adminItem/insertKota')


@include('adminItem/newSensor')


</div>