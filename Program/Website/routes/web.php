<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\UserController;
use App\Http\Controllers\AdminController;
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

Route::get('/login', function () {
    return view('login');
});

Route::get('/signUP', function () {
    return view('signup');
});


Route::get('/main', function () {
    $mainPage=new MainPages();
    return view('layout')
    ->with('semuaKota',$mainPage->getCity())
    ->with("semuaLokasi",$mainPage->getLocation())
    ->with('menu',true)
    ->with('location',true)
    ->with('page','graphSelection');
});

Route::get('/user', function () {
    return view('layout')
    ->with('menu',true)
    ->with('location',false)
    ->with('page','userSetting');
});

Route::get('/admin', function () {
    $mainPage=new MainPages();
    return view('layout')
    ->with('semuaKota',$mainPage->getCity())
    ->with("semuaLokasi",$mainPage->getLocation())
    ->with('menu',true)
    ->with('location',false)
    ->with('page','/admin');
});



/*
|--------------------------------------------------------------------------
| POST ROUTE
|--------------------------------------------------------------------------
|
*/

Route::post('/masuk', [UserController::class, 'login']);

Route::get('/keluar', [UserController::class, 'logout']);

Route::post('/daftar', [UserController::class, 'signup']);

Route::post('/data', [MainPages::class, 'data']);

Route::post('/ganti', [AdminController::class, 'ganti']);

Route::post('/kota', [AdminController::class, 'kota']);

Route::post('/sensorBaru', [AdminController::class, 'addWSN']);