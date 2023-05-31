<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Routing\Controller;
use App\Models\API;

class AdminController extends Controller
{
    public function ganti(Request $request){
        $bs=$request->post('bs');
        $value=$request->post('newInterval');
        $value*=1000;

        $map = array();
        $map['idBS']=$bs;
        $map['command']="setInterval:".$value;
        $map['token']=$request->session()->get('token)', '');

        $result=API::POST('update',$map);
        return redirect('/admin');
    }


    public function kota(Request $request){
        $nama=$request->post('nama');
        $hour=$request->post('hour');
        $minutes=$request->post('minutes');

        $map = array();
        $map['nama']=$nama;
        $map['token']=$request->session()->get('token)', '');

        $result=API::POST('kota',$map);
        return redirect('/admin');
    }

    public function addWSN(Request $request){
        $nama=$request->post('nama');
        $latitude=$request->post('latitude');
        $longtitude=$request->post('longtitude');
        $indoor=($request->post('indoor'))=="on";
        $kota=$request->post('kota');

        $map = array();
        $map['nama']=$nama;
        $map['latitude']=$latitude; //del
        $map['longtitude']=$longtitude;
        $map['indoor']=$indoor;
        $map['idKota']=$kota;
        $map['token']=$request->session()->get('token)', '');

        
        $idLokasi=(API::POST('lokasi',$map)['result'])['id'];


        $map = array();
        $map['idBS']=$request->post('idBS');
        $map['idLokasi']=$idLokasi; //del
        $map['interval']=($request->post('interval')*1000);
        $map['token']=$request->session()->get('token)', '');

        API::POST('bs',$map);

        $sensor=array();

        if($request->post('suhu')=="on"){
            array_push($sensor,'Suhu');
        }

        if($request->post('tekanan')=="on"){
            array_push($sensor,'Kelembapan');
        }

        if($request->post('kelembapan')=="on"){
            array_push($sensor,'Tekanan');
        }

        if($request->post('akselerasi')=="on"){
            array_push($sensor,'Akselerasi');
        }

        $map = array();
        $map['idBS']=$request->post('idBS');
        $map['tipeSensor']=$sensor;
        $map['token']=$request->session()->get('token)', '');
        API::POST('node',$map);


        return redirect('/admin');
    }
}
