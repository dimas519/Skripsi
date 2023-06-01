<?php

namespace App\Http\Controllers;

use App\Models\API;
use Illuminate\Http\Request;
use Illuminate\Routing\Controller;



class GraphController extends Controller
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
        $graph=$request->post('graph');
        if($graph=='box'){
            $stat="raw";
        }else{
            $stat="avg";
        }
        
        $type=$request->post('type');


        

        $map = array();
        $map['idBS']=$idBS;

        $map['start']=$start;
        $map['end']=$end;
        $map['interval']=$interval;
        $map['stat']=$stat;
        $result=API::POST('data',$map)['result'];

        if (!$result){
            return "{\"value\":\"noData\"}";
        }
        

        $waktu=array();
        

        if(strcmp($type,'akselerasi')==0){
            
            $arrX=array();
            $arrY=array();
            $arrZ=array();
            foreach ($result as $row){
                array_push($waktu,$row['timeStamp']);
                array_push($arrX,$row[$type]['x']);
                array_push($arrY,$row[$type]['y']);
                array_push($arrZ,$row[$type]['z']);
            }
            $value=array("x"=>$arrX,"y"=>$arrY,"z"=>$arrZ);
        }else{
            $value=array();
            foreach ($result as $row){
                array_push($waktu,$row['timeStamp']);
                array_push($value,$row[$type]);
            }
        }




        

        $resultPlain=array("time"=>$waktu,"value"=>$value);

        $resultJson=json_encode($resultPlain);



        return $resultJson;
    }




    


}
