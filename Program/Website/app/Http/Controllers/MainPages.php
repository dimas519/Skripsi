<?php

namespace App\Http\Controllers;

use App\Models\API;
use Illuminate\Http\Request;
use Illuminate\Routing\Controller;



class MainPages extends Controller
{
    //
    private $city;
    private $location;

    public function __construct()
    {
        $data=$this->getData()['result'];
        $this->setCity($data);
        $this->setLocation($data);
    }

    private function getData(){
        return API::get('lokasi','');
    }

    private function setCity($data){
        $this->city=$data['kota'];
    }

    private function setLocation($data){
        $this->location=$data['lokasi'];
    }

    public function getCity(){
        return $this->city;
    }

    public function getLocation(){
        return $this->location;
    }

    public function data(Request $request){
        $idBS=$request->post('idBS');
        $start=$request->post('start');
        $end=$request->post('end');
        $interval=$request->post('interval');
        $cleaning=false;
        $type=$request->post('type');

        $map = array();
        $map['idBS']=$idBS;

        $map['start']=$start;
        $map['end']=$end;
        $map['interval']=$interval;
        $map['cleaning']=$cleaning;
        $result=API::POST('data',$map)['result'];

        $waktu=array();
        $value=array();
        foreach ($result as $row){
            array_push($waktu,$row['timeStamp']);
            array_push($value,$row[$type]);
        }

        $resultPlain=array("time"=>$waktu,"value"=>$value);

        $resultJson=json_encode($resultPlain);



        return $resultJson;
    }




    


}
