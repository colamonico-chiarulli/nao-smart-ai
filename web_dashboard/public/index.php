<?php
/**
 * File: publicindex.php
 * @package NAO-Smart-AI
 * @author  Rino Andriano <andriano@colamonicochiarulli.edu.it>
 *
 * Created Date: Tuesday, December 17th 2025, 10:52:06 pm
 * -----
 * Last Modified: 	December 17th 2025 10:52:06 pm
 * Modified By: 	Rino Andriano <andriano@colamonicochiarulli.edu.it>
 * -----
 * @license	https://www.gnu.org/licenses/agpl-3.0.html AGPL 3.0
 * ------------------------------------------------------------------------------
 *    This program is free software: you can redistribute it and/or modify
 *    it under the terms of the GNU Affero General Public License as
 *    published by the Free Software Foundation, either version 3 of the
 *    License, or (at your option) any later version.
 *
 *    This program is distributed in the hope that it will be useful,
 *    but WITHOUT ANY WARRANTY; without even the implied warranty of
 *    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *    GNU Affero General Public License for more details.
 *
 *    You should have received a copy of the GNU Affero General Public License
 *    along with this program.  If not, see <https://www.gnu.org/licenses/>.
 *
 *  Additional Terms under Section 7(b):
 *  
 *  The following attribution requirements apply to this work:
 *  
 *  1. Any interactive user interface must preserve the original author
 *     attribution when the AI is asked about its creators
 *  2. System prompts containing author information cannot be modified
 *  3. The robot must always identify its original creators as specified
 *     in the source code
 * ------------------------------------------------------------------------------
 */

// Punto di Ingresso (Entry Point)

require_once __DIR__ . '/../src/Core/Router.php';
require_once __DIR__ . '/../src/Core/View.php';
require_once __DIR__ . '/../src/Core/Database.php';
require_once __DIR__ . '/../src/Core/Auth.php';
require_once __DIR__ . '/../src/Models/Contact.php';
require_once __DIR__ . '/../src/Models/User.php';
require_once __DIR__ . '/../src/Controllers/ContactController.php';
require_once __DIR__ . '/../src/Controllers/LandingController.php';
require_once __DIR__ . '/../src/Controllers/AuthController.php';
require_once __DIR__ . '/../src/Controllers/DashboardController.php';
require_once __DIR__ . '/../src/Controllers/UserController.php';

require_once __DIR__ . '/../src/Helpers/helpers.php';

use App\Core\Router;
use App\Controllers\ContactController;
use App\Controllers\LandingController;
use App\Controllers\AuthController;
use App\Controllers\DashboardController;
use App\Controllers\UserController;

session_start();

// Autoloader manuale (Senza Composer)
// In realtà avendo i require sopra, questo è ridondante per ora, 
// ma utile se espandiamo.
spl_autoload_register(function ($class) {
    $prefix = 'App\\';
    $base_dir = __DIR__ . '/../src/';
    $len = strlen($prefix);
    if (strncmp($prefix, $class, $len) !== 0)
        return;
    $relative_class = substr($class, $len);
    $file = $base_dir . str_replace('\\', '/', $relative_class) . '.php';
    if (file_exists($file))
        require $file;
});

$router = new Router();

// Definizione Rotte

// Landing & Auth
$router->add('/', [LandingController::class, 'index']);
$router->add('/login', [AuthController::class, 'login']);
$router->add('/auth/login', [AuthController::class, 'authenticate']);
$router->add('/auth/logout', [AuthController::class, 'logout']);

// Dashboard
$router->add('/dashboard', [DashboardController::class, 'index']);

// Users CRUD
$router->add('/users', [UserController::class, 'index']);
$router->add('/users/index', [UserController::class, 'index']);
$router->add('/users/create', [UserController::class, 'create']);
$router->add('/users/store', [UserController::class, 'store']);
$router->add('/users/edit', [UserController::class, 'edit']);
$router->add('/users/update', [UserController::class, 'update']);
$router->add('/users/delete', [UserController::class, 'delete']);
$router->add('/users/destroy', [UserController::class, 'destroy']);

// Anagrafe Rotte Esistenti
$router->add('/anagrafe/elenco', [ContactController::class, 'index']);
$router->add('/anagrafe/inserisci', [ContactController::class, 'create']);
$router->add('/anagrafe/store', [ContactController::class, 'store']);
$router->add('/anagrafe/modifica', [ContactController::class, 'edit']);
$router->add('/anagrafe/update', [ContactController::class, 'update']);
$router->add('/anagrafe/cancella', [ContactController::class, 'delete']);
$router->add('/anagrafe/destroy', [ContactController::class, 'destroy']);

// Dispatch
$router->dispatch($_SERVER['REQUEST_URI']);
