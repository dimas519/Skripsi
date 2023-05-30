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

        $result=API::POST('update',$map);
        return redirect('/admin');
    }


    public function kota(Request $request){
        dd($request['indoor']);
        // $bs=$request->post('bs');
        // $value=$request->post('newInterval');
        // $value*=1000;

        // $map = array();
        // $map['idBS']=$bs;
        // $map['command']="setInterval:".$value;

        // $result=API::POST('update',$map);
        // return redirect('/admin');
    }
}
