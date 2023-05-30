<div>
    <form action="ganti" method="post">
      <div class="row">
        <div class="col-6">
          <Select class="form-select" id="kotaSelection">
            <option value="-1">Pilih Kota</option>
            @foreach ($semuaKota as $kota)
            <option value="{{$kota['id']}}">{{$kota['nama']}}</option>
            @endforeach
          </Select>
        </div>

        <div class="col-6">
          <Select class="form-select" id="lokasiSelection" name="bs"  >
            <option value="-1">Pilih Lokasi</option>
            @foreach ($semuaLokasi as $lokasi)
            <option hidden class="optLokasi" value="{{$lokasi['identifier']}}" city="{{$lokasi['idKota']}}">{{$lokasi['nama']}}</option>
            @endforeach
          </Select>
        </div>
      </div>

      <div class="row">
        <div class="col-2">
          <div class="pt-3">Update Interval </div>
        </div>

        <div class="col-4">
          <input type="number" placeholder="second" class="form-control mt-2" id="intervalInput" name="newInterval" min=1>
        </div>

          <div class="col-2">
            <button type="submit" class="btn btn-primary mt-2">Update Interval</button>
          </div>
      </div>


    </form>
    </div>