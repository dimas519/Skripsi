<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Routing\Controller;
use App\Models\API;



class UserController extends Controller
{

    public function login(Request $request){
        $token=$request->post('_token');
        $email=$request->post('username');
        $password=$request->post('password');
        $keepSignIN=$request->post('signIn');

        $map = array();
        $map['username']=$email;
        $map['password']=$password;
        $map['token']=$token;
        $result=API::POST('login',$map);
        if($result['result']==0){
            return redirect('/main');
        }else{
            return redirect('/?wrong=1');
        }

    }

    public function signUp(Request $request){
        $token=$request->post('_token');
        $username=$request->post('username');
        $email=$request->post('email');
        $password=$request->post('password');

        $map = array();
        $map['username']=$username;
        $map['password']=$password;
        $map['email']=$email;

        $result=API::POST('signup',$map);
        if($result['result']){
            return redirect('/');
        }else{
            return redirect('/signUP?wrong=1');
        }

    }


}
