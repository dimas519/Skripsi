
<script src="https://cdn.plot.ly/plotly-2.23.2.min.js" charset="utf-8"></script>
<script src="{{asset('js/live.js')}}" defer></script>

<link rel="stylesheet" href="{{'css/livePage.css'}}">

<script>
const urlAPI='{{$api}}'


</script>


<br>

<div class="row">
    <div class="col-10">
        <Select class="form-select" id="kotaSelection">
            <option value="-1">Filter by Kota</option>
            @foreach ($semuaKota as $kota)
            <option value="{{$kota['id']}}">{{$kota['nama']}}</option>
            @endforeach
        </Select>


        @foreach ($semuaLokasi as $lokasi)
        <div class="card collapse my-1" id="{{$lokasi['identifier']}}" >
            <div class="card-body">
                <h5 class="card-title">{{$lokasi['nama']}}</h5>
                <h6 id="timeText{{$lokasi['identifier']}}" class="card-text"></h6>
                <div>
                    <div id="kelembapanText{{$lokasi['identifier']}}" class="" style="display:inline-block"></div>
                        <div class="card-text border liveData align-text-bottom">
                            <p class="liveDataTitle text-center">Suhu </p>
                            <div class="text-center text-center">
                                <p id="suhuText{{$lokasi['identifier']}}" class="liveDataText"></p>
                                <p class="liveDataText" hidden>°C</p>
                            </div>
                        </div> 
                    <div class="card-text border liveData align-text-bottom" >
                        <p class="liveDataTitle text-center">Tekanan </p>
                        <div class="text-center">
                            <p id="tekananText{{$lokasi['identifier']}}" class="liveDataText"></p>
                            <p class="liveDataText" hidden>kPa</p>
                        </div>
                    </div>
                    <div class="card-text border liveData align-text-bottom">
                        <p class="liveDataTitle text-center">Akselerasi (x,y,z)</p>
                        <div class="text-center">
                            <p id="akselerasiText{{$lokasi['identifier']}}" class="liveDataText"></p>
                            <p class="liveDataText" hidden>g</p>
                        </div>
                    </div>
                </div>
            </div>
          </div>
          
          @endforeach
    </div>

    <div class="col-2" id="lokSelect">
        <h5>Pilih Lokasi</h5>
        @foreach ($semuaLokasi as $lokasi)
        <div class="optLokasi" city="{{$lokasi['idKota']}}" >
            {{-- <input  data-bs-toggle="collapse"  href="#{{$lokasi['identifier']}}"  aria-expanded="false" aria-controls="collapseExample" class="form-check-input" type="checkbox" name="{{$lokasi['identifier']}}" id="suhuCheck"  onclick="initNewLive('{{$lokasi['identifier']}}',{{$lokasi['interval']}})" >
 
            <label data-bs-toggle="collapse"  href="#{{$lokasi['identifier']}}"  aria-expanded="false" aria-controls="collapseExample" class="form-check-label" for="{{$lokasi['identifier']}}" onclick="initNewLive('{{$lokasi['identifier']}}',{{$lokasi['interval']}})" >{{$lokasi['nama']}}</label> --}}



            <input data-bs-toggle="collapse" href="#{{$lokasi['identifier']}}" aria-expanded="false" 
            aria-controls="collapseExample" onclick="initNewLive('{{$lokasi['identifier']}}',{{$lokasi['interval']}})"
            
            type="checkbox" id="select{{$lokasi['identifier']}}" >
            <label 
            data-bs-toggle="collapse" href="#{{$lokasi['identifier']}}" aria-expanded="false" 
            aria-controls="collapseExample" class="form-check-label" for="select{{$lokasi['identifier']}}">{{$lokasi['nama']}}</label>

            <br><br>
        </div>
        
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



