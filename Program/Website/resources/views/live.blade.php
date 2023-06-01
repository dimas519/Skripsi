
<script src="{{asset('js/live.js')}}" defer></script>
<script src="https://cdn.plot.ly/plotly-2.23.2.min.js" charset="utf-8"></script>
<link rel="stylesheet" href="{{'css/livePage.css'}}">

<br>

<div class="row">
    <div class="col-10">
        <Select class="form-select" id="kotaSelection">
            <option value="-1">Pilih Kota</option>
            @foreach ($semuaKota as $kota)
            <option value="{{$kota['id']}}">{{$kota['nama']}}</option>
            @endforeach
        </Select>


        @foreach ($semuaLokasi as $lokasi)
        <div class="card collapse my-1" id="{{$lokasi['identifier']}}" >
            <div class="card-body">
              <h5 class="card-title">{{$lokasi['nama']}}</h5>
              <span id="suhuText{{$lokasi['identifier']}}"class="card-text border"></span>
               <span id="kelembapanText{{$lokasi['identifier']}}" class="card-text border"></span>
                <span id="tekananText{{$lokasi['identifier']}}" class="card-text border"></span>
                 <span id="akselerasiText{{$lokasi['identifier']}}" class="card-text border"></span>
            </div>
          </div>
          
          @endforeach
    </div>

    <div class="col-2" id="lokSelect">
        <h5>Pilih Lokasi</h5>
        @foreach ($semuaLokasi as $lokasi)
        <a class="aClean" data-bs-toggle="collapse" href="#{{$lokasi['identifier']}}" aria-expanded="false" aria-controls="collapseExample"><input class="form-check-input" type="checkbox" name="{{$lokasi['identifier']}}" id="suhuCheck"></a>  



            <a class="aClean" data-bs-toggle="collapse" href="#{{$lokasi['identifier']}}" aria-expanded="false" aria-controls="collapseExample" onclick="initNewLive('{{$lokasi['identifier']}}',{{$lokasi['interval']}})">
                
                
                <label class="form-check-label" class="optLokasi" for="{{$lokasi['identifier']}}" city="{{$lokasi['idKota']}}">{{$lokasi['nama']}}
                </label>
            
            </a>
        <br>
        @endforeach
    </div>




</div>

{{-- 
<div class="row">
    <div class="col-12">
        @foreach ($semuaLokasi as $lokasi)
            <input class="form-check-input" type="checkbox" name="{{$lokasi['identifier']}}" id="suhuCheck" checked>
            <label class="form-check-label" class="optLokasi" for="{{$lokasi['identifier']}}" city="{{$lokasi['idKota']}}">{{$lokasi['nama']}}</label>

     
        @endforeach
    </div>
</div> --}}



