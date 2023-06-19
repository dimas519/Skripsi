<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\UserController;
use App\Http\Controllers\AdminController;
use App\Http\Controllers\GraphController;

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
    
    return redirect("login");
});

Route::get('/login', function () {
    return view('login');
});

Route::get('/signUP', function () {
    return view('signup');
});


Route::get('/main',[ UserController::class , 'viewUser']);

Route::get('/realTime',[ UserController::class , 'realTimeCont']);

Route::get('user',[UserController::class,'viewUserProfile']);

Route::get('/admin', [AdminController::class, "adminView"]);
    

Route::get('/table',[ UserController::class , 'viewTable']);

Route::get('/statistic',[ UserController::class , 'viewStatistik']);
/*
|--------------------------------------------------------------------------
| POST ROUTE
|--------------------------------------------------------------------------
|
*/

Route::post('/masuk', [UserController::class, 'login']);

Route::get('/keluar', [UserController::class, 'logout']);

Route::post('/daftar', [UserController::class, 'signup']);

Route::post('/data', [GraphController::class, 'data']);

Route::post('/ganti', [AdminController::class, 'ganti']);

Route::post('/kota', [AdminController::class, 'kota']);

Route::post('/sensorBaru', [AdminController::class, 'addWSN']);

Route::post('/baseBaru', [AdminController::class, 'addBase']);