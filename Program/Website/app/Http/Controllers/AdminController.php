<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Routing\Controller;
use App\Models\API;

use App\Http\Controllers\GraphController;

class AdminController extends Controller
{
    public function ganti(Request $request){
        $bs=$request->post('bs');
        $value=$request->post('newInterval');
        $value*=1000;

        $map = array();
        $map['node']=$bs;
        $map['command']="setInterval:".$value;
        $map['token']=$request->session()->get('token)', '');

        $result=API::POST('update',$map);
        return redirect('/admin');
    }


    public function kota(Request $request){
        $nama=$request->post('nama');
        // $hour=$request->post('hour');
        // $minutes=$request->post('minutes');

        $map = array();
        $map['nama']=$nama;
        $map['token']=$request->session()->get('token)', '');

        $result=API::POST('kota',$map);
        return redirect('/admin');
    }

    public function addWSN(Request $request){

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

        
        $indoor=($request->post('indoor'))=="on";
        $map = array();
        $map['identifier']=$request->post('identifier');
        $map['idBS']=$request->post('bs'); //del
        $map['indoor']=$indoor; //del
        $map['nama']=$request->post('nama');
        $map['interval']=($request->post('interval')*1000);
        $map['token']=$request->session()->get('token)', '');
        $map['tipeSensor']=$sensor;

        $result=API::POST('node',$map)['result'];

        if(!$result){
            return redirect('/admin?wrongIndentifier=1');
        }else{
            $key=$result['key'];
            return redirect("/admin?key=$key");
        }        

      
    }

    public function addBase(Request $request){
        $map = array();
        $map['nama']=$request->post('nama');
        $map['latitude']=$request->post('latitude');
        $map['longtitude']=$request->post('longtitude');
        $map['idKota']=$request->post('kota');
        $map['token']=$request->session()->get('token)', '');

        $idLokasi=(API::POST('bs',$map)['result'])['id'];

        return redirect('/admin');
    }



    public function adminView(Request $request){
        $mainPage=new GraphController();
        return view('layout')
        ->with('semuaKota',$mainPage->getCity())
        ->with("semuaLokasi",$mainPage->getLocation())
        ->with("base",$mainPage->getBS())
        ->with('menu',true)
        ->with('location',false)
        ->with('admin',true)
        ->with('page','/admin');

    }
}
