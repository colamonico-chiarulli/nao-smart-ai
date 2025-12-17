<?php
/**
 * File: src/Core/Router.php
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


namespace App\Core;

/**
 * Gestisce il routing delle richieste HTTP verso i Controller corretti.
 */
class Router
{
    private $routes = [];
    private static $instance = null;
    private $baseDir = null;

    /**
     * Costruttore - calcola il base directory una volta sola
     */
    public function __construct()
    {
        $this->baseDir = dirname($_SERVER['SCRIPT_NAME']);
        if ($this->baseDir === '/' || $this->baseDir === '\\') {
            $this->baseDir = '';
        }
        self::$instance = $this;
    }

    /**
     * Aggiunge una rotta alla mappa.
     * 
     * @param string $route Nome della rotta (es. 'home').
     * @param callable|array $action Callback o array [Classe, Metodo] da eseguire.
     */
    public function add($route, $action)
    {
        $this->routes[$route] = $action;
    }

    /**
     * Esegue l'azione associata all'URL o parametro richiesto.
     * 
     * @param string $url L'URL della richiesta (attualmente usa $_GET['option']).
     * @return mixed Risultato dell'azione del controller.
     */
    /**
     * Esegue l'azione associata all'URL richiesto.
     * 
     * @param string $url L'URL completo della richiesta.
     * @return mixed Risultato dell'azione del controller.
     */
    public function dispatch($url)
    {
        // 1. Rimuovi la query string (es. ?id=1)
        $url = parse_url($url, PHP_URL_PATH);

        // 2. Gestisci il "Base Directory" se l'app è in una sottocartella
        // script_name è es. /CorsoPHP/.../public/index.php
        // dirname è es. /CorsoPHP/.../public
        $baseDir = dirname($_SERVER['SCRIPT_NAME']);

        // Se siamo in root /, baseDir è / o vuoto. Uniformiamo.
        if ($baseDir !== '/' && strpos($url, $baseDir) === 0) {
            $url = substr($url, strlen($baseDir));
        }

        // 3. Normalizza il path (es. /elenco/ -> /elenco)
        $url = rtrim($url, '/');
        if ($url === '') {
            $url = '/';
        }

        if (array_key_exists($url, $this->routes)) {
            $callback = $this->routes[$url];

            if (is_array($callback)) {
                $controller = new $callback[0]();
                $method = $callback[1];
                return $controller->$method();
            }
        }

        // Fallback o 404
        if (array_key_exists('404', $this->routes)) {
            $callback = $this->routes['404'];
            if (is_array($callback)) {
                $controller = new $callback[0]();
                $method = $callback[1];
                return $controller->$method();
            }
        }

        // Pagina 404 styled
        http_response_code(404);
        View::render('errors/404', [
            'title' => '404 - Pagina Non Trovata'
        ], 'layout_public');
    }

    /**
     * Genera un URL completo per una rotta.
     * 
     * @param string $route La rotta (es. '/anagrafe/elenco')
     * @return string URL completo
     */
    public static function url($route)
    {
        if (self::$instance === null) {
            // Fallback se il router non è stato istanziato
            $baseDir = dirname($_SERVER['SCRIPT_NAME']);
            if ($baseDir === '/' || $baseDir === '\\') {
                $baseDir = '';
            }
        } else {
            $baseDir = self::$instance->baseDir;
        }

        $route = '/' . ltrim($route, '/');
        return $baseDir . $route;
    }

    /**
     * Effettua un redirect verso una rotta.
     * 
     * @param string $route La rotta di destinazione
     */
    public static function redirect($route)
    {
        header('Location: ' . self::url($route));
        exit;
    }
}
