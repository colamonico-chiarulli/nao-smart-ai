<?php
/**
 * File: src/Helpers/helpers.php
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


/**
 * Effettua l'escape delle entità HTML per prevenire XSS.
 *
 * @param string|null $value Il valore da sottoporre a escape.
 * @return string Il valore con escape effettuato.
 */
function h(?string $value): string
{
    return htmlspecialchars((string) $value, ENT_QUOTES, 'UTF-8');
}

/**
 * Genera un token CSRF e lo memorizza nella sessione.
 *
 * @return string Il token CSRF.
 */
function csrf_token(): string
{
    if (session_status() === PHP_SESSION_NONE) {
        session_start();
    }
    if (empty($_SESSION['csrf_token'])) {
        $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
    }
    return $_SESSION['csrf_token'];
}

/**
 * Crea il campo di input nascosto per il token CSRF.
 * 
 * @return string Elemento input HTML.
 */
function csrf_field(): string
{
    $token = csrf_token();
    return '<input type="hidden" name="csrf_token" value="' . $token . '">';
}

/**
 * Verifica il token CSRF dalla richiesta POST.
 *
 * @return bool True se valido, false altrimenti.
 */
function verify_csrf_token(): bool
{
    if (session_status() === PHP_SESSION_NONE) {
        session_start();
    }
    if (!isset($_POST['csrf_token']) || !isset($_SESSION['csrf_token'])) {
        return false;
    }
    return hash_equals($_SESSION['csrf_token'], $_POST['csrf_token']);
}

/**
 * Genera un URL assoluto per l'applicazione.
 * 
 * @param string $path Percorso relativo (es. 'css/style.css' o 'anagrafe/elenco').
 * @return string URL completo.
 */
function url(string $path = ''): string
{
    // Rimuovi eventuali slash iniziali
    $path = ltrim($path, '/');

    // Ottieni il base path dallo script name
    // es. /public_html/nao-smart-ai/public/index.php -> /public_html/nao-smart-ai/public
    $basePath = dirname($_SERVER['SCRIPT_NAME']);

    // Normalizza su Windows/Unix
    $basePath = str_replace('\\', '/', $basePath);

    // Se il basePath è la root, restituisci direttamente il path con un solo slash
    if ($basePath === '/' || $basePath === '') {
        return '/' . $path;
    }

    // Rimuovi slash finale se presente
    $basePath = rtrim($basePath, '/');

    return $basePath . '/' . $path;
}

/**
 * Genera un messaggio di errore per un campo di input.
 *
 * @param string $field Nome del campo.
 * @param array $errors Array di errori.
 * @return string HTML del messaggio di errore.
 */
function getFormError($field, $errors = [])
{
    if (isset($errors[$field])) {
        return '<div class="text-danger small mt-1"><i class="bi bi-exclamation-circle me-1"></i>' . h($errors[$field]) . '</div>';
    }
    return '';
}