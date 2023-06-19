




<?php 
use Illuminate\Support\Facades\Input; ?>


@if (!session()->has('role'))
    <script>
        //  redirect tidak dilakukan langsung di dalam file Blade karena Blade hanya bertanggung jawab untuk merender tampilan
        window.location.href = "{{ url('/login') }}"; 
    </script>
@else
  @if (session('role')==0)
          <script>
            //  redirect tidak dilakukan langsung di dalam file Blade karena Blade hanya bertanggung jawab untuk merender tampilan
            window.location.href = "{{ url('/user') }}"; 
        </script>
  @endif
  
@endif




<link rel="stylesheet" href="{{'css/location.css'}}">
<link rel="stylesheet" href="{{'css/admin.css'}}">
<script src="{{asset('js/mainAdmin.js')}}" defer></script>

  <br>
<div class="container" id="workSheet">
  


  @if (app('request')->has('wrongIndentifier')==1)
  <br>
  <div class="alert alert-danger" role="alert">
    Node baru gagal disimpan, mohon coba lagi dengan identifier yang berbeda
  </div>
  @endif


  @if (app('request')->has('key'))
  <br>
  <div class="alert alert-info" role="alert">
    Node baru berhasil disimpan. Key: {{app('request')->get('key')}}
  </div>
  @endif


  {{-- bagian update Config --}}
  <a class="btn btn-primary" data-bs-toggle="collapse" href="#updateInterval" role="button" aria-expanded="false" aria-controls="collapseExample">
    Update Interval
  </a>  
  <a class="btn btn-primary" data-bs-toggle="collapse" href="#tambahKota" role="button" aria-expanded="false" aria-controls="collapseExample">
    Tambah Kota
  </a>  

  <a class="btn btn-primary" data-bs-toggle="collapse" href="#tambahBase" role="button" aria-expanded="false" aria-controls="collapseExample">
    Tambah Base Station
  </a>  
  <a class="btn btn-primary" data-bs-toggle="collapse" href="#tambahSensor" role="button" aria-expanded="false" aria-controls="collapseExample">
    Tambah Node Sensor
  </a>  
  
  @include('adminItem/updateInterval')


 @include('adminItem/insertKota')

@include("adminItem/newBase")

@include('adminItem/newSensor')





{{-- {{$request->input('wrongIndentifier')}} --}}

</div>