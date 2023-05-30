<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Routing\Controller;
use App\Models\API;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Session;




class UserController extends Controller
{

    public function login(Request $request){
        $token=$request->post('_token');
        $username=$request->post('username');
        $password=$request->post('password');
        $keepSignIN=$request->post('signIn');

        $map = array();
        $map['username']=$username;
        $map['password']=$password;
        $map['token']=$token;
        $result=API::POST('login',$map);

        

        if($result['result']==0){
            Session::put('username',  $username);
            Session::put('token',  $token);
            Session::put('role',  0);
            return redirect('/main');
        }
        elseif($result['result']==1) {
            Session::put('username',  $username);
            Session::put('token',  $token);
            Session::put('role',  1);
            return redirect('/admin');
        }
        else{
            return redirect('/?wrong=1');
        }

    }

    public function logout(){
        Session::flush();
        Auth::logout();
        return redirect('login');
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
            return redirect('/main');
        }
        else{
            return redirect('/signUP?wrong=1');
        }

    }

   


}