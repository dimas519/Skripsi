<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\UserController;

use App\Http\Controllers\MainPages;
/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| contains the "web" middleware group. Now create something great!
|
*/

Route::get('/', function () {
    
    return view('login');
});

Route::get('/signUP', function () {
    return view('signup');
});


Route::get('/main', function () {
    $mainPage=new MainPages();
    return view('usermain')
    ->with('semuaKota',$mainPage->getCity())
    ->with("semuaLokasi",$mainPage->getLocation());
});

Route::get('/location', function () {
    return view('location');
});


/*
|--------------------------------------------------------------------------
| POST ROUTE
|--------------------------------------------------------------------------
|
*/

Route::post('/masuk', [UserController::class, 'login']);

Route::post('/daftar', [UserController::class, 'signup']);

Route::post('/data', [MainPages::class, 'data']);
