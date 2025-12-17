<?php
/**
 * File: src/Core/Database.php
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

use mysqli;
use Exception;
use mysqli_sql_exception;

/**
 * Gestisce la connessione al database usando il pattern Singleton.
 */
class Database
{
    private static $instance = null;
    private $connection;

    /**
     * Costruttore privato per prevenire istanziazione diretta.
     * Carica la configurazione e stabilisce la connessione MySQLi.
     * 
     * @throws Exception Se la connessione fallisce.
     */
    private function __construct()
    {
        $config = require __DIR__ . '/../../config/db.php';

        mysqli_report(MYSQLI_REPORT_ERROR | MYSQLI_REPORT_STRICT);

        try {
            $this->connection = new mysqli(
                $config['host'],
                $config['user'],
                $config['password'],
                $config['dbname']
            );
            $this->connection->set_charset($config['charset']);
        } catch (mysqli_sql_exception $e) {
            throw new Exception("Errore di connessione al Database: " . $e->getMessage());
        }
    }

    /**
     * Restituisce l'unica istanza della classe Database.
     * 
     * @return Database L'istanza Singleton.
     */
    public static function getInstance()
    {
        if (self::$instance === null) {
            self::$instance = new self();
        }
        return self::$instance;
    }

    /**
     * Restituisce l'oggetto connessione MySQLi.
     * 
     * @return mysqli La connessione attiva.
     */
    public function getConnection()
    {
        return $this->connection;
    }

    /**
     * Previeni la clonazione dell'oggetto (Singleton).
     */
    private function __clone()
    {
    }

    /**
     * Previeni la deserializzazione (Singleton).
     * 
     * @throws Exception Sempre.
     */
    public function __wakeup()
    {
        throw new Exception("Non puoi deserializzare un singleton.");
    }
}
