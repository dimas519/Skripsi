<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

class API extends Model
{
    use HasFactory;
    protected static $apiAddreses="http://127.0.0.1:5000";

    public static function GET($endpoint, $parameter){
        $url=API::$apiAddreses;
        $request = Http::get("$url/$endpoint?$parameter");
        $response=$request->json();

        return $response;
    }

    public static function getURL(){
        return API::$apiAddreses;
    }

    public static function POST($endpoint, $parameter){
        $url=API::$apiAddreses;
        $request = Http::post("$url/$endpoint",$parameter);
        $response=$request->json();
        return $response;
    }





    


}


?>
